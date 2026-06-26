#!/usr/bin/env python3
"""
百炼 TTS 语音合成工具
支持音色选择、文件输出
"""

import os
import sys
import argparse
import dashscope
import requests

# 音色列表
VOICES = {
    "Cherry": {"gender": "女", "desc": "活泼可爱"},
    "Ethan": {"gender": "男", "desc": "稳重成熟"},
    "Bella": {"gender": "女", "desc": "温柔知性"},
    "Dylan": {"gender": "男", "desc": "年轻活力"},
}

# 默认配置
DEFAULT_MODEL = "qwen3-tts-flash"
DEFAULT_VOICE = "Cherry"

def list_voices():
    """列出所有可用音色"""
    print("\n🎙️ 百炼 TTS 可用音色：")
    print("-" * 40)
    for voice, info in VOICES.items():
        marker = "⭐ 默认" if voice == DEFAULT_VOICE else "   "
        print(f"{marker} {voice:10} | {info['gender']} | {info['desc']}")
    print("-" * 40)
    print(f"\n默认音色: {DEFAULT_VOICE}")
    print(f"默认模型: {DEFAULT_MODEL}")

def generate_tts(text, voice=None, output_file=None, api_key=None, model=None):
    """
    生成TTS音频
    
    Args:
        text: 要合成的文本
        voice: 音色名称，默认 Cherry
        output_file: 输出文件路径，默认 /tmp/bailian_tts.opus
        api_key: 百炼API Key，默认从环境变量读取
        model: 模型名称，默认 qwen3-tts-flash
    
    Returns:
        成功返回输出文件路径，失败返回None
    """
    # 设置默认值
    voice = voice or DEFAULT_VOICE
    model = model or DEFAULT_MODEL
    output_file = output_file or "/tmp/bailian_tts.opus"
    
    # 获取API Key
    api_key = api_key or os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        print("❌ 错误：未设置 DASHSCOPE_API_KEY 环境变量")
        return None
    
    # 验证音色
    if voice not in VOICES:
        print(f"❌ 错误：未知音色 '{voice}'")
        print(f"可用音色: {', '.join(VOICES.keys())}")
        return None
    
    # 设置API
    os.environ["DASHSCOPE_API_KEY"] = api_key
    dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'
    
    try:
        print(f"🎙️ 正在生成音频...")
        print(f"   文本: {text[:50]}{'...' if len(text) > 50 else ''}")
        print(f"   音色: {voice} ({VOICES[voice]['gender']}, {VOICES[voice]['desc']})")
        print(f"   模型: {model}")
        
        # 调用API
        response = dashscope.MultiModalConversation.call(
            model=model,
            api_key=api_key,
            text=text,
            voice=voice
        )
        
        if response.status_code == 200:
            # 获取音频URL
            if hasattr(response, 'output') and response.output:
                output = response.output
                if 'audio' in output and 'url' in output['audio']:
                    audio_url = output['audio']['url']
                    
                    # 下载音频
                    audio_response = requests.get(audio_url, timeout=60)
                    if audio_response.status_code == 200:
                        with open(output_file, "wb") as f:
                            f.write(audio_response.content)
                        print(f"✅ 成功生成: {output_file}")
                        return output_file
                    else:
                        print(f"❌ 下载音频失败: {audio_response.status_code}")
                else:
                    print(f"❌ 响应中无音频URL: {output}")
            else:
                print(f"❌ 响应格式错误")
        else:
            print(f"❌ API调用失败: {response.status_code}")
            print(f"   错误信息: {response}")
        
        return None
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    parser = argparse.ArgumentParser(description='百炼TTS语音合成工具')
    parser.add_argument('text', nargs='?', help='要合成的文本')
    parser.add_argument('--voice', '-v', default=DEFAULT_VOICE, 
                       help=f'音色名称 (默认: {DEFAULT_VOICE})')
    parser.add_argument('--output', '-o', default='/tmp/bailian_tts.opus',
                       help='输出文件路径 (默认: /tmp/bailian_tts.opus)')
    parser.add_argument('--list-voices', '-l', action='store_true',
                       help='列出所有可用音色')
    parser.add_argument('--model', '-m', default=DEFAULT_MODEL,
                       help=f'模型名称 (默认: {DEFAULT_MODEL})')
    
    args = parser.parse_args()
    
    # 列出色音
    if args.list_voices:
        list_voices()
        return
    
    # 检查文本
    if not args.text:
        print("❌ 错误：请提供要合成的文本")
        print(f"\n用法: python3 {sys.argv[0]} '你好世界' --voice Cherry")
        print(f"      python3 {sys.argv[0]} --list-voices")
        sys.exit(1)
    
    # 生成音频
    result = generate_tts(
        text=args.text,
        voice=args.voice,
        output_file=args.output,
        model=args.model
    )
    
    if result:
        print(f"\n🎵 音频文件: {result}")
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
