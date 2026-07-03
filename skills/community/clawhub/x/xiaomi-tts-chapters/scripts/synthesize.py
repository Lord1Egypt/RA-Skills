#!/usr/bin/env python3
"""
TTS语音合成主程序
将Markdown章节文件转换为有声小说音频
支持任意章节目录，不仅限于特定版本
支持长文本自动分段处理
支持多个TTS厂商（小米MiMo、OpenAI等）
"""

import os
import re
import glob
import time
import argparse

from mimo_tts import MiMoTTS


def get_chapter_files(chapters_dir: str) -> list[str]:
    """获取所有章节文件（支持 .md 和 .txt），按顺序排列"""
    files = []
    for ext in ('*.md', '*.txt'):
        files.extend(glob.glob(os.path.join(chapters_dir, ext)))
    
    def sort_key(filepath):
        filename = os.path.basename(filepath)
        match = re.match(r'^(\d+)', filename)
        if match:
            return (0, int(match.group(1)), filename)
        else:
            return (1, 0, filename)
    
    files.sort(key=sort_key)
    return files


def main():
    parser = argparse.ArgumentParser(description="TTS语音合成脚本（支持多厂商）")
    parser.add_argument("--api-key", help="MiMo API密钥（也可通过 MIMO_API_KEY 环境变量设置）")
    parser.add_argument("--chapters-dir", required=True, help="章节目录路径")
    parser.add_argument("--output-dir", default=".", help="输出目录路径")
    parser.add_argument("--voice", default="mimo_default", help="语音音色")
    parser.add_argument("--style", default=None, help="语音风格")
    parser.add_argument("--model", default="mimo-v2.5-tts", help="TTS模型")
    parser.add_argument("--base-url", default="https://token-plan-cn.xiaomimimo.com/v1", help="API基础URL")
    parser.add_argument("--delay", type=float, default=1.0, help="请求间隔（秒）")
    parser.add_argument("--start", type=int, default=0, help="起始章节索引")
    parser.add_argument("--end", type=int, default=-1, help="结束章节索引")
    parser.add_argument("--retry-failed", action="store_true", help="只重试失败的章节")
    parser.add_argument("--verify", action="store_true", help="验证已生成的音频文件")
    
    args = parser.parse_args()
    
    api_key = args.api_key or os.environ.get("MIMO_API_KEY")
    if not api_key:
        print("未检测到API密钥")
        api_key = input("请输入小米MiMo API密钥: ").strip()
        if not api_key:
            print("错误: 未提供API密钥")
            return
    
    tts = MiMoTTS(api_key, args.base_url)
    tts.model = args.model
    tts.voice = args.voice
    tts.format = "mp3"
    
    chapters_dir = os.path.abspath(args.chapters_dir)
    chapter_files = get_chapter_files(chapters_dir)
    
    if not chapter_files:
        print(f"错误: 在 {chapters_dir} 中没有找到章节文件")
        return
    
    print(f"找到 {len(chapter_files)} 个章节文件")
    
    start_idx = args.start
    end_idx = args.end if args.end >= 0 else len(chapter_files)
    end_idx = min(end_idx, len(chapter_files))
    
    output_dir = os.path.abspath(args.output_dir)
    os.makedirs(output_dir, exist_ok=True)
    
    # 验证模式
    if args.verify:
        print("\n=== 验证已生成的音频文件 ===")
        abnormal_files = []
        for i in range(len(chapter_files)):
            chapter_file = chapter_files[i]
            filename = os.path.basename(chapter_file)
            name_without_ext = os.path.splitext(filename)[0]
            output_path = os.path.join(output_dir, f"{name_without_ext}.mp3")
            
            if os.path.exists(output_path):
                duration = tts.get_audio_duration(output_path)
                chapter_size = os.path.getsize(chapter_file)
                
                # 检查异常：音频时长太短但章节内容不短
                if duration < 120 and chapter_size > 10000:
                    abnormal_files.append((filename, duration, chapter_size))
                    print(f"  ⚠️  {filename}: {duration:.1f}s (章节 {chapter_size} bytes)")
        
        if abnormal_files:
            print(f"\n发现 {len(abnormal_files)} 个异常文件")
            print("使用 --retry-failed 重新生成这些文件")
        else:
            print("\n所有文件正常")
        return
    
    success_count = 0
    fail_count = 0
    skip_count = 0
    
    for i in range(start_idx, end_idx):
        chapter_file = chapter_files[i]
        filename = os.path.basename(chapter_file)
        name_without_ext = os.path.splitext(filename)[0]
        output_path = os.path.join(output_dir, f"{name_without_ext}.mp3")
        
        if args.retry_failed and os.path.exists(output_path):
            skip_count += 1
            continue
        
        print(f"[{i+1}/{len(chapter_files)}] 处理: {filename}")
        
        if not args.retry_failed and os.path.exists(output_path):
            print(f"  跳过: 已存在")
            skip_count += 1
            continue
        
        if tts.synthesize_chapter(chapter_file, output_path, args.style):
            print(f"  成功")
            success_count += 1
        else:
            print(f"  失败")
            fail_count += 1
        
        if i < end_idx - 1:
            time.sleep(args.delay)
    
    print(f"\n完成: 成功 {success_count}, 失败 {fail_count}, 跳过 {skip_count}")


if __name__ == "__main__":
    main()
