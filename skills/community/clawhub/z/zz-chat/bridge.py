#!/usr/bin/env python3
"""爪爪桥接 v15 — WebSocket + openclaw agent CLI 直连"""
import asyncio, json, os, subprocess, sys, time

# Windows 编码修复
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 清除代理 + 设置 SSL 证书（必须在 import websockets 之前）
os.environ.pop('all_proxy', None)
os.environ.pop('ALL_PROXY', None)
os.environ.pop('http_proxy', None)
os.environ.pop('HTTP_PROXY', None)
os.environ.pop('https_proxy', None)
os.environ.pop('HTTPS_PROXY', None)
try:
    import certifi
    os.environ['SSL_CERT_FILE'] = certifi.where()
except ImportError:
    pass

import websockets, urllib.request, sys

# 优先级: 环境变量 > ~/.zz/worker_url 文件 > 默认值
_API_DEFAULT = "https://ai0000.cn/zz/"
_WORKER_FILE = os.path.expanduser("~/.zz/worker_url")
API = os.environ.get("ZZ_API")
if not API and os.path.exists(_WORKER_FILE):
    API = open(_WORKER_FILE).read().strip().rstrip('/') + '/'
if not API:
    API = _API_DEFAULT

# 支持 --worker 参数
if "--worker" in sys.argv:
    idx = sys.argv.index("--worker")
    if idx + 1 < len(sys.argv):
        API = sys.argv[idx + 1].rstrip('/') + '/'

# 支持 --uid 参数
_uid_override = None
if "--uid" in sys.argv:
    idx = sys.argv.index("--uid")
    if idx + 1 < len(sys.argv):
        _uid_override = sys.argv[idx + 1]

# 读取或获取用户编号
ID_FILE = os.path.expanduser("~/.zz/id")
if _uid_override:
    MY_ID = _uid_override
    os.makedirs(os.path.dirname(ID_FILE), exist_ok=True)
    with open(ID_FILE, "w") as f:
        f.write(MY_ID)
    print(f"[设置] 编号: {MY_ID}", flush=True)
elif os.path.exists(ID_FILE):
    MY_ID = open(ID_FILE).read().strip()
    print(f"[加载] 编号: {MY_ID}", flush=True)
else:
    try:
        req = urllib.request.Request(API + "register", headers={"User-Agent": "zz-bridge/15"})
        resp = urllib.request.urlopen(req)
        data = json.loads(resp.read())
        MY_ID = data["id"]
        os.makedirs(os.path.dirname(ID_FILE), exist_ok=True)
        with open(ID_FILE, "w") as f:
            f.write(MY_ID)
        print(f"[注册成功] 编号: {MY_ID}", flush=True)
    except Exception as e:
        print(f"[错误] 获取编号失败: {e}", flush=True)
        exit(1)

BRIDGE_ID = "D" + MY_ID
SESSION_ID = "zz-" + MY_ID
WS_URL = API.replace("https://", "wss://").replace("http://", "ws://") + f"?role=bridge&uid={MY_ID}"

last_processed_id = ""


def call_openclaw(message):
    """调用 openclaw agent CLI 获取回复"""
    try:
        result = subprocess.run(
            ["openclaw", "agent", "-m", message, "--session-id", SESSION_ID, "--json", "--timeout", "120"],
            capture_output=True, text=True, timeout=130
        )
        # 解析 JSON（过滤 stderr 的 plugin 日志）
        try:
            # 找到 JSON 开始的位置
            stdout = result.stdout
            json_start = stdout.find('{')
            if json_start < 0:
                return None
            data = json.loads(stdout[json_start:])
            payloads = data.get("result", {}).get("payloads", [])
            if payloads:
                return payloads[0].get("text")
            return None
        except (json.JSONDecodeError, IndexError, KeyError):
            return None
    except subprocess.TimeoutExpired:
        print("[CLI 超时]", flush=True)
        return None
    except Exception as e:
        print(f"[CLI 异常] {e}", flush=True)
        return None


async def handle_message(data):
    """处理收到的消息，调 CLI 拿回复，发回去"""
    global last_processed_id
    msg_id = data.get("msg_id", "")
    to = data.get("to", "")
    content = data.get("content", "")

    if not content:
        return
    if msg_id and msg_id == last_processed_id:
        return
    # 只处理发给自己的消息
    if to and to != MY_ID and to != BRIDGE_ID:
        return

    last_processed_id = msg_id
    sender = data.get("from", "")
    print(f"[收] #{sender}: {content[:80]}", flush=True)

    # 在线程池调 CLI（避免阻塞）
    reply = await asyncio.get_event_loop().run_in_executor(None, call_openclaw, content)

    if not reply:
        print(f"[跳过] CLI 无回复", flush=True)
        return

    print(f"[回] → #{sender}: {reply[:80]}", flush=True)
    return {"msg_id": f"reply-{msg_id}", "from": BRIDGE_ID, "to": sender, "content": reply, "ts": int(time.time() * 1000)}


async def main():
    print(f"""
  ┌────────────────────────────────────────┐
  │  🦞 爪爪桥接 v15                      │
  │  编号: {MY_ID:<10s} (bridge: {BRIDGE_ID})  │
  │  引擎: WebSocket + openclaw agent      │
  └────────────────────────────────────────┘
""", flush=True)

    while True:
        try:
            async with websockets.connect(WS_URL, ping_interval=20, ping_timeout=10, proxy=None) as ws:
                print(f"[已连接] {WS_URL}", flush=True)
                # 并发心跳任务
                async def heartbeat():
                    while True:
                        await asyncio.sleep(30)
                        try:
                            print("[心跳] 连接正常", flush=True)
                        except:
                            break
                hb = asyncio.create_task(heartbeat())
                try:
                    async for raw in ws:
                        try:
                            data = json.loads(raw)
                            reply_msg = await handle_message(data)
                            if reply_msg:
                                await ws.send(json.dumps(reply_msg))
                        except json.JSONDecodeError:
                            pass
                        except Exception as e:
                            print(f"[处理错误] {e}", flush=True)
                finally:
                    hb.cancel()
        except Exception as e:
            print(f"[断开] {e}，5秒后重连...", flush=True)
            await asyncio.sleep(5)


if __name__ == "__main__":
    asyncio.run(main())
