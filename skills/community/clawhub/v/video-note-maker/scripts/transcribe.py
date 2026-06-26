#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Whisper 转写脚本
用法：python transcribe.py <音频文件> [模型] [语言]
"""

import sys
import whisper

def transcribe(audio_path, model="small", language="zh"):
    print(f"加载模型：{model}")
    whisper_model = whisper.load_model(model)
    
    print(f"转写音频：{audio_path}")
    result = whisper_model.transcribe(
        audio_path,
        language=language,
        temperature=0
    )
    
    return result['text']

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python transcribe.py <音频文件> [模型] [语言]")
        sys.exit(1)
    
    audio_path = sys.argv[1]
    model = sys.argv[2] if len(sys.argv) > 2 else "small"
    language = sys.argv[3] if len(sys.argv) > 3 else "zh"
    
    text = transcribe(audio_path, model, language)
    print(text)
