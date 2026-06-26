# veo_worker.py
import requests, time, argparse, os, json, sys, re, platform, subprocess, traceback

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(BASE_DIR, "veo_log.txt")
LOCK = os.path.join(BASE_DIR, "veo.lock")
RESULT = os.path.join(BASE_DIR, "veo_result.txt")

URL = "https://maas-openapi.wanjiedata.com/api/v1/chat/completions"


def log(msg: str):
    """每条日志独立追加写入,确保实时落盘;同时输出到原始 stdout。"""
    ts = time.strftime('%Y-%m-%d %H:%M:%S')
    line = f"[{ts}] {msg}"
    try:
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(line + "\n")
            f.flush()
            os.fsync(f.fileno())
    except Exception:
        # 写日志失败也不要影响主流程
        pass

    try:
        print(line, file=sys.__stdout__, flush=True)
    except Exception:
        pass


def log_exc(prefix: str, e: Exception):
    tb = traceback.format_exc()
    log(f"{prefix}: {repr(e)}")
    for tline in tb.rstrip().splitlines():
        log(f"{prefix} TB: {tline}")


def open_url(url):
    """跨平台打开 URL"""
    try:
        if platform.system() == 'Windows':
            os.startfile(url)
        elif platform.system() == 'Darwin':  # macOS
            subprocess.Popen(['open', url])
        else:  # Linux
            subprocess.Popen(['xdg-open', url])
    except Exception as e:
        log_exc("[!] 打开URL失败", e)


def is_process_running(pid):
    """检查指定 PID 的进程是否在运行"""
    try:
        import psutil
        return psutil.pid_exists(pid)
    except ImportError:
        # 没有 psutil:Windows 用 tasklist 粗略判断;其他平台保守不删锁
        try:
            if platform.system() == 'Windows':
                res = subprocess.run(['tasklist', '/FI', f'PID eq {pid}'],
                                     capture_output=True, text=True)
                return str(pid) in res.stdout
        except Exception:
            pass
        return True


def _read_api_key_from_openclaw():
    config_path = os.path.join(os.path.expanduser("~"), ".openclaw", "openclaw.json")
    with open(config_path, 'r', encoding='utf-8') as f:
        cfg = json.load(f)
    return list(cfg['models']['providers'].values())[0]['apiKey']


def generate_video(prompt, model, seconds):
    log("任务初始化")
    log(f"--- 新任务开始 ---")
    log(f"任务输入: prompt='{prompt}', model='{model}', seconds={seconds}")

    log(f"检查锁文件: {LOCK}")
    if os.path.exists(LOCK):
        try:
            with open(LOCK, "r", encoding="utf-8") as f:
                pid = int(f.read().strip() or "0")

            mtime = os.path.getmtime(LOCK)
            if time.time() - mtime > 1800:
                log(f"[!] 任务超时 (PID: {pid}),清理锁...")
                os.remove(LOCK)
            elif pid and is_process_running(pid):
                log(f"[!] 发现活跃任务 (PID: {pid}),当前任务退出。")
                return
            else:
                log(f"发现僵尸锁文件 (PID: {pid}),清理...")
                os.remove(LOCK)
        except Exception as e:
            log_exc("[!] 锁文件处理异常", e)

    log(f"创建锁文件 (PID: {os.getpid()})")
    try:
        with open(LOCK, "w", encoding="utf-8") as f:
            f.write(str(os.getpid()))
            f.flush()
    except Exception as e:
        log_exc("[!] 无法写入锁文件", e)
        return

    try:
        # APIKEY获取方式保持不变
        key = _read_api_key_from_openclaw()
        log(f"API Key 指纹: {key[:6]}...{key[-4:]}")  # 仅日志中打印指纹,避免泄露

        payload = {
            "model": "veo3.1",
            "messages": [{"role": "user", "content": prompt}],
            "stream": True
        }
        log(f"Request URL: {URL}")
        log(f"Payload: {json.dumps(payload, ensure_ascii=False)}")

        headers = {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
        }

        success = False
        session = requests.Session()

        for attempt in range(1, 21):
            log(f"尝试获取视频 (第 {attempt}/20 次)...")

            try:
                # 请求发起打点
                start_t = time.time()
                log("发送请求...")

                res = session.post(
                    URL,
                    headers=headers,
                    json=payload,
                    stream=True,
                    timeout=60
                )

                log(f"收到响应: HTTP {res.status_code} (耗时 {time.time() - start_t:.2f}s)")
                if res.status_code != 200:
                    # 400/401等这里通常有明确原因
                    try:
                        log(f"Response headers: {dict(res.headers)}")
                        log(f"Response body: {res.text}")
                    except Exception as e:
                        log_exc("[!] 读取错误响应失败", e)

                res.raise_for_status()

                full = ""
                got_first_chunk = False
                chunks = 0

                # 读取流式内容
                for raw in res.iter_lines(decode_unicode=True):
                    if not raw:
                        continue

                    if not got_first_chunk:
                        got_first_chunk = True
                        log("已收到首个分块(开始流式读取)")

                    line = raw.strip()
                    chunks += 1

                    # 兼容 SSE: "data: {...}" / 或直接就是 json
                    if line.startswith("data:"):
                        data_str = line[5:].strip()
                    else:
                        data_str = line

                    if data_str == "[DONE]":
                        log("收到 [DONE],流结束")
                        break

                    try:
                        d = json.loads(data_str)
                    except Exception:
                        # 可能是 event:/id: 等非json行,忽略
                        continue

                    # 兼容多种返回结构:delta.content / message.content
                    try:
                        choice = (d.get("choices") or [None])[0] or {}
                        delta = choice.get("delta") or {}
                        msg = choice.get("message") or {}
                        piece = (delta.get("content") or msg.get("content") or "")
                        if piece:
                            full += piece
                    except Exception:
                        pass

                    # 每隔一些chunk打一次点(避免日志爆炸)
                    if chunks % 50 == 0:
                        log(f"流读取中... chunks={chunks}, accumulated_len={len(full)}")

                log(f"流读取完成: chunks={chunks}, accumulated_len={len(full)}")

                match = re.search(r'(https?://\S+)', full)
                if match:
                    url = match.group(1).rstrip(')"\'').replace(')', '').replace(']', '')
                    with open(RESULT, "w", encoding="utf-8") as f:
                        f.write(f"SUCCESS|{url}")
                        f.flush()
                    open_url(url)
                    log(f"成功获取并打开链接: {url}")
                    success = True
                    break
                else:
                    log("[!] 未在返回内容中提取到URL,将重试。")
                    time.sleep(2)

            except Exception as e:
                log_exc(f"[!] 第 {attempt} 次尝试失败", e)
                time.sleep(2)

        if not success:
            with open(RESULT, "w", encoding="utf-8") as f:
                f.write("FAILED|生成失败,请重试")
                f.flush()
            log("[!] 20次重试失败,生成任务结束。")

    finally:
        if os.path.exists(LOCK):
            try:
                os.remove(LOCK)
                log("锁文件已清理。")
            except Exception as e:
                log_exc("[!] 锁文件清理失败", e)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--model", default="veo3.1")
    parser.add_argument("--seconds", type=int, default=8)
    args = parser.parse_args()
    
    generate_video(args.prompt, args.model, args.seconds)