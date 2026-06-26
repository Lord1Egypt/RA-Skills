#!/usr/bin/env python3
"""
XHS Content Generator - 小红书爆款内容生成器
根据热点生成爆款标题和内容框架
"""

import argparse
import json
import os
import sys
from datetime import datetime

# 提示词模板
PROMPT_TEMPLATE = """你是一个专业的小红书内容创作者，擅长打造爆款内容。

## 任务
根据给定的主题和热点，生成小红书爆款内容方案。

## 主题: {topic}
## 热点关键词: {hot_topic}

## 输出要求

### 一、爆款标题（10个）
每个标题要求：
- 带有适当emoji
- 引发好奇或共鸣
- 突出价值或收益
- 使用数字增加可信度

格式：
1. 【emoji】标题文字
2. ...

### 二、内容框架（3个完整方案）

对于每个方案，请包含：

**方案X：标题**
- 开头（hook）：吸引眼球的开场，20字以内
- 正文结构：
  - 要点1：（具体内容）
  - 要点2：（具体内容）
  - 要点3：（具体内容）
- 结尾引导：互动话术，引导评论和收藏

### 三、热门标签
推荐5-10个相关标签

### 四、互动引导话术
3个不同风格的互动文案

## 注意
- 标题要吸引眼球，引发点击欲望
- 内容要有干货，有实用价值
- 语言风格符合小红书年轻化、口语化特点
"""

def load_prompt():
    """加载提示词模板"""
    prompt_path = os.path.join(os.path.dirname(__file__), 'prompt.txt')
    if os.path.exists(prompt_path):
        with open(prompt_path, 'r', encoding='utf-8') as f:
            return f.read()
    return PROMPT_TEMPLATE

def generate_content(topic: str, hot_topic: str) -> str:
    """生成内容"""
    prompt = load_prompt()
    prompt = prompt.format(topic=topic, hot_topic=hot_topic)
    return prompt

def main():
    parser = argparse.ArgumentParser(description='小红书爆款内容生成器')
    parser.add_argument('--topic', default='AI副业', 
                        choices=['AI副业', 'AI工具', '赚钱方法'],
                        help='内容主题')
    parser.add_argument('--hot_topic', default='', help='当前热点关键词')
    parser.add_argument('--output', '-o', default=None, help='输出文件路径')
    
    args = parser.parse_args()
    
    # 生成提示词内容
    content = generate_content(args.topic, args.hot_topic)
    
    # 输出结果
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ 内容已保存到: {args.output}")
    else:
        print("=" * 60)
        print(f"📝 主题: {args.topic}")
        print(f"🔥 热点: {args.hot_topic}")
        print("=" * 60)
        print("\n📋 请将以下内容发送给AI助手获取结果:\n")
        print(content)
        
        # 输出到文件供查看
        output_file = f"output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"主题: {args.topic}\n")
            f.write(f"热点: {args.hot_topic}\n")
            f.write("=" * 60 + "\n")
            f.write(content)
        print(f"\n💾 提示词已保存到: {output_file}")
        print("请复制提示词内容发送给AI助手生成完整内容")

if __name__ == '__main__':
    main()