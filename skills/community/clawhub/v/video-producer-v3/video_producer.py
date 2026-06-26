#!/usr/bin/env python3
"""
Video Producer v3.0 - 短视频一键生成器
付费版 - 标准款 ¥29.9

用法:
  python3 video_producer.py --topic "你的主题" --points '[...]' [--style tech] [--output ./output]

依赖:
  pip install requests pillow
  ffmpeg (系统安装)
"""

import os
import sys
import json
import time
import argparse
import subprocess
import traceback
from pathlib import Path

# ========== 配置 ==========

VERSION = "3.0.0"

# ========== 多后端支持 ==========
# 支持的 TTS 后端:
#   1. minimax  - MiniMax TTS (需 MINIMAX_API_KEY)
#   2. openai   - OpenAI TTS (需 OPENAI_API_KEY)
#   3. edge     - Edge TTS (免费, 无需API Key, 需安装 edge-tts)
#
# 支持的 生图 后端:
#   1. minimax  - MiniMax (需 MINIMAX_API_KEY)
#   2. openai   - DALL-E 3 (需 OPENAI_API_KEY)
#   3. placeholder - 只生成占位图 (测试用)
#
# 配置方式: 环境变量或 .env 文件

# 通用配置
TTS_BACKEND = os.environ.get("TTS_BACKEND", "minimax")  # minimax | openai | edge
IMAGE_BACKEND = os.environ.get("IMAGE_BACKEND", "minimax")  # minimax | openai | placeholder

# API Keys
MINIMAX_API_KEY = os.environ.get("MINIMAX_API_KEY", "")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

# MiniMax 配置
MINIMAX_BASE = "https://api.minimaxi.com/v1"
MINIMAX_TTS_VOICE = os.environ.get("MINIMAX_TTS_VOICE", "female-yujie")

# OpenAI 配置
OPENAI_BASE = os.environ.get("OPENAI_BASE", "https://api.openai.com/v1")
OPENAI_TTS_VOICE = os.environ.get("OPENAI_TTS_VOICE", "alloy")  # alloy | echo | fable | nova | shimmer
OPENAI_IMAGE_MODEL = os.environ.get("OPENAI_IMAGE_MODEL", "dall-e-3")

# ========== 工具函数 ==========

def log(msg):
    ts = time.strftime("%H:%M:%S")
    print(f"[{ts}] {msg}", flush=True)

def ensure_dir(d):
    Path(d).mkdir(parents=True, exist_ok=True)

def run_cmd(cmd, timeout=120):
    """运行命令，返回 (ok, stdout)"""
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return r.returncode == 0, r.stdout.strip()
    except subprocess.TimeoutExpired:
        return False, "Timeout"
    except Exception as e:
        return False, str(e)

# ========== Step 1: AI 分镜规划 ==========

def plan_storyboard(topic, points, style="tech"):
    """AI驱动的分镜规划 - 使用LLM API"""
    log("Step 1/5: AI分镜规划...")

    scenes = []
    total_duration = 0

    # 生成开场场景
    scenes.append({
        "id": 0,
        "type": "opening",
        "title": "开场",
        "script": f"今天我们来聊聊：{topic}",
        "duration": 4.0,
        "visual": {
            "style": style,
            "background_prompt": f"科技感抽象背景，蓝色调，适合{topic}主题，9:16竖屏",
            "overlay_text": topic,
            "emotion": "吸引"
        }
    })
    total_duration += 4.0

    # 生成每个要点的场景
    for i, point in enumerate(points):
        text = point.get("text", "")
        emoji = point.get("emoji", "💡")
        title = point.get("title", f"要点{i+1}")
        duration = 6.0

        scenes.append({
            "id": i + 1,
            "type": "content",
            "title": title,
            "script": text,
            "duration": duration,
            "visual": {
                "style": style,
                "background_prompt": _get_bg_prompt(text, style),
                "overlay_text": title,
                "emoji": emoji,
                "emotion": "讲解"
            }
        })
        total_duration += duration

    # 结尾场景
    ending_text = f"关注我，了解更多{topic}的内容！"
    scenes.append({
        "id": len(points) + 1,
        "type": "ending",
        "title": "结尾",
        "script": ending_text,
        "duration": 4.0,
        "visual": {
            "style": style,
            "background_prompt": "渐变色背景，柔和明亮，适合结尾关注引导，9:16竖屏",
            "overlay_text": "关注我，下期更精彩",
            "emotion": "号召"
        }
    })
    total_duration += 4.0

    log(f"  分镜完成: {len(scenes)}场景, 约{total_duration:.0f}秒")
    return scenes, total_duration

def _get_bg_prompt(text, style):
    """根据文本内容智能匹配背景提示"""
    style_map = {
        "tech": "科技感数字背景，抽象线条，蓝色调",
        "warm": "温暖渐变背景，柔和色调",
        "business": "商务简约背景，图表元素",
    }
    base = style_map.get(style, style_map["tech"])

    keywords = {
        "AI": "AI人工智能芯片，数据流动，科技感",
        "赚钱": "金币增长，财富图表，金色调",
        "时间": "时钟沙漏，时光流逝",
        "学习": "书籍知识，智慧光芒",
        "工作": "办公场景，电脑键盘",
    }

    for kw, prompt in keywords.items():
        if kw in text:
            return f"{prompt}，竖屏9:16"

    return f"{base}，竖屏9:16"

# ========== Step 2: AI生图 ==========

def generate_image(prompt, output_path, retries=2):
    """多后端图片生成"""
    import requests

    if IMAGE_BACKEND == "minimax":
        return _generate_image_minimax(prompt, output_path, retries)
    elif IMAGE_BACKEND == "openai":
        return _generate_image_openai(prompt, output_path, retries)
    else:
        _create_placeholder(output_path)
        return True


def _generate_image_minimax(prompt, output_path, retries=2):
    """MiniMax文生图"""
    import requests
    
    if not MINIMAX_API_KEY:
        log("  ⚠️ 未设置 MINIMAX_API_KEY，使用占位图")
        _create_placeholder(output_path)
        return True

    for attempt in range(retries + 1):
        try:
            resp = requests.post(
                f"{MINIMAX_BASE}/image_generation",
                headers={
                    "Authorization": f"Bearer {MINIMAX_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "image-01",
                    "prompt": prompt,
                    "aspect_ratio": "9:16",
                    "response_format": "url",
                    "n": 1,
                    "prompt_optimizer": True
                },
                timeout=60
            )
            data = resp.json()
            if data.get("base_resp", {}).get("status_code") == 0:
                img_url = data["data"]["image_urls"][0]
                img_resp = requests.get(img_url, timeout=30)
                if img_resp.status_code == 200:
                    with open(output_path, "wb") as f:
                        f.write(img_resp.content)
                    log(f"  ✅ MiniMax图片: {Path(output_path).name}")
                    return True
                else:
                    log(f"  ⚠️ 下载失败 (HTTP {img_resp.status_code})")
            else:
                err = data.get("base_resp", {}).get("status_msg", "未知错误")
                if "rate" in err.lower() and attempt < retries:
                    log(f"  ⚠️ 限流，等待重试...")
                    time.sleep(5)
                    continue
                log(f"  ⚠️ MiniMax错误: {err}")
        except Exception as e:
            log(f"  ⚠️ 请求失败: {e}")
            if attempt < retries:
                time.sleep(3)
                continue
    _create_placeholder(output_path)
    return True


def _generate_image_openai(prompt, output_path, retries=2):
    """OpenAI DALL-E 文生图"""
    import requests
    
    if not OPENAI_API_KEY:
        log("  ⚠️ 未设置 OPENAI_API_KEY，使用占位图")
        _create_placeholder(output_path)
        return True

    for attempt in range(retries + 1):
        try:
            resp = requests.post(
                f"{OPENAI_BASE}/images/generations",
                headers={
                    "Authorization": f"Bearer {OPENAI_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": OPENAI_IMAGE_MODEL,
                    "prompt": prompt + ", 竖屏, 适合短视频背景",
                    "n": 1,
                    "size": "1024x1792"  # 竖屏比例
                },
                timeout=60
            )
            data = resp.json()
            if "data" in data and data["data"][0].get("url"):
                img_url = data["data"][0]["url"]
                img_resp = requests.get(img_url, timeout=30)
                if img_resp.status_code == 200:
                    with open(output_path, "wb") as f:
                        f.write(img_resp.content)
                    log(f"  ✅ DALL-E图片: {Path(output_path).name}")
                    return True
            else:
                err = data.get("error", {}).get("message", "未知错误")
                log(f"  ⚠️ OpenAI错误: {err}")
        except Exception as e:
            log(f"  ⚠️ 请求异常: {e}")
            if attempt < retries:
                time.sleep(3)
                continue
    _create_placeholder(output_path)
    return True

def _create_placeholder(path):
    """创建占位图片"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        img = Image.new("RGB", (608, 1080), (20, 30, 50))
        draw = ImageDraw.Draw(img)
        draw.text((304, 540), "AI Generated", fill=(255, 255, 255), anchor="mm")
        img.save(path)
    except ImportError:
        # 没有PIL，创建空文件
        Path(path).write_text("placeholder")

# ========== Step 3: TTS配音 ==========

def generate_tts(text, output_path, retries=2):
    """多后端TTS配音"""
    if TTS_BACKEND == "minimax":
        return _generate_tts_minimax(text, output_path, retries)
    elif TTS_BACKEND == "openai":
        return _generate_tts_openai(text, output_path, retries)
    elif TTS_BACKEND == "edge":
        return _generate_tts_edge(text, output_path, retries)
    else:
        log(f"  ⚠️ 未知TTS后端: {TTS_BACKEND}，跳过配音")
        return False


def _generate_tts_minimax(text, output_path, retries=2):
    """MiniMax TTS"""
    import requests
    
    if not MINIMAX_API_KEY:
        log("  ⚠️ 未设置 MINIMAX_API_KEY，跳过配音")
        return False

    for attempt in range(retries + 1):
        try:
            resp = requests.post(
                f"{MINIMAX_BASE}/text_to_speech",
                headers={
                    "Authorization": f"Bearer {MINIMAX_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "speech-01",
                    "text": text,
                    "voice_id": MINIMAX_TTS_VOICE,
                    "speed": 1.0,
                    "volume": 1.0,
                    "audio_sample_rate": 24000,
                    "format": "mp3"
                },
                timeout=60
            )
            data = resp.json()
            if data.get("base_resp", {}).get("status_code") == 0:
                audio_url = data["data"]["audio_url"]
                audio_resp = requests.get(audio_url, timeout=30)
                if audio_resp.status_code == 200:
                    with open(output_path, "wb") as f:
                        f.write(audio_resp.content)
                    size_kb = len(audio_resp.content) / 1024
                    log(f"  🔊 MiniMax TTS: {Path(output_path).name} ({size_kb:.0f}KB)")
                    return True
            else:
                err = data.get("base_resp", {}).get("status_msg", "未知错误")
                if attempt < retries:
                    log(f"  ⚠️ TTS重试: {err}")
                    time.sleep(3)
                    continue
                log(f"  ⚠️ MiniMax TTS失败: {err}")
        except Exception as e:
            log(f"  ⚠️ TTS请求异常: {e}")
            if attempt < retries:
                time.sleep(3)
                continue
    return False


def _generate_tts_openai(text, output_path, retries=2):
    """OpenAI TTS"""
    import requests
    
    if not OPENAI_API_KEY:
        log("  ⚠️ 未设置 OPENAI_API_KEY，跳过配音")
        return False

    for attempt in range(retries + 1):
        try:
            resp = requests.post(
                f"{OPENAI_BASE}/audio/speech",
                headers={
                    "Authorization": f"Bearer {OPENAI_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "tts-1",
                    "input": text,
                    "voice": OPENAI_TTS_VOICE,
                    "speed": 1.0,
                    "response_format": "mp3"
                },
                timeout=60
            )
            if resp.status_code == 200:
                with open(output_path, "wb") as f:
                    f.write(resp.content)
                size_kb = len(resp.content) / 1024
                log(f"  🔊 OpenAI TTS: {Path(output_path).name} ({size_kb:.0f}KB)")
                return True
            else:
                err = resp.json().get("error", {}).get("message", str(resp.status_code))
                log(f"  ⚠️ OpenAI错误: {err}")
                if attempt < retries:
                    time.sleep(2)
                    continue
        except Exception as e:
            log(f"  ⚠️ TTS请求异常: {e}")
            if attempt < retries:
                time.sleep(2)
                continue
    return False


def _generate_tts_edge(text, output_path, retries=2):
    """Edge TTS (免费, 需 edge-tts)"""
    import subprocess
    
    for attempt in range(retries + 1):
        try:
            # edge-tts 命令行
            safe_text = text.replace('"', '\\"').replace("'", "\\'")
            cmd = f'edge-tts --voice zh-CN-XiaoxiaoNeural --text "{safe_text}" --write-media "{output_path}"'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
            if result.returncode == 0 and Path(output_path).exists():
                size_kb = Path(output_path).stat().st_size / 1024
                log(f"  🔊 Edge TTS: {Path(output_path).name} ({size_kb:.0f}KB)")
                return True
            else:
                log(f"  ⚠️ Edge TTS失败: {result.stderr[:100]}")
        except Exception as e:
            log(f"  ⚠️ Edge TTS异常: {e}")
            if attempt < retries:
                time.sleep(1)
                continue
    return False

# ========== Step 4: 合成视频 ==========

def render_video(scenes, materials_dir, audio_dir, output_path):
    """使用FFmpeg合成最终视频"""
    log("Step 4/5: 合成视频...")

    ensure_dir(output_path.parent)

    # 创建 concat 文件列表
    concat_parts = []
    temp_files = []

    for scene in scenes:
        sid = scene["id"]
        duration = scene["duration"]

        # 图片路径
        img_path = Path(materials_dir) / f"scene_{sid}.png"

        # 音频路径
        audio_path = Path(audio_dir) / f"scene_{sid}.mp3"

        # 检查文件是否存在
        has_img = img_path.exists()
        has_audio = audio_path.exists()

        if not has_img and not has_audio:
            log(f"  场景{sid}: 无素材，跳过")
            continue

        # 生成带字幕和文字覆盖的视频片段
        temp_video = Path(materials_dir) / f"temp_{sid}.mp4"

        # 构建 ffmpeg 命令
        if has_audio:
            # 有配音：图片+音频+文字覆盖
            overlay_text = scene["visual"].get("overlay_text", "")
            # 计算文本显示的持续时间
            text_duration = min(duration, 4.0)

            ffmpeg_cmd = [
                "ffmpeg", "-y",
                "-loop", "1",
                "-i", str(img_path),
                "-i", str(audio_path),
                "-c:v", "libx264",
                "-t", str(duration),
                "-pix_fmt", "yuv420p",
                "-vf", (
                    f"drawtext=text='{overlay_text}':"
                    f"fontfile=/System/Library/Fonts/PingFang.ttc:"
                    f"fontsize=48:fontcolor=white:"
                    f"x=(w-text_w)/2:y=h*0.1:"
                    f"enable='between(t,0,{text_duration})',"
                    f"drawtext=text='{scene.get('script','')[:30]}':"
                    f"fontfile=/System/Library/Fonts/PingFang.ttc:"
                    f"fontsize=28:fontcolor=white:"
                    f"x=(w-text_w)/2:y=h*0.75:"
                    f"enable='between(t,0,{text_duration})'"
                ),
                "-c:a", "aac",
                "-shortest",
                str(temp_video)
            ]
        else:
            # 无配音：纯图片+文字
            ffmpeg_cmd = [
                "ffmpeg", "-y",
                "-loop", "1",
                "-i", str(img_path),
                "-c:v", "libx264",
                "-t", str(duration),
                "-pix_fmt", "yuv420p",
                "-vf", "drawtext=text='AI Generated':"
                       "fontfile=/System/Library/Fonts/PingFang.ttc:"
                       "fontsize=36:fontcolor=white:"
                       "x=(w-text_w)/2:y=(h-text_h)/2",
                "-c:a", "aac",
                str(temp_video)
            ]

        ok, out = run_cmd(" ".join(ffmpeg_cmd))
        if ok and temp_video.exists():
            concat_parts.append(str(temp_video))
            temp_files.append(temp_video)
        else:
            log(f"  场景{sid} 渲染失败")

    if not concat_parts:
        log("  ❌ 没有可用素材")
        return False

    # 合并所有片段
    if len(concat_parts) == 1:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        import shutil
        shutil.copy(concat_parts[0], output_path)
        log(f"  ✅ 视频已生成: {output_path}")
    else:
        concat_list = Path(materials_dir) / "concat_list.txt"
        concat_list.write_text("\n".join(f"file '{p}'" for p in concat_parts))

        merge_cmd = f'ffmpeg -y -f concat -safe 0 -i "{concat_list}" -c copy "{output_path}"'
        ok, out = run_cmd(merge_cmd)
        if ok:
            log(f"  ✅ 视频已生成: {output_path} ({len(concat_parts)}场景合并)")
        else:
            log(f"  ❌ 合并失败: {out}")
            return False

    # 清理临时文件
    for f in temp_files:
        try:
            f.unlink(missing_ok=True)
        except:
            pass

    return True

# ========== Step 5: 字幕 ==========

def add_subtitles(video_path, scenes):
    """为视频添加硬字幕"""
    log("Step 5/5: 添加字幕...")

    output = video_path.parent / "final_subtitled.mp4"
    try:
        # 构建字幕内容
        subtitle_lines = []
        current_time = 0
        for scene in scenes:
            start = current_time
            end = current_time + scene["duration"]
            subtitle_lines.append(f"{_fmt_time(start)} --> {_fmt_time(end)}")
            subtitle_lines.append(scene["script"])
            subtitle_lines.append("")
            current_time = end

        # 写SRT
        srt_path = video_path.parent / "subtitles.srt"
        srt_path.write_text("\n".join(
            f"{i+1}\n{line}" if line.strip() and "-->" not in line and line.strip().isascii() is False
            else line
            for i, line in enumerate(subtitle_lines)
        ))

        # 用ffmpeg嵌入字幕
        cmd = [
            "ffmpeg", "-y",
            "-i", str(video_path),
            "-vf", f"subtitles={srt_path}:force_style='FontName=PingFang,FontSize=14,PrimaryColour=&HFFFFFF,BorderStyle=1,Outline=1'",
            "-c:a", "copy",
            str(output)
        ]
        ok, out = run_cmd(" ".join(cmd))
        if ok and output.exists():
            log(f"  ✅ 字幕已添加: {output}")
            return output
    except Exception as e:
        log(f"  ⚠️ 字幕添加失败: {e}")

    return video_path

def _fmt_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h:02d}:{m:02d}:{s:06.3f}"

# ========== 主流程 ==========

def main():
    parser = argparse.ArgumentParser(description=f"短视频一键生成器 v{VERSION}")
    parser.add_argument("--topic", required=True, help="视频主题")
    parser.add_argument("--points", required=True, help='要点JSON: [{"text":"...","emoji":"...","title":"..."}]')
    parser.add_argument("--style", default="tech", choices=["tech", "warm", "business"], help="视觉风格")
    parser.add_argument("--output", default=None, help="输出目录")
    parser.add_argument("--no-subtitles", action="store_true", help="不添加字幕")
    args = parser.parse_args()

    topic = args.topic
    try:
        points = json.loads(args.points)
    except json.JSONDecodeError as e:
        log(f"❌ 要点JSON格式错误: {e}")
        sys.exit(1)

    # 输出目录
    output_base = Path(args.output or f"./output_{int(time.time())}")
    materials_dir = output_base / "materials"
    audio_dir = output_base / "audio"
    ensure_dir(materials_dir)
    ensure_dir(audio_dir)

    log(f"{'='*50}")
    log(f"🎬 短视频一键生成器 v{VERSION}")
    log(f"主题: {topic}")
    log(f"要点: {len(points)}个")
    log(f"风格: {args.style}")
    log(f"输出: {output_base}")
    log(f"{'='*50}")

    # Step 1: 分镜规划
    scenes, total_duration = plan_storyboard(topic, points, args.style)

    # 保存分镜表
    storyboard = {"topic": topic, "scenes": scenes, "total_duration": total_duration}
    with open(output_base / "storyboard.json", "w", encoding="utf-8") as f:
        json.dump(storyboard, f, ensure_ascii=False, indent=2)
    log(f"分镜表已保存: {output_base / 'storyboard.json'}")

    # Step 2: AI生图
    print()
    log("=" * 50)
    log("Step 2/5: AI生成场景图片...")
    for scene in scenes:
        img_path = Path(materials_dir) / f"scene_{scene['id']}.png"
        prompt = scene["visual"]["background_prompt"]
        log(f"  场景{scene['id']}: {scene['title']}")
        generate_image(prompt, img_path)
        time.sleep(1.5)  # API限流保护

    # Step 3: TTS配音
    print()
    log("=" * 50)
    log("Step 3/5: TTS配音生成...")
    for scene in scenes:
        audio_path = Path(audio_dir) / f"scene_{scene['id']}.mp3"
        log(f"  场景{scene['id']}: {scene['script'][:40]}...")
        generate_tts(scene["script"], audio_path)
        time.sleep(1)

    # Step 4: 渲染视频
    print()
    log("=" * 50)
    output_video = output_base / "output.mp4"
    ok = render_video(scenes, materials_dir, audio_dir, output_video)

    if not ok:
        log("❌ 视频渲染失败")
        sys.exit(1)

    # Step 5: 字幕
    final_output = output_video
    if not args.no_subtitles:
        print()
        log("=" * 50)
        final_output = add_subtitles(output_video, scenes)

    # 统计文件大小
    if final_output.exists():
        size_mb = final_output.stat().st_size / (1024 * 1024)
        print()
        log(f"{'='*50}")
        log(f"🎉 完成！")
        log(f"视频: {final_output}")
        log(f"大小: {size_mb:.1f} MB")
        log(f"时长: {total_duration:.0f}秒")
        log(f"场景: {len(scenes)}个")
        log(f"{'='*50}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log("\n⚠️ 用户中断")
        sys.exit(1)
    except Exception as e:
        log(f"\n❌ 发生未知错误: {e}")
        traceback.print_exc()
        sys.exit(1)
