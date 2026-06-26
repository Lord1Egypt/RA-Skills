#!/usr/bin/env python3
"""
SenseAudio HTTP ASR 语音识别脚本
用法：python asr.py audio_file.mp3

依赖：只需要 requests 库
接口：https://senseaudio.cn/docs/speech_recognition/http_api
模型：sense-asr-deepthink（深度理解，智能纠错）
"""

import argparse
import json
import os
import sys
import requests

# 默认配置
DEFAULT_ASR_URL = "https://api.senseaudio.cn/v1/audio/transcriptions"
DEFAULT_ASR_MODEL = "sense-asr-deepthink"


def get_api_key():
    """从环境变量或 openclaw.json 获取 API Key"""
    api_key = os.environ.get("SENSE_API_KEY")
    if api_key:
        return api_key.strip()
    
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


def transcribe_audio(audio_file, model=DEFAULT_ASR_MODEL, language=None, translate_to=None):
    """
    使用 HTTP 接口进行语音识别
    
    API: POST https://api.senseaudio.cn/v1/audio/transcriptions
    Content-Type: multipart/form-data
    """
    api_key = get_api_key()
    if not api_key:
        print("❌ 错误：未找到 SENSE_API_KEY")
        return None
    
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    # 构建请求参数
    files = {
        "file": (os.path.basename(audio_file), open(audio_file, "rb"))
    }
    
    data = {
        "model": model,
        "response_format": "verbose_json"  # 获取详细信息
    }
    
    # 可选参数
    if language:
        data["language"] = language
    
    if translate_to:
        data["target_language"] = translate_to
    
    try:
        response = requests.post(DEFAULT_ASR_URL, headers=headers, files=files, data=data, timeout=120)
        response.raise_for_status()
        
        result = response.json()
        
        # 检查错误
        if "error" in result:
            error = result["error"]
            print(f"❌ API 错误：{error.get('message', '未知错误')}")
            return None
        
        return result
        
    except requests.exceptions.Timeout:
        print("❌ 识别超时")
        return None
    except FileNotFoundError:
        print(f"❌ 文件不存在：{audio_file}")
        return None
    except Exception as e:
        print(f"❌ 识别错误：{e}")
        return None
    finally:
        if "files" in locals():
            for f in files.values():
                try:
                    f[1].close()
                except:
                    pass


def format_result(result, verbose=False):
    """格式化识别结果"""
    if not result:
        return ""
    
    text = result.get("text", "")
    
    if verbose:
        print("\n=== 识别结果 ===")
        print(f"文本：{text}")
        
        duration = result.get("duration", 0)
        if duration:
            print(f"时长：{duration:.2f}秒")
        
        # 显示分段信息（如果有）
        segments = result.get("segments", [])
        if segments:
            print(f"\n分段 ({len(segments)}):")
            for seg in segments:
                start = seg.get("start", 0)
                end = seg.get("end", 0)
                seg_text = seg.get("text", "")
                speaker = seg.get("speaker", "")
                print(f"  [{start:.2f}s - {end:.2f}s] {speaker}: {seg_text}")
        
        # 显示翻译（如果有）
        if "translation" in result:
            print(f"\n翻译：{result['translation']}")
        
        print()
    else:
        print(text)
    
    return text


def main():
    parser = argparse.ArgumentParser(description="SenseAudio HTTP ASR 语音识别")
    parser.add_argument("audio_file", help="音频文件路径")
    parser.add_argument("--model", "-m", default=DEFAULT_ASR_MODEL,
                       choices=["sense-asr-lite", "sense-asr", "sense-asr-pro", "sense-asr-deepthink"],
                       help=f"识别模型 (默认：{DEFAULT_ASR_MODEL})")
    parser.add_argument("--language", "-l", help="音频语言代码 (如 zh/en/ja，留空自动检测)")
    parser.add_argument("--translate", "-t", help="翻译成目标语言代码 (如 en/zh)")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="显示详细信息（时长、分段等）")
    parser.add_argument("--output", "-o", help="输出到文件")
    
    args = parser.parse_args()
    
    # 执行识别
    result = transcribe_audio(args.audio_file, args.model, args.language, args.translate)
    
    if result:
        # 格式化输出
        text = format_result(result, args.verbose)
        
        # 输出到文件
        if args.output:
            try:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(text)
                print(f"✅ 结果已保存到：{args.output}")
            except Exception as e:
                print(f"❌ 保存失败：{e}")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
