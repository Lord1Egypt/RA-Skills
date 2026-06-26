#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
闲鱼大字报配图使用示例
"""

from xianyu_poster_generator import generate_xianyu_poster_images, get_default_poster_prompts

def demo_poster_generation():
    """演示大字报配图生成"""
    
    # 示例1：AI客服服务
    service_type = "AI智能客服定制"
    cases = ["淘宝店铺自动回复", "小红书私信管理", "企业微信客服机器人"]
    
    prompts = generate_xianyu_poster_images(service_type, cases, "red")
    print("=== AI客服服务大字报配图 ===")
    for i, prompt in enumerate(prompts, 1):
        print(f"图片 {i} prompt: {prompt}")
    
    print("\n" + "="*50 + "\n")
    
    # 示例2：数据分析服务
    prompts2 = get_default_poster_prompts("数据分析")
    print("=== 数据分析服务默认大字报配图 ===")
    for i, prompt in enumerate(prompts2, 1):
        print(f"图片 {i} prompt: {prompt}")

if __name__ == "__main__":
    demo_poster_generation()