#!/usr/bin/env python3
"""
语音转文本脚本 - 基于 SiliconFlow API
支持模型：FunAudioLLM/SenseVoiceSmall, TeleAI/TeleSpeechASR
"""

import argparse
import os
import sys
import json

try:
    import requests
except ImportError:
    print("错误: 需要 requests 库，请运行: pip3 install requests", file=sys.stderr)
    sys.exit(1)

API_URL = "https://api.siliconflow.cn/v1/audio/transcriptions"
AVAILABLE_MODELS = ["FunAudioLLM/SenseVoiceSmall", "TeleAI/TeleSpeechASR"]
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB


def transcribe(audio_path: str, api_key: str, model: str = "FunAudioLLM/SenseVoiceSmall") -> dict:
    """
    转录音频文件为文本
    
    Args:
        audio_path: 音频文件路径
        api_key: SiliconFlow API Key
        model: 模型名称
    
    Returns:
        dict: {"success": bool, "text": str, "error": str}
    """
    # 检查文件是否存在
    if not os.path.exists(audio_path):
        return {"success": False, "error": f"文件不存在: {audio_path}"}
    
    # 检查文件大小
    file_size = os.path.getsize(audio_path)
    if file_size > MAX_FILE_SIZE:
        return {"success": False, "error": f"文件过大 ({file_size / 1024 / 1024:.1f}MB)，限制 50MB"}
    
    # 设置请求头
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    # 准备文件
    try:
        with open(audio_path, "rb") as f:
            files = {
                "file": (os.path.basename(audio_path), f)
            }
            data = {
                "model": model
            }
            
            print(f"正在转录: {audio_path}", file=sys.stderr)
            print(f"使用模型: {model}", file=sys.stderr)
            
            response = requests.post(API_URL, headers=headers, files=files, data=data, timeout=120)
            
            if response.status_code == 200:
                result = response.json()
                text = result.get("text", "")
                return {"success": True, "text": text}
            else:
                error_msg = f"API 错误 ({response.status_code}): {response.text}"
                return {"success": False, "error": error_msg}
                
    except requests.exceptions.Timeout:
        return {"success": False, "error": "请求超时 (120s)"}
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "网络连接失败"}
    except Exception as e:
        return {"success": False, "error": f"未知错误: {str(e)}"}


def main():
    parser = argparse.ArgumentParser(description="语音转文本 - SiliconFlow API")
    parser.add_argument("audio_file", help="音频文件路径")
    parser.add_argument("--model", "-m", choices=AVAILABLE_MODELS, default="FunAudioLLM/SenseVoiceSmall",
                       help="选择模型 (默认: FunAudioLLM/SenseVoiceSmall)")
    parser.add_argument("--api-key", "-k", help="SiliconFlow API Key (也可设置环境变量 SILICONFLOW_API_KEY)")
    parser.add_argument("--output", "-o", help="输出文件路径 (默认输出到 stdout)")
    parser.add_argument("--json", action="store_true", help="以 JSON 格式输出")
    
    args = parser.parse_args()
    
    # 获取 API Key
    api_key = args.api_key or os.environ.get("SILICONFLOW_API_KEY", "")
    if not api_key:
        print("错误: 请提供 API Key (--api-key) 或设置环境变量 SILICONFLOW_API_KEY", file=sys.stderr)
        sys.exit(1)
    
    # 执行转录
    result = transcribe(args.audio_file, api_key, args.model)
    
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif result["success"]:
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(result["text"])
            print(f"✅ 转录完成，已保存到: {args.output}", file=sys.stderr)
        else:
            print(result["text"])
    else:
        print(f"❌ {result['error']}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
