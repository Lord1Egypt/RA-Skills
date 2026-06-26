#!/usr/bin/env python3
"""
voice-clone - 语音合成与声音克隆工具
支持多种 TTS 引擎: Edge TTS, OpenAI TTS, ElevenLabs, Coqui TTS
"""

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Optional

# 缓存目录
CACHE_DIR = Path.home() / ".cache" / "voice-clone"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

# 可用的声音列表
VOICES = {
    # 中文声音
    "zh-xiaoxiao": {"name": "晓晓", "lang": "zh-CN", "engine": "edge"},
    "zh-xiaoyi": {"name": "晓伊", "lang": "zh-CN", "engine": "edge"},
    "zh-yunyang": {"name": "云扬", "lang": "zh-CN", "engine": "edge"},
    "zh-yunxi": {"name": "云希", "lang": "zh-CN", "engine": "edge"},
    # 英文声音
    "en-jenny": {"name": "Jenny", "lang": "en-US", "engine": "edge"},
    "en-aria": {"name": "Aria", "lang": "en-US", "engine": "edge"},
    "en-guy": {"name": "Guy", "lang": "en-US", "engine": "edge"},
    "en-sonia": {"name": "Sonia", "lang": "en-GB", "engine": "edge"},
    # OpenAI 声音
    "openai-alloy": {"name": "Alloy", "engine": "openai"},
    "openai-echo": {"name": "Echo", "engine": "openai"},
    "openai-fable": {"name": "Fable", "engine": "openai"},
    "openai-onyx": {"name": "Onyx", "engine": "openai"},
    "openai-shimmer": {"name": "Shimmer", "engine": "openai"},
    # ElevenLabs 预设
    "elevenRachel": {"name": "Rachel", "engine": "elevenlabs"},
    "elevenAdam": {"name": "Adam", "engine": "elevenlabs"},
}


async def edge_tts_speak(text: str, voice: str = "zh-CN-XiaoxiaoNeural", 
                          rate: str = "+0%", pitch: str = "+0Hz", 
                          output_file: Optional[str] = None) -> str:
    """使用 Edge TTS 进行语音合成"""
    try:
        import edge_tts
    except ImportError:
        print("错误: 请安装 edge-tts 库: pip install edge-tts")
        sys.exit(1)
    
    if output_file is None:
        output_file = str(CACHE_DIR / f"edge_{int(asyncio.get_event_loop().time())}.mp3")
    
    communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
    await communicate.save(output_file)
    return output_file


async def openai_tts_speak(text: str, voice: str = "alloy", 
                            model: str = "tts-1", output_file: Optional[str] = None) -> str:
    """使用 OpenAI TTS 进行语音合成"""
    try:
        from openai import OpenAI
    except ImportError:
        print("错误: 请安装 openai 库: pip install openai")
        sys.exit(1)
    
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("错误: 请设置 OPENAI_API_KEY 环境变量")
        sys.exit(1)
    
    if output_file is None:
        output_file = str(CACHE_DIR / f"openai_{int(asyncio.get_event_loop().time())}.mp3")
    
    client = OpenAI(api_key=api_key)
    response = client.audio.speech.create(
        model=model,
        voice=voice,
        input=text
    )
    
    response.stream_to_file(output_file)
    return output_file


async def elevenlabs_tts_speak(text: str, voice_id: str = "21m00Tcm4TlvDq8ikWAM",
                                output_file: Optional[str] = None) -> str:
    """使用 ElevenLabs 进行语音合成"""
    try:
        from elevenlabs import generate, save
    except ImportError:
        print("错误: 请安装 elevenlabs 库: pip install elevenlabs")
        sys.exit(1)
    
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        print("错误: 请设置 ELEVENLABS_API_KEY 环境变量")
        sys.exit(1)
    
    if output_file is None:
        output_file = str(CACHE_DIR / f"elevenlabs_{int(asyncio.get_event_loop().time())}.mp3")
    
    audio = generate(text=text, voice_id=voice_id, api_key=api_key)
    save(audio, output_file)
    return output_file


async def coqui_tts_speak(text: str, model: str = "tts_models/multilingual/multi-dataset/xtts_v2",
                          output_file: Optional[str] = None) -> str:
    """使用 Coqui TTS 进行语音合成"""
    try:
        from TTS.api import TTS
    except ImportError:
        print("错误: 请安装 TTS 库: pip install TTS")
        sys.exit(1)
    
    if output_file is None:
        output_file = str(CACHE_DIR / f"coqui_{int(asyncio.get_event_loop().time())}.wav")
    
    tts = TTS(model_path=model, gpu=False)
    tts.tts_to_file(text=text, file_path=output_file)
    return output_file


def list_voices():
    """列出所有可用的声音"""
    print("\n=== 可用的声音列表 ===\n")
    print("【中文声音 (Edge TTS)】")
    for voice_id, info in VOICES.items():
        if info.get("lang", "").startswith("zh"):
            print(f"  {voice_id}: {info['name']} ({info['lang']})")
    
    print("\n【英文声音 (Edge TTS)】")
    for voice_id, info in VOICES.items():
        if info.get("lang", "").startswith("en") and info.get("engine") == "edge":
            print(f"  {voice_id}: {info['name']} ({info['lang']})")
    
    print("\n【OpenAI 声音】")
    for voice_id, info in VOICES.items():
        if info.get("engine") == "openai":
            print(f"  {voice_id}: {info['name']}")
    
    print("\n【ElevenLabs 预设声音】")
    for voice_id, info in VOICES.items():
        if info.get("engine") == "elevenlabs":
            print(f"  {voice_id}: {info['name']}")
    
    print("\n使用示例:")
    print("  voice-clone -t '你好世界' -v zh-xiaoxiao")
    print("  voice-clone -t 'Hello world' -v en-jenny --engine edge")
    print("  voice-clone -t 'Hello' -v openai-alloy --engine openai")


async def main():
    parser = argparse.ArgumentParser(
        description="voice-clone - 语音合成与声音克隆工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  voice-clone -t "你好世界" -v zh-xiaoxiao
  voice-clone -t "Hello" -v en-jenny --engine openai
  voice-clone --list-voices

支持的声音类型:
  zh-xiaoxiao, zh-xiaoyi, zh-yunyang, zh-yunxi (中文)
  en-jenny, en-aria, en-guy, en-sonia (英文)
  openai-alloy, openai-echo, openai-fable, openai-onyx, openai-shimmer
  elevenRachel, elevenAdam
        """
    )
    
    parser.add_argument("-t", "--text", type=str, help="要转换的文本")
    parser.add_argument("-v", "--voice", type=str, default="zh-xiaoxiao", 
                        help="选择声音 (默认: zh-xiaoxiao)")
    parser.add_argument("-e", "--engine", type=str, default="edge", 
                        choices=["edge", "openai", "elevenlabs", "coqui"],
                        help="TTS 引擎 (默认: edge)")
    parser.add_argument("-r", "--rate", type=str, default="+0%", 
                        help="语速调整，如 +50%, -50% (仅 Edge TTS)")
    parser.add_argument("-p", "--pitch", type=str, default="+0Hz", 
                        help="音调调整，如 +5Hz, -5Hz (仅 Edge TTS)")
    parser.add_argument("-o", "--output", type=str, 
                        help="输出文件路径")
    parser.add_argument("--list-voices", action="store_true", 
                        help="列出所有可用的声音")
    parser.add_argument("--model", type=str, default="tts-1",
                        help="OpenAI TTS 模型 (默认: tts-1)")
    
    args = parser.parse_args()
    
    if args.list_voices:
        list_voices()
        return
    
    if not args.text:
        parser.print_help()
        print("\n错误: 请提供要转换的文本 (-t 或 --text)")
        sys.exit(1)
    
    print(f"正在使用 {args.engine} 引擎合成语音...")
    print(f"文本: {args.text[:50]}{'...' if len(args.text) > 50 else ''}")
    print(f"声音: {args.voice}")
    
    try:
        if args.engine == "edge":
            # 映射到 Edge TTS 声音名称
            edge_voices = {
                "zh-xiaoxiao": "zh-CN-XiaoxiaoNeural",
                "zh-xiaoyi": "zh-CN-XiaoyiNeural",
                "zh-yunyang": "zh-CN-YunyangNeural",
                "zh-yunxi": "zh-CN-YunxiNeural",
                "en-jenny": "en-US-JennyNeural",
                "en-aria": "en-US-AriaNeural",
                "en-guy": "en-US-GuyNeural",
                "en-sonia": "en-GB-SoniaNeural",
            }
            voice = edge_voices.get(args.voice, "zh-CN-XiaoxiaoNeural")
            output_file = await edge_tts_speak(args.text, voice, args.rate, args.pitch, args.output)
            
        elif args.engine == "openai":
            openai_voices = ["alloy", "echo", "fable", "onyx", "shimmer"]
            voice = args.voice.replace("openai-", "") if args.voice.startswith("openai-") else args.voice
            if voice not in openai_voices:
                voice = "alloy"
            output_file = await openai_tts_speak(args.text, voice, args.model, args.output)
            
        elif args.engine == "elevenlabs":
            voice_id = "21m00Tcm4TlvDq8ikWAM"  # 默认 Rachel
            if args.voice.startswith("eleven"):
                voice_id = {
                    "elevenRachel": "21m00Tcm4TlvDq8ikWAM",
                    "elevenAdam": "pNInz6obpgDQGcFmaJgB",
                }.get(args.voice, "21m00Tcm4TlvDq8ikWAM")
            output_file = await elevenlabs_tts_speak(args.text, voice_id, args.output)
            
        elif args.engine == "coqui":
            output_file = await coqui_tts_speak(args.text, output_file=args.output)
        
        print(f"\n✅ 语音合成成功!")
        print(f"📁 输出文件: {output_file}")
        
        # 尝试播放 (如果可用)
        try:
            os.system(f"xdg-open '{output_file}' >/dev/null 2>&1 &")
        except:
            pass
        
    except Exception as e:
        print(f"❌ 语音合成失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
