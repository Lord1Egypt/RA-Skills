#!/usr/bin/env python3
"""Smart TTS Batch - 批量智能语音合成"""

import os
import sys

# 配置：从环境变量读取 API Key
API_KEY = os.environ.get("DASHSCOPE_API_KEY", "")
if not API_KEY:
    print("Error: Please set DASHSCOPE_API_KEY environment variable")
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

# 默认语音文本
DEFAULT_TEXTS = [
    "机械臂正在清零，请保证机器四周无任何障碍物，请勿触碰，避免造成伤害",
    "清零超时，请断电重启或联系厂家",
    "清零成功，已返回初始位置"
]

def generate(text, output_path):
    """尝试生成语音，自动切换模型直到成功"""
    
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
    workspace = os.path.expanduser("~/.openclaw/workspace")
    
    texts = DEFAULT_TEXTS
    if len(sys.argv) > 1:
        # 从命令行参数读取文本文件
        import json
        try:
            with open(sys.argv[1], 'r', encoding='utf-8') as f:
                texts = json.load(f)
        except:
            texts = sys.argv[1:]
    
    for i, text in enumerate(texts, 1):
        output_path = os.path.join(workspace, f"tts_{i}.wav")
        print(f"\n--- [{i}/{len(texts)}] ---")
        print(f"Text: {text}")
        generate(text, output_path)
    
    print("\n=== All done! ===")

if __name__ == "__main__":
    main()
