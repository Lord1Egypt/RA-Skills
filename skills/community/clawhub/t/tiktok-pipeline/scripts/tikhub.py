"""
TikHub API 工具包 v4
支持: 抖音 / TikTok / B站 / 小红书 等多平台

实测经验总结:
- 免费端点 web/fetch_video_high_quality_play_url 返回空 → 用 app/v3/fetch_video_high_quality_play_url（付费）
- 视频直链请求需带 Referer + User-Agent，否则 403
- 国内用户用 api.tikhub.dev（不需要代理）

★★★ 转写方案优先级（2026-03 实测）★★★
1. mlx-whisper（Apple GPU / MPS）：40秒 / small 模型 → 首选！
   安装: pip install mlx-whisper
   用法: from mlx_whisper import transcribe
2. openai-whisper small（CPU）：82秒 → 无 Apple GPU 时的首选
3. openai-whisper medium（CPU）：220秒 → 精度最高，但 Mac mini 会被 SIGTERM kill
注意: faster-whisper 不支持 Apple MPS，不要用！
"""

import os
import time
import subprocess
import requests
import json

# ============ 配置区 ============
API_KEY = "YOUR_API_KEY_HERE"
BASE_URL = "https://api.tikhub.io"  # 国内用户改为 https://api.tikhub.dev
HEADERS = {"Authorization": f"Bearer {API_KEY}"}
# ================================


def _get(endpoint: str, params: dict = None, retries: int = 3):
    """通用 GET 请求"""
    for i in range(retries):
        try:
            resp = requests.get(f"{BASE_URL}{endpoint}", headers=HEADERS, params=params, timeout=30)
            if resp.status_code == 429:
                print(f"⚠️ 频率限制，等待 5 秒... ({i+1}/{retries})")
                time.sleep(5)
                continue
            return resp.json()
        except Exception as e:
            print(f"❌ 请求失败: {e}，重试中 ({i+1}/{retries})")
            time.sleep(2)
    return None


def _post(endpoint: str, json_data: dict = None, retries: int = 3):
    """通用 POST 请求"""
    for i in range(retries):
        try:
            resp = requests.post(f"{BASE_URL}{endpoint}", headers=HEADERS, json=json_data, timeout=30)
            if resp.status_code == 429:
                print(f"⚠️ 频率限制，等待 5 秒...")
                time.sleep(5)
                continue
            return resp.json()
        except Exception as e:
            print(f"❌ 请求失败: {e}")
            time.sleep(2)
    return None


# ========================
# 视频信息（免费）
# ========================

def get_video_info(aweme_id: str) -> dict:
    """
    获取视频详细信息（免费接口）
    路径: /api/v1/douyin/web/fetch_one_video
    返回: {"data": {"aweme_detail": {...}}}
    """
    return _get("/api/v1/douyin/web/fetch_one_video", params={"aweme_id": aweme_id})


def get_video_info_by_url(url: str) -> dict:
    """
    通过分享链接获取视频信息（免费接口）
    路径: /api/v1/douyin/web/fetch_one_video_by_share_url
    """
    return _get("/api/v1/douyin/web/fetch_one_video_by_share_url", params={"share_url": url})


def parse_aweme_id(url: str) -> str:
    """
    从抖音 URL 解析 aweme_id
    支持:
      - https://v.douyin.com/xxxxx
      - https://www.douyin.com/video/7618502770185833766
      - https://www.douyin.com/jingxuan?modal_id=7618502770185833766
    """
    if "modal_id=" in url:
        return url.split("modal_id=")[-1].split("&")[0]
    if "/video/" in url:
        return url.split("/video/")[-1].split("?")[0]
    return url


# ========================
# 视频下载（需付费端点）
# ========================

def get_high_quality_url(aweme_id: str) -> str:
    """
    获取无水印高画质视频直链（付费接口）
    路径: /api/v1/douyin/app/v3/fetch_video_high_quality_play_url
    注意: 免费端点 web/ 返回空，必须用 app/v3/
    返回: 视频直链，或 None
    """
    data = _get("/api/v1/douyin/app/v3/fetch_video_high_quality_play_url",
                params={"aweme_id": aweme_id})
    if data and data.get("data", {}).get("url_list"):
        return data["data"]["url_list"][0]
    # fallback: 试普通视频信息里的地址（可能有水印）
    info = get_video_info(aweme_id)
    urls = (info.get("data", {}).get("aweme_detail", {})
            .get("video", {}).get("play_addr", {}).get("url_list", []))
    return urls[0] if urls else None


def download_video(aweme_id: str, output_dir: str = "./downloads",
                   video_url: str = None) -> str:
    """
    下载视频到本地，返回文件路径
    aweme_id: 视频 ID
    video_url: 可选，传入直链可跳过 API 调用
    请求头需要 Referer + User-Agent，否则 403
    """
    os.makedirs(output_dir, exist_ok=True)

    if not video_url:
        video_url = get_high_quality_url(aweme_id)

    if not video_url:
        print("❌ 无法获取视频地址，请确认 API 余额充足")
        return None

    local_path = os.path.join(output_dir, f"{aweme_id}.mp4")
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://www.douyin.com/",
    }

    print(f"⬇️  开始下载: {video_url[:80]}...")
    resp = requests.get(video_url, headers=headers, stream=True, timeout=120)
    if resp.status_code == 403:
        print("❌ 403 拒绝，请尝试更换 Referer 或使用代理")
        return None

    downloaded = 0
    total = int(resp.headers.get("Content-Length", 0))
    with open(local_path, "wb") as f:
        for chunk in resp.iter_content(chunk_size=1024 * 1024):
            if chunk:
                f.write(chunk)
                downloaded += len(chunk)
                if total:
                    pct = downloaded / total * 100
                    print(f"\r    进度: {downloaded/1024/1024:.1f}MB / {total/1024/1024:.1f}MB ({pct:.1f}%)", end="", flush=True)

    print(f"\n✅ 下载完成: {local_path} ({os.path.getsize(local_path)/1024/1024:.1f} MB)")
    return local_path


def batch_download(aweme_ids: list, output_dir: str = "./downloads", delay: float = 2.0):
    """批量下载"""
    results = []
    for i, aid in enumerate(aweme_ids):
        print(f"[{i+1}/{len(aweme_ids)}] 处理: {aid}")
        try:
            path = download_video(aid, output_dir)
            results.append({"aweme_id": aid, "status": "success" if path else "failed", "path": path})
        except Exception as e:
            results.append({"aweme_id": aid, "status": "error", "error": str(e)})
        time.sleep(delay)
    return results


# ========================
# 评论（免费）
# ========================

def get_video_comments(aweme_id: str, cursor: str = None, max_count: int = 50) -> dict:
    """获取视频评论（免费接口）"""
    params = {"aweme_id": aweme_id, "count": max_count}
    if cursor:
        params["cursor"] = cursor
    return _get("/api/v1/douyin/web/fetch_video_comments", params=params)


def get_all_comments(aweme_id: str, max_count: int = 200) -> list:
    """循环获取全量评论"""
    all_comments = []
    cursor = None
    while len(all_comments) < max_count:
        data = get_video_comments(aweme_id, cursor=cursor)
        if not data:
            break
        comments = data.get("data", {}).get("comments", [])
        if not comments:
            break
        all_comments.extend(comments)
        cursor = data["data"].get("cursor")
        if not cursor:
            break
        time.sleep(1)
    return all_comments[:max_count]


# ========================
# 用户信息（部分接口需特定 uid 格式）
# ========================

def get_user_profile(uid: str) -> dict:
    """通过 uid 获取用户资料"""
    return _get("/api/v1/douyin/web/fetch_user_profile_by_uid", params={"uid": uid})


def get_user_videos(uid_or_unique_id: str, max_count: int = 10) -> dict:
    """获取用户视频列表"""
    return _get("/api/v1/douyin/web/fetch_user_post_videos",
                params={"uid": uid_or_unique_id, "max_count": max_count})


def get_user_followers(unique_id: str, max_count: int = 20) -> dict:
    """获取粉丝列表"""
    return _get("/api/v1/douyin/web/fetch_user_fans_list",
                params={"unique_id": unique_id, "count": max_count})


# ========================
# B站
# ========================

def bilibili_video_info(bvid: str) -> dict:
    """获取B站视频信息"""
    return _get("/api/v1/bilibili/web/fetch_one_video", params={"bvid": bvid})


def bilibili_video_url(bvid: str) -> str:
    """获取B站视频直链"""
    data = _get("/api/v1/bilibili/web/fetch_video_play_info", params={"bvid": bvid})
    if data and data.get("data", {}).get("durl"):
        return data["data"]["durl"][0]["url"]
    return None


# ========================
# 音频处理
# ========================

def extract_audio(video_path: str, output_path: str = None) -> str:
    """
    从视频提取音频（需 ffmpeg）
    输出格式: 16kHz 单声道 PCM WAV（Whisper 推荐格式）
    """
    if not output_path:
        output_path = video_path.rsplit(".", 1)[0] + ".wav"
    result = subprocess.run([
        "ffmpeg", "-i", video_path, "-vn",
        "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1",
        output_path, "-y"
    ], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"⚠️ ffmpeg 警告: {result.stderr[-200:]}")
    size = os.path.getsize(output_path) / 1024 / 1024
    print(f"🔊 音频提取: {output_path} ({size:.1f} MB)")
    return output_path


def whisper_transcribe(audio_path: str, model: str = "medium",
                       language: str = "Chinese",
                       output_path: str = None,
                       background: bool = True) -> str:
    """
    [已废弃，推荐用 mlx_whisper_transcribe！]
    Whisper 转写（需安装: pip install openai-whisper）

    参数:
        audio_path: 音频文件路径（WAV 格式推荐）
        model: tiny/base/small/medium/large，medium 精度速度平衡好
        language: 语言代码，Chinese
        output_path: 可选，文字稿输出路径
        background: True 用 nohup 后台跑（推荐，CPU 慢）；False 同步等待
    返回: 文字稿文件路径（后台模式立即返回路径，不等待完成）
    """
    if not output_path:
        output_path = audio_path.replace(".wav", ".txt")

    output_dir = os.path.dirname(audio_path) or "."

    cmd = [
        "whisper", audio_path,
        "--model", model,
        "--language", language,
        "--output_format", "txt",      # 注意：是 --output_format，不是 --output-txt
        "--output_dir", output_dir,
    ]

    if background:
        log_file = f"/tmp/whisper_{os.path.basename(audio_path)}.log"
        nohup_cmd = f"nohup {' '.join(cmd)} > {log_file} 2>&1 &"
        print(f"🚀 Whisper 后台转写启动，日志: {log_file}")
        subprocess.run(nohup_cmd, shell=True)
        print(f"📝 文字稿将保存到: {output_path}")
        print(f"⏱️  medium 模型 CPU 转写 1 分钟音频约需 1-2 分钟，请耐心等待")
        return output_path
    else:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ Whisper 错误: {result.stderr[-300:]}")
        print(f"📝 转写完成: {output_path}")
        return output_path


def mlx_whisper_transcribe(audio_path: str,
                            model_size: str = "small",
                            language: str = "zh",
                            output_path: str = None) -> str:
    """
    mlx-whisper 转写（Apple GPU / MPS 加速版）

    依赖: pip install mlx-whisper
    模型: mlx-community/whisper-small-mlx（small）
          mlx-community/whisper-medium-mlx（medium）
    速度: ~40秒（small，14分钟音频），比 CPU 快 2-5 倍

    参数:
        audio_path: 音频文件路径（WAV/MP3/M4A）
        model_size: small / medium（默认 small，速度快）
        language: zh（中文）/ en（英文）
        output_path: 可选，文字稿输出路径
    返回: 文字稿内容（str）
    """
    try:
        from mlx_whisper import transcribe
    except ImportError:
        print("❌ mlx-whisper 未安装，请运行: pip install mlx-whisper")
        return None

    if not output_path:
        output_path = audio_path.replace(".wav", "_mlx.txt")

    model_repo = f"mlx-community/whisper-{model_size}-mlx"

    print(f"🎮 开始 mlx-whisper GPU 转写（{model_size}）...")
    t0 = time.time()

    result = transcribe(
        audio_path,
        path_or_hf_repo=model_repo,
        language=language,
    )

    elapsed = time.time() - t0
    text = result.get("text", "")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"✅ 转写完成: {elapsed:.1f}秒 | {len(text)}字 | 保存到: {output_path}")
    return text


def full_pipeline_douyin_to_text(aweme_id: str, output_dir: str = "./downloads",
                                  use_gpu: bool = True,
                                  whisper_model: str = "small") -> str:
    """
    完整 pipeline：aweme_id → 下载视频 → 提取音频 → Whisper 转写

    参数:
        aweme_id: 抖音视频 ID
        output_dir: 下载目录
        use_gpu: True 用 mlx-whisper（Apple GPU），False 用 openai-whisper（CPU）
        whisper_model: small / medium（仅 use_gpu=False 时生效）
    """
    print(f"\n=== Step 1: 下载视频 {aweme_id} ===")
    video_path = download_video(aweme_id, output_dir)
    if not video_path:
        return None

    print(f"\n=== Step 2: 提取音频 ===")
    audio_path = extract_audio(video_path)

    print(f"\n=== Step 3: 转写 ===")
    if use_gpu:
        print("🎮 使用 mlx-whisper（Apple GPU 加速）")
        text = mlx_whisper_transcribe(audio_path, model_size="small")
        output_path = audio_path.replace(".wav", "_mlx.txt")
        if text:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"✅ 文字稿已保存: {output_path}（{len(text)}字）")
        return output_path if text else None
    else:
        print("🔧 使用 openai-whisper（CPU，后台运行）")
        return whisper_transcribe(audio_path, model=whisper_model, background=True)


# ========================
# 工具函数
# ========================

def set_api_key(key: str, use_china_domain: bool = False):
    """运行时设置 API Key"""
    global API_KEY, BASE_URL, HEADERS
    API_KEY = key
    if use_china_domain:
        BASE_URL = "https://api.tikhub.dev"
    else:
        BASE_URL = "https://api.tikhub.io"
    HEADERS = {"Authorization": f"Bearer {API_KEY}"}


def check_balance() -> dict:
    """查询账户余额"""
    return _get("/api/v1/tikhub/user/get_user_info")


if __name__ == "__main__":
    print("TikHub API v3 工具包")
    print("用法:")
    print("  set_api_key('your_key')")
    print("  get_video_info('7618502770185833766')")
    print("  get_all_comments('7618502770185833766')")
    print("  full_pipeline_douyin_to_text('7618502770185833766')")
