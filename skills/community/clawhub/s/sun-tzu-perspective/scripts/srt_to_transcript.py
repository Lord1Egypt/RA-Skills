#!/usr/bin/env python3
# SRT字幕转纯文本脚本
# 用法: python3 srt_to_transcript.py <input.srt> [output.txt]

import sys
import re

def clean_srt_lines(lines):
    """清理SRT格式，提取纯文本"""
    transcript = []
    skip_pattern = re.compile(r'^\d+$|^\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}$')
    last_line = ""
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if skip_pattern.match(line):
            continue
        # 去除HTML标签
        line = re.sub(r'<[^>]+>', '', line)
        # 去连续重复行
        if line != last_line:
            transcript.append(line)
            last_line = line
    
    return transcript

def main():
    if len(sys.argv) < 2:
        print("用法: python3 srt_to_transcript.py <input.srt> [output.txt]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    transcript = clean_srt_lines(lines)
    output_text = '\n'.join(transcript)
    
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(output_text)
        print(f"已保存: {output_file} ({len(transcript)} 行)")
    else:
        print(output_text)

if __name__ == "__main__":
    main()
