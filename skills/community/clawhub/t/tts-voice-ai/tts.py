#!/usr/bin/env python3
"""
AI TTS - 语音合成工具
支持国内版和国际版 API，自动音色匹配
"""

import os
import sys
import json
import argparse
import requests
from pathlib import Path

# API 端点
API_CN_BASE = "https://api.minimaxi.com"
API_INT_BASE = "https://api.minimax.io"

DEFAULT_MODEL = "speech-2.8-turbo"

# 支持的语言增强选项
LANGUAGE_BOOST_OPTIONS = [
    "Chinese", "Chinese,Yue", "English", "Arabic", "Russian", "Spanish",
    "French", "Portuguese", "German", "Turkish", "Dutch", "Ukrainian",
    "Vietnamese", "Indonesian", "Japanese", "Italian", "Korean", "Thai",
    "Polish", "Romanian", "Greek", "Czech", "Finnish", "Hindi", "Bulgarian",
    "Danish", "Hebrew", "Malay", "Persian", "Slovak", "Swedish", "Croatian",
    "Filipino", "Hungarian", "Norwegian", "Slovenian", "Catalan", "Nynorsk",
    "Tamil", "Afrikaans", "auto"
]

# 语言到 language_boost 的映射
LANGUAGE_BOOST_MAP = {
    "chinese": "Chinese",
    "cantonese": "Chinese,Yue",
    "yue": "Chinese,Yue",
    "english": "English",
    "japanese": "Japanese",
    "korean": "Korean",
    "taiwan": "Chinese",
}

# 黄金音色表
GOLDEN_VOICES = {
    # 中文
    "chinese_female_gentle": "girlfriend_5_speech02_01",
    "chinese_female_playful": "girlfriend_1_speech02_01",
    "chinese_female_energetic": "ttv-voice-2026011810595326-hxYkopxR",
    "chinese_male": "ttv-voice-2026011806464526-IPLmlZ8C",
    "chinese_male_humorous": "ttv-voice-2026011910402426-5fSKtVmM",
    
    # 英文
    "english_female": "english_voice_agent_ivc_female_nora",
    "english_male": "english_voice_agent_ivc_male_julian",
    "english_female_maya": "english_voice_agent_ivc_female_maya",
    
    # 粤语
    "cantonese_female": "HK_Cantonese_female1",
    "cantonese_male": "Cantonese_ProfessionalHost（M)",
    
    # 台湾
    "taiwan": "vc_wanwan_0303_01",
    
    # 日语
    "japanese_female": "Japanese_DecisivePrincess",
    "japanese_male": "Japanese_IntellectualSenior",
    
    # 韩语
    "korean_female": "Korean_SweetGirl",
    "korean_male": "Korean_StrictBoss",
}

# 音色匹配表
VOICE_MAPPING = {
    ("chinese", "female", "young", "gentle"): "girlfriend_5_speech02_01",
    ("chinese", "female", "young", "playful"): "girlfriend_1_speech02_01",
    ("chinese", "female", "young", "energetic"): "ttv-voice-2026011810595326-hxYkopxR",
    ("chinese", "female", "young"): "girlfriend_1_speech02_01",
    ("chinese", "female", "middle"): "ttv-voice-2026011805455726-GZEh2lxO",
    ("chinese", "female", "elder"): "ttv-voice-2026011803190026-eQrDK9f4",
    ("chinese", "female"): "girlfriend_5_speech02_01",
    
    ("chinese", "male", "young", "energetic"): "ttv-voice-2026011806464526-IPLmlZ8C",
    ("chinese", "male", "middle", "humorous"): "ttv-voice-2026011910402426-5fSKtVmM",
    ("chinese", "male", "middle"): "ttv-voice-2026011809355426-eOpoATJe",
    ("chinese", "male", "elder"): "ttv-voice-2026011913000426-5s6vR4kU",
    ("chinese", "male"): "ttv-voice-2026011806464526-IPLmlZ8C",
    
    # 粤语
    ("cantonese", "female"): "HK_Cantonese_female1",
    ("cantonese", "male"): "Cantonese_ProfessionalHost（M)",
    
    ("english", "female"): "english_voice_agent_ivc_female_nora",
    ("english", "female", "young"): "english_voice_agent_ivc_female_maya",
    ("english", "male"): "english_voice_agent_ivc_male_julian",
    ("english", "male", "young"): "english_voice_agent_ivc_male_leo",
    
    ("taiwan",): "vc_wanwan_0303_01",
    
    ("japanese", "female"): "Japanese_DecisivePrincess",
    ("japanese", "male"): "Japanese_IntellectualSenior",
    
    ("korean", "female"): "Korean_SweetGirl",
    ("korean", "male"): "Korean_StrictBoss",
}

DEFAULT_VOICES = {
    "cn": "girlfriend_5_speech02_01",
    "int": "english_voice_agent_ivc_female_nora",
}


def get_api_endpoints(api_version: str) -> tuple:
    """获取 API 端点"""
    if api_version == "cn":
        return (f"{API_CN_BASE}/v1/t2a_v2", f"{API_CN_BASE}/v1/get_voice")
    return (f"{API_INT_BASE}/v1/t2a_v2", f"{API_INT_BASE}/v1/get_voice")


def get_api_key() -> str:
    key = os.environ.get("MINIMAX_API_KEY")
    if not key:
        print("Error: MINIMAX_API_KEY not set", file=sys.stderr)
        print("Run: export MINIMAX_API_KEY='your-key'", file=sys.stderr)
        sys.exit(1)
    return key


def detect_language(text: str) -> str:
    # 日语
    if any('\u3040' <= c <= '\u309F' or '\u30A0' <= c <= '\u30FF' for c in text):
        return "japanese"
    # 韩语
    if any('\uAC00' <= c <= '\uD7AF' for c in text):
        return "korean"
    # 粤语特征
    cantonese_words = ["吖", "咁", "唔", "叻", "睇", "屋企", "佢", "咩", "嘢"]
    if any(w in text for w in cantonese_words):
        return "cantonese"
    # 中文/英文检测
    chinese_chars = sum(1 for c in text if '\u4E00' <= c <= '\u9FFF')
    english_words = len([w for w in text.split() if w.isascii()])
    
    if chinese_chars > english_words * 2:
        return "chinese"
    elif english_words > chinese_chars * 2:
        return "english"
    return "chinese"


def get_language_boost(language: str) -> str:
    """获取 language_boost 值"""
    return LANGUAGE_BOOST_MAP.get(language, "auto")


def select_voice(language: str = None, gender: str = None, age: str = None, style: str = None, api_version: str = "cn") -> str:
    if language or gender or age or style:
        params = []
        if language: params.append(language.lower())
        if gender: params.append(gender.lower())
        if age: params.append(age.lower())
        if style: params.append(style.lower())
        
        key = tuple(params)
        if key in VOICE_MAPPING:
            return VOICE_MAPPING[key]
        
        for i in range(len(params), 0, -1):
            partial_key = tuple(params[:i])
            for k, v in VOICE_MAPPING.items():
                if k[:len(partial_key)] == partial_key:
                    return v
    
    if language:
        lang_key = f"{language}_female"
        if gender:
            lang_key = f"{language}_{gender}"
        if lang_key in GOLDEN_VOICES:
            return GOLDEN_VOICES[lang_key]
    
    return DEFAULT_VOICES.get(api_version, "girlfriend_5_speech02_01")


def get_voice_list(api_key: str, api_version: str):
    _, voice_url = get_api_endpoints(api_version)
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {"voice_type": "all"}
    
    try:
        resp = requests.post(voice_url, headers=headers, json=data, timeout=30)
        resp.raise_for_status()
        result = resp.json()
        
        print(f"\n=== Voice List (API: {api_version}) ===\n")
        
        if "system_voice" in result and result["system_voice"]:
            print("--- System Voices ---")
            for v in result["system_voice"]:
                print(f"  {v.get('voice_id')}: {v.get('voice_name')}")
        
        if "voice_cloning" in result and result["voice_cloning"]:
            print(f"\n--- Cloned Voices ({len(result['voice_cloning'])}) ---")
            for v in result["voice_cloning"][:10]:
                print(f"  {v.get('voice_id')}")
                
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def text_to_speech(text: str, api_key: str, api_version: str = "cn",
                   model: str = DEFAULT_MODEL, voice: str = None, 
                   language: str = None, gender: str = None, age: str = None, style: str = None,
                   language_boost: str = None,
                   speed: float = 1.0, format: str = "mp3", output_file: str = None):
    
    tts_url, _ = get_api_endpoints(api_version)
    
    # 自动选择音色和语言增强
    if voice is None:
        if language is None:
            language = detect_language(text)
        voice = select_voice(language, gender, age, style, api_version)
        print(f"Auto-selected voice: {voice} (language: {language})", file=sys.stderr)
    
    # 自动设置 language_boost
    if language_boost is None and language:
        language_boost = get_language_boost(language)
        print(f"Language boost: {language_boost}", file=sys.stderr)
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # 构建 payload
    payload = {
        "model": model,
        "text": text,
        "stream": False,
    }
    
    # 添加 language_boost
    if language_boost:
        payload["language_boost"] = language_boost
    
    payload["voice_setting"] = {
        "voice_id": voice,
        "speed": speed,
        "vol": 1,
        "pitch": 0
    }
    
    payload["audio_setting"] = {
        "format": format,
        "sample_rate": 32000,
        "bitrate": 128000,
        "channel": 1
    }
    
    try:
        print(f"Generating speech...", file=sys.stderr)
        resp = requests.post(tts_url, headers=headers, json=payload, timeout=60)
        resp.raise_for_status()
        result = resp.json()
        
        if result.get("base_resp", {}).get("status_code") != 0:
            error_msg = result.get("base_resp", {}).get("status_msg", "Unknown error")
            print(f"API Error: {error_msg}", file=sys.stderr)
            sys.exit(1)
        
        audio_data = result.get("data", {}).get("audio")
        if not audio_data:
            print("Error: No audio data", file=sys.stderr)
            sys.exit(1)
        
        audio_bytes = bytes.fromhex(audio_data)
        
        if not output_file:
            output_file = f"tts_output.{format}"
        
        with open(output_file, "wb") as f:
            f.write(audio_bytes)
        
        extra = result.get("extra_info", {})
        duration_ms = extra.get("audio_length", 0)
        duration_sec = duration_ms / 1000 if duration_ms else 0
        
        print(f"✅ Saved to: {output_file}", file=sys.stderr)
        print(f"   Duration: {duration_sec:.2f}s", file=sys.stderr)
        print(f"   Voice: {voice}", file=sys.stderr)
        if language_boost:
            print(f"   Language boost: {language_boost}", file=sys.stderr)
        
        return output_file
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="AI TTS - Text to Speech")
    parser.add_argument("text", nargs="?", help="Text to convert to speech")
    parser.add_argument("--list-voices", action="store_true", help="List all available voices")
    parser.add_argument("--model", "-m", default=DEFAULT_MODEL, help="Model")
    parser.add_argument("--voice", "-v", default=None, help="Voice ID")
    parser.add_argument("--language", "-l", default=None,
                       choices=["chinese", "english", "japanese", "korean", "cantonese", "taiwan"],
                       help="Language")
    parser.add_argument("--gender", "-g", default=None, choices=["male", "female"], help="Gender")
    parser.add_argument("--age", default=None, choices=["young", "middle", "elder", "child"], help="Age")
    parser.add_argument("--style", "-s", default=None,
                       choices=["gentle", "energetic", "serious", "playful", "professional"], help="Style")
    parser.add_argument("--language-boost", "-b", default=None,
                       choices=LANGUAGE_BOOST_OPTIONS,
                       help="Language boost for dialect/specialty (e.g., Chinese,Yue for Cantonese)")
    parser.add_argument("--speed", type=float, default=1.0, help="Speed (0.5-2.0)")
    parser.add_argument("--format", "-f", default="mp3", help="Audio format")
    parser.add_argument("--output", "-o", help="Output file")
    parser.add_argument("--api", choices=["cn", "int"], default="cn", help="API version (cn: api.minimaxi.com, int: api.minimax.io)")
    
    args = parser.parse_args()
    
    api_key = get_api_key()
    api_version = args.api
    
    if args.list_voices:
        get_voice_list(api_key, api_version)
        return
    
    if not args.text:
        parser.print_help()
        print("\nExamples:")
        print(f"  {sys.argv[0]} \"Hello world\"")
        print(f"  {sys.argv[0]} \"你好\" --language chinese --style gentle")
        print(f"  {sys.argv[0]} \"喂\" --language cantonese --language-boost Chinese,Yue")
        print(f"  {sys.argv[0]} --list-voices")
        sys.exit(1)
    
    output_file = text_to_speech(
        text=args.text,
        api_key=api_key,
        api_version=api_version,
        model=args.model,
        voice=args.voice,
        language=args.language,
        gender=args.gender,
        age=args.age,
        style=args.style,
        language_boost=args.language_boost,
        speed=args.speed,
        format=args.format,
        output_file=args.output
    )
    
    print(output_file)


if __name__ == "__main__":
    main()
