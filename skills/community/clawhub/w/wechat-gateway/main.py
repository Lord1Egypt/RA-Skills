import os
import re
import json
import time
import queue
import base64
import hashlib
import logging
import threading
import subprocess
import configparser
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from typing import Optional, Dict
from urllib.parse import quote

import requests
import qrcode
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
import uvicorn
from PIL import Image, ImageDraw, ImageFont

# ============================================================
# 路径与日志
# ============================================================
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
LOG_DIR = os.path.join(BASE_DIR, "logs")
IMG_DIR = os.path.join(BASE_DIR, "images")
CONFIG_PATH = os.path.join(BASE_DIR, "config.ini")

os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(IMG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(threadName)s %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(LOG_DIR, "gateway.log"), encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("WeChatGateway")

NO_PROXY = {"http": None, "https": None}
app = FastAPI(title="WeChat OpenClaw Gateway", version="10.0.0")
app.mount("/images", StaticFiles(directory=IMG_DIR), name="images")

# ============================================================
# 全局状态
# ============================================================
worker_queues = []
session_pending = defaultdict(int)
recent_message_ids: Dict[str, float] = {}
recent_lock = threading.Lock()
openclaw_executor = None

# ============================================================
# 地区列表
# ============================================================
REGIONS = {
    "110000": "北京市", "120000": "天津市", "130000": "河北省", "140000": "山西省", "150000": "内蒙古",
    "210000": "辽宁省", "220000": "吉林省", "230000": "黑龙江",
    "310000": "上海市", "320000": "江苏省", "330000": "浙江省", "340000": "安徽省", "350000": "福建省", "360000": "江西省", "370000": "山东省",
    "410000": "河南省", "420000": "湖北省", "430000": "湖南省", "440000": "广东省", "450000": "广西省", "460000": "海南省",
    "500000": "重庆市", "510000": "四川省", "520000": "贵州省", "530000": "云南省", "540000": "西藏自治区",
    "610000": "陕西省", "620000": "甘肃省", "630000": "青海省", "640000": "宁夏自治区", "650000": "新疆自治区"
}

# ============================================================
# 配置模板
# ============================================================
CONFIG_TEMPLATE = """# ============================================================
# WeChat OpenClaw Gateway 配置文件
# 修改后重启 main.py 生效
# ============================================================

[wechat]
# 你的微信 API 基础地址
# 示例：http://api.wechatapi.net/finder/v2/api
base_url = {base_url}

# 你的微信 API Token
api_token = {api_token}

# 登录成功后程序会自动写入 app_id
# 一般不需要手动修改
app_id = {app_id}

# 你的公网回调地址 / 外网访问地址
# 例如：http://你的公网IP:5000
# 注意：真正的回调地址应为 public_url + /wechat/callback
public_url = {public_url}

# 群聊触发词
# 群聊消息必须以这个词开头，机器人才会处理
group_trigger = {group_trigger}

# 私聊白名单，多个 wxid 用英文逗号分隔
# 用户也可以发送“我是你的主人”自动加入白名单
white_list_wxid = {white_list_wxid}

[server]
# 网关监听端口
port = {port}

# worker 数量
# 不同会话并行，同一会话固定到同一 worker 保证顺序
worker_count = {worker_count}

# 每个 worker 队列最大容量
queue_maxsize = {queue_maxsize}

# 单个会话最多允许积压多少条未处理任务
max_pending_per_session = {max_pending_per_session}

[session]
# 群聊上下文模式：
# shared   = 整个群共用一个上下文
# per_user = 群里每个人单独一个上下文
group_session_mode = {group_session_mode}

# 群回复前缀，留空表示不加
group_reply_prefix = {group_reply_prefix}

[performance]
# 是否开启消息去重
enable_dedup = {enable_dedup}

# 去重时间窗口（秒）
dedup_window_seconds = {dedup_window_seconds}

# 是否发送“处理中”
# 默认关闭
send_processing_tip = {send_processing_tip}

# 超过多少秒后才发“处理中”
processing_tip_delay = {processing_tip_delay}

[openclaw]
# 当前支持：
# cli = 直接命令行调用 openclaw
mode = {openclaw_mode}

# OpenClaw 可执行文件名
bin = {openclaw_bin}

# 普通对话超时时间（秒）
chat_timeout = {chat_timeout}

# 命令执行超时时间（秒）
cmd_timeout = {cmd_timeout}

# OpenClaw 执行线程池大小
executor_workers = {executor_workers}

[permissions]
# 是否允许在群共享上下文中直接 /reset
allow_group_shared_reset = {allow_group_shared_reset}

[init]
# 首次初始化时输入的地区代码
region_id = {region_id}
"""

DEFAULTS = {
    "base_url": "http://api.wechatapi.net/finder/v2/api",
    "api_token": "",
    "app_id": "",
    "public_url": "",
    "group_trigger": "狗子",
    "white_list_wxid": "",
    "port": "5000",
    "worker_count": "6",
    "queue_maxsize": "2000",
    "max_pending_per_session": "5",
    "group_session_mode": "shared",
    "group_reply_prefix": "",
    "enable_dedup": "true",
    "dedup_window_seconds": "15",
    "send_processing_tip": "false",
    "processing_tip_delay": "0.6",
    "openclaw_mode": "cli",
    "openclaw_bin": "openclaw",
    "chat_timeout": "180",
    "cmd_timeout": "20",
    "executor_workers": "4",
    "allow_group_shared_reset": "false",
    "region_id": "320000",
}

# ============================================================
# 配置工具
# ============================================================
def str2bool(v: str, default=False) -> bool:
    if v is None:
        return default
    return str(v).strip().lower() in ("1", "true", "yes", "on", "y")

def print_region_table():
    print("地区 ID 列表（按你接口支持的地区填写）:")
    items = list(REGIONS.items())
    col_width = 22
    per_row = 5

    for i in range(0, len(items), per_row):
        row = items[i:i + per_row]
        line = "".join([f"{code}={name}".ljust(col_width) for code, name in row])
        print(line.rstrip())
    print()

def write_config(data: dict):
    merged = DEFAULTS.copy()
    merged.update(data)
    content = CONFIG_TEMPLATE.format(**merged)
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        f.write(content)

def interactive_init():
    print("\n" + "=" * 56)
    print("              WeChat OpenClaw Gateway")
    print("                    首次初始化")
    print("=" * 56)
    print("  📢 技术支持：wechatapi.net")
    print("  🌐 官网注册后可享受免费测试")
    print("  ⚡ 快速接入微信 API 与机器人能力\n")

    while True:
        api_token = input("请输入 WX_API_TOKEN: ").strip()
        if len(api_token) < 25:
            print("⚠️ WX_API_TOKEN 长度异常，通常应为 25 位以上，请检查后重新输入。\n")
            continue
        break

    base_url = DEFAULTS["base_url"]

    while True:
        public_url = input("请输入公网回调地址 PUBLIC_URL（不能为空）: ").strip().rstrip("/")
        if not public_url:
            print("⚠️ PUBLIC_URL 不能为空，请输入可被外部访问的地址。\n")
            continue
        break

    group_trigger = input(f"请输入群触发词（默认 {DEFAULTS['group_trigger']}）: ").strip() or DEFAULTS["group_trigger"]

    print()
    print_region_table()

    while True:
        region_id = input(f"请输入地区代码（默认 {DEFAULTS['region_id']}）: ").strip() or DEFAULTS["region_id"]
        if region_id not in REGIONS:
            print("⚠️ 地区代码不在当前列表中，请从上面的地区 ID 列表中选择。\n")
            continue
        break

    cfg = DEFAULTS.copy()
    cfg.update({
        "api_token": api_token,
        "base_url": base_url.rstrip("/"),
        "public_url": public_url,
        "group_trigger": group_trigger,
        "region_id": region_id,
    })
    write_config(cfg)

    print(f"\n✅ 已生成配置文件：{CONFIG_PATH}")
    print("👉 回调地址应填写为：PUBLIC_URL + /wechat/callback\n")

def ensure_config_exists():
    if not os.path.exists(CONFIG_PATH):
        interactive_init()

def load_config() -> dict:
    ensure_config_exists()
    parser = configparser.ConfigParser()
    parser.read(CONFIG_PATH, encoding="utf-8")

    cfg = {
        "WX_BASE_URL": parser.get("wechat", "base_url", fallback=DEFAULTS["base_url"]).rstrip("/"),
        "WX_API_TOKEN": parser.get("wechat", "api_token", fallback="").strip(),
        "WX_APP_ID": parser.get("wechat", "app_id", fallback="").strip(),
        "PUBLIC_URL": parser.get("wechat", "public_url", fallback="").strip().rstrip("/"),
        "GROUP_TRIGGER": parser.get("wechat", "group_trigger", fallback=DEFAULTS["group_trigger"]).strip(),
        "WHITE_LIST_WXID": [x.strip() for x in parser.get("wechat", "white_list_wxid", fallback="").split(",") if x.strip()],

        "PORT": parser.getint("server", "port", fallback=int(DEFAULTS["port"])),
        "WORKER_COUNT": parser.getint("server", "worker_count", fallback=int(DEFAULTS["worker_count"])),
        "QUEUE_MAXSIZE": parser.getint("server", "queue_maxsize", fallback=int(DEFAULTS["queue_maxsize"])),
        "MAX_PENDING_PER_SESSION": parser.getint("server", "max_pending_per_session", fallback=int(DEFAULTS["max_pending_per_session"])),

        "GROUP_SESSION_MODE": parser.get("session", "group_session_mode", fallback=DEFAULTS["group_session_mode"]).strip().lower(),
        "GROUP_REPLY_PREFIX": parser.get("session", "group_reply_prefix", fallback="").strip(),

        "ENABLE_DEDUP": str2bool(parser.get("performance", "enable_dedup", fallback=DEFAULTS["enable_dedup"]), True),
        "DEDUP_WINDOW_SECONDS": parser.getint("performance", "dedup_window_seconds", fallback=int(DEFAULTS["dedup_window_seconds"])),
        "SEND_PROCESSING_TIP": str2bool(parser.get("performance", "send_processing_tip", fallback=DEFAULTS["send_processing_tip"]), False),
        "PROCESSING_TIP_DELAY": parser.getfloat("performance", "processing_tip_delay", fallback=float(DEFAULTS["processing_tip_delay"])),

        "OPENCLAW_MODE": parser.get("openclaw", "mode", fallback=DEFAULTS["openclaw_mode"]).strip().lower(),
        "OPENCLAW_BIN": parser.get("openclaw", "bin", fallback=DEFAULTS["openclaw_bin"]).strip(),
        "CHAT_TIMEOUT": parser.getint("openclaw", "chat_timeout", fallback=int(DEFAULTS["chat_timeout"])),
        "CMD_TIMEOUT": parser.getint("openclaw", "cmd_timeout", fallback=int(DEFAULTS["cmd_timeout"])),
        "EXECUTOR_WORKERS": parser.getint("openclaw", "executor_workers", fallback=int(DEFAULTS["executor_workers"])),

        "ALLOW_GROUP_SHARED_RESET": str2bool(parser.get("permissions", "allow_group_shared_reset", fallback=DEFAULTS["allow_group_shared_reset"]), False),

        "REGION_ID": parser.get("init", "region_id", fallback=DEFAULTS["region_id"]).strip(),
    }
    return cfg

def update_config_key(section: str, key: str, value: str):
    parser = configparser.ConfigParser()
    parser.read(CONFIG_PATH, encoding="utf-8")
    if not parser.has_section(section):
        parser.add_section(section)
    parser.set(section, key, value)
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        parser.write(f)

def save_app_id(app_id: str):
    update_config_key("wechat", "app_id", app_id)

def save_public_url(public_url: str):
    update_config_key("wechat", "public_url", public_url)

def add_whitelist(wxid: str):
    parser = configparser.ConfigParser()
    parser.read(CONFIG_PATH, encoding="utf-8")
    current = parser.get("wechat", "white_list_wxid", fallback="").strip()
    items = [x.strip() for x in current.split(",") if x.strip()]
    if wxid not in items:
        items.append(wxid)
    parser.set("wechat", "white_list_wxid", ",".join(items))
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        parser.write(f)

# ============================================================
# 通用工具
# ============================================================
def now_ts() -> float:
    return time.time()

def short_text(text: str, n: int = 120) -> str:
    text = (text or "").replace("\n", " ").strip()
    return text[:n] + ("..." if len(text) > n else "")

def remove_ansi(text: str) -> str:
    return re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])').sub('', text or '')

def safe_session_id(session_id: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_-]", "_", str(session_id or ""))

def cleanup_dedup_window(window_seconds: int):
    cutoff = now_ts() - window_seconds
    with recent_lock:
        expired = [k for k, v in recent_message_ids.items() if v < cutoff]
        for k in expired:
            recent_message_ids.pop(k, None)

def is_duplicate_message(message_id: str, window_seconds: int) -> bool:
    cleanup_dedup_window(window_seconds)
    with recent_lock:
        if message_id in recent_message_ids:
            return True
        recent_message_ids[message_id] = now_ts()
        return False

def make_fallback_msg_id(wxid: str, from_user: str, to_user: str, raw_content: str, msg_type) -> str:
    raw = f"{wxid}|{from_user}|{to_user}|{raw_content}|{msg_type}|{int(time.time() // 3)}"
    return hashlib.md5(raw.encode("utf-8")).hexdigest()

def build_subprocess_env() -> dict:
    env = os.environ.copy()
    for key in [
        "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY",
        "http_proxy", "https_proxy", "all_proxy"
    ]:
        env.pop(key, None)
    env["NO_PROXY"] = "*"
    env["no_proxy"] = "*"
    return env

def save_incoming_image_from_base64(img_b64: str, msg_id: str) -> Optional[str]:
    if not img_b64:
        return None
    try:
        padded = img_b64 + "=" * (-len(img_b64) % 4)
        img_bytes = base64.b64decode(padded)
        filename = f"incoming_{msg_id}_{int(time.time())}.jpg"
        file_path = os.path.join(IMG_DIR, filename)
        with open(file_path, "wb") as f:
            f.write(img_bytes)
        return filename
    except Exception as e:
        logger.error("❌ 保存图片失败: %s", e)
        return None

# ============================================================
# 微信登录
# ============================================================
class WeChatLogin:
    def __init__(self, config: dict):
        self.base_url = config["WX_BASE_URL"]
        self.token = config["WX_API_TOKEN"]
        self.saved_app_id = config["WX_APP_ID"]

    def _headers(self):
        return {
            "VideosApi-token": self.token,
            "Content-Type": "application/json"
        }

    def check_online(self) -> bool:
        if not self.saved_app_id:
            return False
        try:
            logger.info("📡 正在检测微信在线状态...")
            res = requests.post(
                f"{self.base_url}/login/checkOnline",
                headers=self._headers(),
                json={"appId": self.saved_app_id},
                timeout=10,
                proxies=NO_PROXY
            )
            data = res.json()
            return data.get("data") is True
        except Exception as e:
            logger.warning("⚠️ 在线检测失败: %s", e)
            return False

    def get_qr_and_login(self, region_id: str) -> bool:
        try:
            logger.info("📡 正在获取登录二维码...")
            res = requests.post(
                f"{self.base_url}/login/getLoginQrCode",
                headers=self._headers(),
                json={
                    "appId": self.saved_app_id,
                    "proxyIp": "",
                    "regionId": region_id,
                    "type": "mac"
                },
                timeout=15,
                proxies=NO_PROXY
            ).json()

            if res.get("ret") != 200:
                logger.error("❌ 获取二维码失败: %s", res)
                return False

            d = res["data"]
            qr = qrcode.QRCode()
            qr.add_data(d["qrData"])
            qr.print_ascii(invert=True)
            return self.poll_check(d["appId"], d["uuid"])
        except Exception as e:
            logger.error("❌ 登录流程异常: %s", e)
            return False

    def poll_check(self, app_id: str, uuid: str) -> bool:
        elapsed = 0
        while elapsed < 120:
            try:
                res = requests.post(
                    f"{self.base_url}/login/checkLogin",
                    headers=self._headers(),
                    json={
                        "appId": app_id,
                        "proxyIp": "",
                        "uuid": uuid,
                        "autoSliding": "true"
                    },
                    timeout=10,
                    proxies=NO_PROXY
                ).json()

                if res.get("ret") == 200 and res.get("data", {}).get("status") == 2:
                    save_app_id(app_id)
                    logger.info("✅ 微信登录成功")
                    return True
            except Exception as e:
                logger.warning("⚠️ 登录轮询异常: %s", e)

            time.sleep(3)
            elapsed += 3
        return False

# ============================================================
# 图片输出
# ============================================================
def create_terminal_image(text: str, session_id: str) -> str:
    font_size = 20
    font = None
    font_paths = [
        "/System/Library/Fonts/Supplemental/PingFang.ttc",
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        "C:\\Windows\\Fonts\\msyh.ttc",
    ]

    for path in font_paths:
        try:
            font = ImageFont.truetype(path, font_size)
            break
        except Exception:
            continue

    if font is None:
        font = ImageFont.load_default()

    line_height = font_size + 8
    wrapped_lines = []
    max_safe_width = 1000

    raw_lines = text.replace("\r", "").split("\n")
    for i, line in enumerate(raw_lines):
        line = line.replace("\t", "    ")
        if not line.strip() and i > 0 and not raw_lines[i - 1].strip():
            continue

        current_segment = ""
        for char in line:
            bbox = font.getbbox(current_segment + char)
            pixel_w = bbox[2] if bbox else 0
            if pixel_w > max_safe_width:
                wrapped_lines.append(current_segment)
                current_segment = char
            else:
                current_segment += char
        wrapped_lines.append(current_segment)

    if len(wrapped_lines) > 80:
        wrapped_lines = wrapped_lines[:80] + ["... (截断) ..."]

    actual_max_width = 400
    for line in wrapped_lines:
        bbox = font.getbbox(line)
        w = bbox[2] if bbox else 0
        actual_max_width = max(actual_max_width, w)

    img_width = int(actual_max_width) + 60
    img_height = len(wrapped_lines) * line_height + 80

    img = Image.new("RGB", (img_width, img_height), color=(30, 33, 39))
    draw = ImageDraw.Draw(img)

    btn_y = 20
    draw.ellipse((20, btn_y, 32, btn_y + 12), fill=(255, 95, 86))
    draw.ellipse((45, btn_y, 57, btn_y + 12), fill=(255, 189, 46))
    draw.ellipse((70, btn_y, 82, btn_y + 12), fill=(39, 201, 63))

    y_text = 60
    for line in wrapped_lines:
        draw.text((30, y_text), line, font=font, fill=(180, 185, 195))
        y_text += line_height

    filename = f"cmd_{safe_session_id(session_id)}_{int(time.time())}.png"
    file_path = os.path.join(IMG_DIR, filename)
    img.save(file_path)
    return filename

# ============================================================
# 发送消息
# ============================================================
def reply_text(to_wxid: str, text: str, config: dict):
    if not text:
        return
    logger.info("📤 [发送文本] TO=%s | %s", to_wxid, short_text(text))
    try:
        requests.post(
            f"{config['WX_BASE_URL']}/message/postText",
            headers={"VideosApi-token": config["WX_API_TOKEN"]},
            json={
                "appId": config["WX_APP_ID"],
                "toWxid": to_wxid,
                "content": text
            },
            timeout=10,
            proxies=NO_PROXY
        )
    except Exception as e:
        logger.error("❌ 发文本失败: %s", e)

def reply_image(to_wxid: str, img_name: str, config: dict):
    public_url = config["PUBLIC_URL"]
    if not public_url:
        reply_text(to_wxid, "⚠️ 图片已生成，但未配置或未识别到 PUBLIC_URL。", config)
        return

    filename = os.path.basename(img_name)
    img_url = f"{public_url}/images/{quote(filename)}"
    logger.info("🖼️ [发送图片] TO=%s | %s", to_wxid, img_url)

    try:
        resp = requests.post(
            f"{config['WX_BASE_URL']}/message/postImage",
            headers={
                "VideosApi-token": config["WX_API_TOKEN"],
                "Content-Type": "application/json"
            },
            json={
                "appId": config["WX_APP_ID"],
                "toWxid": to_wxid,
                "imgUrl": img_url
            },
            timeout=15,
            proxies=NO_PROXY
        )
        try:
            data = resp.json()
            if data.get("ret") != 200:
                logger.warning("⚠️ 图片发送异常: %s", data)
        except Exception:
            logger.warning("⚠️ 图片发送返回非 JSON: %s", resp.text)
    except Exception as e:
        logger.error("❌ 发图失败: %s", e)

# ============================================================
# OpenClaw 调用层
# ============================================================
class OpenClawAdapter:
    def __init__(self, config: dict):
        self.bin = config["OPENCLAW_BIN"]
        self.chat_timeout = config["CHAT_TIMEOUT"]
        self.cmd_timeout = config["CMD_TIMEOUT"]
        self.env = build_subprocess_env()

    def _run_subprocess(self, cmd, timeout):
        future = openclaw_executor.submit(
            subprocess.run,
            cmd,
            capture_output=True,
            text=True,
            stdin=subprocess.DEVNULL,
            timeout=timeout,
            env=self.env
        )
        return future.result()

    def chat(self, session_id: str, message: str) -> dict:
        sid = safe_session_id(session_id)
        cmd = [self.bin, "agent", "--session-id", sid, "--message", message.strip()]
        logger.info("🤖 [OpenClaw CHAT] sid=%s | %s", sid, short_text(message))
        try:
            res = self._run_subprocess(cmd, self.chat_timeout)
            reply = remove_ansi(res.stdout).strip() if res.returncode == 0 else (
                (remove_ansi(res.stderr).strip() + "\n" + remove_ansi(res.stdout).strip()).strip()
            )
            return {"ok": res.returncode == 0, "reply": reply or "✅ 已处理"}
        except subprocess.TimeoutExpired:
            return {"ok": False, "reply": "❌ OpenClaw 对话超时"}
        except Exception as e:
            return {"ok": False, "reply": f"❌ OpenClaw 调用失败: {e}"}

    def command(self, session_id: str, command_text: str) -> dict:
        sid = safe_session_id(session_id)
        parts = command_text[1:].strip().split() if command_text.startswith("/") else command_text.strip().split()
        if not parts:
            return {"ok": False, "reply": "❌ 空命令"}

        cmd = [self.bin] + parts
        logger.info("🛠️ [OpenClaw CMD] sid=%s | %s", sid, " ".join(cmd))
        try:
            res = self._run_subprocess(cmd, self.cmd_timeout)
            reply = remove_ansi(res.stdout).strip() if res.returncode == 0 else (
                (remove_ansi(res.stderr).strip() + "\n" + remove_ansi(res.stdout).strip()).strip()
            )
            return {"ok": res.returncode == 0, "reply": reply or "✅ 指令执行完毕"}
        except subprocess.TimeoutExpired:
            return {"ok": False, "reply": "❌ 命令执行超时"}
        except Exception as e:
            return {"ok": False, "reply": f"❌ 命令执行失败: {e}"}

    def reset(self, session_id: str) -> dict:
        return {
            "ok": True,
            "reply": f"✅ 已标记重置：{session_id}\n若你的 OpenClaw 有原生 reset 命令，可把 reset() 这里替换掉。"
        }

# ============================================================
# Session 规则
# ============================================================
def build_session_id(chat_id: str, sender_wxid: str, is_group: bool, config: dict) -> str:
    def norm(s: str) -> str:
        return re.sub(r"[^a-zA-Z0-9_-]", "_", str(s or "").strip())

    if not is_group:
        return f"wechat_dm_{norm(chat_id)}"

    if config["GROUP_SESSION_MODE"] == "per_user":
        return f"wechat_group_{norm(chat_id)}_user_{norm(sender_wxid)}"

    return f"wechat_group_{norm(chat_id)}"

# ============================================================
# 本地命令
# ============================================================
def local_help_text() -> str:
    return (
        "📘 可用命令：\n"
        "/help - 查看帮助\n"
        "/status - 查看系统状态\n"
        "/mode - 查看当前模式\n"
        "/workers - 查看 worker 状态\n"
        "/reset - 重置当前会话\n"
    )

def local_status_text(config: dict, session_id: str) -> str:
    total_pending = sum(session_pending.values())
    queue_sizes = [q.qsize() for q in worker_queues]
    return (
        "✅ 系统运行正常\n"
        f"SESSION_ID: {session_id}\n"
        f"OPENCLAW_MODE: {config['OPENCLAW_MODE']}\n"
        f"GROUP_SESSION_MODE: {config['GROUP_SESSION_MODE']}\n"
        f"WORKER_COUNT: {config['WORKER_COUNT']}\n"
        f"EXECUTOR_WORKERS: {config['EXECUTOR_WORKERS']}\n"
        f"CURRENT_SESSION_PENDING: {session_pending.get(session_id, 0)}\n"
        f"TOTAL_PENDING: {total_pending}\n"
        f"QUEUE_SIZES: {queue_sizes}"
    )

def local_mode_text(config: dict) -> str:
    return (
        "🧠 当前模式\n"
        f"OpenClaw: {config['OPENCLAW_MODE']}\n"
        f"Group session mode: {config['GROUP_SESSION_MODE']}"
    )

def local_workers_text(config: dict) -> str:
    q_sizes = [q.qsize() for q in worker_queues]
    return (
        "👷 Worker 状态\n"
        f"WORKER_COUNT: {config['WORKER_COUNT']}\n"
        f"EXECUTOR_WORKERS: {config['EXECUTOR_WORKERS']}\n"
        f"QUEUE_SIZES: {q_sizes}\n"
        f"MAX_PENDING_PER_SESSION: {config['MAX_PENDING_PER_SESSION']}"
    )

def run_local_command(command_text: str, session_id: str, is_group: bool, config: dict, adapter: OpenClawAdapter):
    cmd = command_text.strip().lower()

    if cmd == "/help":
        return {"type": "text", "content": local_help_text()}
    if cmd == "/status":
        return {"type": "text", "content": local_status_text(config, session_id)}
    if cmd == "/mode":
        return {"type": "text", "content": local_mode_text(config)}
    if cmd == "/workers":
        return {"type": "text", "content": local_workers_text(config)}
    if cmd == "/reset":
        if is_group and config["GROUP_SESSION_MODE"] == "shared" and not config["ALLOW_GROUP_SHARED_RESET"]:
            return {
                "type": "text",
                "content": "⚠️ 当前是群共享上下文，默认不允许 /reset。\n如需允许，请把 config.ini 中的 allow_group_shared_reset 改成 true。"
            }
        result = adapter.reset(session_id)
        return {"type": "text", "content": result.get("reply", "✅ 已重置")}
    return None

# ============================================================
# 回调解析（按 videosapi 文档）
# ============================================================
def parse_wechat_payload(data):
    if not isinstance(data, dict):
        logger.warning("⚠️ 回调顶层不是 dict: %r", data)
        return None

    type_name = data.get("TypeName")
    if not isinstance(type_name, str):
        logger.warning("⚠️ TypeName 不是字符串: %r | raw=%r", type_name, data)
        return None

    if type_name != "AddMsg":
        return {
            "event_type": type_name,
            "raw": data
        }

    wxid = str(data.get("Wxid", "") or "").strip()
    msg_data = data.get("Data", {})
    if not isinstance(msg_data, dict):
        logger.warning("⚠️ Data 不是 dict: %r", msg_data)
        return None

    from_obj = msg_data.get("FromUserName", {})
    to_obj = msg_data.get("ToUserName", {})
    content_obj = msg_data.get("Content", {})
    img_buf_obj = msg_data.get("ImgBuf", {})

    from_user = from_obj.get("string", "") if isinstance(from_obj, dict) else str(from_obj or "")
    to_user = to_obj.get("string", "") if isinstance(to_obj, dict) else str(to_obj or "")
    raw_content = content_obj.get("string", "") if isinstance(content_obj, dict) else str(content_obj or "")
    img_buffer_b64 = img_buf_obj.get("buffer", "") if isinstance(img_buf_obj, dict) else ""

    msg_type = msg_data.get("MsgType")
    msg_id = str(msg_data.get("MsgId", "") or "").strip()
    new_msg_id = str(msg_data.get("NewMsgId", "") or "").strip()

    if not from_user and not to_user:
        logger.warning("⚠️ 缺少 FromUserName / ToUserName: %r", data)
        return None

    is_self = bool(wxid and from_user == wxid)
    is_group = from_user.endswith("@chatroom") or to_user.endswith("@chatroom")

    if from_user.endswith("@chatroom"):
        chat_id = from_user
    elif to_user.endswith("@chatroom"):
        chat_id = to_user
    else:
        chat_id = from_user if not is_self else to_user

    sender_wxid = from_user
    actual_text = (raw_content or "").strip()

    if is_group and raw_content and ":\n" in raw_content:
        possible_sender, possible_text = raw_content.split(":\n", 1)
        possible_sender = (possible_sender or "").strip()
        if possible_sender.startswith("wxid_") or possible_sender.startswith("v1_") or possible_sender.startswith("gh_"):
            sender_wxid = possible_sender
            actual_text = (possible_text or "").strip()

    if not msg_id:
        msg_id = new_msg_id or make_fallback_msg_id(wxid, from_user, to_user, raw_content, msg_type)

    return {
        "event_type": "AddMsg",
        "wxid": wxid,
        "msg_id": msg_id,
        "new_msg_id": new_msg_id,
        "msg_type": msg_type,
        "from_user": from_user,
        "to_user": to_user,
        "chat_id": chat_id,
        "sender_wxid": sender_wxid,
        "actual_text": actual_text,
        "raw_content": raw_content,
        "img_buffer_b64": img_buffer_b64,
        "is_group": is_group,
        "is_self": is_self,
        "raw": data,
    }

# ============================================================
# Worker 调度
# ============================================================
def shard_index_for_session(session_id: str, worker_count: int) -> int:
    h = int(hashlib.md5(session_id.encode("utf-8")).hexdigest(), 16)
    return h % worker_count

def send_processing_tip_later(to_wxid: str, session_id: str, config: dict):
    time.sleep(config["PROCESSING_TIP_DELAY"])
    if session_pending.get(session_id, 0) > 0:
        reply_text(to_wxid, "⏳ 正在处理中...", config)

def process_task(task: dict):
    config = task["config"]
    to_wxid = task["to_wxid"]
    text = task["text"]
    session_id = task["session_id"]
    is_group = task["is_group"]

    adapter = OpenClawAdapter(config)

    if config["SEND_PROCESSING_TIP"] and not text.strip().startswith("/"):
        threading.Thread(
            target=send_processing_tip_later,
            args=(to_wxid, session_id, config),
            daemon=True
        ).start()

    local_result = run_local_command(text, session_id, is_group, config, adapter)
    if local_result:
        reply_text(to_wxid, local_result["content"], config)
        return

    if text.strip().startswith("/"):
        result = adapter.command(session_id, text.strip())
        if not result.get("ok", False):
            logger.error("❌ OpenClaw 命令失败 sid=%s | err=%s", session_id, result.get("reply", ""))
            reply_text(to_wxid, "⚠️ 命令执行失败，请稍后重试。", config)
            return

        image_name = create_terminal_image(result.get("reply", "✅ 指令执行完毕"), session_id)
        reply_image(to_wxid, image_name, config)
        return

    result = adapter.chat(session_id, text.strip())
    if not result.get("ok", False):
        logger.error("❌ OpenClaw 对话失败 sid=%s | err=%s", session_id, result.get("reply", ""))
        reply_content = "⚠️ 当前处理失败，请稍后重试。"
    else:
        reply_content = result.get("reply", "✅ 已处理")

    if is_group and config["GROUP_REPLY_PREFIX"]:
        reply_content = f"{config['GROUP_REPLY_PREFIX']}{reply_content}"

    reply_text(to_wxid, reply_content, config)

def worker_loop(worker_id: int, task_queue: queue.Queue):
    logger.info("👷 Worker-%s 已启动", worker_id)
    while True:
        task = task_queue.get()
        session_id = task["session_id"]
        try:
            process_task(task)
        except Exception as e:
            logger.exception("❌ Worker-%s 处理异常: %s", worker_id, e)
            try:
                reply_text(task["to_wxid"], f"❌ 网关处理异常: {e}", task["config"])
            except Exception:
                pass
        finally:
            session_pending[session_id] = max(0, session_pending[session_id] - 1)
            task_queue.task_done()

def start_workers(config: dict):
    global worker_queues
    worker_count = max(1, config["WORKER_COUNT"])
    worker_queues = []

    for i in range(worker_count):
        q = queue.Queue(maxsize=config["QUEUE_MAXSIZE"])
        worker_queues.append(q)
        t = threading.Thread(
            target=worker_loop,
            args=(i + 1, q),
            daemon=True,
            name=f"Worker-{i+1}"
        )
        t.start()

def start_openclaw_executor(config: dict):
    global openclaw_executor
    openclaw_executor = ThreadPoolExecutor(
        max_workers=max(1, config["EXECUTOR_WORKERS"]),
        thread_name_prefix="OpenClawExec"
    )
    logger.info("⚙️ OpenClaw 执行池已启动，大小=%s", config["EXECUTOR_WORKERS"])

# ============================================================
# FastAPI 路由
# ============================================================
@app.get("/healthz")
async def healthz():
    cfg = load_config()
    return {
        "ok": True,
        "openclaw_mode": cfg["OPENCLAW_MODE"],
        "group_session_mode": cfg["GROUP_SESSION_MODE"],
        "worker_count": cfg["WORKER_COUNT"],
        "executor_workers": cfg["EXECUTOR_WORKERS"],
        "queue_sizes": [q.qsize() for q in worker_queues]
    }

@app.post("/wechat/callback")
async def handle_wechat(request: Request):
    try:
        config = load_config()
        body = await request.body()
        logger.info("📦 原始回调: %s", body.decode("utf-8", errors="ignore"))
        data = json.loads(body)

        parsed = parse_wechat_payload(data)
        if not parsed:
            return {"status": "ignored"}

        if parsed.get("event_type") != "AddMsg":
            logger.info("📦 非 AddMsg 事件，已忽略: %s", parsed.get("event_type"))
            return {"status": "ignored_event"}

        if parsed.get("is_self"):
            logger.info("🔁 忽略自己发送的消息: %s", parsed.get("msg_id"))
            return {"status": "ignored_self"}

        msg_id = parsed["msg_id"]
        msg_type = parsed["msg_type"]
        chat_id = parsed["chat_id"]
        sender_wxid = parsed["sender_wxid"]
        actual_text = parsed["actual_text"]
        img_buffer_b64 = parsed.get("img_buffer_b64", "")
        is_group = parsed["is_group"]

        logger.info(
            "📥 [收到消息] msg_type=%s | chat_id=%s | sender=%s | is_group=%s | text=%s",
            msg_type, chat_id, sender_wxid, is_group, short_text(actual_text)
        )

        if config["ENABLE_DEDUP"]:
            if is_duplicate_message(msg_id, config["DEDUP_WINDOW_SECONDS"]):
                logger.info("♻️ [消息去重] msg_id=%s", msg_id)
                return {"status": "duplicate"}

        # 只处理文本和图片
        if msg_type not in (1, 3):
            logger.info("📭 暂时只处理文本和图片消息，已忽略 MsgType=%s", msg_type)
            return {"status": "ignored_msg_type"}

        if msg_type == 1 and actual_text == "我是你的主人":
            if sender_wxid not in config["WHITE_LIST_WXID"]:
                add_whitelist(sender_wxid)
                reply_text(chat_id, "👑 认主成功，已加入白名单。", config)
            return {"status": "master_added"}

        if is_group:
            trigger = config["GROUP_TRIGGER"]
            if msg_type == 1:
                if trigger and not actual_text.startswith(trigger):
                    return {"status": "ignored_group_no_trigger"}
                if trigger:
                    actual_text = actual_text[len(trigger):].strip()
        else:
            if sender_wxid not in config["WHITE_LIST_WXID"]:
                logger.info("🚫 私聊未通过白名单: sender=%s", sender_wxid)
                return {"status": "ignored_not_whitelisted"}

        # 图片消息：保存图片并交给 OpenClaw 分析
        if msg_type == 3:
            filename = save_incoming_image_from_base64(img_buffer_b64, msg_id)
            if not filename:
                reply_text(chat_id, "⚠️ 收到图片，但暂时无法解析图片数据。", config)
                return {"status": "image_save_failed"}

            local_path = os.path.join(IMG_DIR, filename)
            image_url = f"{config['PUBLIC_URL']}/images/{quote(filename)}" if config["PUBLIC_URL"] else ""

            actual_text = (
                "请识别并分析这张图片，用中文回答。\n"
                f"本地文件路径：{local_path}\n"
                f"图片URL：{image_url}\n"
                "如果 URL 可访问，优先读取 URL；否则尝试读取本地文件路径。"
            )

        if not actual_text:
            return {"status": "empty"}

        session_id = build_session_id(chat_id, sender_wxid, is_group, config)

        if session_pending[session_id] >= config["MAX_PENDING_PER_SESSION"]:
            logger.warning("⚠️ 会话积压过多 sid=%s", session_id)
            reply_text(chat_id, "⚠️ 当前会话任务过多，请稍后再试。", config)
            return {"status": "too_many_pending"}

        session_pending[session_id] += 1

        shard_idx = shard_index_for_session(session_id, config["WORKER_COUNT"])
        worker_queues[shard_idx].put_nowait({
            "to_wxid": chat_id,
            "text": actual_text,
            "session_id": session_id,
            "is_group": is_group,
            "config": config
        })

        return {
            "status": "queued",
            "session_id": session_id,
            "worker": shard_idx,
            "queue_size": worker_queues[shard_idx].qsize()
        }

    except queue.Full:
        logger.error("❌ 对应 worker 队列已满")
        return {"status": "queue_full"}
    except Exception as e:
        logger.exception("❌ 回调处理异常: %s", e)
        return {"status": "error", "message": str(e)}

@app.api_route("/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "CONNECT"])
async def catch_all(path_name: str):
    return {"status": "caught", "path": path_name}

# ============================================================
# 主入口
# ============================================================
def print_usage_guide(config: dict):
    logger.info("🎊 系统启动完成")
    logger.info("👉 群触发词: %s", config["GROUP_TRIGGER"])
    logger.info("👉 OpenClaw 模式: %s", config["OPENCLAW_MODE"])
    logger.info("👉 Worker 数量: %s", config["WORKER_COUNT"])
    logger.info("👉 OpenClaw 执行池: %s", config["EXECUTOR_WORKERS"])
    logger.info("👉 群上下文模式: %s", config["GROUP_SESSION_MODE"])
    logger.info("👉 正在处理中提示: %s", config["SEND_PROCESSING_TIP"])
    logger.info("👉 命令: /help /status /mode /workers /reset")
    logger.info("👉 回调地址: %s/wechat/callback", config["PUBLIC_URL"])

def main():
    config = load_config()

    if not config["WX_API_TOKEN"]:
        logger.error("❌ api_token 为空，请重新运行初始化。")
        return

    logger.info("🔌 欢迎使用 WeChat OpenClaw Gateway 单文件版（完整最终版）")

    login_handler = WeChatLogin(config)
    if login_handler.check_online():
        logger.info("✅ 微信账号在线，直接启动")
    else:
        region_id = config["REGION_ID"] or "320000"
        logger.info("📍 使用地区代码: %s", region_id)
        if not login_handler.get_qr_and_login(region_id):
            logger.error("❌ 登录失败，程序退出")
            return

    config = load_config()
    start_openclaw_executor(config)
    start_workers(config)
    print_usage_guide(config)

    uvicorn.run(app, host="0.0.0.0", port=config["PORT"])

if __name__ == "__main__":
    main()