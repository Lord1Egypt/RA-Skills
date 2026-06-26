#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
豆包 SeedTTS 2.0 - 批量生成示例
"""

from tts_client import SeedTTS2, batch_generate

# 初始化
tts = SeedTTS2()

print("=" * 60)
print("豆包 SeedTTS 2.0 - 批量生成示例")
print("=" * 60)

# 方式 1：简单列表（使用默认音色）
print("\n1️⃣ 简单列表（默认音色）")
texts = [
    "第一句：你好",
    "第二句：欢迎使用豆包语音合成",
    "第三句：祝你使用愉快",
]
outputs = tts.batch_generate(texts, output_dir="./output/batch_simple")
print(f"   已生成 {len(outputs)} 个文件")
for o in outputs:
    print(f"   - {o}")

# 方式 2：字典列表（指定不同音色）
print("\n2️⃣ 字典列表（不同音色）")
texts_with_speakers = [
    {
        "text": "你好，我是儒雅逸辰",
        "speaker": "zh_male_ruyayichen_uranus_bigtts",
    },
    {
        "text": "你好，我是 Vivi",
        "speaker": "zh_female_vv_uranus_bigtts",
    },
    {
        "text": "Hello, I'm Dacey",
        "speaker": "en_female_dacey_uranus_bigtts",
    },
]
outputs = tts.batch_generate(texts_with_speakers, output_dir="./output/batch_mixed")
print(f"   已生成 {len(outputs)} 个文件")
for o in outputs:
    print(f"   - {o}")

print("\n" + "=" * 60)
print("批量生成完成！")
print("=" * 60)
