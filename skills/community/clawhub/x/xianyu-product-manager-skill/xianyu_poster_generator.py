#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
闲鱼大字报风格商品配图生成器
专为AI服务商品设计的简单直接的大字报风格配图
"""

from typing import List, Dict, Optional
import random

def generate_xianyu_poster_images(
    service_type: str,
    cases: List[str],
    style: str = "professional"
) -> List[str]:
    """
    生成闲鱼大字报风格商品配图
    
    Args:
        service_type: 服务类型主标题 (如 "AI智能定制服务")
        cases: 具体案例列表 (如 ["电商客服自动化", "内容创作助手"])
        style: 风格类型 ("red", "blue", "black", "professional")
    
    Returns:
        List[str]: 生成的图片URL列表（至少2张）
    """
    
    # 根据服务类型和案例生成不同的prompt
    prompts = []
    
    # 第一张：主标题 + 案例展示
    if style == "red":
        prompt1 = f"Chinese poster style design with large bold main title \"{service_type}\" at top in red, followed by case examples below in smaller black text: {', '.join(cases[:3])}, clean white background, professional business layout, clear hierarchy, suitable for Xianyu marketplace product image"
    elif style == "blue":
        prompt1 = f"Simple Chinese business poster with large main title \"{service_type}\" in bold blue at top, followed by successful case examples in black: {', '.join(cases[:3])}, clean white background, professional layout with clear text hierarchy, suitable for second-hand marketplace product listing"
    elif style == "black":
        prompt1 = f"Bold Chinese poster design with main headline \"{service_type}\" in large black characters at top, subtitle \"已服务50+客户\" in red below, then case studies: {', '.join(cases[:3])}, minimalist white background, clear typography hierarchy, professional Xianyu marketplace style"
    else:  # professional
        prompt1 = f"Professional Chinese business poster with large main title \"{service_type}\" in bold black at top, case examples below: {', '.join(cases[:3])}, clean white background, no complex graphics, no QR codes, no platform logos, suitable for Xianyu AI service product"
    
    prompts.append(prompt1)
    
    # 第二张：简洁版本或不同布局
    if len(cases) >= 2:
        prompt2 = f"Minimalist Chinese poster with large title \"{service_type.split(' ')[0] if ' ' in service_type else service_type}\" in bold font, simple case list: {cases[0]}, {cases[1] if len(cases) > 1 else ''}, white background, no decorations, no logos, no QR codes, professional Xianyu marketplace style"
    else:
        prompt2 = f"Clean Chinese business poster with large title \"{service_type}\" and subtitle \"专业AI服务\", white background, minimal design, no complex patterns, no platform logos, no QR codes, suitable for second-hand marketplace"
    
    prompts.append(prompt2)
    
    return prompts

def get_default_poster_prompts(service_category: str = "AI服务") -> List[str]:
    """
    获取默认的大字报配图prompt
    
    Args:
        service_category: 服务类别
        
    Returns:
        List[str]: 默认的prompt列表
    """
    
    default_cases = {
        "AI客服": ["电商店铺智能客服", "小红书私信自动回复", "企业微信客服机器人"],
        "数据分析": ["抖音爆款选题分析", "小红书竞品数据报告", "淘宝店铺经营分析"],
        "工作流自动化": ["闲鱼商品自动上架", "多平台内容同步", "客户信息自动整理"],
        "内容创作": ["小红书爆款文案生成", "抖音脚本自动生成", "电商产品描述优化"]
    }
    
    cases = default_cases.get(service_category, ["电商客服自动化", "内容创作助手", "工作流优化专家"])
    service_title = f"{service_category}定制开发"
    
    return generate_xianyu_poster_images(service_title, cases, "professional")

# 使用示例和测试数据
if __name__ == "__main__":
    # 测试生成
    test_prompts = get_default_poster_prompts("AI客服")
    print("Generated prompts:")
    for i, prompt in enumerate(test_prompts, 1):
        print(f"{i}. {prompt}")