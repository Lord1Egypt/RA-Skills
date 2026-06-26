#!/usr/bin/env python3
"""MiniMax TTS 语音合成"""
import json
import requests
import sys
import os
from pathlib import Path
import time
import base64

CONFIG_PATH = Path(__file__).parent.parent / "config.json"
OUTPUT_DIR = Path(__file__).parent / "output"


def load_config():
    with open(CONFIG_PATH, encoding='utf-8') as f:
        return json.load(f)


def text_to_speech(text, voice_id=None):
    config = load_config()
    api_key = config["api_key"]
    voice = voice_id or config.get("voice_id", "male-qn-qingse")
    
    # MiniMax 官方 API
    url = "https://api.minimaxi.com/v1/t2a_v2"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "speech-01-turbo",
        "text": text,
        "stream": False,
        "voice_setting": {
            "voice_id": voice,
            "speed": 1.0,
            "vol": 1.0,
            "pitch": 0
        },
        "audio_setting": {
            "sample_rate": 32000,
            "bitrate": 128000,
            "format": "mp3",
            "channel": 1
        },
        "output_format": "hex"
    }
    
    print(f"正在合成: {text[:30]}...")
    
    try:
        resp = requests.post(url, headers=headers, json=data, timeout=60)
        result = resp.json()
        
        if result.get("base_resp", {}).get("status_code") == 0:
            audio_hex = result.get("data", {}).get("audio")
            if audio_hex:
                # 解码并保存
                OUTPUT_DIR.mkdir(exist_ok=True)
                output_file = OUTPUT_DIR / f"tts_{int(time.time())}.mp3"
                
                audio_bytes = bytes.fromhex(audio_hex)
                with open(output_file, "wb") as f:
                    f.write(audio_bytes)
                
                print(f"[OK] 已生成: {output_file}")
                return str(output_file)
        
        print(f"错误: {result}")
        return None
            
    except Exception as e:
        print(f"错误: {e}")
        return None


def list_voices():
    """列出可用音色"""
    voices = [
        "male-qn-qingse - 青涩青年",
        "male-qn-jingying - 精英青年", 
        "male-qn-badao - 霸道总裁",
        "female-shaonv - 活泼少女",
        "female-yujie - 温柔御姐",
        "female-chengshu - 都市白领"
    ]
    print("可用音色:")
    for v in voices:
        print(f"  - {v}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法:")
        print("  python mm_tts.py \"要说话的文本\"")
        print("  python mm_tts.py --voices  # 查看可用音色")
        sys.exit(1)
    
    if sys.argv[1] == "--voices":
        list_voices()
    else:
        text = " ".join(sys.argv[1:])
        text_to_speech(text)
