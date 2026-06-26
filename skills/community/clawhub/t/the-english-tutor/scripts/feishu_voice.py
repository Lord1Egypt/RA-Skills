#!/usr/bin/env python3
"""
飞书语音消息发送 · 纯 Python 实现
无需 Node.js，直接调飞书 API + MiniMax TTS + Piper 兜底

流程：
  文本 → MiniMax TTS (MP3) → ffmpeg 转 Opus → 上传飞书 → 发 audio 消息
                     ↑
            配额耗尽时自动切换 Piper
                     ↓
            Piper WAV → ffmpeg Opus

用法:
  python3 feishu_voice.py <text>                    # 发送语音
  python3 feishu_voice.py <text> --dry-run          # 仅 TTS，不发飞书
  python3 feishu_voice.py <text> --provider piper   # 强制用 Piper
"""
import argparse
import base64
import http.client
import json
import logging
import os
import subprocess
import sys
import tempfile
from urllib.request import urlopen, Request
from urllib.error import URLError

logging.basicConfig(
    level=logging.INFO,
    format="[FeishuVoice] %(levelname)s %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("feishu_voice")

DEFAULT_CONFIG = os.path.join(os.path.expanduser("~"), ".openclaw", "english-tutor", "config.json")


# ── 日志 ───────────────────────────────────────────────────
def log(msg):
    logger.info(msg)


def die(msg):
    logger.error("❌ %s", msg)
    sys.exit(1)


# ── 配置加载 ───────────────────────────────────────────────
def load_config(path=None):
    """从 JSON 文件读取配置（不写磁盘），敏感字段从环境变量优先读取"""
    cfg = {}
    p = path or DEFAULT_CONFIG
    if os.path.exists(p):
        try:
            with open(p) as f:
                cfg = json.load(f)
        except Exception:
            pass

    # 环境变量优先（生产环境由 cron env 注入）
    return {
        "feishu_app_id":      os.environ.get("FEISHU_APP_ID")      or cfg.get("feishu_app_id", ""),
        "feishu_app_secret":  os.environ.get("FEISHU_APP_SECRET")  or cfg.get("feishu_app_secret", ""),
        "feishu_user_open_id":os.environ.get("FEISHU_USER_OPEN_ID") or cfg.get("feishu_user_open_id", ""),
        "minimax_api_key":    os.environ.get("MINIMAX_API_KEY")    or cfg.get("minimax_api_key", ""),
        "tts_provider":       os.environ.get("TTS_PROVIDER")       or cfg.get("tts_provider", "minimax"),
        "minimax_tts_model":  os.environ.get("MINIMAX_TTS_MODEL")  or cfg.get("minimax_tts_model", ""),  # 有 Key 时推荐 speech-2.8-hd
        "minimax_tts_speed":  os.environ.get("MINIMAX_TTS_SPEED")  or cfg.get("minimax_tts_speed", "1.05"),
        "minimax_tts_voice":  os.environ.get("MINIMAX_TTS_VOICE_ID") or cfg.get("minimax_tts_voice_id", ""),  # 有 Key 时推荐 male-qn-qingse
        "piper_bin":          os.environ.get("PIPER_BIN")          or cfg.get("piper_bin", ""),
        "piper_model":        os.environ.get("PIPER_MODEL")        or cfg.get("piper_model", ""),
    }


# ── 飞书 API ──────────────────────────────────────────────
def feishu_req(method, path, token=None, body=None):
    """纯 Python 调飞书 HTTPS API，无 curl"""
    conn = http.client.HTTPSConnection("open.feishu.cn", timeout=30)
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if body:
        body = json.dumps(body).encode()
        headers["Content-Length"] = str(len(body))
    conn.request(method, path, body=body, headers=headers)
    resp = conn.getresponse()
    data = resp.read()
    conn.close()
    try:
        return json.loads(data)
    except Exception:
        return {"raw": data.decode(errors="replace")}


def get_feishu_token(app_id, app_secret):
    if not app_id or not app_secret:
        raise RuntimeError("FEISHU_CONFIG_MISSING")
    r = feishu_req("POST", "/open-apis/auth/v3/tenant_access_token/internal",
                   body={"app_id": app_id, "app_secret": app_secret})
    if r.get("code") != 0:
        raise RuntimeError(f"Feishu token failed: {r.get('msg')}")
    return r["tenant_access_token"]


def upload_file(token, file_path, file_type="opus"):
    """上传文件到飞书，返回 file_key"""
    import io
    boundary = f"----Feishu{B}oundary{os.getpid()}"
    file_name = os.path.basename(file_path)
    file_data = open(file_path, "rb").read()

    parts = [
        b"--" + boundary.encode() + b"\r\nContent-Disposition: form-data; name=\"file_type\"\r\n\r\n" + file_type.encode() + b"\r\n",
        b"--" + boundary.encode() + b"\r\nContent-Disposition: form-data; name=\"file_name\"\r\n\r\n" + file_name.encode() + b"\r\n",
        b"--" + boundary.encode() + b"\r\nContent-Disposition: form-data; name=\"file\"; filename=\"" + file_name.encode() + b"\"\r\nContent-Type: audio/mpeg\r\n\r\n",
        file_data,
        b"\r\n--" + boundary.encode() + b"--\r\n",
    ]
    body = b"".join(parts)
    conn = http.client.HTTPSConnection("open.feishu.cn", timeout=30)
    conn.request("POST", "/open-apis/im/v1/files",
                 body=body,
                 headers={"Authorization": f"Bearer {token}",
                          "Content-Type": f"multipart/form-data; boundary={boundary}"})
    resp = conn.getresponse()
    data = json.loads(resp.read())
    conn.close()
    if data.get("code") != 0:
        raise RuntimeError(f"Upload failed: {data.get('msg')}")
    return data["data"]["file_key"]


def send_audio(token, receive_id, file_key):
    r = feishu_req("POST", "/open-apis/im/v1/messages?receive_id_type=open_id",
                    token=token,
                    body={"receive_id": receive_id, "msg_type": "audio",
                          "content": json.dumps({"file_key": file_key})})
    if r.get("code") != 0:
        raise RuntimeError(f"Send failed: {r.get('msg')}")
    return r["data"]


# ── MiniMax TTS ────────────────────────────────────────────
def minimax_tts(api_key, text, model, speed, voice_id):
    """纯 Python MiniMax TTS，返回 MP3 文件路径"""
    if not api_key:
        raise RuntimeError("MINIMAX_API_KEY_NOT_CONFIGURED")

    # 有 API Key 时应用推荐值
    resolved_model = model or 'speech-2.8-hd'
    resolved_voice = voice_id or 'male-qn-qingse'

    payload = json.dumps({
        "model": resolved_model,
        "text": text,
        "stream": False,
        "voice_setting": {
            "voice_id": resolved_voice,
            "speed": float(speed),
            "vol": 1, "pitch": 0,
        },
        "audio_setting": {
            "sample_rate": 32000,
            "bitrate": 128000,
            "format": "mp3",
            "channel": 1,
        },
    }).encode()

    req = Request(
        "https://api.minimax.com/v1/t2a_v2",
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Content-Length": str(len(payload)),
        },
        method="POST",
    )
    with urlopen(req, timeout=30) as resp:
        raw = resp.read()

    data = json.loads(raw)
    if data.get("base_resp", {}).get("status_code") != 0:
        raise RuntimeError(f"TTS error: {data.get('base_resp', {}).get('status_msg')}")

    hex_audio = data.get("data", {}).get("audio", "")
    if not hex_audio:
        raise RuntimeError("TTS returned no audio")

    mp3_path = os.path.join(tempfile.gettempdir(), f"tts_{os.getpid()}.mp3")
    with open(mp3_path, "wb") as f:
        f.write(bytes.fromhex(hex_audio))
    return mp3_path


# ── Piper TTS ─────────────────────────────────────────────
def piper_tts(text, piper_bin, piper_model):
    """本地 Piper TTS，返回 WAV 文件路径"""
    if not os.path.exists(piper_bin):
        raise RuntimeError(f"PIPER_BIN not found: {piper_bin}")
    if not os.path.exists(piper_model):
        raise RuntimeError(f"PIPER_MODEL not found: {piper_model}")

    wav_path = os.path.join(tempfile.gettempdir(), f"piper_{os.getpid()}.wav")
    env = os.environ.copy()
    lib_dir = os.path.dirname(piper_bin)
    env["LD_LIBRARY_PATH"] = lib_dir + (":" + env["LD_LIBRARY_PATH"] if env.get("LD_LIBRARY_PATH") else "")

    proc = subprocess.run(
        [piper_bin, "--model", piper_model, "--output_file", wav_path],
        input=text.encode(),  # piper 从 stdin 读文本
        env=env, timeout=60, capture_output=True,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"Piper failed: {proc.stderr.decode()[:200]}")
    return wav_path


# ── ffmpeg 转换 ───────────────────────────────────────────
def convert_to_opus(input_path):
    """ffmpeg 转 opus，返回 opus 文件路径"""
    opus_path = input_path.replace(".mp3", ".opus").replace(".wav", ".opus")
    r = subprocess.run(
        ["ffmpeg", "-y", "-i", input_path,
         "-ar", "16000", "-ac", "1", "-acodec", "libopus", "-b:a", "128k", opus_path],
        capture_output=True, timeout=60,
    )
    if r.returncode != 0:
        raise RuntimeError(f"ffmpeg failed: {r.stderr.decode()[:200]}")
    # 清理输入文件
    try:
        os.unlink(input_path)
    except Exception:
        pass
    return opus_path


# ── 主流程 ────────────────────────────────────────────────
def send_voice(text, user_open_id=None, provider="minimax", **kwargs):
    """
    发送飞书语音消息
    返回 {"message_id": "...} 或 {"skipped": True}
    """
    if not user_open_id:
        log("FEISHU_USER_OPEN_ID 未配置，跳过")
        return {"skipped": True}
    if not kwargs.get("feishu_app_id") or not kwargs.get("feishu_app_secret"):
        log("飞书配置缺失，跳过")
        return {"skipped": True}

    audio_path = None
    try:
        # Step 1: TTS
        if provider == "piper":
            log("使用 Piper 本地 TTS")
            wav = piper_tts(text, kwargs["piper_bin"], kwargs["piper_model"])
            audio_path = convert_to_opus(wav)
        else:
            try:
                log("使用 MiniMax 云端 TTS")
                # 有 Key 时应用推荐默认值
                resolved_model = kwargs["minimax_tts_model"] or 'speech-2.8-hd'
                resolved_voice = kwargs["minimax_tts_voice"] or 'male-qn-qingse'
                mp3 = minimax_tts(
                    kwargs["minimax_api_key"], text,
                    resolved_model,
                    kwargs["minimax_tts_speed"],
                    resolved_voice,
                )
                audio_path = convert_to_opus(mp3)
            except RuntimeError as e:
                msg = str(e)
                if "MINIMAX_API_KEY_NOT_CONFIGURED" in msg or "TTS error" in msg:
                    # 配额耗尽或未配置，尝试 Piper 兜底
                    if kwargs.get("piper_bin") and kwargs.get("piper_model"):
                        log(f"MiniMax TTS 失败，切换 Piper: {msg}")
                        wav = piper_tts(text, kwargs["piper_bin"], kwargs["piper_model"])
                        audio_path = convert_to_opus(wav)
                    else:
                        raise
                else:
                    raise

        # Step 2: 飞书
        token = get_feishu_token(kwargs["feishu_app_id"], kwargs["feishu_app_secret"])
        file_key = upload_file(token, audio_path)
        result = send_audio(token, user_open_id, file_key)
        log(f"发送成功: {result['message_id']}")
        return result

    finally:
        if audio_path and os.path.exists(audio_path):
            try:
                os.unlink(audio_path)
            except Exception:
                pass


# ── CLI ────────────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="发送飞书语音消息")
    parser.add_argument("text", nargs="?", help="要发送的文字内容")
    parser.add_argument("--dry-run", action="store_true", help="仅 TTS，不发飞书")
    parser.add_argument("--provider", choices=["minimax", "piper"], default="minimax",
                        help="TTS 方案")
    args = parser.parse_args()

    if not args.text:
        die("用法: feishu_voice.py <文字内容> [--dry-run] [--provider piper]")

    cfg = load_config()

    if args.dry_run:
        try:
            if args.provider == "piper":
                p = piper_tts(args.text, cfg["piper_bin"], cfg["piper_model"])
            else:
                p = minimax_tts(args.text, cfg["minimax_api_key"],
                                cfg["minimax_tts_model"], cfg["minimax_tts_speed"],
                                cfg["minimax_tts_voice"])
            print(f"TTS OK: {p}")
        except Exception as e:
            die(f"TTS 失败: {e}")
    else:
        result = send_voice(args.text, cfg["feishu_user_open_id"],
                            args.provider, **cfg)
        print(json.dumps(result))
