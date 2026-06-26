#!/usr/bin/env python3
"""
声音克隆技能 - 快速演示脚本
支持：声音克隆、文字转语音、批量生成
"""

import os
import sys

def check_environment():
    """检查运行环境"""
    print("=== 环境检查 ===")
    
    # 检查 Python 版本
    if sys.version_info < (3, 10):
        print("❌ Python 版本需要 3.10+")
        return False
    print(f"✅ Python 版本: {sys.version.split()[0]}")
    
    # 检查 mlx-audio
    try:
        import mlx_audio
        print("✅ mlx-audio 已安装")
    except ImportError:
        print("❌ mlx-audio 未安装，请运行: pip install mlx-audio")
        return False
    
    return True

def clone_voice():
    """声音克隆示例"""
    print("\n=== 声音克隆演示 ===")
    
    ref_audio = input("请输入参考音频路径 (WAV 格式): ").strip()
    if not ref_audio or not os.path.exists(ref_audio):
        print("❌ 音频文件不存在")
        return
    
    text = input("请输入要合成的文本: ").strip()
    if not text:
        text = "这是一个声音克隆测试，使用参考音频的声音特征来生成语音。"
    
    output = input("请输入输出文件名前缀 (默认: output): ").strip() or "output"
    
    from mlx_audio.tts.utils import load_model
    from mlx_audio.tts.generate import generate_audio
    
    print("加载模型中...")
    model = load_model('mlx-community/Qwen3-TTS-12Hz-1.7B-Base-8bit')
    
    print("生成音频中...")
    generate_audio(
        model=model,
        text=text,
        ref_audio=ref_audio,
        lang_code="zh",
        file_prefix=output,
        max_tokens=3000
    )
    print(f"✅ 音频已生成: {output}_000.wav")

def tts_builtin():
    """使用内置声音模板的文字转语音"""
    print("\n=== 内置声音模板 ===")
    
    voices = [
        ('af_heart', '温暖友好 - 女声'),
        ('af_chat', '日常对话 - 女声'),
        ('af_narration', '故事叙述 - 女声'),
        ('am_adventure', '冒险风格 - 男声'),
        ('am_broadcast', '专业播报 - 男声'),
        ('am_chat', '日常对话 - 男声'),
        ('am_narration', '故事叙述 - 男声'),
    ]
    
    print("\n可用的声音模板:")
    for i, (code, name) in enumerate(voices, 1):
        print(f"  {i}. {name} ({code})")
    
    choice = input("\n请选择声音模板编号 (默认:1): ").strip()
    try:
        idx = int(choice) - 1 if choice else 0
        voice = voices[idx][0]
        voice_name = voices[idx][1]
    except:
        voice = 'af_heart'
        voice_name = '温暖友好 - 女声'
    
    text = input("请输入要合成的文本: ").strip()
    if not text:
        text = f"你好，这是一个{voice_name}的语音合成测试。"
    
    output = input("请输入输出文件名 (默认: tts_output.wav): ").strip() or "tts_output.wav"
    
    from mlx_audio.tts.utils import load_model
    
    print("加载模型中...")
    model = load_model('mlx-community/Qwen3-TTS-12Hz-1.7B-Base-8bit')
    
    print(f"正在使用 {voice_name} 生成音频...")
    results = list(model.generate(
        text=text,
        voice=voice,
        language='Chinese'
    ))
    
    with open(output, 'wb') as f:
        for result in results:
            f.write(result.audio)
    
    print(f"✅ 音频已生成: {output}")

def main():
    if not check_environment():
        return
    
    print("\n=== 声音克隆技能 (Voice Cloning Skill)")
    print("=" * 40)
    print("1. 声音克隆（使用参考音频）")
    print("2. 文字转语音（内置声音模板）")
    print("3. 退出")
    
    choice = input("\n请选择功能: ").strip()
    
    if choice == '1':
        clone_voice()
    elif choice == '2':
        tts_builtin()
    else:
        print("再见！")

if __name__ == '__main__':
    main()
