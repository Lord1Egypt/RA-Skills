#!/usr/bin/env python3
"""Smart TTS - 智能语音合成，自动重试直到成功"""

import os
import sys

# 配置：从环境变量读取 API Key
API_KEY = os.environ.get("DASHSCOPE_API_KEY", "")
if not API_KEY:
    print("Error: Please set DASHSCOPE_API_KEY environment variable")
    print("  Windows: set DASHSCOPE_API_KEY=your-api-key")
    print("  Or add to openclaw.json env section")
    sys.exit(1)

import dashscope
from dashscope.audio.tts_v2 import SpeechSynthesizer

dashscope.api_key = API_KEY

# 可用的模型和音色组合（按优先级排序）
VOICE_OPTIONS = [
    {"model": "cosyvoice-v2", "voice": "longshao_v2"},
    {"model": "cosyvoice-v2", "voice": "longanyang"},
    {"model": "cosyvoice-v3-flash", "voice": "longanyang"},
    {"model": "cosyvoice-v3-flash", "voice": "longanhuan"},
    {"model": "cosyvoice-v3-flash", "voice": "longhuhu_v3"},
    {"model": "cosyvoice-v3-flash", "voice": "longpaopao_v3"},
    {"model": "cosyvoice-v3-flash", "voice": "longjielidou_v3"},
]

def generate(text, output_path=None):
    """尝试生成语音，自动切换模型直到成功"""
    
    if output_path is None:
        workspace = os.path.expanduser("~/.openclaw/workspace")
        output_path = os.path.join(workspace, "tts_output.wav")
    
    last_error = None
    
    for i, option in enumerate(VOICE_OPTIONS):
        model = option["model"]
        voice = option["voice"]
        print(f"Try {i+1}/{len(VOICE_OPTIONS)}: {model} + {voice} ...")
        
        try:
            synthesizer = SpeechSynthesizer(
                model=model,
                voice=voice
            )
            
            result = synthesizer.call(text)
            
            if hasattr(result, 'audio'):
                audio_data = result.audio
            else:
                audio_data = result
            
            if audio_data:
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                print(f"[OK] Saved: {output_path}")
                print(f"     Using: {model} + {voice}")
                return True
            
        except Exception as e:
            error_msg = str(e)
            last_error = error_msg
            
            if "418" in error_msg:
                print(f"   [X] 418 Not available, trying next...")
            elif "AccessDenied" in error_msg:
                print(f"   [X] Access denied, trying next...")
            else:
                print(f"   [X] Error: {error_msg[:80]}")
            
            try:
                synthesizer.close()
            except:
                pass
            continue
    
    print(f"[X] All options failed. Last error: {last_error}")
    return False

def main():
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
    else:
        text = "你好，这是智能语音合成测试"
    
    print(f"Generating: {text}\n")
    generate(text)

if __name__ == "__main__":
    main()
