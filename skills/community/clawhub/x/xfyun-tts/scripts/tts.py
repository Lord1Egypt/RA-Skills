#!/usr/bin/env python3
"""iFlytek Ultra-Realistic TTS (超拟人语音合成).

Synthesize natural, expressive speech from text using iFlytek's
ultra-realistic voice synthesis WebSocket API.

Environment variables:
    XFYUN_APP_ID      - Required. App ID from https://console.xfyun.cn
    XFYUN_API_KEY     - Required. API Key
    XFYUN_API_SECRET  - Required. API Secret

Usage:
    python tts.py "你好，欢迎使用科大讯飞语音合成。"
    python tts.py "Hello world" --output hello.mp3
    python tts.py --file article.txt --voice x5_lingyuzhao_flow
    echo "流式文本输入" | python tts.py --output speech.mp3
    python tts.py "测试" --format pcm --sample-rate 16000
    python tts.py "测试" --speed 70 --volume 80
"""

import argparse
import base64
import hashlib
import hmac
import json
import os
import ssl
import struct
import sys
import threading
import time
import urllib.parse
from datetime import datetime
from wsgiref.handlers import format_date_time
from time import mktime

WS_API_URL = "wss://cbm01.cn-huabei-1.xf-yun.com/v1/private/mcd9m97e6"
DEFAULT_VCN = "x5_lingyuzhao_flow"


# ─── Minimal WebSocket client (stdlib only, no pip) ───────────────────────────

class SimpleWebSocket:
    """Bare-bones RFC 6455 WebSocket client using only stdlib."""

    def __init__(self, url, on_message=None, on_error=None, on_close=None, on_open=None):
        self.url = url
        self.on_message = on_message or (lambda ws, msg: None)
        self.on_error = on_error or (lambda ws, err: None)
        self.on_close = on_close or (lambda ws: None)
        self.on_open = on_open or (lambda ws: None)
        self._sock = None
        self._closed = False

    def connect(self):
        """Connect and run the message loop."""
        parsed = urllib.parse.urlparse(self.url)
        host = parsed.hostname
        port = parsed.port or (443 if parsed.scheme == "wss" else 80)
        path = parsed.path
        if parsed.query:
            path += "?" + parsed.query

        import socket
        raw = socket.create_connection((host, port), timeout=30)
        if parsed.scheme == "wss":
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            self._sock = ctx.wrap_socket(raw, server_hostname=host)
        else:
            self._sock = raw

        # WebSocket handshake
        ws_key = base64.b64encode(os.urandom(16)).decode()
        handshake = (
            f"GET {path} HTTP/1.1\r\n"
            f"Host: {host}\r\n"
            f"Upgrade: websocket\r\n"
            f"Connection: Upgrade\r\n"
            f"Sec-WebSocket-Key: {ws_key}\r\n"
            f"Sec-WebSocket-Version: 13\r\n"
            f"\r\n"
        )
        self._sock.sendall(handshake.encode())

        # Read handshake response
        resp = b""
        while b"\r\n\r\n" not in resp:
            chunk = self._sock.recv(4096)
            if not chunk:
                raise ConnectionError("Connection closed during handshake")
            resp += chunk

        status_line = resp.split(b"\r\n")[0].decode()
        if "101" not in status_line:
            raise ConnectionError(f"WebSocket handshake failed: {status_line}")

        try:
            self.on_open(self)
        except Exception as e:
            self.on_error(self, e)
            return

        # Message loop
        while not self._closed:
            try:
                msg = self._recv_frame()
                if msg is None:
                    break
                self.on_message(self, msg)
            except Exception as e:
                if not self._closed:
                    self.on_error(self, e)
                break

        self.on_close(self)

    def send(self, data):
        """Send a text frame."""
        if isinstance(data, str):
            data = data.encode("utf-8")
        self._send_frame(data, opcode=0x1)

    def close(self):
        """Close the connection."""
        self._closed = True
        try:
            self._send_frame(b"", opcode=0x8)
        except Exception:
            pass
        try:
            self._sock.close()
        except Exception:
            pass

    def _send_frame(self, data, opcode=0x1):
        """Send a masked WebSocket frame."""
        length = len(data)
        header = bytearray()
        header.append(0x80 | opcode)  # FIN + opcode

        if length < 126:
            header.append(0x80 | length)  # MASK bit set
        elif length < 65536:
            header.append(0x80 | 126)
            header.extend(struct.pack("!H", length))
        else:
            header.append(0x80 | 127)
            header.extend(struct.pack("!Q", length))

        mask = os.urandom(4)
        header.extend(mask)

        masked = bytearray(data)
        for i in range(len(masked)):
            masked[i] ^= mask[i % 4]

        self._sock.sendall(bytes(header) + bytes(masked))

    def _recv_exact(self, n):
        """Read exactly n bytes."""
        buf = b""
        while len(buf) < n:
            chunk = self._sock.recv(n - len(buf))
            if not chunk:
                return None
            buf += chunk
        return buf

    def _recv_frame(self):
        """Receive and decode one WebSocket frame."""
        head = self._recv_exact(2)
        if head is None:
            return None

        opcode = head[0] & 0x0F
        masked = (head[1] & 0x80) != 0
        length = head[1] & 0x7F

        if length == 126:
            raw = self._recv_exact(2)
            if raw is None:
                return None
            length = struct.unpack("!H", raw)[0]
        elif length == 127:
            raw = self._recv_exact(8)
            if raw is None:
                return None
            length = struct.unpack("!Q", raw)[0]

        if masked:
            mask = self._recv_exact(4)
            if mask is None:
                return None

        payload = self._recv_exact(length)
        if payload is None:
            return None

        if masked:
            payload = bytearray(payload)
            for i in range(len(payload)):
                payload[i] ^= mask[i % 4]
            payload = bytes(payload)

        if opcode == 0x8:  # Close frame
            return None
        if opcode == 0x9:  # Ping
            self._send_frame(payload, opcode=0xA)
            return self._recv_frame()
        if opcode == 0xA:  # Pong
            return self._recv_frame()

        return payload.decode("utf-8") if opcode == 0x1 else payload


# ─── Auth ─────────────────────────────────────────────────────────────────────

def build_ws_auth_url(request_url: str, api_key: str, api_secret: str) -> str:
    """Build HMAC-SHA256 signed WebSocket authentication URL."""
    parsed = urllib.parse.urlparse(request_url)
    host = parsed.hostname
    path = parsed.path
    date = format_date_time(mktime(datetime.now().timetuple()))

    signature_origin = f"host: {host}\ndate: {date}\nGET {path} HTTP/1.1"
    signature_sha = hmac.new(
        api_secret.encode("utf-8"),
        signature_origin.encode("utf-8"),
        digestmod=hashlib.sha256,
    ).digest()
    signature_b64 = base64.b64encode(signature_sha).decode("utf-8")

    authorization_origin = (
        f'api_key="{api_key}", algorithm="hmac-sha256", '
        f'headers="host date request-line", signature="{signature_b64}"'
    )
    authorization = base64.b64encode(authorization_origin.encode("utf-8")).decode("utf-8")

    params = {"host": host, "date": date, "authorization": authorization}
    return request_url + "?" + urllib.parse.urlencode(params)


# ─── TTS Logic ────────────────────────────────────────────────────────────────

class TTSSynthesizer:
    """Handles the TTS WebSocket session."""

    def __init__(self, app_id, api_key, api_secret, args):
        self.app_id = app_id
        self.api_key = api_key
        self.api_secret = api_secret
        self.args = args
        self.audio_chunks = []
        self.error = None
        self.sid = None
        self.done = threading.Event()

    def _build_request(self, text: str) -> dict:
        """Build the WebSocket request payload."""
        a = self.args

        # Map format name to encoding parameter
        encoding_map = {"mp3": "lame", "pcm": "raw", "speex": "speex", "opus": "opus"}
        audio_encoding = encoding_map.get(a.format, a.format)

        request = {
            "header": {
                "app_id": self.app_id,
                "status": 2,  # single-shot (full text at once)
            },
            "parameter": {
                "tts": {
                    "vcn": a.voice,
                    "volume": a.volume,
                    "speed": a.speed,
                    "pitch": a.pitch,
                    "bgs": a.bgs,
                    "reg": a.reg,
                    "rdn": a.rdn,
                    "rhy": 0,
                    "audio": {
                        "encoding": audio_encoding,
                        "sample_rate": a.sample_rate,
                        "channels": 1,
                        "bit_depth": 16,
                        "frame_size": 0,
                    },
                },
            },
            "payload": {
                "text": {
                    "encoding": "utf8",
                    "compress": "raw",
                    "format": "plain",
                    "status": 2,
                    "seq": 0,
                    "text": base64.b64encode(text.encode("utf-8")).decode("utf-8"),
                },
            },
        }
        return request

    def _on_message(self, ws, message):
        try:
            msg = json.loads(message)
            code = msg.get("header", {}).get("code", -1)
            self.sid = msg.get("header", {}).get("sid", self.sid)

            if code != 0:
                err_msg = msg.get("header", {}).get("message", "unknown error")
                self.error = f"Error (code {code}): {err_msg}"
                ws.close()
                return

            if "payload" in msg and "audio" in msg["payload"]:
                audio_data = msg["payload"]["audio"].get("audio", "")
                if audio_data:
                    self.audio_chunks.append(base64.b64decode(audio_data))
                status = msg["payload"]["audio"].get("status", 0)
                if status == 2:
                    ws.close()

        except Exception as e:
            self.error = f"Parse error: {e}"
            ws.close()

    def _on_error(self, ws, error):
        self.error = str(error)
        self.done.set()

    def _on_close(self, ws):
        self.done.set()

    def _on_open(self, ws):
        def send_text():
            try:
                request = self._build_request(self.text)
                ws.send(json.dumps(request))
            except Exception as e:
                self.error = f"Send error: {e}"
                ws.close()

        t = threading.Thread(target=send_text, daemon=True)
        t.start()

    def synthesize(self, text: str) -> bytes:
        """Synthesize text to audio bytes."""
        self.text = text
        self.audio_chunks = []
        self.error = None
        self.done.clear()

        auth_url = build_ws_auth_url(WS_API_URL, self.api_key, self.api_secret)

        ws = SimpleWebSocket(
            auth_url,
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close,
            on_open=self._on_open,
        )

        # Run WebSocket in a thread
        ws_thread = threading.Thread(target=ws.connect, daemon=True)
        ws_thread.start()

        # Wait for completion with timeout
        self.done.wait(timeout=120)

        if self.error:
            raise RuntimeError(self.error)

        return b"".join(self.audio_chunks)


# ─── CLI ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="iFlytek Ultra-Realistic TTS (超拟人语音合成) — synthesize expressive speech from text."
    )
    parser.add_argument("text", nargs="?", default=None, help="Text to synthesize")
    parser.add_argument("--file", "-f", help="Read text from a file")
    parser.add_argument("--output", "-o", help="Output audio file path (default: output.mp3)")
    parser.add_argument(
        "--voice", "-v",
        default=DEFAULT_VCN,
        help=f"Voice name / vcn (default: {DEFAULT_VCN})",
    )
    parser.add_argument(
        "--format",
        choices=["mp3", "pcm", "speex", "opus"],
        default="mp3",
        help="Audio output format (default: mp3)",
    )
    parser.add_argument("--sample-rate", type=int, default=24000, choices=[8000, 16000, 24000], help="Sample rate (default: 24000)")
    parser.add_argument("--speed", type=int, default=50, help="Speed 0-100, 50=normal (default: 50)")
    parser.add_argument("--volume", type=int, default=50, help="Volume 0-100, 50=normal (default: 50)")
    parser.add_argument("--pitch", type=int, default=50, help="Pitch 0-100, 50=normal (default: 50)")
    parser.add_argument("--bgs", type=int, default=0, choices=[0, 1, 2], help="Background sound: 0=none, 1=bg1, 2=bg2 (default: 0)")
    parser.add_argument("--reg", type=int, default=0, choices=[0, 1, 2], help="English pronunciation: 0=auto, 1=spell, 2=letter (default: 0)")
    parser.add_argument("--rdn", type=int, default=0, choices=[0, 1, 2, 3], help="Number pronunciation: 0=auto, 1=value, 2=string, 3=string-prefer (default: 0)")
    parser.add_argument("--list-voices", action="store_true", help="List available voices and exit")

    args = parser.parse_args()

    if args.list_voices:
        print_voice_list()
        return

    # Determine input text
    if args.file:
        if not os.path.exists(args.file):
            print(f"Error: File not found: {args.file}", file=sys.stderr)
            sys.exit(1)
        with open(args.file, "r", encoding="utf-8") as f:
            text = f.read().strip()
    elif args.text:
        text = args.text
    else:
        if not sys.stdin.isatty():
            text = sys.stdin.read().strip()
        else:
            print("Error: No input. Pass text as argument, use --file, or pipe via stdin.", file=sys.stderr)
            parser.print_help(sys.stderr)
            sys.exit(1)

    if not text:
        print("Error: Input text is empty.", file=sys.stderr)
        sys.exit(1)

    # Read credentials
    app_id = os.environ.get("XFYUN_APP_ID")
    api_key = os.environ.get("XFYUN_API_KEY")
    api_secret = os.environ.get("XFYUN_API_SECRET")

    missing = []
    if not app_id:
        missing.append("XFYUN_APP_ID")
    if not api_key:
        missing.append("XFYUN_API_KEY")
    if not api_secret:
        missing.append("XFYUN_API_SECRET")
    if missing:
        print(f"Error: Missing environment variables: {', '.join(missing)}", file=sys.stderr)
        print("Get credentials from https://console.xfyun.cn", file=sys.stderr)
        sys.exit(1)

    # Determine output path
    ext_map = {"mp3": ".mp3", "pcm": ".pcm", "speex": ".speex", "opus": ".opus"}
    if args.output:
        output_path = args.output
    else:
        output_path = "output" + ext_map.get(args.format, ".mp3")

    # Synthesize
    print(f"Synthesizing with voice '{args.voice}'...", file=sys.stderr)
    synth = TTSSynthesizer(app_id, api_key, api_secret, args)

    try:
        audio_data = synth.synthesize(text)
    except RuntimeError as e:
        print(f"Synthesis failed: {e}", file=sys.stderr)
        sys.exit(1)

    if not audio_data:
        print("Error: No audio data received.", file=sys.stderr)
        sys.exit(1)

    with open(output_path, "wb") as f:
        f.write(audio_data)

    size_kb = len(audio_data) / 1024
    print(f"✅ Audio saved to {output_path} ({size_kb:.1f} KB)", file=sys.stderr)
    if synth.sid:
        print(f"SID: {synth.sid}", file=sys.stderr)

    # Print the absolute path to stdout for easy piping
    print(os.path.abspath(output_path))


def print_voice_list():
    """Print available voice names."""
    voices = [
        ("x5_lingyuzhao_flow", "聆玉昭", "成年女", "中文普通话", "交互聊天"),
        ("x5_lingxiaotang_flow", "聆小糖", "成年女", "中文普通话", "语音助手"),
        ("x5_EnUs_Grant_flow", "Grant", "成年女", "英文美式口音", "交互聊天"),
        ("x5_EnUs_Lila_flow", "Lila", "成年女", "英文美式口音", "交互聊天"),
        ("x6_lingxiaoli_pro", "聆小璃", "成年女", "中文普通话", "交互聊天"),
        ("x6_xiaoqiChat_pro", "聆小琪", "成年女", "中文普通话", "交互聊天"),
        ("x6_lingfeiyi_pro", "聆飞逸", "成年男", "中文普通话", "交互聊天"),
        ("x6_feizheChat_pro", "聆飞哲", "成年男", "中文普通话", "交互聊天"),
        ("x6_lingxiaoyue_pro", "聆小玥", "成年女", "中文普通话", "交互聊天"),
        ("x6_lingxiaoxuan_pro", "聆小璇", "成年女", "中文普通话", "交互聊天"),
        ("x6_lingyuyan_pro", "聆玉言", "成年女", "中文普通话", "交互聊天"),
        ("x6_pangbainan1_pro", "旁白男声", "成年男", "中文普通话", "旁白配音"),
        ("x6_pangbainv1_pro", "旁白女声", "成年女", "中文普通话", "旁白配音"),
        ("x6_lingfeihan_pro", "聆飞瀚", "成年男", "中文普通话", "纪录片"),
        ("x6_lingfeihao_pro", "聆飞皓", "成年男", "中文普通话", "广告促销"),
        ("x6_gufengpangbai_pro", "古风旁白", "成年男", "中文普通话", "旁白配音"),
        ("x6_lingyuaner_pro", "聆园儿", "成年女", "中文普通话", "儿童绘本"),
        ("x6_ganliannvxing_pro", "干练女性", "成年女", "中文普通话", "角色配音"),
        ("x6_ruyadashu_pro", "儒雅大叔", "成年男", "中文普通话", "角色配音"),
        ("x6_lingyufei_pro", "聆玉菲", "成年女", "中文普通话", "时政新闻"),
        ("x6_lingxiaoshan_pro", "聆小珊", "成年女", "中文普通话", "时政新闻"),
        ("x6_lingxiaoyun_pro", "聆小芸", "成年女", "中文普通话", "角色配音"),
        ("x6_lingyouyou_pro", "聆佑佑", "童年女", "中文普通话", "交互聊天"),
        ("x6_lingxiaoying_pro", "聆小颖", "成年女", "中文普通话", "交互聊天"),
        ("x6_lingxiaozhen_pro", "聆小瑱", "成年女", "中文普通话", "直播带货"),
        ("x6_lingfeibo_pro", "聆飞博", "成年男", "中文普通话", "时政新闻"),
        ("x6_waiguodashu_pro", "外国大叔", "成年男", "中文普通话（外国人说中文）", "角色配音"),
        ("x6_gaolengnanshen_pro", "高冷男神", "成年男", "中文普通话", "角色配音"),
        ("x6_dongmanshaonv_pro", "动漫少女", "成年女", "中文普通话", "动漫角色"),
        ("x6_wennuancixingnansheng_mini", "温暖磁性男声", "成年男", "中文普通话", "角色配音"),
        ("x6_xiaonaigoudidi_mini", "小奶狗弟弟", "成年男", "中文普通话", "角色配音"),
        ("x6_shibingnvsheng_mini", "士兵女声", "成年女", "中文普通话", "角色配音"),
        ("x6_kongbunvsheng_mini", "恐怖女声", "成年女", "中文普通话", "旁白配音_悬疑恐怖"),
        ("x6_yulexinwennvsheng_mini", "娱乐新闻女声", "成年女", "中文普通话", "娱乐新闻"),
        ("x6_wenrounansheng_mini", "温柔男声", "成年男", "中文普通话", "售后客服"),
        ("x6_jingqudaolannvsheng_mini", "景区导览女声", "成年女", "中文普通话", "景区导览解说"),
        ("x6_daqixuanchuanpiannansheng_mini", "大气宣传片男声", "成年男", "中文普通话", "广告宣传片"),
        ("x6_cuishounvsheng_pro", "催收女声", "成年女", "中文普通话", "催收客服"),
        ("x6_yingxiaonv_pro", "营销女声", "成年女", "中文普通话", "营销客服"),
        ("x6_huanlemianbao_pro", "海绵宝宝", "童年男", "中文普通话", "IP模仿"),
        ("x6_xiangruiyingyu_pro", "商务殷语", "成年男", "中文普通话", "IP模仿"),
        ("x6_taiqiangnuannan_pro", "台湾腔温柔男声", "成年男", "台湾话", "台湾话"),
        ("x6_wumeinv_pro", "妩媚姐姐", "成年女", "中文普通话", "角色配音"),
        ("x6_lingbosong_pro", "聆伯松", "成年男", "中文普通话", "角色配音"),
        ("x6_dudulibao_pro", "少女可莉", "童年女", "中文普通话", "IP模仿"),
        ("x6_huajidama_pro", "滑稽大妈", "成年女", "中文普通话", "角色配音"),
        ("x6_huoposhaonian_pro", "活泼少年", "成年男", "中文普通话", "角色配音"),
        ("x6_lingxiaoxue_pro", "聆小雪", "成年女", "中文普通话", "角色配音"),
        ("x6_gufengxianv_mini", "古风侠女", "成年女", "中文普通话", "角色配音"),
        ("x6_wuyediantai_mini", "午夜电台", "成年女", "中文普通话", "角色配音"),
        ("x6_tiexinnanyou_mini", "贴心男友", "成年男", "中文普通话", "角色配音"),
        ("x4_zijin_oral", "子津", "成年男", "天津话", "交互聊天"),
        ("x4_ziyang_oral", "子阳", "成年男", "东北话", "交互聊天"),
    ]

    print(f"{'VCN':<45} {'名称':<12} {'性别':<6} {'语言':<20} {'场景'}")
    print("-" * 120)
    for vcn, name, gender, lang, scene in voices:
        print(f"{vcn:<45} {name:<12} {gender:<6} {lang:<20} {scene}")
    print(f"\nTotal: {len(voices)} voices")
    print("Note: x4 series support oral configuration (parameter.oral). Use --list-voices to see all options.")
    print("Voices must be enabled in your console before use: https://console.xfyun.cn")


if __name__ == "__main__":
    main()
