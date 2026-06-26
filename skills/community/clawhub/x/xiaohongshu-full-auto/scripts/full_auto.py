#!/usr/bin/env python3
"""
小红书全链路自动化脚本
热点抓取 → 选题匹配 → 内容生成 → 封面生成 → 发布 → 日志记录
"""

import argparse
import json
import os
import sys
import time
import yaml
from typing import List, Dict

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from get_hot_topics import get_xiaohongshu_hot_topics
from match_topics import match_topics_by_niches
from generate_content import generate_xiaohongshu_content
from generate_cover import generate_cover_image
from publish import publish_to_xiaohongshu
from logger import log_published


def load_config(config_path: str = "../references/config-example.yaml") -> Dict:
    """加载配置文件"""
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def full_auto_workflow(config: Dict, niches: List[str] = None, count: int = 1):
    """
    全自动化工作流
    """
    print("🚀 开始小红书全链路自动化工作流\n")
    
    # 1. 获取热点
    print("🔍 步骤 1/6: 获取小红书热榜...")
    hot_topics = get_xiaohongshu_hot_topics(limit=50)
    print(f"✅ 获取到 {len(hot_topics)} 个热点话题\n")
    
    # 2. 选题匹配
    print("🎯 步骤 2/6: 根据垂类匹配选题...")
    target_niches = niches or config.get('niches', [])
    selected_topics = match_topics_by_niches(hot_topics, target_niches, count)
    print(f"✅ 选出 {len(selected_topics)} 个选题\n")
    
    # 3. 逐个处理
    results = []
    for i, topic in enumerate(selected_topics):
        print(f"\n📝 处理第 {i+1}/{len(selected_topics)} 个选题: {topic['title']}")
        
        # 检查是否需要用户确认（半自动模式）
        if config['mode'] == 'semi-auto':
            confirm = input(f"❓ 是否确认发布这个选题? (y/n/y 跳过): ").strip().lower()
            if confirm.startswith('n'):
                print("⏭️ 跳过")
                continue
            if confirm.startswith('s'):
                continue
        
        # 3. 生成内容
        print("✍️ 生成小红书文案...")
        content = generate_xiaohongshu_content(topic['title'], config['writing_style'])
        print(f"✅ 文案生成完成，{len(content['text'])} 字\n")
        
        # 4. 生成封面
        cover_path = None
        if config['cover']['enable']:
            print("🖼️ 生成封面图...")
            cover_path = generate_cover_image(content['title'], config['cover'])
            if cover_path:
                print(f"✅ 封面生成完成: {cover_path}\n")
        
        # 5. 发布
        if config['publish']['enable']:
            print("📤 发布到小红书...")
            result = publish_to_xiaohongshu(
                title=content['title'],
                content=content['text'],
                cover_path=cover_path,
                tags=content['tags'],
                config=config['publish']
            )
            print(f"✅ 发布完成: {result.get('url', 'N/A')}\n")
            
            # 6. 记录日志
            log_published({
                'topic': topic['title'],
                'title': content['title'],
                'tags': content['tags'],
                'cover_path': cover_path,
                'publish_url': result.get('url'),
                'publish_time': time.strftime('%Y-%m-%d %H:%M:%S'),
                'status': result.get('status', 'success')
            })
            
            results.append({
                'topic': topic,
                'content': content,
                'cover_path': cover_path,
                'result': result
            })
            
            # 间隔等待，避免限流
            if i < len(selected_topics) - 1:
                interval = config['publish'].get('interval_minutes', 30) * 60
                print(f"⏳ 等待 {interval//60} 分钟后发布下一篇...")
                time.sleep(interval)
    
    print(f"\n🎉 全流程完成！成功发布 {len(results)} 篇笔记")
    return results


def main():
    parser = argparse.ArgumentParser(description='小红书全链路自动化')
    parser.add_argument('--config', default='../references/config-example.yaml', help='配置文件路径')
    parser.add_argument('--niches', help='内容垂类，逗号分隔')
    parser.add_argument('--count', type=int, default=1, help='生成几篇')
    args = parser.parse_args()
    
    config = load_config(args.config)
    
    niches_list = None
    if args.niches:
        niches_list = [n.strip() for n in args.niches.split(',')]
    
    full_auto_workflow(config, niches_list, args.count)


if __name__ == "__main__":
    main()
