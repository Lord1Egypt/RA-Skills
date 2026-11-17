"""wdp_checkpoint — 可恢复批处理参考模块（纯标准库，无第三方依赖）。

由 AI 生成批处理脚本时嵌入。提供：
  - Checkpoint : 按 seed 命名空间隔离的断点续跑记录（原子写）
  - Progress   : 进度与 ETA（结构化 stderr 输出）
  - FailLog    : 追加式 JSON-lines 失败日志（唯一失败真相来源）
  - run_batch  : 单写者 Coordinator 并发批处理（排队 + max_workers 限流）
  - Transient / Permanent / Fatal : 错误三分类

使用约定：脚本把本文件复制到脚本目录后 `import wdp_checkpoint as wdp`。
"""
import json
import os
import signal
import sys
import tempfile
import threading
import time
import traceback
from concurrent.futures import FIRST_COMPLETED, ProcessPoolExecutor, ThreadPoolExecutor, wait
from concurrent.futures import CancelledError as concurrent_futures_CancelledError


class Transient(Exception):
    """瞬态错误：可退避重试（网络抖动等）。"""


class Permanent(Exception):
    """永久错误：记录到 FailLog 后继续，不重试。"""


class Fatal(Exception):
    """致命错误：flush checkpoint 后停止整个任务。"""


def _retry_on_windows_lock(fn, attempts=5, delay=0.05):
    """重试撞上 Windows 瞬态文件锁的操作。

    杀毒/索引器会瞬时以拒绝模式打开刚写入的文件，使 os.replace / open 抛出
    PermissionError（WinError 5 / WinError 32）。这是毫秒级的瞬态，重试几次即可
    冲掉；持续失败则照常抛出（不能静默丢失 checkpoint 落盘）。
    """
    for _ in range(attempts - 1):
        try:
            return fn()
        except PermissionError:
            time.sleep(delay)
    return fn()


def _atomic_write_json(path, obj):
    """temp + os.replace 原子写 JSON，避免崩溃留下半写文件。"""
    directory = os.path.dirname(os.path.abspath(path))
    os.makedirs(directory, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=directory, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False, indent=2)
        # Windows 下 AV 可能正锁着目标文件 → 重试瞬态 PermissionError（E2E 实测）
        _retry_on_windows_lock(lambda: os.replace(tmp, path))
    finally:
        if os.path.exists(tmp):
            try:
                os.remove(tmp)
            except PermissionError:
                pass  # 清理失败可接受：临时文件残留无害，不能掩盖主结果


class Checkpoint:
    """按 seed 命名空间隔离的断点续跑记录。

    - 只记录已完成项 key；mark_failed 记录失败项（下次运行会重试）。
    - flush 原子写；seed 不匹配视为旧命名空间，整体忽略。
    """

    def __init__(self, path, key_fn=str, seed="v1"):
        self.path = path
        self.key_fn = key_fn
        self.seed = seed
        self._done = set()
        self._failed = {}
        self._dirty = False
        self._load()

    def _load(self):
        try:
            with open(self.path, encoding="utf-8") as f:
                data = json.load(f)
        except (OSError, ValueError):
            return
        if data.get("seed") != self.seed:
            return  # 旧命名空间 → 视为全新
        self._done = set(data.get("done", []))
        self._failed = dict(data.get("failed", {}))

    def is_done(self, item):
        return self.key_fn(item) in self._done

    def mark_done(self, item):
        key = self.key_fn(item)
        self._done.add(key)
        self._failed.pop(key, None)
        self._dirty = True

    def mark_failed(self, item, reason):
        self._failed[self.key_fn(item)] = str(reason)
        self._dirty = True

    def flush(self):
        if not self._dirty:
            return
        _atomic_write_json(self.path, {
            "seed": self.seed,
            "done": sorted(self._done),
            "failed": self._failed,
        })
        self._dirty = False

    @property
    def counts(self):
        return {"done": len(self._done), "failed": len(self._failed)}

    @property
    def failed_items(self):
        return sorted(self._failed)


class Progress:
    """进度与 ETA 输出（结构化，写往 stderr 以便 stdout 保持机器可读）。"""

    def __init__(self, total, stream=None, every=10, label=""):
        self.total = total
        self.stream = stream if stream is not None else sys.stderr
        self.every = max(1, every)
        self.label = label
        self._n = 0
        self._start = time.time()

    def tick(self, n=1, label=None):
        self._n += n
        if self._n % self.every == 0 or self._n >= self.total:
            self._emit(label)

    def _emit(self, label=None):
        elapsed = time.time() - self._start
        remaining = int(elapsed / self._n * (self.total - self._n)) if self._n else 0
        parts = [f"[{self.label}] {self._n}/{self.total}", f"eta={remaining}s"]
        if label:
            parts.append(str(label))
        print(" ".join(parts), file=self.stream, flush=True)

    def summary(self):
        self._emit("done")


class FailLog:
    """追加式 JSON-lines 失败日志（机器可读，唯一的失败真相来源）。

    行字段: ts, item_key, category, retries, error_type, error_msg, traceback, stderr_tail
    保留全部失败记录（append-only，含最终被放弃的项），供审计与恢复。
    注意：item_key 一律 str() 化（含 int/哈希等非字符串键），重试过滤须 str(key) 匹配。
    """

    def __init__(self, path):
        self.path = path
        directory = os.path.dirname(os.path.abspath(path))
        os.makedirs(directory, exist_ok=True)

    def record(self, item, error, category="permanent", retries=0, stderr_tail=None, tb=""):
        if isinstance(error, BaseException):
            err = error
            tb = tb or traceback.format_exc().strip()
        else:
            err = RuntimeError(str(error))
        row = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "item_key": str(item),
            "category": category,
            "retries": retries,
            "error_type": type(err).__name__,
            "error_msg": str(err),
            "traceback": tb,
            "stderr_tail": stderr_tail or "",
        }
        _append_json_line(self.path, row)

    def failed_items(self):
        """返回 {item_key: row}，供重试与恢复诊断。"""
        result = {}
        if not os.path.exists(self.path):
            return result
        with open(self.path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    row = json.loads(line)
                except ValueError:
                    continue
                # 跳过「合法 JSON 但形状不符」的行（外部手改/损坏）：恢复路径不能崩
                if not isinstance(row, dict):
                    continue
                key = row.get("item_key")
                # FailLog 的 item_key 一律 str 化：非 str 键（如 [1,2]）是外源数据，跳过
                if not isinstance(key, str):
                    continue
                result[key] = row
        return result

    def summary(self):
        """按 category 计数。"""
        counts = {}
        for row in self.failed_items().values():
            # 缺失或为 null 的 category 一律归 permanent（绝不产生 None 键）
            category = row.get("category") or "permanent"
            counts[category] = counts.get(category, 0) + 1
        return counts


def _append_json_line(path, row):
    """追加一行 JSON；Windows 下 AV 会瞬时独占文件，撞上 PermissionError 就重试。"""

    def _append():
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    _retry_on_windows_lock(_append)


def _guarded_worker(worker_fn, item, retries, retry_backoff):
    """在 worker 内执行单项并翻译错误分类。模块级函数以支持进程池 picklable。"""
    attempt = 0
    while True:
        try:
            worker_fn(item)
            return ("done", None, 0, "")
        except Transient as e:
            attempt += 1
            if attempt > retries:
                return ("failed", e, attempt - 1, traceback.format_exc().strip())
            time.sleep(retry_backoff * attempt)
        except Permanent as e:
            return ("failed", e, attempt, traceback.format_exc().strip())
        except Fatal as e:
            return ("fatal", e, attempt, traceback.format_exc().strip())
        except Exception as e:
            # 未知异常 → 按永久失败处理（软失败哲学：记录并继续）
            return ("failed", e, attempt, traceback.format_exc().strip())


def run_batch(items, worker_fn, *, max_workers=None, checkpoint, progress,
              failures, retries=3, retry_backoff=1.0, use_processes=False,
              stop_event=None):
    """单写者 Coordinator 并发批处理。

    - Coordinator（主线程）唯一写 checkpoint / FailLog / Progress；worker 不碰文件。
    - worker_fn 内可抛 Transient（退避重试）/ Permanent（记录继续）/ Fatal（停止）。
    - 优雅中断：stop_event 置位 / SIGINT(SIGTERM) → 停止派发，等 in-flight 收尾后落盘。
    - 硬杀（kill -9）最坏只丢 ≤ max_workers 项，且已落盘的 checkpoint 仍有效。

    返回 {"total", "done", "failed", "fatal", "interrupted"}。
    """
    max_workers = max_workers or min(8, os.cpu_count() or 1)
    Executor = ProcessPoolExecutor if use_processes else ThreadPoolExecutor
    stop = stop_event if stop_event is not None else threading.Event()
    # SIGTERM → 置 stop（优雅收尾：停止派发、in-flight 收尾、落盘后退出）
    _restore_sigterm = None
    if hasattr(signal, "SIGTERM") and threading.current_thread() is threading.main_thread():
        _restore_sigterm = signal.signal(signal.SIGTERM, lambda *_: stop.set())
    seen = 0
    done = failed = fatal = 0
    results = {}
    it = iter(items)

    def _dispatch_one():
        nonlocal seen
        for item in it:
            if checkpoint.is_done(item):
                continue
            fut = executor.submit(_guarded_worker, worker_fn, item, retries, retry_backoff)
            results[fut] = item
            seen += 1
            return True
        return False

    def _apply(fut):
        nonlocal done, failed, fatal
        item = results.pop(fut)
        try:
            kind, err, nretry, tb = fut.result()
        except concurrent_futures_CancelledError:
            return  # 取消的任务从未执行，resume 会重跑
        if kind == "done":
            checkpoint.mark_done(item)
            progress.tick()
            done += 1
        elif kind == "failed":
            # 用 checkpoint 的 key_fn 作为失败日志的 item_key —— FailLog 与 checkpoint
            # 共享同一身份约定，--retry-failures 才能按 key_of(item) 匹配到失败项。
            failures.record(checkpoint.key_fn(item), err, category="permanent",
                            retries=nretry, tb=tb)
            checkpoint.mark_failed(item, err)
            progress.tick()
            failed += 1
        else:  # fatal
            failures.record(checkpoint.key_fn(item), err, category="fatal",
                            retries=nretry, tb=tb)
            checkpoint.mark_failed(item, err)
            progress.tick()
            fatal += 1
            stop.set()
        # 每项落盘：硬杀（kill -9 / TerminateProcess）不跑 finally，只在两次落盘之间丢
        # ≤ max_workers 项（checklist 维度 2「崩溃丢失 ≤N 项」；E2E 断言 dup ≤ max_workers）。
        checkpoint.flush()

    with Executor(max_workers=max_workers) as executor:
        for _ in range(max_workers * 2):  # 有界 lookahead 窗口
            if not _dispatch_one():
                break
        interrupted = False
        while results:
            try:
                done_futs, _ = wait(list(results), timeout=0.2,
                                    return_when=FIRST_COMPLETED)
            except KeyboardInterrupt:
                stop.set()
                interrupted = True
                for fut in list(results):
                    fut.cancel()
                continue
            if not done_futs:
                if stop.is_set():
                    for fut in list(results):
                        fut.cancel()
                continue
            for fut in done_futs:
                _apply(fut)
                if not stop.is_set():
                    _dispatch_one()
        executor.shutdown(wait=True)
        checkpoint.flush()
        progress.summary()
        if _restore_sigterm is not None:
            signal.signal(signal.SIGTERM, _restore_sigterm)
        return {
            "total": seen, "done": done, "failed": failed, "fatal": fatal,
            "interrupted": interrupted or stop.is_set(),
        }
