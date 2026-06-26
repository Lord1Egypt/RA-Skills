#!/usr/bin/env python3
"""
小红书爬虫 Skill 包
用于 OpenClaw 集成

使用示例:
    from xhs_crawler import crawl_notes
    from feishu_app_bot import FeishuAppBot
    
    # 搜索笔记
    results = crawl_notes("新燕宝", max_notes=5)
    
    # 处理结果
    for note in results:
        print(note['标题'])
        print(note['笔记链接'])
"""

# 注意：此文件用于向后兼容，建议直接使用具体模块
# from xhs_crawler import crawl_notes
# from feishu_app_bot import FeishuAppBot

__version__ = "1.0.0"
__author__ = "OpenClaw Skill"

__all__ = []
