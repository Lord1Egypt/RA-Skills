# -*- coding: utf-8 -*-
"""
Tencent TTS Tool - AgentScope Tool Interface
Supports long text generation (10+ minute podcasts)
"""
from typing import Literal
from agentscope.tool import ToolResponse
from agentscope.message import TextBlock, AudioBlock
from agentscope.message import Base64Source

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from tts_podcast import (
    main as tts_main, VOICE_TYPES, 
    estimate_duration, validate_text_length
)

import base64

# Import config manager
try:
    from core.tts_config import get_tts_credentials
except ImportError:
    # Fallback if core module not available
    def get_tts_credentials():
        import os
        return (
            os.environ.get("TENCENT_TTS_SECRET_ID", ""),
            os.environ.get("TENCENT_TTS_SECRET_KEY", ""),
        )


def tengxun_tts_generate(
    text: str,
    voice: Literal[
        "普通女声", "普通男声", "情感女声", "情感男声",
        "智障少女", "阳光少年", "温柔淑女", "成熟青年",
        "严厉管事", "亲和女声", "甜美女声", "磁性男声",
        "播音主播", "客服女声", "售前客服", "售后客服",
        "亲和客服", "小旭", "小巴", "思驰", "思佳",
        "思悦", "小宁", "小杨", "云扬", "云飞"
    ] = "小旭",
) -> ToolResponse:
    """
    Convert text to speech audio using Tencent Cloud TTS.
    
    Supports generating podcasts up to 30 minutes long. Long texts are automatically
    split into chunks and processed in parallel, then merged into a complete audio file.

    Args:
        text (`str`):
            Text content to convert to speech, supports Chinese, unlimited length.
            Supports content up to 30 minutes (~7200 characters).
        voice (`Literal[...]`, defaults to `"小旭"`):
            Voice name. Options include:
            - Basic: 普通女声, 普通男声, 情感女声, 情感男声
            - Featured: 智障少女, 阳光少年, 温柔淑女, 成熟青年, 严厉管事, 亲和女声, 甜美女声, 磁性男声, 播音主播
            - Customer service: 客服女声, 售前客服, 售后客服, 亲和客服
            - Tencent featured: 小旭, 小巴, 思驰, 思佳, 思悦, 小宁, 小杨, 云扬, 云飞

    Returns:
        `ToolResponse`:
            Contains generated audio file (AudioBlock) and generation info (TextBlock)
    """
    try:
        # Validate text length
        valid, msg = validate_text_length(text)
        if not valid:
            return ToolResponse(
                [
                    TextBlock(
                        type="text",
                        text=f"❌ {msg}",
                    ),
                ],
            )
        
        # Estimate duration
        estimated_minutes = estimate_duration(len(text))
        
        # Map voice name to ID
        voice_map = {v: k for k, v in VOICE_TYPES.items()}
        voice_type = voice_map.get(voice, "502006")

        # Get credentials
        secret_id, secret_key = get_tts_credentials()

        # Call TTS generation
        result = tts_main({
            "Text": text,
            "VoiceType": voice_type,
            "secret_id": secret_id,
            "secret_key": secret_key,
            "max_workers": 3,  # Concurrent processing
        })

        if result.get("Code") == 0:
            audio_file = result.get("AudioUrl", "")
            actual_duration = result.get("duration", estimated_minutes)
            
            # Read audio file and convert to base64
            with open(audio_file, "rb") as f:
                audio_bytes = f.read()
            audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")

            return ToolResponse(
                [
                    TextBlock(
                        type="text",
                        text=f"✅ Podcast generated successfully!\n"
                             f"📊 Text length: {len(text)} characters\n"
                             f"⏱️ Estimated duration: ~{actual_duration:.1f} minutes\n"
                             f"🎙️ Voice used: {voice}",
                    ),
                    AudioBlock(
                        type="audio",
                        source=Base64Source(
                            type="base64",
                            media_type="audio/wav",
                            data=audio_base64,
                        ),
                    ),
                ],
            )
        else:
            return ToolResponse(
                [
                    TextBlock(
                        type="text",
                        text=f"❌ Generation failed: {result.get('Msg', 'Unknown error')}",
                    ),
                ],
            )
    except Exception as e:
        return ToolResponse(
            [
                TextBlock(
                    type="text",
                    text=f"❌ Error: Failed to generate audio. {str(e)}",
                ),
            ],
        )


def tengxun_tts_list_voices() -> ToolResponse:
    """
    Get list of all supported voices from Tencent Cloud TTS.

    Returns:
        `ToolResponse`:
            Contains available voice names list (TextBlock)
    """
    voices = ", ".join(VOICE_TYPES.values())
    return ToolResponse(
        [
            TextBlock(
                type="text",
                text=f"Available voices: {voices}",
            ),
        ],
    )
