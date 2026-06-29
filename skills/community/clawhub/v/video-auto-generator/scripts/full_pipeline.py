#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ClawHub推广视频全自动流水线
功能：AI生成脚本 → edge-tts配音 → PIL分镜图 → ffmpeg合成视频

使用方法：
  python full_pipeline.py --topic "你的选题" --duration 90 --voice zh-CN-XiaoxiaoNeural
"""

import os
import sys
import json
import subprocess
import argparse
from datetime import datetime
from pathlib import Path

# ============ 配置 ============
VOICE_MAP = {
    "zh-CN-XiaoxiaoNeural": "zh-CN-XiaoxiaoNeural",
    "zh-CN-YunxiNeural": "zh-CN-YunxiNeural",
    "zh-CN-XiaoyiNeural": "zh-CN-XiaoyiNeural",
}

COLOR_PALETTE = [
    "#1e3a5f", "#2d1b4e", "#1b4e2d",
    "#4e2d1b", "#2d4e1b", "#4e1b2d",
    "#1a3a5f", "#3d1b4e", "#1b4e3d",
]

# ============ 核心类 ============

class PromoVideoPipeline:
    """ClawHub推广视频全自动流水线"""

    def __init__(self, output_dir, voice="zh-CN-XiaoxiaoNeural"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.voice = VOICE_MAP.get(voice, voice)
        self.shots = []

    def generate_script(self, topic, duration=90):
        """生成视频脚本（硬编码模板，可替换为AI API调用）"""
        print(f"\n📝 生成视频脚本: {topic}")

        # 分镜配置（可自定义）
        segments = [
            {"title": "开场", "seconds": 5, "emoji": "💰",
             "text": f"你知道吗？我用AI做了5个技能，在ClawHub上卖，月入过万！"},
            {"title": "热点追踪器", "seconds": 15, "emoji": "🔥",
             "text": "第一个技能叫热点追踪器。每天自动追踪抖音、小红书、微博热门话题，帮你找到最容易爆的选题，每天省下2小时。"},
            {"title": "视频自动生成器", "seconds": 15, "emoji": "🎬",
             "text": "第二个是视频自动生成器。输入主题，AI自动写脚本、配音、加字幕，一键生成短视频，每天能做10条，效率提升20倍。"},
            {"title": "竞品价格监控", "seconds": 15, "emoji": "💰",
             "text": "第三个是竞品价格监控。自动追踪竞争对手价格变化，设置提醒，电商运营必备。"},
            {"title": "选题生成器", "seconds": 15, "emoji": "💡",
             "text": "第四个是选题生成器。输入账号定位，AI自动生成一周选题计划，支持抖音、小红书、B站、知乎。"},
            {"title": "多平台发布器", "seconds": 13, "emoji": "📤",
             "text": "第五个是多平台自动发布器。一篇文章自动改写成各平台版本，同时发布到抖音、小红书、B站，一个内容全网分发。"},
            {"title": "引导购买", "seconds": max(5, duration - sum(s["seconds"] for s in [
                {"seconds":5},{"seconds":15},{"seconds":15},{"seconds":15},{"seconds":15},{"seconds":13}
            ])), "emoji": "🎁",
             "text": f"这5个技能单独买237元，现在全家桶套餐只要199，一次购买终身使用。点击链接，早用早赚钱！"},
        ]

        # 计算总时长
        total = sum(s["seconds"] for s in segments)
        if total != duration:
            segments[-1]["seconds"] += (duration - total)

        self.shots = segments

        # 生成脚本文件
        script_md = f"""# {topic}

## 基本信息
- 标题：{topic}
- 时长：{duration}秒
- 风格：review
- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 分镜

"""
        voice_lines = []
        for i, seg in enumerate(segments):
            start = sum(s["seconds"] for s in segments[:i])
            script_md += f"### 镜头{i+1}（{start}-{start+seg['seconds']}秒）：{seg['title']}\n"
            script_md += f"**画面**：{seg['emoji']} {seg['title']}\n"
            script_md += f"**配音**：{seg['text']}\n\n"
            voice_lines.append(seg["text"])

        voice_text = "".join(f"{t}。" for t in voice_lines)
        script_md += f"## 配音文本\n\n{voice_text}"

        script_path = self.output_dir / "script.md"
        script_path.write_text(script_md, encoding="utf-8")
        print(f"   ✅ 脚本已保存: {script_path}")

        # 保存配音文本
        voice_path = self.output_dir / "voice_text.txt"
        voice_path.write_text(voice_text, encoding="utf-8")
        print(f"   ✅ 配音文本已保存")

        # 保存分镜JSON
        shots_path = self.output_dir / "shots.json"
        shots_path.write_text(json.dumps(segments, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"   ✅ 分镜JSON已保存")

        return script_path

    def generate_voice(self):
        """使用edge-tts生成配音"""
        print(f"\n🎤 生成配音: {self.voice}")
        voice_text = (self.output_dir / "voice_text.txt").read_text(encoding="utf-8")

        # 写入临时文件（避免命令行编码问题）
        text_file = self.output_dir / "_temp_voice.txt"
        text_file.write_text(voice_text, encoding="utf-8")

        cmd = [
            sys.executable, "-m", "edge_tts",
            "--file", str(text_file),
            "--voice", self.voice,
            "--write-media", str(self.output_dir / "voice.mp3")
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        text_file.unlink(missing_ok=True)

        if result.returncode != 0:
            print(f"   ⚠️  edge-tts失败，尝试直接传文本")
            cmd[-2] = "--text"
            cmd[-1] = voice_text[:500]  # 截断避免超长
            result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            size = os.path.getsize(self.output_dir / "voice.mp3")
            print(f"   ✅ 配音已生成: {(size/1024):.1f} KB")
        else:
            print(f"   ❌ 配音生成失败: {result.stderr[-300:]}")
        return self.output_dir / "voice.mp3"

    def generate_images(self):
        """使用PIL生成各镜头图片"""
        print(f"\n🖼️  生成{len(self.shots)}张分镜图...")

        try:
            from PIL import Image, ImageDraw, ImageFont
        except ImportError:
            print("   ⚠️  PIL未安装，跳过图片生成")
            return

        for i, seg in enumerate(self.shots):
            color = COLOR_PALETTE[i % len(COLOR_PALETTE)]
            img = Image.new('RGB', (1080, 1920), color=color)
            draw = ImageDraw.Draw(img)

            # 标题
            draw.text((540, 700), seg.get("emoji", "📺"), fill="white", anchor="mm")
            draw.text((540, 820), seg["title"], fill="white", anchor="mm")
            draw.text((540, 920), "ClawHub Skills", fill="#FFD700", anchor="mm")
            draw.text((540, 1800), f"{i+1}/{len(self.shots)}", fill="#888888", anchor="mm")

            img.save(str(self.output_dir / f"shot_{i}.png"))

        # 封面图
        cover = Image.new('RGB', (1080, 1920), color="#0a0a1a")
        draw = ImageDraw.Draw(cover)
        draw.text((540, 700), "ClawHub", fill="white", anchor="mm")
        draw.text((540, 820), "赚钱实战", fill="#FFD700", anchor="mm")
        draw.text((540, 950), "5个AI技能 月入过万", fill="white", anchor="mm")
        draw.text((540, 1100), "洪辰的作品", fill="#888888", anchor="mm")
        cover.save(str(self.output_dir / "cover.png"))

        print(f"   ✅ {len(self.shots)+1}张图片已生成")

    def assemble_video(self):
        """使用ffmpeg合成视频（分段渲染+合并）"""
        print(f"\n🎬 合成视频...")

        shots = sorted(self.output_dir.glob("shot_*.png"))
        if not shots:
            print("   ❌ 未找到分镜图片")
            return None

        seg_dir = self.output_dir / "segments"
        seg_dir.mkdir(exist_ok=True)

        # Step 1: 渲染每张图片为独立视频片段
        print(f"   📐 渲染 {len(shots)} 个片段...")
        for i, img_path in enumerate(shots):
            seg_path = seg_dir / f"seg_{i:02d}.mp4"
            dur = self.shots[i]["seconds"]

            if seg_path.exists():
                print(f"      跳过 seg_{i:02d} (已存在)")
                continue

            cmd = [
                sys.executable, "-c",
                f"""
import subprocess, sys
cmd = ['ffmpeg', '-y', '-loop', '1',
       '-i', r'{img_path}',
       '-c:v', 'libx264', '-preset', 'fast', '-crf', '23',
       '-t', '{dur}', '-r', '30',
       '-pix_fmt', 'yuv420p',
       '-vf', 'scale=1080:1920,setsar=1',
       r'{seg_path}']
r = subprocess.run(cmd)
sys.exit(r.returncode)
"""
            ]
            result = subprocess.run(cmd, capture_output=True)
            if result.returncode == 0:
                size = os.path.getsize(seg_path)
                print(f"      ✅ seg_{i:02d} ({dur}s)")
            else:
                print(f"      ❌ seg_{i:02d}: {result.stderr[-200:].decode('utf-8','ignore')}")

        # Step 2: 生成文件列表
        list_file = seg_dir / "filelist.txt"
        with open(list_file, "w") as f:
            for i in range(len(shots)):
                f.write(f"file 'seg_{i:02d}.mp4'\n")

        # Step 3: 合并所有片段
        output_path = self.output_dir / "final_promo.mp4"
        audio_path = self.output_dir / "voice.mp3"

        cmd = [
            "ffmpeg", "-y",
            "-f", "concat", "-safe", "0",
            "-i", str(list_file),
            "-i", str(audio_path),
            "-c:v", "libx264", "-crf", "23",
            "-c:a", "aac", "-b:a", "128k",
            "-pix_fmt", "yuv420p",
            str(output_path)
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"   ❌ 合并失败: {result.stderr[-500:]}")
            return None

        size = os.path.getsize(output_path)
        print(f"   ✅ 视频已合成: {(size/1024):.1f} KB ({output_path.name})")
        return output_path

    def run(self, topic, duration=90):
        """运行完整流水线"""
        print(f"\n{'='*60}")
        print(f"🚀 ClawHub推广视频流水线")
        print(f"{'='*60}")
        print(f"📋 选题: {topic}")
        print(f"⏱️  时长: {duration}秒")
        print(f"🎤 音色: {self.voice}")
        print(f"📁 输出: {self.output_dir}")
        print(f"{'='*60}")

        self.generate_script(topic, duration)
        self.generate_voice()
        self.generate_images()
        video = self.assemble_video()

        if video:
            print(f"\n{'='*60}")
            print(f"🎉 完成！视频: {video}")
            print(f"{'='*60}")
        return video


# ============ 入口 ============
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ClawHub推广视频流水线")
    parser.add_argument("--topic", type=str, default="ClawHub赚钱实战：5个AI技能月入过万",
                        help="视频主题")
    parser.add_argument("--duration", type=int, default=90, help="视频时长（秒）")
    parser.add_argument("--voice", type=str, default="zh-CN-XiaoxiaoNeural",
                        help="配音音色")
    parser.add_argument("--output", type=str,
                        default=None, help="输出目录")

    args = parser.parse_args()

    # 清理topic作为目录名
    safe_name = "".join(c if c.isalnum() or c in " -" else "_" for c in args.topic)[:30]
    output_dir = args.output or str(Path.home() / "Desktop" / f"video_{safe_name}")

    pipeline = PromoVideoPipeline(output_dir, voice=args.voice)
    pipeline.run(args.topic, args.duration)
