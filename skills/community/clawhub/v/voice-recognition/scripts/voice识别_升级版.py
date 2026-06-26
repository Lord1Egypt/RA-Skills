#!/usr/bin/env python3
"""
升级版语音识别工具
功能：
1. 本地 Whisper 识别（免费）
2. 中文优化识别
3. 中英翻译
4. 语音摘要
5. 支持多语言
"""

import subprocess
import os
from pathlib import Path

# 配置
WHISPER_CMD = "whisper"
DEFAULT_MODEL = "medium"  # 平衡速度和准确度

def transcribe(audio_path, language="zh", translate=False, summarize=False):
    """
    语音识别主函数
    
    Args:
        audio_path: 音频文件路径
        language: 语言 (zh/en/auto)
        translate: 是否翻译成英文
        summarize: 是否生成摘要
    
    Returns:
        dict: 包含文本、翻译、摘要的结果
    """
    audio_path = Path(audio_path)
    
    if not audio_path.exists():
        return {"error": f"文件不存在: {audio_path}"}
    
    # 检测文件类型
    ext = audio_path.suffix.lower()
    if ext not in ['.mp3', '.m4a', '.wav', '.ogg', '.flac', '.webm']:
        return {"error": f"不支持的文件格式: {ext}"}
    
    # 设置参数
    task = "translate" if translate else "transcribe"
    lang_code = "Chinese" if language == "zh" else "English"
    
    cmd = [
        WHISPER_CMD,
        str(audio_path),
        "--model", DEFAULT_MODEL,
        "--language", lang_code,
        "--task", task,
        "--output_format", "txt",
        "--output_dir", str(audio_path.parent),
        "--verbose", "False"
    ]
    
    # 执行识别
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    output_file = audio_path.with_suffix(".txt")
    transcript = ""
    
    if output_file.exists():
        transcript = output_file.read_text(encoding='utf-8')
    
    response = {
        "transcript": transcript.strip(),
        "language": language,
        "translated": translate,
        "summarized": summarize
    }
    
    # 生成摘要（如果需要）
    if summarize and transcript:
        response["summary"] = generate_summary(transcript)
    
    return response

def transcribe_zh(audio_path):
    """中文语音识别（简化接口）"""
    return transcribe(audio_path, language="zh", translate=False)

def transcribe_auto(audio_path):
    """自动检测语言"""
    audio_path = Path(audio_path)
    
    cmd = [
        WHISPER_CMD,
        str(audio_path),
        "--model", DEFAULT_MODEL,
        "--task", "transcribe",
        "--output_format", "txt",
        "--output_dir", str(audio_path.parent)
    ]
    
    subprocess.run(cmd, capture_output=True, text=True)
    
    output_file = audio_path.with_suffix(".txt")
    if output_file.exists():
        return {"transcript": output_file.read_text(encoding='utf-8').strip()}
    
    return {"error": "识别失败"}

def generate_summary(text):
    """生成简洁摘要"""
    if len(text) < 50:
        return text
    
    # 简单摘要：取前100字 + 最后50字
    if len(text) > 150:
        return text[:100] + "..." + text[-50:]
    return text

def quick_check():
    """检查 Whisper 是否可用"""
    result = subprocess.run([WHISPER_CMD, "--help"], capture_output=True, text=True)
    return "whisper" in result.stdout.lower()

# CLI 接口
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python3 voice识别.py <音频文件> [--zh] [--en] [--translate] [--summarize]")
        print("示例:")
        print("  python3 voice识别.py audio.m4a           # 中文识别")
        print("  python3 voice识别.py audio.m4a --zh       # 中文识别")
        print("  python3 voice识别.py audio.m4a --en       # 英文识别")
        print("  python3 voice识别.py audio.m4a --translate # 识别并翻译成英文")
        sys.exit(1)
    
    audio = sys.argv[1]
    zh = "--zh" in sys.argv
    en = "--en" in sys.argv
    translate = "--translate" in sys.argv
    summarize = "--summarize" in sys.argv
    
    language = "zh" if zh else ("en" if en else "auto")
    
    result = transcribe(audio, language, translate, summarize)
    
    if "error" in result:
        print(f"错误: {result['error']}")
        sys.exit(1)
    
    print("=" * 50)
    print("📝 识别结果:")
    print("=" * 50)
    print(result["transcript"])
    
    if translate:
        print("\n🌐 翻译:")
        print("(Whisper translate模式已翻译)")
    
    if summarize and "summary" in result:
        print("\n📋 摘要:")
        print(result["summary"])
