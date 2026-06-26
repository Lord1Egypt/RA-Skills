#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
豆包 SeedTTS 2.0 - 基础使用示例
"""

from tts_client import SeedTTS2

# 初始化（自动从环境变量读取配置）
tts = SeedTTS2()

print("=" * 60)
print("豆包 SeedTTS 2.0 - 基础使用示例")
print("=" * 60)

# 示例 1：使用默认音色（儒雅逸辰 2.0 - JARVIS 官方）
print("\n1️⃣ 使用默认音色（JARVIS 官方）")
output = tts.say("你好，我是你的智能助手。有什么可以帮你的吗？")
print(f"   已生成：{output}")

# 示例 2：指定音色（女声）
print("\n2️⃣ 使用女声（Vivi 2.0）")
output = tts.say(
    "你好呀，很高兴认识你！今天想聊点什么呢？",
    speaker="zh_female_vv_uranus_bigtts"
)
print(f"   已生成：{output}")

# 示例 3：保存到指定文件
print("\n3️⃣ 保存到指定文件")
output = tts.say(
    "这是保存测试",
    speaker="zh_male_ruyayichen_uranus_bigtts",
    output="./output/custom_name.mp3"
)
print(f"   已生成：{output}")

# 示例 4：英文合成
print("\n4️⃣ 英文合成")
output = tts.say(
    "Hello, I am your AI assistant. How can I help you today?",
    speaker="en_female_dacey_uranus_bigtts"
)
print(f"   已生成：{output}")

print("\n" + "=" * 60)
print("示例完成！")
print("=" * 60)
