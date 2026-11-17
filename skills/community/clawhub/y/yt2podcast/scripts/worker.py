#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""yt2podcast pipeline worker.

跑完一个 job 的五个阶段,并在结束(成功/失败)时把结果唤醒回原会话。

    pending -> sourcing -> generating -> postprocess -> uploading -> done
                                                          \\-> failed

Job 文件: <root>/jobs/<job_id>.json
Job 目录: <root>/jobs/<job_id>/   (worker.log / audio.wav / cover.jpg / episode.m4a)
通知载荷: <root>/jobs/<job_id>/notify.json

用法:
    worker.py <job_id>              # 跑(自动从断点续跑)
    worker.py <job_id> --rerun      # 失败后重跑(复用已有 notebook,不重新建本)
    worker.py <job_id> --notify-only  # 只重新发一次通知
    worker.py <job_id> --no-notify  # 跑但不唤醒会话(调试用)
    worker.py <job_id> --dry-run    # 不调外部命令,只跑状态机(离线自检)

环境变量:
    YT2PODCAST_ROOT       根目录,默认 ~/.openclaw/workspace/yt2podcast
    YT2PODCAST_PODCAST_ID  小宇宙节目 id(必填,或在建 job 时用 --podcast 指定)
    YT2PODCAST_PROXY       访问 Google 用的 HTTP 代理(不给则读 macOS 系统代理)
    YT2PODCAST_FFMPEG    ffmpeg 路径,默认 which ffmpeg
    YT2PODCAST_FFPROBE   ffprobe 路径,默认 which ffprobe
"""

from __future__ import annotations

import argparse
import fcntl
import json
import os
import shlex
import shutil
import subprocess
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# --------------------------------------------------------------------------
# 配置
# --------------------------------------------------------------------------

SKILL_DIR = Path(__file__).resolve().parent.parent
ROOT = Path(os.environ.get("YT2PODCAST_ROOT", "~/.openclaw/workspace/yt2podcast")).expanduser()
JOBS_DIR = ROOT / "jobs"

# 小宇宙节目 id:没有内置默认值,必须由 --podcast 或 YT2PODCAST_PODCAST_ID 提供,
# 否则 uploading 阶段会报 PODCAST_ID_MISSING(避免把别人的节目写死进代码)。
DEFAULT_PODCAST_ID = os.environ.get("YT2PODCAST_PODCAST_ID", "")
FFMPEG = os.environ.get("YT2PODCAST_FFMPEG") or shutil.which("ffmpeg") or "/opt/homebrew/bin/ffmpeg"
FFPROBE = os.environ.get("YT2PODCAST_FFPROBE") or shutil.which("ffprobe") or "/opt/homebrew/bin/ffprobe"

# 各阶段外部调用的超时(秒)。opencli 自身没有全局 --timeout,超时由这里兜底。
# 都可用环境变量覆盖(排障/测试时调小)。
def _timeout(name: str, default: int) -> int:
    try:
        return int(os.environ.get(name, default))
    except (TypeError, ValueError):
        return default


TIMEOUT_CREATE = _timeout("YT2PODCAST_TIMEOUT_CREATE", 300)          # notebooklm create
TIMEOUT_ADD_SOURCE = _timeout("YT2PODCAST_TIMEOUT_ADD_SOURCE", 300)  # notebooklm add-source
TIMEOUT_OPEN = _timeout("YT2PODCAST_TIMEOUT_OPEN", 300)              # notebooklm open
TIMEOUT_SOURCE_READY = _timeout("YT2PODCAST_TIMEOUT_SOURCE_READY", 900)  # 等源处理完(源抽取一般几分钟)
TIMEOUT_GENERATE = _timeout("YT2PODCAST_TIMEOUT_GENERATE", 2400)     # 生成+下载+转码,实测约 20 分钟,外层留足余量
TIMEOUT_UPLOAD = _timeout("YT2PODCAST_TIMEOUT_UPLOAD", 1200)         # xiaoyuzhou upload(上传+转码)
TIMEOUT_YOUTUBE_META = _timeout("YT2PODCAST_TIMEOUT_YOUTUBE_META", 120)  # youtube video
TIMEOUT_WAKE = _timeout("YT2PODCAST_TIMEOUT_WAKE", 90)               # openclaw system event / agent

SOURCE_POLL_INTERVAL = _timeout("YT2PODCAST_SOURCE_POLL_INTERVAL", 30)  # 等源处理完的轮询间隔
AUDIO_BITRATE = "128k"

# 打开 notebook 后必须保留 tab,后续 source-guide / summary 才能读到那个页面
# (实测:不加 --keep-tab true,下一次 opencli 调用会报 NOTEBOOKLM_UNAVAILABLE)
NB_SESSION = ["--site-session", "persistent", "--keep-tab", "true"]

STAGES = ["sourcing", "generating", "postprocess", "uploading"]

DRY_RUN = False


# --------------------------------------------------------------------------
# 基础工具
# --------------------------------------------------------------------------


class StageError(Exception):
    """带 code/hint/suggestion 的阶段错误,方便失败时给出人工建议。"""

    def __init__(self, code: str, message: str, hint: Optional[str] = None,
                 suggestion: Optional[str] = None,
                 repair: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.hint = hint
        self.suggestion = suggestion or default_suggestion(code)
        # repair: agent 可自主执行的安全修复动作
        #   {"safe": bool, "cmd": str, "then": str, "note": str}
        # safe=True 表示幂等、只动本机 opencli/skill 目录、不装全局包、不登录账号,
        # agent 可以直接跑完再重试一次;sae=False 必须交回用户。
        self.repair = repair or default_repair(code)

    def to_dict(self) -> Dict[str, Any]:
        payload = {
            "code": self.code,
            "message": self.message,
            "hint": self.hint,
            "suggestion": self.suggestion,
        }
        if self.repair:
            payload["repair"] = self.repair
        return payload


def default_repair(code: str) -> Optional[Dict[str, Any]]:
    """按错误码给出 agent 能不能自己修的判断(见 SKILL.md「自主修复策略」)。"""
    setup = "bash %s/scripts/setup.sh" % SKILL_DIR
    if code in ("ADAPTER_MISSING", "NOTEBOOKLM_UNAVAILABLE"):
        return {
            "safe": True,
            "cmd": setup,
            "then": "重跑同一个 job(worker.py <job_id>)",
            "note": "只安装/校验本机 adapter,不改用户配置",
        }
    if code == "PENDING_STALLED":
        return {
            "safe": True,
            "cmd": "python3 %s/scripts/resume-stalled.py --resume" % SKILL_DIR,
            "then": "等待新的完成通知",
            "note": "按落盘产物断点续跑,不重复消耗生成配额",
        }
    if code in ("MISSING_BINARY", "QUOTA_EXHAUSTED", "NEED_LOGIN", "PODCAST_ID_MISSING",
                "PUBLISH_NOT_ALLOWED", "COMMAND_EXEC"):
        return {
            "safe": False,
            "reason": "需要用户决策或提供凭据(安装全局包 / 登录账号 / 节目 id / 公开发布确认 / 网络代理)",
        }
    return None


def default_suggestion(code: str) -> str:
    table = {
        "NEED_LOGIN": "在 Chrome 里重新登录对应站点(NotebookLM / 小宇宙主播后台),然后重跑该 job。",
        "AUTH_REQUIRED": "在 Chrome 里重新登录对应站点(NotebookLM / 小宇宙主播后台),然后重跑该 job。",
        "QUOTA_EXHAUSTED": "NotebookLM 每日音频生成配额已用尽,明天再重跑该 job。",
        "ADAPTER_MISSING": "配套的 opencli adapter 没装: 跑一次 bash scripts/setup.sh 即可(或 scripts/install-adapters.sh --install)。",
        "CMD_TIMEOUT": "外部命令超时,检查 Chrome 是否在前台运行、网络是否通畅,然后重跑该 job。",
        "SOURCE_PROCESS_TIMEOUT": "YouTube 源抽取超时,确认链接可访问(非会员/非地区限制)后重跑该 job。",
        "AUDIO_MISSING": "没拿到 NotebookLM 音频产物,确认配额与登录态后重跑该 job。",
        "FFMPEG_FAILED": "音频转码失败,已降级直接上传 wav;可手动转码后重跑上传阶段。",
        "UPLOAD_FAILED": "小宇宙上传失败,登录态过期时重新扫码登录后重跑该 job。",
        "NOTIFY_FAILED": "通知没发出去,结果已写在 job 目录里,可手动查看并重发通知。",
        "BUSY": "另一个 job 正在跑(串行约束),等它结束再重跑。",
    }
    return table.get(code, "查看 job 目录下的 worker.log 定位问题后重跑该 job。")


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def log(job: Optional["Job"], message: str) -> None:
    line = "[%s] %s" % (now_iso(), message)
    print(line, flush=True)
    if job is not None:
        job.log(line)


def human_duration(seconds: Optional[float]) -> str:
    if not seconds or seconds <= 0:
        return "未知"
    total = int(round(seconds))
    hours, rem = divmod(total, 3600)
    minutes, secs = divmod(rem, 60)
    if hours:
        return "%d 小时 %d 分 %d 秒" % (hours, minutes, secs)
    if minutes:
        return "%d 分 %d 秒" % (minutes, secs)
    return "%d 秒" % secs


def human_size(num_bytes: Optional[int]) -> str:
    if not num_bytes or num_bytes <= 0:
        return "未知"
    mb = num_bytes / (1024.0 * 1024.0)
    if mb >= 1:
        return "%.1f MB" % mb
    return "%.1f KB" % (num_bytes / 1024.0)


def rows_of(data: Any) -> List[Dict[str, Any]]:
    """把 opencli 的 data 归一成 list[dict]。"""
    if isinstance(data, list):
        return [row for row in data if isinstance(row, dict)]
    if isinstance(data, dict):
        return [data]
    return []


def pick(data: Any, *keys: str) -> Any:
    """从 opencli 输出里取第一个非空字段。"""
    for row in rows_of(data):
        for key in keys:
            value = row.get(key)
            if value not in (None, ""):
                return value
    if isinstance(data, dict):
        for key in keys:
            value = data.get(key)
            if value not in (None, ""):
                return value
    return None


def field_value_map(data: Any) -> Dict[str, Any]:
    """youtube video 返回 [{field,value}],转成普通 dict。"""
    mapping: Dict[str, Any] = {}
    for row in rows_of(data):
        if "field" in row and "value" in row:
            mapping[str(row["field"])] = row["value"]
    return mapping


# --------------------------------------------------------------------------
# 外部命令
# --------------------------------------------------------------------------


def system_proxy() -> Optional[str]:
    """找一个可用的 HTTP 代理:显式环境变量优先,其次 macOS 系统代理。

    NotebookLM 的音频文件挂在 lh3.googleusercontent.com,国内直连会
    "fetch failed";而 opencli 内部用 Node 的 fetch,它不读 macOS 系统代理设置,
    必须把代理塞进环境变量并打开 NODE_USE_ENV_PROXY(见 child_env)。
    """
    explicit = (
        os.environ.get("YT2PODCAST_PROXY")
        or os.environ.get("HTTPS_PROXY")
        or os.environ.get("https_proxy")
        or os.environ.get("HTTP_PROXY")
        or os.environ.get("http_proxy")
    )
    if explicit:
        return explicit
    if sys.platform != "darwin":
        return None
    try:
        out = subprocess.run(
            ["scutil", "--proxy"], stdout=subprocess.PIPE, timeout=5
        ).stdout.decode("utf-8", "replace")
    except (OSError, subprocess.SubprocessError):
        return None
    fields: Dict[str, str] = {}
    for line in out.splitlines():
        key, sep, value = line.partition(":")
        if sep:
            fields[key.strip()] = value.strip()
    if fields.get("HTTPSEnable") == "1" and fields.get("HTTPSProxy"):
        return "http://%s:%s" % (fields["HTTPSProxy"], fields.get("HTTPSPort") or "80")
    if fields.get("SOCKSEnable") == "1" and fields.get("SOCKSProxy"):
        return "http://%s:%s" % (fields["SOCKSProxy"], fields.get("SOCKSPort") or "1080")
    return None


_PROXY_APPLIED = False
CHILD_ENV: Optional[Dict[str, str]] = None


def child_env() -> Dict[str, str]:
    """子进程环境:补上代理,让 Node fetch 走得通。"""
    global CHILD_ENV, _PROXY_APPLIED
    if CHILD_ENV is None:
        env = dict(os.environ)
        proxy = system_proxy()
        if proxy:
            for key in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY"):
                env.setdefault(key, proxy)
                env.setdefault(key.lower(), proxy)
            # Node 24+ 需要这个才会让内置 fetch 读取上面的代理变量
            env["NODE_USE_ENV_PROXY"] = "1"
            _PROXY_APPLIED = True
        CHILD_ENV = env
    return CHILD_ENV


def run_cmd(args: List[str], timeout: int, cwd: Optional[str] = None) -> Tuple[int, str, str]:
    """执行外部命令,带超时;超时不抛 Python 异常,交给调用方判断。"""
    try:
        proc = subprocess.run(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            cwd=cwd,
            env=child_env(),
        )
    except FileNotFoundError:
        return 127, "", "命令不存在: %s" % args[0]
    except subprocess.TimeoutExpired:
        return 124, "", "命令超时(%ss): %s" % (timeout, shlex.join(args))
    stdout = proc.stdout.decode("utf-8", "replace")
    stderr = proc.stderr.decode("utf-8", "replace")
    return proc.returncode, stdout, stderr


def parse_json_output(text: str) -> Optional[Any]:
    """opencli 输出的是单行 JSON;容错:整段解析失败就找最后一行 JSON。"""
    text = (text or "").strip()
    if not text:
        return None
    try:
        return json.loads(text)
    except ValueError:
        pass
    for line in reversed(text.splitlines()):
        line = line.strip()
        if line.startswith("{") or line.startswith("["):
            try:
                return json.loads(line)
            except ValueError:
                continue
    return None


def classify_error(payload: Any, stderr: str) -> StageError:
    """把 opencli 的错误 JSON 转成 StageError,顺便识别 NEED_LOGIN / 配额等。"""
    code = "OPENCLI_ERROR"
    message = (stderr or "").strip() or "opencli 调用失败"
    hint = None
    if isinstance(payload, dict):
        err = payload.get("error")
        if isinstance(err, dict):
            code = str(err.get("code") or code)
            message = str(err.get("message") or message)
            hint = err.get("hint")
        elif err:
            message = str(err)
    haystack = " ".join(str(x) for x in (code, message, hint) if x).lower()
    if "unknowncommand" in haystack or "unknown command" in haystack:
        code = "ADAPTER_MISSING"
        message = "opencli 没有这个子命令(adapter 未安装): %s" % message
        hint = hint or "先安装对应的 opencli adapter(见 tasks/TASK-A.md、TASK-B.md),再重跑该 job。"
    elif "quota" in haystack or "配额" in haystack or "daily limit" in haystack:
        code = "QUOTA_EXHAUSTED"
    elif ("need_login" in haystack or "auth" in haystack or "login" in haystack
          or "登录" in haystack or "sign in" in haystack or "unauthorized" in haystack
          or "forbidden" in haystack or "401" in haystack or "403" in haystack
          or "notebooklm_unavailable" in haystack or "browser session" in haystack
          or "chrome" in haystack):
        code = "NEED_LOGIN"
        if code == "NEED_LOGIN" and "chrome" in haystack:
            hint = hint or "打开 Chrome 并登录 NotebookLM / 小宇宙主播后台(保持 persistent session 有效),然后重跑该 job。"
    return StageError(code, message, hint)


def opencli(args: List[str], timeout: int, job: Optional["Job"] = None) -> Any:
    """调用 opencli 并返回 data;失败抛 StageError。"""
    cmd = ["opencli"] + list(args) + ["-f", "json"]
    log(job, "exec: %s" % shlex.join(cmd))
    if DRY_RUN:
        return dry_run_opencli(args)
    rc, stdout, stderr = run_cmd(cmd, timeout)
    payload = parse_json_output(stdout) or parse_json_output(stderr)
    if rc != 0 or (isinstance(payload, dict) and payload.get("ok") is False):
        raise classify_error(payload, stderr or stdout)
    if payload is None:
        raise StageError(
            "OPENCLI_UNPARSABLE",
            "opencli 输出无法解析: %s" % (stdout or stderr or "")[:300],
        )
    if isinstance(payload, dict):
        return payload.get("data")
    return payload


def dry_run_opencli(args: List[str]) -> Any:
    """--dry-run 下的假数据,用来离线验证状态机。"""
    sub = args[0] if args else ""
    cmd = args[1] if len(args) > 1 else ""
    if sub == "notebooklm" and cmd == "create":
        return [{"id": "dryrun-notebook-id", "title": "dryrun", "url": "https://notebook.google.com/notebook/dryrun-notebook-id"}]
    if sub == "notebooklm" and cmd == "add-source":
        return [{"notebook_id": "dryrun-notebook-id", "source_id": "dryrun-source-id", "kind": "url",
                 "identifier": "https://youtu.be/dryrun", "notebook_url": "https://notebook.google.com/notebook/dryrun-notebook-id"}]
    if sub == "notebooklm" and cmd == "source-guide":
        return [{"source_id": "dryrun-source-id", "title": "dryrun", "summary": "dryrun summary", "keywords": ["a", "b"]}]
    if sub == "notebooklm" and cmd == "download-audio":
        # 造一个假的音频文件,让后面的阶段能接着跑
        try:
            output = None
            for index, item in enumerate(args):
                if item in ("-o", "--output") and index + 1 < len(args):
                    output = Path(args[index + 1])
            if output:
                output.parent.mkdir(parents=True, exist_ok=True)
                output.write_bytes(b"RIFF----WAVEfmt " + b"0" * 1024)
        except OSError:
            pass
        return {"notebook_id": "dryrun-notebook-id", "file": "audio.wav", "bytes": 1024, "status": "done"}
    if sub == "notebooklm" and cmd in ("open", "source-list", "summary"):
        return [{"id": "dryrun-notebook-id"}]
    if sub == "xiaoyuzhou" and cmd == "upload":
        return {"episode_id": "dryrun-episode-id", "episode_url": "https://www.xiaoyuzhoufm.com/episode/dryrun",
                "title": "dryrun", "status": "draft" if "--draft" in args else "published", "draft": "--draft" in args}
    if sub == "youtube" and cmd == "video":
        return [{"field": "title", "value": "dryrun video title"},
                {"field": "description", "value": "dryrun description"},
                {"field": "duration", "value": "120s"}]
    return []


# --------------------------------------------------------------------------
# Job
# --------------------------------------------------------------------------


class Job:
    """job 文件的读写封装(原子写)。"""

    def __init__(self, data: Dict[str, Any], path: Path) -> None:
        self.data = data
        self.path = path
        self.dir = path.parent / path.stem

    @classmethod
    def load(cls, job_id: str) -> "Job":
        path = JOBS_DIR / ("%s.json" % job_id)
        if not path.exists():
            raise StageError("JOB_NOT_FOUND", "job 文件不存在: %s" % path)
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        job = cls(data, path)
        job.dir.mkdir(parents=True, exist_ok=True)
        return job

    def save(self) -> None:
        self.data["updated_at"] = now_iso()
        tmp = self.path.with_suffix(".json.tmp")
        with tmp.open("w", encoding="utf-8") as handle:
            json.dump(self.data, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        os.replace(str(tmp), str(self.path))

    def log(self, line: str) -> None:
        try:
            self.dir.mkdir(parents=True, exist_ok=True)
            with (self.dir / "worker.log").open("a", encoding="utf-8") as handle:
                handle.write(line + "\n")
        except OSError:
            pass

    def history(self, event: str, **extra: Any) -> None:
        entries = self.data.setdefault("history", [])
        entry = {"ts": now_iso(), "stage": self.data.get("stage"), "event": event}
        entry.update(extra)
        entries.append(entry)

    def get(self, key: str, default: Any = None) -> Any:
        value = self.data.get(key)
        return default if value is None else value

    def set_stage(self, stage: str) -> None:
        self.data["stage"] = stage
        self.save()

    def done_stage(self, stage: str) -> None:
        stages = self.data.setdefault("stages_done", [])
        if stage not in stages:
            stages.append(stage)
        self.save()


# --------------------------------------------------------------------------
# 阶段 1:sourcing
# --------------------------------------------------------------------------


def wait_for_source(job: Job) -> Optional[Dict[str, Any]]:
    """轮询直到源抽取完成(能拿到 source-guide / summary 就视为就绪)。"""
    notebook_id = job.get("notebook_id")
    source_id = job.get("source_id")
    deadline = time.time() + TIMEOUT_SOURCE_READY

    try:
        opencli(["notebooklm", "open", notebook_id] + NB_SESSION, TIMEOUT_OPEN, job)
    except StageError as exc:
        log(job, "打开 notebook 失败(继续尝试读源): %s" % exc.message)

    last_error = None
    while time.time() < deadline:
        try:
            guide = opencli(
                ["notebooklm", "source-guide", source_id] + NB_SESSION,
                TIMEOUT_OPEN,
                job,
            )
            rows = rows_of(guide)
            if rows:
                payload = rows[0]
                summary = payload.get("summary") or ""
                if summary:
                    log(job, "源已就绪,拿到 guide 摘要(%d 字)" % len(summary))
                    with (job.dir / "source-guide.json").open("w", encoding="utf-8") as handle:
                        json.dump(payload, handle, ensure_ascii=False, indent=2)
                    return payload
                last_error = "source-guide 还没有 summary"
            else:
                last_error = "source-guide 返回空"
        except StageError as exc:
            last_error = exc.message
        log(job, "等源处理中(%s),%d 秒后再试" % (last_error or "处理中", SOURCE_POLL_INTERVAL))
        time.sleep(SOURCE_POLL_INTERVAL)

    # 超时:源可能还是能用的,降级继续(记 warning),把问题留给 generating 阶段暴露
    warnings = job.data.setdefault("warnings", [])
    warnings.append({
        "ts": now_iso(),
        "stage": "sourcing",
        "code": "SOURCE_PROCESS_TIMEOUT",
        "message": "等待源处理超时(%ds),最后一次错误: %s" % (TIMEOUT_SOURCE_READY, last_error),
    })
    log(job, "警告: 等待源处理超时,继续往下走")
    return None


def fetch_youtube_meta(job: Job) -> None:
    """拉 YouTube 元数据(标题/简介/时长),作为标题与简介的兜底。

    只读、不消耗 NotebookLM 配额;失败不致命。
    """
    data = job.data
    if data.get("video_title") and data.get("video_duration_sec"):
        return
    try:
        meta = opencli(["youtube", "video", data["youtube_url"]], TIMEOUT_YOUTUBE_META, job)
    except StageError as exc:
        log(job, "取 YouTube 元数据失败(忽略): %s" % exc.message)
        return
    mapping = field_value_map(meta)
    if mapping.get("title"):
        data["video_title"] = mapping["title"]
    if mapping.get("description"):
        data["video_description"] = mapping["description"]
    if mapping.get("channel"):
        data["video_channel"] = mapping["channel"]
    duration = str(mapping.get("duration") or "")
    if duration.endswith("s"):
        try:
            data["video_duration_sec"] = int(float(duration[:-1]))
        except ValueError:
            pass
    if mapping.get("thumbnail"):
        data["video_thumbnail"] = mapping["thumbnail"]
    job.save()


def canonical_youtube_url(video_id: str) -> str:
    """规范化成干净的 watch?v= 链接再喂 NotebookLM。

    带 ?si= 追踪参数的短链(youtu.be/xxx?si=...)会让 AddSources RPC 静默失败
    (返回 no source id),所以加源前统一转成 https://www.youtube.com/watch?v=<id>。
    """
    return "https://www.youtube.com/watch?v=%s" % video_id


def stage_sourcing(job: Job) -> None:
    data = job.data
    video_id = data["video_id"]
    notebook_id = data.get("notebook_id")

    fetch_youtube_meta(job)

    if not notebook_id:
        title = data.get("title") or data.get("video_title") or ("yt2podcast-%s" % video_id)
        log(job, "建 notebook: %s" % title)
        created = opencli(
            ["notebooklm", "create", title, "--execute"] + NB_SESSION,
            TIMEOUT_CREATE,
            job,
        )
        notebook_id = pick(created, "id", "notebook_id")
        if not notebook_id:
            raise StageError("NOTEBOOK_CREATE_FAILED", "notebooklm create 没有返回 notebook id")
        data["notebook_id"] = notebook_id
        data["notebook_url"] = pick(created, "url", "notebook_url")
        job.save()
        log(job, "notebook_id=%s" % notebook_id)
    else:
        log(job, "复用已有 notebook: %s" % notebook_id)

    source_id = data.get("source_id")
    if not source_id:
        source_url = canonical_youtube_url(video_id)
        log(job, "加 YouTube 源: %s" % source_url)
        added = opencli(
            ["notebooklm", "add-source", notebook_id, "--url", source_url,
             "--execute"] + NB_SESSION,
            TIMEOUT_ADD_SOURCE,
            job,
        )
        source_id = pick(added, "source_id", "id")
        if not source_id:
            raise StageError("SOURCE_ADD_FAILED", "notebooklm add-source 没有返回 source id")
        data["source_id"] = source_id
        job.save()
        log(job, "source_id=%s" % source_id)
    else:
        log(job, "复用已有 source: %s" % source_id)

    guide = wait_for_source(job)
    if guide:
        data["source_summary"] = guide.get("summary") or ""
        data["source_keywords"] = guide.get("keywords") or []
        data["source_title"] = guide.get("title") or ""
        job.save()

    # notebook 级别的 summary 作为补充(拿不到不影响主流程)
    if not data.get("source_summary"):
        try:
            summary = opencli(["notebooklm", "summary"] + NB_SESSION, TIMEOUT_OPEN, job)
            text = pick(summary, "summary", "text", "content")
            if text:
                data["source_summary"] = str(text)
                job.save()
        except StageError as exc:
            log(job, "取 notebook summary 失败(忽略): %s" % exc.message)

    job.done_stage("sourcing")


# --------------------------------------------------------------------------
# 阶段 2:generating
# --------------------------------------------------------------------------


def stage_generating(job: Job) -> None:
    data = job.data
    notebook_id = data.get("notebook_id")
    if not notebook_id:
        raise StageError("NOTEBOOK_MISSING", "job 里没有 notebook_id,无法生成音频")

    audio_path = job.dir / "audio.wav"
    if audio_path.exists() and audio_path.stat().st_size > 0:
        log(job, "音频已存在,跳过生成: %s" % audio_path)
        data["audio_file"] = str(audio_path)
        job.save()
        job.done_stage("generating")
        return

    log(job, "触发 Audio Overview 并下载音频(最长 %d 秒)" % TIMEOUT_GENERATE)
    result = opencli(
        ["notebooklm", "download-audio", notebook_id, "--generate", "--timeout", "1800",
         "--output", str(audio_path)] + NB_SESSION,
        TIMEOUT_GENERATE,
        job,
    )
    status = pick(result, "status")
    if status and str(status).lower() not in ("done", "ready", "ok", "success"):
        raise StageError("AUDIO_NOT_READY", "download-audio 返回状态: %s" % status)

    if not audio_path.exists() or audio_path.stat().st_size <= 0:
        raise StageError(
            "AUDIO_MISSING",
            "没有拿到音频文件: %s" % audio_path,
            hint="确认 NotebookLM 配额与登录态;也可手动把 wav 放到该路径后重跑。",
        )

    data["audio_file"] = str(audio_path)
    data["audio_bytes"] = audio_path.stat().st_size
    job.save()
    log(job, "音频就绪: %s (%s)" % (audio_path, human_size(data["audio_bytes"])))
    job.done_stage("generating")


# --------------------------------------------------------------------------
# 阶段 3:postprocess
# --------------------------------------------------------------------------


def ffprobe_duration(path: Path) -> Optional[float]:
    if DRY_RUN:
        return 120.0
    rc, stdout, _ = run_cmd(
        [FFPROBE, "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        60,
    )
    if rc != 0:
        return None
    try:
        value = float(stdout.strip())
    except ValueError:
        return None
    return value if value > 0 else None


def download_cover(video_id: str, dest: Path, job: Job) -> Optional[Path]:
    """抓 YouTube 封面(有就嵌进 m4a)。"""
    if DRY_RUN:
        return None
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) yt2podcast/1.0"}
    for name in ("maxresdefault.jpg", "hqdefault.jpg"):
        url = "https://i.ytimg.com/vi/%s/%s" % (video_id, name)
        try:
            request = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(request, timeout=30) as response:
                payload = response.read()
        except Exception as exc:  # noqa: BLE001 - 封面失败不致命
            log(job, "下载封面失败(%s): %s" % (name, exc))
            continue
        if len(payload) > 2048:
            dest.write_bytes(payload)
            log(job, "封面就绪: %s (%s)" % (dest, human_size(len(payload))))
            return dest
    return None


def stage_postprocess(job: Job) -> None:
    data = job.data
    audio_path = Path(data.get("audio_file") or (job.dir / "audio.wav"))
    if not audio_path.exists():
        raise StageError("AUDIO_MISSING", "音频文件不存在: %s" % audio_path)

    duration = ffprobe_duration(audio_path)
    if duration:
        data["duration_sec"] = int(round(duration))
    cover = download_cover(data["video_id"], job.dir / "cover.jpg", job)
    if cover:
        data["cover_file"] = str(cover)

    final_path = job.dir / "episode.m4a"
    title = data.get("title") or data.get("source_title") or ("yt2podcast-%s" % data["video_id"])
    artist = data.get("author") or "yt2podcast"
    album = data.get("podcast_name") or "yt2podcast"

    if DRY_RUN:
        final_path = audio_path
        data["postprocess_degraded"] = False
    elif final_path.exists() and final_path.stat().st_size > 0 and not data.get("postprocess_degraded"):
        log(job, "成品已存在,跳过后处理: %s" % final_path)
    else:
        cmd = [FFMPEG, "-y", "-i", str(audio_path)]
        if cover and cover.exists():
            cmd += ["-i", str(cover)]
        cmd += ["-map", "0:a:0"]
        if cover and cover.exists():
            cmd += ["-map", "1:v:0", "-c:v", "mjpeg", "-disposition:v:0", "attached_pic"]
        cmd += [
            "-c:a", "aac", "-b:a", AUDIO_BITRATE,
            "-movflags", "+faststart",
            "-metadata", "title=%s" % title,
            "-metadata", "artist=%s" % artist,
            "-metadata", "album=%s" % album,
            "-metadata", "comment=%s" % (data.get("source_url") or data.get("youtube_url") or ""),
            str(final_path),
        ]
        log(job, "转码: %s" % " ".join(cmd))
        rc, stdout, stderr = run_cmd(cmd, 600)
        ok = rc == 0 and final_path.exists() and final_path.stat().st_size > 0
        if not ok:
            # 降级:直接用 wav
            warnings = data.setdefault("warnings", [])
            warnings.append({
                "ts": now_iso(),
                "stage": "postprocess",
                "code": "FFMPEG_FAILED",
                "message": "ffmpeg 转 m4a 失败,降级直接使用 wav: %s" % ((stderr or stdout or "")[-400:]),
            })
            log(job, "ffmpeg 失败,降级直接用 wav: %s" % (stderr or stdout or "").strip()[-300:])
            final_path = audio_path
            data["postprocess_degraded"] = True
        else:
            data["postprocess_degraded"] = False

    data["final_file"] = str(final_path)
    data["final_bytes"] = final_path.stat().st_size if final_path.exists() else None
    data["final_format"] = final_path.suffix.lstrip(".").lower() or "wav"
    if not duration:
        duration = ffprobe_duration(final_path)
        if duration:
            data["duration_sec"] = int(round(duration))
    job.save()
    log(job, "后处理完成: %s (%s, %s)" % (
        final_path, human_size(data.get("final_bytes")), human_duration(data.get("duration_sec"))))
    job.done_stage("postprocess")


# --------------------------------------------------------------------------
# 阶段 4:uploading
# --------------------------------------------------------------------------


def build_description(job: Job) -> str:
    """简介优先级:agent 给的中文简介 > 源摘要 > 视频标题。

    worker 不做 LLM 提炼;中文润色由 wake 回来后的 agent 负责(见 SKILL.md 边界说明)。
    """
    data = job.data
    description = (data.get("description") or "").strip()
    if description:
        return description
    summary = (data.get("source_summary") or "").strip()
    title = (data.get("title") or data.get("source_title") or "").strip()
    parts = []
    if title:
        parts.append("本期播客整理自 YouTube 视频《%s》。" % title)
    if summary:
        parts.append(summary[:500])
    parts.append("原视频: %s" % (data.get("youtube_url") or ""))
    return "\n".join(parts).strip()


def stage_uploading(job: Job) -> None:
    data = job.data
    if data.get("episode_url"):
        log(job, "已上传过,跳过: %s" % data.get("episode_url"))
        job.done_stage("uploading")
        return

    final_path = Path(data.get("final_file") or (job.dir / "episode.m4a"))
    if not final_path.exists():
        raise StageError("FINAL_FILE_MISSING", "待上传文件不存在: %s" % final_path)

    title = (data.get("title") or data.get("source_title") or ("yt2podcast-%s" % data["video_id"])).strip()
    description = build_description(job)
    podcast_id = (data.get("podcast_id") or DEFAULT_PODCAST_ID or "").strip()
    if not podcast_id:
        raise StageError(
            "PODCAST_ID_MISSING",
            "没有给小宇宙节目 id:建 job 时传 --podcast <id>,或设置 YT2PODCAST_PODCAST_ID",
        )

    cmd = ["xiaoyuzhou", "upload", str(final_path), "--title", title, "--description", description]
    cmd += ["--podcast", podcast_id]
    cover = data.get("cover_file")
    if cover and Path(cover).exists():
        cmd += ["--cover", cover]
    if data.get("draft"):
        cmd += ["--draft"]
    else:
        # 公开发布不可撤销,必须由调用方显式授权(环境变量),否则拒绝执行。
        if os.environ.get("YT2PODCAST_ALLOW_PUBLISH") != "1":
            raise StageError(
                "PUBLISH_NOT_ALLOWED",
                "公开发布需要显式授权:设置 YT2PODCAST_ALLOW_PUBLISH=1 后重跑;默认只存草稿",
            )
        cmd += ["--publish"]
    cmd += ["--timeout", "900"]

    log(job, "上传小宇宙: %s" % shlex.join(cmd))
    result = opencli(cmd, TIMEOUT_UPLOAD, job)

    episode_url = pick(result, "episode_url", "url", "link")
    episode_id = pick(result, "episode_id", "eid", "id")
    if not episode_url and not episode_id:
        raise StageError("UPLOAD_FAILED", "上传返回里没有 episode_url/episode_id")
    data["episode_url"] = episode_url
    data["episode_id"] = episode_id
    data["episode_status"] = pick(result, "status")
    data["upload_draft"] = bool(data.get("draft"))
    job.save()
    log(job, "上传完成: %s" % (episode_url or episode_id))

    # 回查平台真实状态:小宇宙的"草稿"只是 INITIALIZED(后台显示"单集审核中"),
    # 审核通过后可能自动上线,所以通知里不能凭 draft 标志就宣称"未发布"。
    verify_episode_status(job, episode_id, podcast_id)

    job.done_stage("uploading")


# --------------------------------------------------------------------------
# 通知(wake)
# --------------------------------------------------------------------------


def verify_episode_status(job: Job, episode_id: Optional[str], podcast_id: str) -> None:
    """上传后回查单集状态,把平台口径记进 job(失败不影响主流程)。"""
    data = job.data
    if not episode_id:
        return
    try:
        result = opencli(
            ["xiaoyuzhou", "upload-status", episode_id, "--podcast", podcast_id,
             "--site-session", "persistent", "--keep-tab", "true"],
            TIMEOUT_UPLOAD,
            job,
        )
    except StageError as exc:
        log(job, "回查单集状态失败(忽略): %s" % exc.message)
        return
    row = result[0] if isinstance(result, list) and result else result
    if not isinstance(row, dict):
        return
    data["episode_status"] = row.get("status")
    data["review_status"] = row.get("review_status")
    data["episode_published"] = bool(row.get("published"))
    job.save()
    log(job, "平台状态: %s / review=%s / published=%s"
        % (data["episode_status"], data["review_status"], data["episode_published"]))


def build_payload(job: Job, ok: bool) -> Dict[str, Any]:
    data = job.data
    payload: Dict[str, Any] = {
        "skill": "yt2podcast",
        "job_id": data.get("job_id"),
        "video_id": data.get("video_id"),
        "youtube_url": data.get("youtube_url"),
        "ok": ok,
        "stage": data.get("stage"),
        "title": data.get("title"),
        "description": build_description(job),
        "source_summary": data.get("source_summary"),
        "duration_sec": data.get("duration_sec"),
        "duration_text": human_duration(data.get("duration_sec")),
        "size_bytes": data.get("final_bytes"),
        "size_text": human_size(data.get("final_bytes")),
        "podcast_id": data.get("podcast_id") or DEFAULT_PODCAST_ID,
        "draft": bool(data.get("draft")),
        # 是否需要用户确认后才上传
        "needs_confirmation": data.get("stage") == "awaiting_upload",
        "final_file": data.get("final_file"),
        # 平台真实状态(draft / reviewing / published);draft 标志只代表"没显式点发布"
        "episode_status": data.get("episode_status"),
        "review_status": data.get("review_status"),
        "episode_published": data.get("episode_published"),
        "episode_url": data.get("episode_url"),
        "episode_id": data.get("episode_id"),
        "artifacts": {
            "job_dir": str(job.dir),
            "final_file": data.get("final_file"),
            "audio_file": data.get("audio_file"),
            "cover_file": data.get("cover_file"),
            "log": str(job.dir / "worker.log"),
        },
        "warnings": data.get("warnings") or [],
    }
    if not ok:
        error = data.get("error") or {}
        payload["error"] = error
        payload["suggestion"] = error.get("suggestion") or default_suggestion(str(error.get("code")))
    return payload


def wake(job: Job, payload: Dict[str, Any]) -> bool:
    """把结果唤醒回原会话。

    openclaw 2026.7.1-2 没有 `gateway wake` 子命令,等价能力是
    `openclaw system event --mode now`(手动唤醒见 docs/gateway/heartbeat.md)。
    """
    text = "yt2podcast " + json.dumps(payload, ensure_ascii=False)
    session_key = job.get("session_key")

    notify_path = job.dir / "notify.json"
    try:
        with notify_path.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)
    except OSError as exc:
        log(job, "写 notify.json 失败: %s" % exc)

    cmd = ["openclaw", "system", "event", "--text", text, "--mode", "now"]
    if session_key:
        cmd += ["--session-key", session_key]
    log(job, "wake: %s" % shlex.join(cmd))
    if DRY_RUN:
        log(job, "dry-run:跳过真实 wake")
        job.data["notified_at"] = now_iso()
        job.data["notify_ok"] = True
        job.save()
        return True
    rc, stdout, stderr = run_cmd(cmd, TIMEOUT_WAKE)
    if rc == 0:
        log(job, "wake 成功")
        job.data["notified_at"] = now_iso()
        job.data["notify_ok"] = True
        job.save()
        return True

    log(job, "system event 失败(rc=%s): %s" % (rc, (stderr or stdout or "").strip()[-300:]))

    # 兜底:直接跑一个 agent 回合并投递到原会话
    fallback = ["openclaw", "agent", "--message", text, "--deliver"]
    if session_key:
        fallback += ["--session-key", session_key]
    else:
        fallback += ["--channel", "last"]
    log(job, "wake 兜底: %s" % shlex.join(fallback))
    rc2, stdout2, stderr2 = run_cmd(fallback, TIMEOUT_WAKE)
    if rc2 == 0:
        log(job, "兜底 wake 成功")
        job.data["notified_at"] = now_iso()
        job.data["notify_ok"] = True
        job.save()
        return True

    job.data["notify_ok"] = False
    job.data["notify_error"] = (stderr2 or stdout2 or stderr or stdout or "").strip()[-400:]
    job.save()
    log(job, "通知失败,结果仍保留在 %s" % notify_path)
    return False


# --------------------------------------------------------------------------
# 主流程
# --------------------------------------------------------------------------


def acquire_lock() -> Optional[Any]:
    """串行约束:同一时间只允许一个 worker。"""
    JOBS_DIR.mkdir(parents=True, exist_ok=True)
    handle = open(str(JOBS_DIR / ".worker.lock"), "w")
    try:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        handle.close()
        return None
    handle.write("%d\n" % os.getpid())
    handle.flush()
    return handle


REQUIRED_ADAPTERS = [
    "notebooklm/download-audio.js",
    "xiaoyuzhou/upload.js",
    "xiaoyuzhou/upload-status.js",
]


def preflight(job: Job) -> None:
    """开跑前快速自检(毫秒级,不启浏览器):缺 adapter 就立刻停下并给修复命令。

    为什么要 fail closed:跑到 generating/uploading 才发现 adapter 缺失,既浪费时间
    又可能已经消耗了 NotebookLM 生成配额。
    """
    clis = Path(os.environ.get("OPENCLI_HOME", "~/.opencli")).expanduser() / "clis"
    missing = [rel for rel in REQUIRED_ADAPTERS if not (clis / rel).is_file()]
    fix = "bash %s/scripts/setup.sh" % SKILL_DIR
    if missing:
        raise StageError(
            "ADAPTER_MISSING",
            "缺少配套 adapter: %s" % ", ".join(missing),
            hint="这些命令 opencli 官方基线里没有,由本 skill 自带",
            suggestion="跑一次 %s(装 adapter + 环境自检)后重跑本 job" % fix,
            repair={
                "safe": True,
                "cmd": fix,
                "then": "重跑本 job: python3 %s/scripts/worker.py %s" % (SKILL_DIR, job.get("job_id")),
                "note": "只安装本机 adapter(自动备份旧文件),不装全局包、不登录账号",
            },
        )
    bins = ["opencli", "ffmpeg", "ffprobe"]
    absent = [b for b in bins if not shutil.which(b)]
    if absent:
        raise StageError(
            "MISSING_BINARY",
            "缺少命令行工具: %s" % ", ".join(absent),
            suggestion="brew install ffmpeg / npm i -g @jackwener/opencli,再跑 %s" % fix,
        )


def run_pipeline(job: Job, notify: bool = True, allow_upload: bool = False) -> int:
    data = job.data
    if data.get("stage") == "done":
        log(job, "job 已完成,直接退出(幂等)")
        return 0

    job.history("start", stage=data.get("stage"))
    job.save()
    log(job, "代理: %s" % (system_proxy() or "未检测到(直连)"))
    preflight(job)

    for stage in STAGES:
        if data.get("stage") == "done":
            break
        if stage in (data.get("stages_done") or []):
            log(job, "阶段 %s 已完成,跳过" % stage)
            continue
        data["stage"] = stage
        job.save()
        log(job, "----- 阶段 %s 开始 -----" % stage)
        if stage == "sourcing":
            stage_sourcing(job)
        elif stage == "generating":
            stage_generating(job)
        elif stage == "postprocess":
            stage_postprocess(job)
        elif stage == "uploading":
            # 默认一条龙上传(用户已确认这是期望行为)。
            # 可选 --hold-upload: 生成完先停下,等用户点头再跑 worker.py <id> --upload。
            if data.get("hold_upload") and not allow_upload:
                data["stage"] = "awaiting_upload"
                job.history("awaiting_upload")
                job.save()
                log(job, "音频已就绪,等待用户确认后再上传(回复确认后跑 worker.py %s --upload)"
                    % data.get("job_id"))
                if notify:
                    wake(job, build_payload(job, ok=True))
                return 0
            stage_uploading(job)

    data["stage"] = "done"
    data["finished_at"] = now_iso()
    data.pop("error", None)
    job.history("done")
    job.save()
    log(job, "全部阶段完成")

    if notify:
        wake(job, build_payload(job, ok=True))
    return 0


def handle_failure(job: Job, exc: StageError) -> int:
    data = job.data
    previous_stage = data.get("stage")
    data["stage"] = "failed"
    data["failed_stage"] = data.get("failed_stage") or previous_stage
    data["error"] = exc.to_dict()
    data["failed_at"] = now_iso()
    job.history("failed", code=exc.code, message=exc.message)
    job.save()
    log(job, "失败[%s]: %s" % (exc.code, exc.message))
    if exc.hint:
        log(job, "hint: %s" % exc.hint)
    wake(job, build_payload(job, ok=False))
    return 1


def notify_only(job: Job) -> int:
    ok = job.get("stage") == "done"
    return 0 if wake(job, build_payload(job, ok=ok)) else 1


def main(argv: List[str]) -> int:
    global DRY_RUN

    parser = argparse.ArgumentParser(description="yt2podcast pipeline worker")
    parser.add_argument("job_id", help="job id(= YouTube video id)")
    parser.add_argument("--rerun", action="store_true",
                        help="失败后重跑(复用已有 notebook,不重新建本)")
    parser.add_argument("--notify-only", action="store_true", help="只重发通知")
    parser.add_argument("--no-notify", action="store_true", help="不唤醒会话")
    parser.add_argument("--dry-run", action="store_true", help="不调外部命令,只跑状态机")
    parser.add_argument("--upload", action="store_true",
                        help="用户已确认,执行上传(默认生成到 m4a 就停下等确认)")
    args = parser.parse_args(argv)

    DRY_RUN = args.dry_run

    try:
        job = Job.load(args.job_id)
    except StageError as exc:
        print("[%s] %s" % (now_iso(), exc.message), file=sys.stderr)
        return 2

    lock = acquire_lock()
    if lock is None:
        log(job, "另一个 job 正在运行,本次退出(串行约束)")
        return 3

    try:
        if args.notify_only:
            return notify_only(job)

        if args.rerun:
            failed_stage = job.get("failed_stage")
            try:
                cut = STAGES.index(failed_stage) if failed_stage in STAGES else 0
            except ValueError:
                cut = 0
            job.data["stages_done"] = [
                stage for stage in (job.get("stages_done") or [])
                if stage in STAGES and STAGES.index(stage) < cut
            ]
            job.data["stage"] = failed_stage or "pending"
            job.data.pop("error", None)
            job.data.pop("failed_stage", None)
            job.history("rerun", from_stage=job.data["stage"])
            job.save()
            log(job, "重跑 job %s(从 %s 开始)" % (args.job_id, job.data["stage"]))

        return run_pipeline(job, notify=not args.no_notify, allow_upload=args.upload)
    except StageError as exc:
        return handle_failure(job, exc)
    except KeyboardInterrupt:
        log(job, "收到中断信号")
        job.data["stage"] = "failed"
        job.data["error"] = StageError("INTERRUPTED", "worker 被中断").to_dict()
        job.save()
        return 130
    except Exception as exc:  # noqa: BLE001 - 兜底:任何异常都要落到 job 文件里
        log(job, "未预期异常: %r" % exc)
        return handle_failure(job, StageError("UNEXPECTED", repr(exc)))
    finally:
        try:
            fcntl.flock(lock.fileno(), fcntl.LOCK_UN)
            lock.close()
        except OSError:
            pass


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
