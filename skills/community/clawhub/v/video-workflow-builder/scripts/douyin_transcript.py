# -*- coding: utf-8 -*-
"""
抖音视频 → 口播稿 一键流水线

用法:
    python scripts/douyin_transcript.py "<抖音分享链接或含链接的整段文案>"

流程:
    1. 下载抖音视频 (复用外部 TikTokDownloader, GPL, 需 cookie)
    2. ffmpeg 抽取音频并转码为 16kHz 单声道 (阿里云 ASR 要求)
    3. 上传音频到阿里云 OSS, 生成带签名的临时 URL
    4. 阿里云录音文件识别 (file-trans) 转写为文字
    5. LLM (deepseek-v4-pro) 纠正转写错误, 整理成口播稿
    6. 保存原始转写 + 口播稿, 文档以视频标题命名

凭证从技能根目录的 .env 读取 (环境变量优先); 见 .env.example。
外部 TikTokDownloader 目录由 TIKTOK_DOWNLOADER_DIR 指定。
"""
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

import httpx

# Windows 控制台默认 GBK，本脚本会打印 ✅ 等字符，强制 stdout/stderr 走 UTF-8 免崩
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

SCRIPT_DIR = Path(__file__).resolve().parent      # scripts/
SKILL_ROOT = SCRIPT_DIR.parent                    # 技能根目录（.env 所在处）
OUTPUT_DIR = SKILL_ROOT / "output"
FINAL_DIR = OUTPUT_DIR / "口播稿"  # 最终纠错后的口播稿单独归档
SERVER_URL = "http://127.0.0.1:5555"

# 本脚本需要的配置键（用于从 .env / 环境变量中收集）
_KNOWN_KEYS = (
    "ALIYUN_AK_ID", "ALIYUN_AK_SECRET", "NLS_APP_KEY",
    "OSS_BUCKET", "OSS_ENDPOINT",
    "LLM_GATEWAY_API_KEY", "LLM_GATEWAY_BASE_URL",
    "TIKTOK_DOWNLOADER_DIR",
)

# ---------- 配置加载 ----------

def load_env() -> dict:
    env = {}
    envfile = SKILL_ROOT / ".env"
    if envfile.exists():
        for line in envfile.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip()
    # 环境变量优先（覆盖 .env，也补充 .env 中缺失的键）
    for k in _KNOWN_KEYS:
        if os.environ.get(k):
            env[k] = os.environ[k]
    return env


CFG = load_env()

# 外部 TikTokDownloader（GPL，单独 clone，不纳入本仓库）目录，运行时校验
DOWNLOADER = Path(CFG["TIKTOK_DOWNLOADER_DIR"]) if CFG.get("TIKTOK_DOWNLOADER_DIR") else None


def require(*keys):
    missing = [k for k in keys if not CFG.get(k)]
    if missing:
        sys.exit(f"[配置错误] .env 缺少: {', '.join(missing)}")


def log(stage, msg):
    print(f"[{stage}] {msg}", flush=True)


def safe_name(text: str, limit: int = 40) -> str:
    """把标题清洗成合法文件名。"""
    text = re.sub(r'[\\/:*?"<>|#\r\n\t]+', "_", text).strip().strip("_")
    return text[:limit] or "douyin_video"


# ---------- 阶段 1: 下载视频 ----------

class Downloader:
    """管理 TikTokDownloader 无头服务的生命周期。"""

    def __init__(self):
        self.proc = None

    def __enter__(self):
        if DOWNLOADER is None:
            sys.exit("[下载] 未配置 TIKTOK_DOWNLOADER_DIR，请在 .env 指向外部 TikTokDownloader 目录（见 .env.example）")
        server_script = DOWNLOADER / "headless_server.py"
        if not server_script.exists():
            sys.exit(f"[下载] 找不到 {server_script}（TIKTOK_DOWNLOADER_DIR 指向的目录里应有 headless_server.py，见 docs/）")
        log("下载", "启动下载服务...")
        self.proc = subprocess.Popen(
            [sys.executable, str(server_script)],
            cwd=str(DOWNLOADER),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
        )
        # 等待服务就绪
        for _ in range(20):
            try:
                httpx.get(f"{SERVER_URL}/docs", timeout=3)
                log("下载", "服务已就绪")
                return self
            except Exception:
                time.sleep(1)
        self.__exit__(None, None, None)
        sys.exit("[下载] 服务启动超时")

    def __exit__(self, *a):
        if self.proc:
            self.proc.terminate()
            try:
                self.proc.wait(timeout=5)
            except Exception:
                self.proc.kill()

    def fetch_detail(self, share_text: str) -> dict:
        # 先解析分享短链 → 真实链接 (detail 接口需要 detail_id)
        log("下载", "解析分享链接...")
        share = httpx.post(
            f"{SERVER_URL}/douyin/share",
            json={"text": share_text}, timeout=30,
        ).json()
        real_url = share.get("url")
        if not real_url:
            sys.exit(f"[下载] 链接解析失败: {share.get('message')}")
        m = re.search(r"/video/(\d+)", real_url) or re.search(r"(\d{15,})", real_url)
        if not m:
            sys.exit(f"[下载] 无法从 {real_url} 提取作品 ID")
        detail_id = m.group(1)
        log("下载", f"作品 ID: {detail_id}")
        resp = httpx.post(
            f"{SERVER_URL}/douyin/detail",
            json={"detail_id": detail_id}, timeout=60,
        ).json()
        if resp.get("message") != "获取数据成功！" or not resp.get("data"):
            sys.exit(f"[下载] 获取作品数据失败: {resp.get('message')} "
                     f"(cookie 可能已过期, 需在 settings.json 更新)")
        return resp["data"]


def download_video(data: dict, base: str) -> Path:
    url = data["downloads"]
    OUTPUT_DIR.mkdir(exist_ok=True)
    mp4 = OUTPUT_DIR / f"{base}.mp4"
    cookie = json.loads(
        (DOWNLOADER / "Volume" / "settings.json").read_text(encoding="utf-8")
    )["cookie"]
    headers = {
        "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                       "(KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36"),
        "Referer": "https://www.douyin.com/",
        "Cookie": cookie,
    }
    log("下载", "下载视频文件...")
    with httpx.stream("GET", url, headers=headers, follow_redirects=True, timeout=120) as r:
        r.raise_for_status()
        with open(mp4, "wb") as f:
            for chunk in r.iter_bytes(1 << 18):
                f.write(chunk)
    log("下载", f"已保存 {mp4.name} ({mp4.stat().st_size/1024/1024:.1f} MB)")
    return mp4


# ---------- 阶段 2: 抽取音频 (16kHz 单声道) ----------

def extract_audio(mp4: Path, base: str) -> Path:
    wav = OUTPUT_DIR / f"{base}.wav"
    log("音频", "ffmpeg 抽取音频 → 16kHz 单声道 (ASR 要求)...")
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(mp4),
         "-vn", "-ac", "1", "-ar", "16000", "-f", "wav", str(wav)],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    log("音频", f"已生成 {wav.name} ({wav.stat().st_size/1024/1024:.1f} MB)")
    return wav


# ---------- 阶段 3: 上传 OSS 拿签名 URL ----------

def upload_to_oss(wav: Path, base: str) -> str:
    require("OSS_BUCKET", "OSS_ENDPOINT", "ALIYUN_AK_ID", "ALIYUN_AK_SECRET")
    import oss2
    auth = oss2.Auth(CFG["ALIYUN_AK_ID"], CFG["ALIYUN_AK_SECRET"])
    bucket = oss2.Bucket(auth, f"https://{CFG['OSS_ENDPOINT']}", CFG["OSS_BUCKET"])
    key = f"douyin-asr/{base}.wav"
    log("上传", f"上传音频到 OSS: {key}")
    bucket.put_object_from_file(key, str(wav))
    # 私有桶: 生成 1 小时有效的签名 URL 供 ASR 拉取
    url = bucket.sign_url("GET", key, 3600, slash_safe=True)
    log("上传", "已生成签名 URL")
    return url


# ---------- 阶段 4: 阿里云 ASR ----------

def transcribe(file_url: str) -> str:
    require("ALIYUN_AK_ID", "ALIYUN_AK_SECRET", "NLS_APP_KEY")
    from aliyunsdkcore.client import AcsClient
    from aliyunsdkcore.request import CommonRequest
    client = AcsClient(CFG["ALIYUN_AK_ID"], CFG["ALIYUN_AK_SECRET"], "cn-shanghai")
    DOMAIN = "filetrans.cn-shanghai.aliyuncs.com"

    post = CommonRequest()
    post.set_domain(DOMAIN); post.set_version("2018-08-17")
    post.set_product("nls-filetrans"); post.set_action_name("SubmitTask")
    post.set_method("POST")
    post.add_body_params("Task", json.dumps({
        "appkey": CFG["NLS_APP_KEY"], "file_link": file_url,
        "version": "4.0", "enable_words": False,
    }))
    log("转写", "提交识别任务...")
    resp = json.loads(client.do_action_with_exception(post))
    if resp.get("StatusText") != "SUCCESS":
        sys.exit(f"[转写] 提交失败: {resp}")
    task_id = resp["TaskId"]
    log("转写", f"任务 ID: {task_id}, 轮询结果...")

    get = CommonRequest()
    get.set_domain(DOMAIN); get.set_version("2018-08-17")
    get.set_product("nls-filetrans"); get.set_action_name("GetTaskResult")
    get.set_method("GET"); get.add_query_param("TaskId", task_id)
    while True:
        g = json.loads(client.do_action_with_exception(get))
        st = g.get("StatusText")
        if st in ("RUNNING", "QUEUEING"):
            time.sleep(8); continue
        if st in ("SUCCESS", "SUCCESS_WITH_NO_VALID_FRAGMENT"):
            sentences = g.get("Result", {}).get("Sentences", []) or []
            text = "".join(s.get("Text", "") for s in sentences)
            log("转写", f"完成, 共 {len(text)} 字")
            return text
        sys.exit(f"[转写] 识别失败: {st} | {json.dumps(g, ensure_ascii=False)[:300]}")


# ---------- 阶段 5: LLM 纠错成口播稿 ----------

def correct_transcript(raw: str, title: str) -> str:
    require("LLM_GATEWAY_API_KEY", "LLM_GATEWAY_BASE_URL")
    import openai
    client = openai.OpenAI(
        base_url=CFG["LLM_GATEWAY_BASE_URL"],
        api_key=CFG["LLM_GATEWAY_API_KEY"],
    )
    log("纠错", "调用 LLM 整理口播稿...")
    prompt = (
        "下面是一段抖音视频的语音转写文字，可能存在同音错别字、专有名词识别错误、"
        "缺少标点和分段等问题。请你在【不改变原意、不增删内容观点】的前提下：\n"
        "1. 纠正错别字和明显的同音识别错误；\n"
        "2. 修正专有名词（人名/公司名/术语，如药明康德等）；\n"
        "3. 补全标点、合理分段，使其成为通顺可读的口播文稿；\n"
        "4. 不要添加原文没有的信息，不要总结、不要加标题。\n"
        f"\n视频标题参考：{title}\n\n转写原文：\n{raw}"
    )
    resp = client.chat.completions.create(
        model="deepseek-v4-pro",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    text = resp.choices[0].message.content.strip()
    log("纠错", f"完成, 口播稿 {len(text)} 字")
    return text


# ---------- 主流程 ----------

def main():
    if len(sys.argv) < 2:
        sys.exit('用法: python pipeline.py "<抖音分享链接>"')
    share_text = sys.argv[1]
    OUTPUT_DIR.mkdir(exist_ok=True)
    FINAL_DIR.mkdir(parents=True, exist_ok=True)

    with Downloader() as dl:
        data = dl.fetch_detail(share_text)
        title = data.get("desc", "").split("#")[0].strip() or data["id"]
        base = f'{data.get("nickname","")}-{safe_name(title)}-{data["id"]}'.strip("-")
        log("信息", f"标题: {title}")
        # downloads 为直链, 在 server 关闭前下载完成
        mp4 = download_video(data, base)

    wav = extract_audio(mp4, base)
    file_url = upload_to_oss(wav, base)
    raw = transcribe(file_url)

    raw_path = OUTPUT_DIR / f"{base}.转写原文.txt"
    raw_path.write_text(raw, encoding="utf-8")
    log("保存", f"原始转写: {raw_path.name}")

    final = correct_transcript(raw, title)
    doc_path = FINAL_DIR / f"{base}.口播稿.txt"
    doc_path.write_text(final, encoding="utf-8")
    log("保存", f"口播稿 → {FINAL_DIR.name}/{doc_path.name}")

    print(f"\n✅ 全部完成！\n   视频:     {mp4}\n   转写原文: {raw_path}\n   口播稿:   {doc_path}")


if __name__ == "__main__":
    main()
