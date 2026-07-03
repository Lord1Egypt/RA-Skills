#!/usr/bin/env python3
"""
小米MiMo TTS语音合成实现
继承自 BaseTTS 基类
"""

import base64
from typing import Optional

try:
    from openai import OpenAI
except ImportError:
    print("请先安装openai库: pip install openai")
    exit(1)

from base_tts import BaseTTS


class MiMoTTS(BaseTTS):
    """小米MiMo TTS语音合成类"""
    
    def __init__(self, api_key: str, base_url: str = "https://token-plan-cn.xiaomimimo.com/v1"):
        super().__init__()
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url,
            timeout=600.0
        )
        self.model = "mimo-v2.5-tts"
        self.voice = "mimo_default"
        self.format = "mp3"
    
    def _synthesize_segment(self, text: str, output_path: str, style: Optional[str] = None) -> bool:
        """合成单个文本段 - 小米MiMo实现"""
        try:
            content = text
            if style:
                content = f"({style}){text}"
            
            messages = [
                {
                    "role": "assistant",
                    "content": content
                }
            ]
            
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                audio={
                    "format": self.format,
                    "voice": self.voice
                }
            )
            
            if not completion.choices or not completion.choices[0].message.audio:
                print(f"      API返回空音频数据")
                return False
            
            audio_data = completion.choices[0].message.audio.data
            audio_bytes = base64.b64decode(audio_data)
            
            with open(output_path, 'wb') as f:
                f.write(audio_bytes)
            
            return True
        except Exception as e:
            print(f"      API错误: {e}")
            return False
