#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视频自动生成器 - 主程序
功能：输入选题，自动生成完整视频（脚本+配音+字幕+封面+剪辑）
作者：QClaw AI
创建时间：2026-06-12
"""

import os
import sys
import subprocess
import json
from datetime import datetime

class VideoAutoGenerator:
    """视频自动生成器主类"""
    
    def __init__(self, output_dir='output'):
        """初始化生成器"""
        self.output_dir = output_dir
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.project_dir = os.path.dirname(self.script_dir)
        
        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"🚀 视频自动生成器初始化完成")
        print(f"📁 输出目录：{os.path.abspath(output_dir)}")
    
    def generate_script(self, topic, duration=60, style='tutorial'):
        """第1步：生成视频脚本"""
        print(f"\n📝 第1步：生成视频脚本...")
        print(f"   选题：{topic}")
        print(f"   时长：{duration}秒")
        print(f"   风格：{style}")
        
        # 这里应该调用video-script-gen技能
        # 简化版本：生成一个基础脚本模板
        script = self._generate_script_template(topic, duration, style)
        
        # 保存脚本
        script_path = os.path.join(self.output_dir, 'script.md')
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script)
        
        print(f"   ✅ 脚本已生成：{script_path}")
        return script, script_path
    
    def _generate_script_template(self, topic, duration, style):
        """生成脚本模板（简化版本）"""
        # 这里应该是调用AI生成脚本，现在先用模板
        script = f"""# 视频脚本：{topic}

## 基本信息
- 标题：{topic}
- 时长：{duration}秒
- 风格：{style}
- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 分镜脚本

### 镜头1（0-5秒）：开场
**画面**：标题动画 + 背景音乐
**配音**：{topic}！今天给大家详细介绍
**字幕**：{topic}

### 镜头2（5-30秒）：主体内容
**画面**：相关内容展示
**配音**：详细内容请观看视频...
**字幕**：详细内容

### 镜头3（30-60秒）：结尾
**画面**：总结 + 引导关注
**配音**：如果觉得有用，请点赞关注
**字幕**：点赞关注不迷路

## 配音文本（纯文本，用于TTS）
{topic}！今天给大家详细介绍。详细内容请观看视频。如果觉得有用，请点赞关注。
"""
        return script
    
    def generate_voice(self, text, voice_name='zh-CN-XiaoxiaoNeural', rate='+0%'):
        """第2步：生成配音（TTS）"""
        print(f"\n🎤 第2步：生成配音...")
        print(f"   音色：{voice_name}")
        print(f"   语速：{rate}")
        
        # 保存文本到临时文件
        text_file = os.path.join(self.output_dir, 'voice_text.txt')
        with open(text_file, 'w', encoding='utf-8') as f:
            f.write(text)
        
        # 调用edge-tts生成配音（使用python -m方式）
        voice_path = os.path.join(self.output_dir, 'voice.mp3')
        cmd = [
            'python', '-m', 'edge_tts',
            '--text', text,
            '--voice', voice_name,
            '--rate', rate,
            '--write-media', voice_path
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"   ✅ 配音已生成：{voice_path}")
            return voice_path
        except subprocess.CalledProcessError as e:
            print(f"   ❌ 配音生成失败：{e}")
            # 如果edge-tts失败，使用备用方案（返回None）
            return None
    
    def generate_cover(self, title, style='tech'):
        """第4步：生成封面图"""
        print(f"\n🖼️  第4步：生成封面...")
        print(f"   标题：{title}")
        print(f"   风格：{style}")
        
        # 检查是否有Pillow库
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            # 创建画布
            img = Image.new('RGB', (1280, 720), color='#1a1a2e')
            draw = ImageDraw.Draw(img)
            
            # 尝试加载字体
            font_path = os.path.join(self.project_dir, 'assets', 'msyh.ttc')
            if os.path.exists(font_path):
                font = ImageFont.truetype(font_path, 60)
            else:
                font = ImageFont.load_default()
            
            # 绘制标题（居中）
            bbox = draw.textbbox((0, 0), title, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            x = (1280 - text_width) // 2
            y = (720 - text_height) // 2
            
            # 绘制描边和文字
            draw.text((x-2, y-2), title, font=font, fill='black')
            draw.text((x, y), title, font=font, fill='white')
            
            # 保存
            cover_path = os.path.join(self.output_dir, 'cover.png')
            img.save(cover_path)
            
            print(f"   ✅ 封面已生成：{cover_path}")
            return cover_path
            
        except ImportError:
            print(f"   ⚠️  未安装Pillow库，跳过封面生成")
            return None
    
    def compile_video(self, audio_file, cover_image, output_name='final_video.mp4'):
        """第5步：合成视频"""
        print(f"\n🎬 第5步：合成视频...")
        
        if not audio_file or not os.path.exists(audio_file):
            print(f"   ❌ 音频文件不存在，无法合成视频")
            return None
        
        output_path = os.path.join(self.output_dir, output_name)
        
        # 构建FFmpeg命令
        if cover_image and os.path.exists(cover_image):
            # 方案1：静态图片 + 音频
            cmd = [
                'ffmpeg',
                '-loop', '1',
                '-i', cover_image,
                '-i', audio_file,
                '-c:v', 'libx264',
                '-tune', 'stillimage',
                '-c:a', 'aac',
                '-b:a', '192k',
                '-shortest',
                '-y',
                output_path
            ]
        else:
            # 方案2：只有音频，生成波形图
            print(f"   ⚠️  封面图不存在，生成音频波形视频")
            cmd = [
                'ffmpeg',
                '-i', audio_file,
                '-filter_complex', '[0:a]showwaves=s=1280x720:mode=line,format=yuv420p[v]',
                '-map', '[v]',
                '-map', '0:a',
                '-c:v', 'libx264',
                '-c:a', 'aac',
                '-b:a', '192k',
                '-y',
                output_path
            ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"   ✅ 视频已合成：{output_path}")
            return output_path
        except subprocess.CalledProcessError as e:
            print(f"   ❌ 视频合成失败：{e}")
            return None
    
    def generate(self, topic, duration=60, style='tutorial', voice_name='zh-CN-XiaoxiaoNeural'):
        """完整流程：一键生成视频"""
        print(f"\n{'='*60}")
        print(f"🚀 开始生成视频")
        print(f"{'='*60}")
        print(f"📋 选题：{topic}")
        print(f"⏱️  时长：{duration}秒")
        print(f"🎨 风格：{style}")
        print(f"🎤 音色：{voice_name}")
        
        # 第1步：生成脚本
        script, script_path = self.generate_script(topic, duration, style)
        
        # 提取配音文本（简化：直接用标题）
        voice_text = f"{topic}！详细内容请观看视频。如果觉得有用，请点赞关注。"
        
        # 第2步：生成配音
        voice_path = self.generate_voice(voice_text, voice_name)
        
        # 第3步：生成字幕（可选，暂时跳过）
        subtitle_path = None
        
        # 第4步：生成封面
        cover_path = self.generate_cover(topic)
        
        # 第5步：合成视频
        video_path = self.compile_video(voice_path, cover_path)
        
        # 生成报告
        report = {
            'topic': topic,
            'duration': duration,
            'style': style,
            'voice_name': voice_name,
            'script_path': script_path,
            'voice_path': voice_path,
            'cover_path': cover_path,
            'video_path': video_path,
            'generate_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        report_path = os.path.join(self.output_dir, 'report.json')
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n{'='*60}")
        print(f"🎉 视频生成完成！")
        print(f"{'='*60}")
        print(f"📁 输出目录：{os.path.abspath(self.output_dir)}")
        print(f"📄 生成报告：{report_path}")
        if video_path:
            print(f"🎬 最终视频：{video_path}")
        print(f"{'='*60}\n")
        
        return video_path, report_path


def main():
    """主函数"""
    import argparse
    
    # 命令行参数解析
    parser = argparse.ArgumentParser(description='AI视频自动生成器')
    parser.add_argument('--topic', type=str, default='2026年最值得用的5个AI工具', help='视频主题')
    parser.add_argument('--duration', type=int, default=60, help='视频时长（秒）')
    parser.add_argument('--style', type=str, default='review', choices=['review', 'tutorial', 'story'], help='视频风格')
    parser.add_argument('--voice', type=str, default='zh-CN-XiaoxiaoNeural', help='配音音色')
    parser.add_argument('--output-dir', type=str, default='output', help='输出目录')
    
    args = parser.parse_args()
    
    # 创建生成器
    generator = VideoAutoGenerator(output_dir=args.output_dir)
    
    # 生成视频
    video_path, report_path = generator.generate(
        topic=args.topic,
        duration=args.duration,
        style=args.style,
        voice_name=args.voice
    )
    
    if video_path:
        print(f"✅ 成功！视频已生成：{video_path}")
        print(f"✅ 报告已生成：{report_path}")
    else:
        print(f"❌ 视频生成失败，请检查错误信息")


if __name__ == '__main__':
    main()
