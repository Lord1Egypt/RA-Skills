#!/usr/bin/env python3
"""
SenseAudio + Edge TTS 语音播放脚本
用法：python tts.py [--voice VOICE] [--engine ENGINE] [--lang LANG] [--play] [--output FILE] "文本内容"

依赖：只需要 requests 库（Edge TTS 可选）
接口：
  - SenseAudio: https://senseaudio.cn/docs/text_to_speech_api
  - Edge TTS: Microsoft Edge Service (无需 API Key)
"""

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import requests
from datetime import datetime

# 默认配置
DEFAULT_ENGINE = "auto"  # auto/senseaudio/edge
DEFAULT_LANG = "auto"    # auto/zh/en/ja
DEFAULT_TTS_URL = "https://api.senseaudio.cn/v1/t2a_v2"
DEFAULT_TTS_MODEL = "SenseAudio-TTS-1.0"
DEFAULT_TTS_FORMAT = "wav"  # WAV 格式，系统兼容性好，无需额外解码器
DEFAULT_TTS_SAMPLE_RATE = 32000

# Edge TTS 默认声音
EDGE_VOICES = {
    "en": "en-US-JennyNeural",      # 英语女声（默认）
    "en-US-GuyNeural": "en-US-GuyNeural",   # 英语男声
    "en-US-AriaNeural": "en-US-AriaNeural", # 英语女声
    "ja": "ja-JP-NanamiNeural",     # 日语女声（默认）
    "ja-JP-KeitaNeural": "ja-JP-KeitaNeural", # 日语男声
}

# 音频文件存储目录（工作区目录）
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# skills/senseaudio-voice/scripts -> skills -> 工作区根目录
BASE_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..", ".."))
AUDIO_DIR = os.path.join(BASE_DIR, "audio")

# 确保音频目录存在
os.makedirs(AUDIO_DIR, exist_ok=True)


def detect_language(text):
    """
    检测文本的主要语言
    
    返回：'zh' (中文), 'ja' (日语), 'en' (英语/拉丁字母), 'unknown'
    """
    if not text:
        return "unknown"
    
    # 统计各类字符数量
    chinese_chars = 0
    japanese_chars = 0  # 假名
    latin_chars = 0
    total_chars = 0
    
    for char in text:
        code = ord(char)
        total_chars += 1
        
        # 中文字符 (CJK Unified Ideographs)
        if 0x4E00 <= code <= 0x9FFF:
            chinese_chars += 1
        # 日文假名 (Hiragana + Katakana)
        elif 0x3040 <= code <= 0x30FF:
            japanese_chars += 1
        # 拉丁字母
        elif 0x0041 <= code <= 0x007A:
            latin_chars += 1
    
    # 判断主要语言
    if total_chars == 0:
        return "unknown"
    
    # 优先判断日语（假名是日语的特征）
    if japanese_chars > 0 and japanese_chars >= chinese_chars:
        return "ja"
    
    # 判断中文
    if chinese_chars > 0 and chinese_chars >= latin_chars:
        return "zh"
    
    # 默认英语/拉丁字母
    if latin_chars > 0:
        return "en"
    
    return "unknown"


def select_engine(lang, force_engine=None):
    """
    根据语言选择合适的 TTS 引擎
    
    Args:
        lang: 检测到的语言 (zh/en/ja/unknown)
        force_engine: 强制指定的引擎 (None/auto/senseaudio/edge)
    
    Returns:
        engine: 'senseaudio' 或 'edge'
        reason: 选择原因
    """
    if force_engine and force_engine != "auto":
        return force_engine, f"用户强制指定 {force_engine}"
    
    # 自动选择逻辑
    if lang == "zh":
        return "senseaudio", "中文使用 SenseAudio（大陆用户免费）"
    elif lang == "ja":
        return "edge", "日语使用 Edge TTS（海外友好，无需认证）"
    elif lang == "en":
        return "edge", "英语使用 Edge TTS（海外友好，无需认证）"
    else:
        # 未知语言，默认 Edge TTS
        return "edge", "未知语言，默认使用 Edge TTS"


def get_default_voice(lang, engine):
    """
    根据语言和引擎获取默认声音
    
    Args:
        lang: 语言 (zh/en/ja)
        engine: 引擎 (senseaudio/edge)
    
    Returns:
        默认声音 ID
    """
    if engine == "senseaudio":
        return "child_0001_a"  # 童声，适合学习场景
    elif engine == "edge":
        if lang == "ja":
            return "ja-JP-NanamiNeural"
        else:
            return "en-US-JennyNeural"
    return "child_0001_a"


def detect_available_players():
    """
    检测当前系统可用的音频播放器
    
    返回：按优先级排序的可用播放器列表
    """
    import shutil
    
    # 播放器配置：(命令列表，描述，支持格式)
    player_configs = [
        (["aplay", "-q"], "ALSA (WAV 原生支持)", ["wav"]),
        (["paplay"], "PulseAudio", ["wav", "mp3", "flac", "ogg"]),
        (["ffplay", "-nodisp", "-autoexit", "-loglevel", "error"], "FFmpeg", ["wav", "mp3", "flac", "ogg", "m4a"]),
        (["mpv", "--no-video", "--really-quiet"], "MPV", ["wav", "mp3", "flac", "ogg", "m4a"]),
        (["play"], "SoX", ["wav", "mp3", "flac", "ogg"]),
    ]
    
    available_players = []
    
    for cmd, name, formats in player_configs:
        exe = cmd[0]
        if shutil.which(exe):
            available_players.append({
                "cmd": cmd,
                "name": name,
                "exe": exe,
                "formats": formats
            })
    
    return available_players


# 全局变量：缓存可用的播放器
AVAILABLE_PLAYERS = None


def get_available_players(audio_format="wav"):
    """
    获取可用的播放器列表（支持指定音频格式）
    
    Args:
        audio_format: 音频格式 (wav, mp3, etc.)
    
    Returns:
        可用的播放器列表
    """
    global AVAILABLE_PLAYERS
    
    if AVAILABLE_PLAYERS is None:
        AVAILABLE_PLAYERS = detect_available_players()
    
    # 过滤支持指定格式的播放器
    if audio_format:
        return [p for p in AVAILABLE_PLAYERS if audio_format in p["formats"]]
    return AVAILABLE_PLAYERS


def get_api_key():
    """从环境变量或 openclaw.json 获取 API Key"""
    # 优先使用环境变量
    api_key = os.environ.get("SENSE_API_KEY")
    if api_key:
        return api_key.strip()
    
    # 尝试从 openclaw.json 读取
    config_paths = [
        os.path.expanduser("~/.openclaw/openclaw.json"),
        os.path.expanduser("~/.openclaw/agents/kids-study/openclaw.json"),
    ]
    
    for config_path in config_paths:
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                api_key = config.get("env", {}).get("SENSE_API_KEY", "")
                if api_key:
                    return api_key.strip()
        except:
            continue
    
    return ""


def synthesize_edge_tts(text, voice_id, output_file, speed=1.0, timeout=60):
    """
    使用 Edge TTS 生成语音文件
    
    依赖：edge-tts 库（可选，如未安装则尝试 HTTP 调用）
    """
    # 尝试使用 edge-tts 库
    try:
        import edge_tts
        import asyncio
        
        async def generate():
            communicate = edge_tts.Communicate(text, voice_id)
            await communicate.save(output_file)
        
        asyncio.run(generate())
        print(f"   使用引擎：Edge TTS (edge-tts 库)")
        return True
        
    except ImportError:
        # edge-tts 库未安装，尝试 HTTP 调用
        print("⚠️  edge-tts 库未安装，尝试使用 HTTP 接口...")
        print("   建议安装：pip install edge-tts")
        
        # 简单的 HTTP 调用（备用方案）
        # 注意：Edge TTS 没有官方公开 API，这里仅作为降级方案
        print("❌ Edge TTS HTTP 接口不可用，请安装 edge-tts 库")
        return False
        
    except Exception as e:
        print(f"❌ Edge TTS 错误：{e}")
        return False


def synthesize_tts(text, voice_id, output_file, speed=1.0, volume=1.0, audio_format="wav", timeout=60, engine="senseaudio"):
    """
    使用 HTTP 接口生成语音文件
    
    Args:
        engine: 'senseaudio' 或 'edge'
    
    API: 
      - SenseAudio: POST https://api.senseaudio.cn/v1/t2a_v2
      - Edge TTS: edge-tts 库
    """
    if engine == "edge":
        return synthesize_edge_tts(text, voice_id, output_file, speed, timeout)
    
    # SenseAudio 引擎
    api_key = get_api_key()
    if not api_key:
        print("❌ 错误：未找到 SENSE_API_KEY")
        print("   请在 openclaw.json 的 env 中配置，或设置环境变量")
        return False
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # 构建请求体（HTTP 接口）
    payload = {
        "model": DEFAULT_TTS_MODEL,
        "text": text,
        "stream": False,  # HTTP 非流式，直接返回完整结果
        "voice_setting": {
            "voice_id": voice_id,
            "speed": speed,
            "vol": volume
        },
        "audio_setting": {
            "format": audio_format,
            "sample_rate": DEFAULT_TTS_SAMPLE_RATE
        }
    }
    
    try:
        response = requests.post(DEFAULT_TTS_URL, headers=headers, json=payload, timeout=timeout)
        response.raise_for_status()
        
        data = response.json()
        
        # 检查错误
        base_resp = data.get("base_resp", {})
        status_code = base_resp.get("status_code", 0)
        if status_code != 0:
            status_msg = base_resp.get("status_msg", "未知错误")
            print(f"❌ API 错误 ({status_code}): {status_msg}")
            return False
        
        # 提取 hex 音频数据并解码
        audio_hex = data.get("data", {}).get("audio", "")
        if not audio_hex:
            print("❌ 没有音频数据")
            return False
        
        # hex 解码为二进制
        audio_bytes = bytes.fromhex(audio_hex)
        
        # 写入文件并确保刷新到磁盘
        with open(output_file, 'wb') as f:
            f.write(audio_bytes)
            f.flush()
            os.fsync(f.fileno())  # 强制写入磁盘
        
        # 短暂延迟确保文件系统完成写入
        import time
        time.sleep(0.1)
        
        # 显示音频信息
        extra = data.get("extra_info", {})
        duration_ms = extra.get("audio_length", 0)
        if duration_ms:
            print(f"   时长：约 {duration_ms}ms")
        
        return True
        
    except requests.exceptions.Timeout:
        print("❌ 生成超时")
        return False
    except requests.exceptions.RequestException as e:
        print(f"❌ 网络错误：{e}")
        return False
    except Exception as e:
        print(f"❌ 生成错误：{e}")
        return False


def play_audio(file_path, audio_format=None):
    """
    播放音频文件，带完整的异常处理
    
    流程：
    1. 验证文件
    2. 检测系统可用的播放器
    3. 按优先级尝试播放
    4. 记录详细的错误日志
    
    Args:
        file_path: 音频文件路径
        audio_format: 音频格式 (wav, mp3 等)，自动从文件扩展名推断
    
    Returns:
        bool: 播放是否成功
    """
    # 自动推断音频格式
    if audio_format is None:
        audio_format = os.path.splitext(file_path)[1].lower().lstrip('.')
    
    # 验证文件是否存在
    if not os.path.exists(file_path):
        print(f"❌ 播放失败：文件不存在")
        print(f"   路径：{file_path}")
        return False
    
    # 验证文件大小
    try:
        file_size = os.path.getsize(file_path)
    except OSError as e:
        print(f"❌ 播放失败：无法读取文件")
        print(f"   错误：{e}")
        return False
    
    if file_size < 1000:  # 音频文件至少应该有几 KB
        print(f"⚠️  文件太小 ({file_size} bytes)，可能已损坏")
        return False
    
    # 获取可用的播放器（按优先级排序）
    players = get_available_players(audio_format)
    
    if not players:
        print(f"❌ 播放失败：未找到支持 .{audio_format} 格式的播放器")
        print(f"   建议安装：sudo apt-get install alsa-utils 或 sudo apt-get install ffmpeg")
        print(f"   文件已保存：{file_path}")
        return False
    
    failed_attempts = []
    
    # 按优先级尝试每个播放器
    for player in players:
        player_cmd = player["cmd"] + [file_path]
        player_name = player["name"]
        player_exe = player["exe"]
        
        try:
            result = subprocess.run(
                player_cmd,
                capture_output=True,
                timeout=60
            )
            
            if result.returncode == 0:
                # 播放成功
                if failed_attempts:
                    print(f"   (已尝试：{', '.join([f['name'] for f in failed_attempts])})")
                return True
            else:
                # 播放失败，分析错误原因
                stderr = result.stderr.decode('utf-8', errors='ignore') if result.stderr else ""
                error_msg = stderr.split('\n')[0].strip() if stderr else "未知错误"
                
                # 判断是否是致命错误
                is_fatal = False
                if "Invalid data" in stderr or "corrupt" in stderr.lower():
                    print(f"⚠️  {player_name}: 文件格式可能损坏")
                    is_fatal = True
                elif "No such file" in stderr or "cannot open" in stderr.lower():
                    print(f"⚠️  {player_name}: 文件无法访问")
                    is_fatal = True
                
                failed_attempts.append({
                    "name": player_name,
                    "error": error_msg[:60],
                    "fatal": is_fatal
                })
                
                # 如果是致命错误，不再尝试
                if is_fatal:
                    break
                    
        except subprocess.TimeoutExpired:
            failed_attempts.append({"name": player_name, "error": "播放超时", "fatal": False})
            continue
        except FileNotFoundError:
            # 理论上不会发生，因为已经检查过 shutil.which
            failed_attempts.append({"name": player_name, "error": "播放器未找到", "fatal": False})
            continue
        except Exception as e:
            failed_attempts.append({"name": player_name, "error": str(e), "fatal": False})
            continue
    
    # 所有播放器都失败
    print(f"❌ 播放失败")
    print(f"   已尝试 {len(failed_attempts)} 个播放器:")
    for attempt in failed_attempts:
        status = "⚠️" if attempt["fatal"] else "   "
        print(f"   {status} {attempt['name']}: {attempt['error']}")
    print(f"   文件已保存：{file_path}")
    
    # 给出建议
    if len(failed_attempts) > 0:
        last_error = failed_attempts[-1]["error"].lower()
        if "permission" in last_error:
            print(f"   💡 提示：检查文件权限或使用 sudo")
        elif "device" in last_error or "audio" in last_error:
            print(f"   💡 提示：检查音频输出设备是否连接")
        else:
            print(f"   💡 提示：可尝试手动播放：aplay {file_path}")
    
    return False


def list_voices():
    """列出可用的语音"""
    print("\n🎤 可用的语音:")
    print("=" * 70)
    
    print("\n【SenseAudio - 中文】(需要大陆手机号 + 身份认证)")
    print("-" * 70)
    print(f"{'声音 ID':<20} {'性别':<6} {'描述'}")
    print("-" * 70)
    print(f"{'child_0001_a':<20} 童声  ✅ 默认，亲切活泼，适合学习场景")
    print(f"{'male_0004_a':<20} 男    温暖男声")
    print(f"{'male_0001_a':<20} 男    成熟男声")
    print(f"{'female_0001_a':<20} 女    温柔女声")
    print(f"{'female_0002_a':<20} 女    活泼女声")
    
    print("\n【Edge TTS - 英语/日语】(海外友好，无需认证)")
    print("-" * 70)
    print(f"{'声音 ID':<25} {'语言':<8} {'描述'}")
    print("-" * 70)
    print(f"{'en-US-JennyNeural':<25} 英语    女声，清晰友好（默认）")
    print(f"{'en-US-GuyNeural':<25} 英语    男声，温暖专业")
    print(f"{'en-US-AriaNeural':<25} 英语    女声，活泼自然")
    print(f"{'ja-JP-NanamiNeural':<25} 日语    女声，温柔清晰（默认）")
    print(f"{'ja-JP-KeitaNeural':<25} 日语    男声，成熟稳重")
    
    print("\n" + "=" * 70)
    print("\n💡 使用建议:")
    print("   - 中文内容：使用 SenseAudio（配置 SENSE_API_KEY）")
    print("   - 英语/日语：使用 Edge TTS（无需 API Key）")
    print("   - 自动模式：--lang auto（默认，根据文本自动选择）")
    print("\n使用示例:")
    print("  python tts.py --play \"宝贝，该写作业啦\"           # 中文，自动用 SenseAudio")
    print("  python tts.py --play \"Hello! How are you?\"      # 英语，自动用 Edge TTS")
    print("  python tts.py --play \"こんにちは\"               # 日语，自动用 Edge TTS")
    print("  python tts.py --engine edge --voice en-US-GuyNeural --play \"Hello\"")


def check_players():
    """检查系统音频播放器状态"""
    print("\n🔊 系统音频播放器检测")
    print("=" * 60)
    
    players = detect_available_players()
    
    if not players:
        print("❌ 未找到可用的音频播放器")
        print("\n💡 建议安装以下播放器之一:")
        print("   sudo apt-get install alsa-utils    # aplay (推荐，支持 WAV)")
        print("   sudo apt-get install pulseaudio    # paplay")
        print("   sudo apt-get install ffmpeg        # ffplay (支持多种格式)")
        return
    
    print(f"✅ 找到 {len(players)} 个可用播放器:\n")
    
    for i, player in enumerate(players, 1):
        print(f"{i}. {player['name']}")
        print(f"   命令：{' '.join(player['cmd'])}")
        print(f"   支持格式：{', '.join(player['formats'])}")
        print()
    
    # 推荐最佳播放器
    print("💡 推荐:")
    wav_players = [p for p in players if "wav" in p["formats"]]
    if wav_players:
        print(f"   播放 WAV: {wav_players[0]['name']} (优先级最高)")
    
    mp3_players = [p for p in players if "mp3" in p["formats"]]
    if mp3_players:
        print(f"   播放 MP3: {mp3_players[0]['name']}")
    else:
        print(f"   播放 MP3: ⚠️  需要安装 ffmpeg 或 pulseaudio")


def main():
    parser = argparse.ArgumentParser(description="SenseAudio + Edge TTS 语音播放")
    parser.add_argument("text", nargs="?", help="要转换的文本")
    parser.add_argument("--voice", "-v", default=None,
                       help="语音 ID (默认：根据语言自动选择)")
    parser.add_argument("--output", "-o", help="输出文件路径")
    parser.add_argument("--play", "-p", action="store_true", default=True,
                       help="生成后自动播放 (默认：开启)")
    parser.add_argument("--no-play", action="store_true",
                       help="不自动播放")
    parser.add_argument("--list", "-l", action="store_true",
                       help="列出可用的语音")
    parser.add_argument("--speed", type=float, default=1.0,
                       help="语速 0.5-2.0 (默认：1.0)")
    parser.add_argument("--volume", type=float, default=1.0,
                       help="音量 0-10 (默认：1.0)")
    parser.add_argument("--format", "-f", default=DEFAULT_TTS_FORMAT,
                       choices=["wav", "mp3"],
                       help=f"音频格式 (默认：{DEFAULT_TTS_FORMAT})")
    parser.add_argument("--check-players", action="store_true",
                       help="检查系统可用的音频播放器")
    parser.add_argument("--engine", "-e", default=DEFAULT_ENGINE,
                       choices=["auto", "senseaudio", "edge"],
                       help=f"引擎选择 (默认：{DEFAULT_ENGINE})")
    parser.add_argument("--lang", "-L", default=DEFAULT_LANG,
                       choices=["auto", "zh", "en", "ja"],
                       help=f"语言选择 (默认：{DEFAULT_LANG})")
    
    args = parser.parse_args()
    
    # 检查播放器
    if args.check_players:
        check_players()
        return
    
    # 列出语音
    if args.list:
        list_voices()
        return
    
    # 检查文本
    if not args.text:
        parser.print_help()
        print("\n❌ 错误：请提供要转换的文本")
        sys.exit(1)
    
    # 语言检测
    if args.lang == "auto":
        detected_lang = detect_language(args.text)
        print(f"🔍 检测到语言：{detected_lang}")
    else:
        detected_lang = args.lang
    
    # 选择引擎
    engine, reason = select_engine(detected_lang, args.engine)
    print(f"🎯 选择引擎：{engine} ({reason})")
    
    # 选择默认声音（如果用户未指定）
    voice_id = args.voice if args.voice else get_default_voice(detected_lang, engine)
    if not args.voice:
        print(f"🎤 使用默认声音：{voice_id}")
    
    # 生成输出文件路径
    if args.output:
        output_file = args.output
    else:
        # 使用工作区 audio 目录，按日期分类
        date_str = datetime.now().strftime("%Y-%m-%d")
        date_dir = os.path.join(AUDIO_DIR, date_str)
        os.makedirs(date_dir, exist_ok=True)
        
        # 生成文件名：时间戳_引擎_语音 ID_文本前缀.format
        timestamp = datetime.now().strftime("%H%M%S")
        engine_short = engine[:4]
        voice_short = voice_id.replace("_", "")[:12]
        text_preview = args.text[:20].strip()[:10] if args.text else "tts"
        # 清理文件名中的非法字符
        safe_text = "".join(c for c in text_preview if c.isalnum() or c in "，。,.")
        ext = args.format if args.format else DEFAULT_TTS_FORMAT
        filename = f"{timestamp}_{engine_short}_{voice_short}_{safe_text}.{ext}"
        output_file = os.path.join(date_dir, filename)
    
    # 生成语音
    text_preview = args.text[:50] + ('...' if len(args.text) > 50 else '')
    print(f"🔊 生成语音：{text_preview}")
    print(f"   使用声音：{voice_id}")
    if args.speed != 1.0:
        print(f"   语速：{args.speed}")
    if args.volume != 1.0:
        print(f"   音量：{args.volume}")
    print(f"   格式：{args.format}")
    print(f"   引擎：{engine}")
    
    if synthesize_tts(args.text, voice_id, output_file, args.speed, args.volume, args.format, engine=engine):
        # 显示相对路径（更简洁）
        try:
            rel_path = os.path.relpath(output_file, BASE_DIR)
        except:
            rel_path = output_file
        print(f"✅ 生成成功：{rel_path}")
        
        # 播放
        if not args.no_play and args.play:
            print("🔊 正在播放...")
            play_audio(output_file)
            print("✅ 播放完成")
    else:
        print("❌ 生成失败")
        sys.exit(1)


if __name__ == "__main__":
    main()
