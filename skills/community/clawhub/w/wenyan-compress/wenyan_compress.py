#!/usr/bin/env python3
"""
文言文压缩器 - 主入口
将白话文/英文压缩成简洁的文言文
"""

import sys
import json

# 默认的压缩提示词
DEFAULT_PROMPT = """请把下面这段话压缩成简洁的文言文，保留核心意思，尽量精简字数：

{input_text}

要求：
1. 用最少的字表达最完整的意思
2. 保持文言文的风格和韵味
3. 不丢失关键信息
"""

def compress_to_wenyan(text: str, style: str = "normal") -> str:
    """
    调用大模型将文本压缩为文言文
    
    Args:
        text: 输入的文本
        style: 压缩风格 - normal(普通), detailed(详细), minimalist(极简), poetic(诗意)
    
    Returns:
        压缩后的文言文
    """
    
    style_prompts = {
        "normal": "用精简的文言文表达核心意思",
        "detailed": "用文言文表达，保留更多细节",
        "minimalist": "极度压缩，只保留最关键的信息，用最少的字",
        "poetic": "用诗意的文言文表达，稍带文采"
    }
    
    style_instruction = style_prompts.get(style, style_prompts["normal"])
    
    full_prompt = f"""请把下面这段话压缩成{style_instruction}：

{text}

要求：
1. 用最少的字表达最完整的意思
2. 保持文言文的风格
3. 不丢失关键信息
"""
    
    # 这里需要调用大模型API
    # 由于技能运行在OpenClaw环境中，直接返回提示
    # 实际调用由OpenClaw框架处理
    
    return f"[需要调用大模型处理]\n\n输入文本: {text}\n风格: {style}"

def main():
    """主入口 - 处理命令行参数或标准输入"""
    
    if len(sys.argv) > 1:
        # 从命令行参数读取
        text = " ".join(sys.argv[1:])
    else:
        # 从标准输入读取
        text = sys.stdin.read().strip()
    
    if not text:
        print("Usage: python wenyan_compress.py <text>")
        print("Or: echo 'text' | python wenyan_compress.py")
        sys.exit(1)
    
    # 获取风格参数
    style = "normal"
    if "--style" in sys.argv:
        idx = sys.argv.index("--style")
        if idx + 1 < len(sys.argv):
            style = sys.argv[idx + 1]
    
    result = compress_to_wenyan(text, style)
    print(result)

if __name__ == "__main__":
    main()