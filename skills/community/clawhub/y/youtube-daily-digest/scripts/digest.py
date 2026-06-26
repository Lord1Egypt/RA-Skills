#!/usr/bin/env python3
"""
YouTube Daily Digest — 零配置版
安装 skill 后只需 pip install youtube-transcript-api，即可直接运行。

- YouTube 原生 RSS（不需要 Docker/RSSHub）
- 飞书 + Gateway 配置自动从 OpenClaw 读取
- 频道列表内置
"""

import json
import os
import sys
import time
import urllib.request
import urllib.error
import subprocess
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
STATE_PATH = SCRIPT_DIR / "state.json"

# ── 内置频道列表（Jade 精选 AI/产品/科技播客）────────────────────────────────
CHANNELS = [
    ("Lex Fridman",                        "UCSHZKyawb77ixDdsGog4iWA"),
    ("Lenny's Podcast",                    "UC6t1O76G0jYXOAoYCm153dA"),
    ("a16z speedrun",                      "UCp-aroxb6hOKPQGyGp0c3Dw"),
    ("Latent Space",                       "UCxBcwypKK-W3GHd_RZ9FZrQ"),
    ("AI Engineer",                        "UCLKPca3kwwd-B59HNr-_lvA"),
    ("Aakash Gupta",                       "UCsHBhXybRz2CCfpU0hWp7ow"),
    ("App Breakdown",                      "UC5d5jyLMsze4S8x16-X71-A"),
    ("WhynotTV",                           "UC5xLV_gJAP9psKcyrJ3ZIcw"),
    ("Ben Erez",                           "UCZ37wuLYmh5fHTUbqy2VNGA"),
    ("Brock Mesarich | AI for Non Techies","UCjc1vfduI7BhVMXBLJLDjmA"),
    ("David Ondrej",                       "UCPGrgwfbkjTIgPoOh2q1BAg"),
    ("Paul J Lipsky",                      "UCmeU2DYiVy80wMBGZzEWnbw"),
    ("Ali H. Salem",                       "UCHMjsLKv6MkrmHnx4HrGndQ"),
]

LOOKBACK_HOURS = 48


# ── 自动读取 OpenClaw 配置 ───────────────────────────────────────────────────

def load_openclaw_config():
    """从 OpenClaw 配置中自动读取飞书和 Gateway 信息"""
    config_path = Path.home() / ".openclaw" / "openclaw.json"
    if not config_path.exists():
        raise FileNotFoundError("找不到 ~/.openclaw/openclaw.json，请确认 OpenClaw 已安装")

    with open(config_path, encoding="utf-8") as f:
        oc = json.load(f)

    # 飞书配置
    feishu_channels = oc.get("channels", {}).get("feishu", {})
    accounts = feishu_channels.get("accounts", {})
    default_account = feishu_channels.get("defaultAccount", "main")
    account = accounts.get(default_account, {})
    app_id = account.get("appId", "")
    app_secret = account.get("appSecret", "")

    # Gateway 配置
    gateway = oc.get("gateway", {})
    gateway_port = gateway.get("port", 18789)
    gateway_auth = gateway.get("auth", {})
    gateway_token = gateway_auth.get("token", "")

    return {
        "feishu_app_id": app_id,
        "feishu_app_secret": app_secret,
        "gateway_url": f"http://localhost:{gateway_port}/v1",
        "gateway_token": gateway_token,
    }


# ── YouTube 原生 RSS（不需要 RSSHub / Docker）───────────────────────────────

def fetch_latest_videos(channel_id, max_videos=3):
    """用 YouTube 原生 Atom feed 获取最新视频"""
    url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    req = urllib.request.Request(url, headers={"User-Agent": "YTDigest/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            content = resp.read().decode("utf-8")
    except Exception as e:
        raise RuntimeError(f"获取 RSS 失败: {e}")

    ns = {"atom": "http://www.w3.org/2005/Atom", "yt": "http://www.youtube.com/xml/schemas/2015"}
    root = ET.fromstring(content)
    videos = []

    for entry in root.findall("atom:entry", ns)[:max_videos]:
        title_el = entry.find("atom:title", ns)
        link_el = entry.find("atom:link", ns)
        pub_el = entry.find("atom:published", ns)
        vid_el = entry.find("yt:videoId", ns)

        title = title_el.text.strip() if title_el is not None and title_el.text else "Untitled"
        link = link_el.get("href", "") if link_el is not None else ""
        pub_str = pub_el.text.strip() if pub_el is not None and pub_el.text else None
        video_id = vid_el.text.strip() if vid_el is not None and vid_el.text else None

        if not video_id and link and "watch?v=" in link:
            video_id = link.split("watch?v=")[-1].split("&")[0]

        pub_ts = None
        if pub_str:
            try:
                from datetime import timezone
                dt = datetime.fromisoformat(pub_str.replace("Z", "+00:00"))
                pub_ts = dt.timestamp()
            except Exception:
                pass

        if video_id:
            videos.append({
                "video_id": video_id,
                "title": title,
                "link": link or f"https://www.youtube.com/watch?v={video_id}",
                "published_ts": pub_ts,
            })

    return videos


# ── 字幕获取 ─────────────────────────────────────────────────────────────────

def fetch_transcript(video_id):
    """用 youtube-transcript-api 获取字幕（免费无需 API key）"""
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        api = YouTubeTranscriptApi()
        for langs in [("en",), ("en-US", "en-GB"), ("zh", "zh-Hans")]:
            try:
                segments = api.fetch(video_id, languages=langs)
                return " ".join(seg.text for seg in segments if seg.text).strip()
            except Exception:
                continue
        try:
            segments = api.fetch(video_id)
            return " ".join(seg.text for seg in segments if seg.text).strip()
        except Exception:
            return None
    except ImportError:
        print("  ⚠ 请安装: pip3 install youtube-transcript-api")
        return None
    except Exception:
        return None


def fetch_transcript_ytdlp(video_id):
    """备用方案：用 yt-dlp 获取字幕"""
    import tempfile, glob, re
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            subprocess.run([
                "yt-dlp", "--write-sub", "--write-auto-sub",
                "--sub-lang", "en", "--skip-download", "--sub-format", "vtt",
                "-o", f"{tmpdir}/sub",
                f"https://www.youtube.com/watch?v={video_id}",
            ], capture_output=True, text=True, timeout=30)

            vtt_files = glob.glob(f"{tmpdir}/*.vtt")
            if not vtt_files:
                return None

            with open(vtt_files[0], encoding="utf-8") as f:
                content = f.read()

            lines = content.split("\n")
            text_lines = []
            for line in lines:
                line = line.strip()
                if not line or line.startswith("WEBVTT") or line.startswith("Kind:") or line.startswith("Language:"):
                    continue
                if re.match(r"^\d{2}:\d{2}", line) or re.match(r"^\d+$", line):
                    continue
                line = re.sub(r"<[^>]+>", "", line)
                if line:
                    text_lines.append(line)
            return " ".join(text_lines).strip() if text_lines else None
    except Exception:
        return None


# ── Claude 摘要 ──────────────────────────────────────────────────────────────

def call_claude(prompt, oc_config):
    from openai import OpenAI
    client = OpenAI(api_key=oc_config["gateway_token"], base_url=oc_config["gateway_url"])
    response = client.chat.completions.create(
        model="anthropic/claude-sonnet-4-6",
        max_tokens=1500,
        messages=[
            {"role": "system", "content": "你是顶级播客内容编辑，擅长提炼视频核心观点，输出简洁有力的中文摘要。"},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content.strip()


def summarize_video(title, channel, transcript, oc_config):
    excerpt = transcript[:12000]
    prompt = f"""视频标题：{title}
频道：{channel}

字幕内容：
{excerpt}

请返回两行纯文本（不要 JSON，不要引号，不要花括号）：
第一行：视频标题的中文翻译（简洁准确）
第二行开始：150-250字中文梗概
- 第一句话点明嘉宾身份和核心主题
- 提炼 2-3 个最有价值的观点，要具体不泛泛
- 如果有反直觉的判断或金句，一定要写进去
- 写法：像一个聪明的朋友在跟你说「这期必听，因为...」"""

    result = call_claude(prompt, oc_config)
    lines = result.strip().split("\n", 1)
    title_zh = lines[0].strip().strip('"') if lines else ""
    summary = lines[1].strip() if len(lines) > 1 else result.strip()
    return title_zh, summary


# ── 飞书推送 ─────────────────────────────────────────────────────────────────

def feishu_token(oc_config):
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    data = json.dumps({"app_id": oc_config["feishu_app_id"], "app_secret": oc_config["feishu_app_secret"]}).encode()
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read())["tenant_access_token"]


def get_bot_user_id(token):
    """获取与 bot 对话的用户 open_id（取最近一条消息的发送者）"""
    # 简单方案：从环境变量或 OpenClaw identity 读取
    identity_path = Path.home() / ".openclaw" / "identity"
    if identity_path.exists():
        for f in identity_path.iterdir():
            if f.suffix == ".json":
                try:
                    data = json.loads(f.read_text())
                    if data.get("open_id"):
                        return data["open_id"]
                except Exception:
                    continue
    return os.environ.get("FEISHU_USER_OPEN_ID", "")


def feishu_send(token, payload):
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id",
        data=body,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=15) as r:
        resp = json.loads(r.read())
        if resp.get("code") != 0:
            raise RuntimeError(f"飞书发送失败: {resp}")


def build_card(videos, today):
    elements = []
    for i, v in enumerate(videos, 1):
        title_line = f'[{v["title"]}]({v["link"]})'
        if v.get("title_zh"):
            title_line += f'\n{v["title_zh"]}'
        md = f'**{i}. {v["channel"]}**\n{title_line}\n\n{v["summary"]}'
        elements.append({"tag": "div", "text": {"tag": "lark_md", "content": md}})
        if i < len(videos):
            elements.append({"tag": "hr"})

    elements.append({"tag": "hr"})
    elements.append({"tag": "div", "text": {"tag": "lark_md", "content": "Claw 🐾 自动生成"}})

    return {
        "config": {"wide_screen_mode": True},
        "header": {
            "title": {"content": f"📺 YouTube 每日更新 · {today} · 共 {len(videos)} 个新视频", "tag": "plain_text"},
            "template": "blue",
        },
        "elements": elements,
    }


# ── 主流程 ────────────────────────────────────────────────────────────────────

def run():
    # 自动读取 OpenClaw 配置
    oc_config = load_openclaw_config()
    today = datetime.now().strftime("%Y-%m-%d")
    cutoff = time.time() - LOOKBACK_HOURS * 3600

    # 加载已推送记录
    state = json.loads(STATE_PATH.read_text()) if STATE_PATH.exists() else {"seen_videos": []}
    seen = set(state.get("seen_videos", []))

    # 获取用户 open_id
    user_id = get_bot_user_id(None) or os.environ.get("FEISHU_USER_OPEN_ID", "")
    if not user_id:
        print("⚠ 无法确定飞书用户 ID。请设置环境变量 FEISHU_USER_OPEN_ID")
        return

    print(f"[{today}] 扫描 {len(CHANNELS)} 个频道...")
    videos_data = []

    for name, cid in CHANNELS:
        print(f"  → {name}...", flush=True)
        try:
            videos = fetch_latest_videos(cid)
        except Exception as e:
            print(f"     ✗ RSS 失败: {e}")
            continue

        for v in videos[:1]:
            if v["video_id"] in seen:
                continue
            if v["published_ts"] and v["published_ts"] < cutoff:
                continue

            time.sleep(2)
            transcript = fetch_transcript(v["video_id"])
            if not transcript:
                transcript = fetch_transcript_ytdlp(v["video_id"])
            if not transcript:
                print(f"     ✗ 无字幕: {v['title'][:40]}")
                continue

            print(f"     ✓ {v['title'][:50]}", flush=True)
            title_zh, summary = summarize_video(v["title"], name, transcript, oc_config)

            videos_data.append({
                "channel": name,
                "title": v["title"],
                "title_zh": title_zh,
                "link": v["link"],
                "summary": summary,
            })

            seen.add(v["video_id"])
            time.sleep(1)

    # 保存 state
    state["seen_videos"] = list(seen)[-500:]
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2))

    if not videos_data:
        print("今日无新视频")
        return

    # 推送飞书
    print(f"\n共 {len(videos_data)} 个新视频，推送飞书...")
    token = feishu_token(oc_config)
    card = build_card(videos_data, today)
    feishu_send(token, {"receive_id": user_id, "msg_type": "interactive", "content": json.dumps(card)})
    print("✅ 推送完成！")


if __name__ == "__main__":
    run()
