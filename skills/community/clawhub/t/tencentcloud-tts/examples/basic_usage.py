#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
腾讯云语音合成基础使用示例
演示如何使用tencent-tts技能包进行文本转语音
"""

import os
import sys

# 添加技能包路径到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from tencent_tts import TextToSpeech


def basic_synthesis():
    """基础语音合成示例"""
    print("=== 腾讯云语音合成基础示例 ===")
    
    # 检查环境变量配置
    if not os.getenv("TENCENTCLOUD_SECRET_ID") or not os.getenv("TENCENTCLOUD_SECRET_KEY"):
        print("❌ 请先设置环境变量:")
        print("   export TENCENTCLOUD_SECRET_ID='your-secret-id'")
        print("   export TENCENTCLOUD_SECRET_KEY='your-secret-key'")
        return
    
    try:
        # 创建TTS客户端
        tts = TextToSpeech()
        
        # 示例文本
        text = "Welcome to Tencent Cloud Text-to-Speech service. This is a basic usage example."
        
        print("📝 合成文本: {}".format(text))
        print("🔄 正在合成语音...")
        
        # 调用语音合成
        result = tts.synthesize(
            text=text,
            voice_type=101001,  # 标准女声
            codec="mp3",
            output_file="basic_example.mp3"
        )
        
        if result["success"]:
            print("✅ 语音合成成功！")
            print("📁 输出文件: {}".format(result['output_file']))
            print("📊 文件大小: {} 字节".format(result['file_size']))
            print("🎵 语音类型: {}".format(result['voice_type']))
            print("🎵 音频格式: {}".format(result['codec']))
        else:
            print("❌ 合成失败: {}".format(result['error']))
            
    except Exception as e:
        print("❌ 发生错误: {}".format(e))


if __name__ == "__main__":
    # 运行基础示例
    basic_synthesis()
    
    print("\n=== 示例运行完成 ===")
    print("💡 提示: 您可以使用音频播放器播放生成的音频文件进行测试")