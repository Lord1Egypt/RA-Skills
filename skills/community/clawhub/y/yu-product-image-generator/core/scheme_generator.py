#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
方案生成模块
根据产品分析结果，生成3个不同风格的方案
"""

import random
from typing import Dict, List, Any
from dataclasses import dataclass, field


@dataclass
class ColorScheme:
    """色彩方案"""
    primary: str       # 主色
    primary_hex: str
    secondary: str     # 辅助色
    secondary_hex: str
    accent: str        # 点缀色
    accent_hex: str
    background: str    # 背景色
    background_hex: str


@dataclass
class Typography:
    """字体方案"""
    title_font: str
    body_font: str
    title_size: str
    body_size: str


@dataclass
class VisualLanguage:
    """视觉语言"""
    lighting: str          # 光线风格
    background_style: str  # 背景风格
    decoration: str        # 装饰元素
    composition: str       # 构图方式


@dataclass
class Scheme:
    """设计方案"""
    id: int
    name: str                      # 方案名称
    name_en: str                   # 英文名称
    icon: str                      # 图标
    description: str               # 描述
    color_scheme: ColorScheme
    typography: Typography
    visual_language: VisualLanguage
    copywriting_style: str         # 文案风格
    target_mood: str               # 目标氛围
    suitable_products: List[str]   # 适合的产品类型


class SchemeGenerator:
    """方案生成器"""
    
    # 预定义的风格模板
    STYLE_TEMPLATES = {
        'healing_warm': {
            'name': '治愈系温馨风',
            'name_en': 'Healing & Warm',
            'icon': '🌿',
            'description': '柔和光线、木质背景、温暖色调，营造自然清新的居家氛围',
            'color_scheme': {
                'primary': '米色', 'primary_hex': '#F5F5DC',
                'secondary': '棕色', 'secondary_hex': '#8B4513',
                'accent': '浅绿', 'accent_hex': '#90EE90',
                'background': '暖黄', 'background_hex': '#FFF8DC'
            },
            'typography': {
                'title_font': '圆润手写体',
                'body_font': '清新细体',
                'title_size': '36px',
                'body_size': '24px'
            },
            'visual_language': {
                'lighting': '柔和自然光，暖色调',
                'background_style': '木质纹理、棉麻质感',
                'decoration': '绿植点缀、木质托盘',
                'composition': '产品居中，留白舒适'
            },
            'copywriting_style': '温暖治愈，强调自然与家的连接',
            'target_mood': '温馨、舒适、放松',
            'suitable_products': ['绿植', '家居', '香薰', '纺织品', '手工制品']
        },
        
        'minimal_business': {
            'name': '简约商务风',
            'name_en': 'Minimal & Business',
            'icon': '📦',
            'description': '纯白背景、极简几何、专业感，突出产品品质与功能',
            'color_scheme': {
                'primary': '纯白', 'primary_hex': '#FFFFFF',
                'secondary': '深灰', 'secondary_hex': '#333333',
                'accent': '蓝色', 'accent_hex': '#0066CC',
                'background': '浅灰', 'background_hex': '#F5F5F5'
            },
            'typography': {
                'title_font': '现代无衬线体',
                'body_font': '标准黑体',
                'title_size': '40px',
                'body_size': '24px'
            },
            'visual_language': {
                'lighting': '均匀白光，无阴影',
                'background_style': '纯白或浅灰纯色',
                'decoration': '极简几何线条',
                'composition': '产品居中，对称构图'
            },
            'copywriting_style': '专业简洁，强调品质与效率',
            'target_mood': '专业、高效、可信赖',
            'suitable_products': ['数码产品', '办公用品', '工业制品', '工具', '商务礼品']
        },
        
        'fashion_trendy': {
            'name': '时尚潮流风',
            'name_en': 'Fashion & Trendy',
            'icon': '✨',
            'description': '撞色背景、渐变元素、ins风格，打造年轻个性的视觉冲击力',
            'color_scheme': {
                'primary': '珊瑚红', 'primary_hex': '#FF6B6B',
                'secondary': '青绿', 'secondary_hex': '#4ECDC4',
                'accent': '明黄', 'accent_hex': '#FFE66D',
                'background': '薄荷绿', 'background_hex': '#95E1D3'
            },
            'typography': {
                'title_font': '创意艺术体',
                'body_font': '潮流圆体',
                'title_size': '42px',
                'body_size': '26px'
            },
            'visual_language': {
                'lighting': '明亮多彩，渐变效果',
                'background_style': '撞色、渐变、几何图形',
                'decoration': '潮流元素、贴纸风格',
                'composition': '动态构图，产品突出'
            },
            'copywriting_style': '年轻个性，强调态度与潮流',
            'target_mood': '活力、个性、时尚',
            'suitable_products': ['饰品', '美妆', '潮玩', '文创', '个性化礼品']
        }
    }
    
    def __init__(self):
        self.templates = self.STYLE_TEMPLATES
    
    def generate_schemes(self, product_analysis: Dict[str, Any]) -> List[Scheme]:
        """
        根据产品分析生成3个方案
        
        Args:
            product_analysis: 产品分析结果
        
        Returns:
            3个设计方案
        """
        schemes = []
        
        # 根据产品类型选择最适合的3个方案
        product_type = product_analysis.get('product_type', '')
        style = product_analysis.get('style', '')
        
        # 默认方案顺序
        scheme_order = ['healing_warm', 'minimal_business', 'fashion_trendy']
        
        # 根据产品类型调整顺序
        if '绿植' in product_type or '家居' in product_type:
            scheme_order = ['healing_warm', 'fashion_trendy', 'minimal_business']
        elif '工艺' in product_type or '陶瓷' in product_type:
            scheme_order = ['minimal_business', 'healing_warm', 'fashion_trendy']
        elif '饰品' in product_type or '美妆' in product_type:
            scheme_order = ['fashion_trendy', 'healing_warm', 'minimal_business']
        
        # 生成3个方案
        for idx, template_key in enumerate(scheme_order, start=1):
            template = self.templates[template_key]
            
            scheme = Scheme(
                id=idx,
                name=template['name'],
                name_en=template['name_en'],
                icon=template['icon'],
                description=template['description'],
                color_scheme=ColorScheme(**template['color_scheme']),
                typography=Typography(**template['typography']),
                visual_language=VisualLanguage(**template['visual_language']),
                copywriting_style=template['copywriting_style'],
                target_mood=template['target_mood'],
                suitable_products=template['suitable_products']
            )
            
            schemes.append(scheme)
        
        return schemes
    
    def format_scheme_for_display(self, scheme: Scheme) -> str:
        """格式化方案用于显示"""
        lines = [
            f"方案{scheme.id}：{scheme.icon} {scheme.name}",
            f"风格：{scheme.description}",
            f"",
            f"🎨 色彩系统：",
            f"  主色：{scheme.color_scheme.primary} ({scheme.color_scheme.primary_hex})",
            f"  辅助色：{scheme.color_scheme.secondary} ({scheme.color_scheme.secondary_hex})",
            f"  点缀色：{scheme.color_scheme.accent} ({scheme.color_scheme.accent_hex})",
            f"",
            f"✨ 视觉风格：",
            f"  光线：{scheme.visual_language.lighting}",
            f"  背景：{scheme.visual_language.background_style}",
            f"  构图：{scheme.visual_language.composition}",
            f"",
            f"📝 文案风格：{scheme.copywriting_style}",
            f"🎯 目标氛围：{scheme.target_mood}"
        ]
        
        return '\n'.join(lines)


# 便捷函数
def generate_schemes(product_analysis: Dict[str, Any]) -> List[Scheme]:
    """便捷函数：生成方案"""
    generator = SchemeGenerator()
    return generator.generate_schemes(product_analysis)


if __name__ == '__main__':
    # 测试
    print("🎨 方案生成器 - 测试")
    print("=" * 50)
    
    # 模拟产品分析
    test_analysis = {
        'product_type': '绿植盆栽',
        'style': '自然清新'
    }
    
    schemes = generate_schemes(test_analysis)
    
    print(f"\n为【{test_analysis['product_type']}】生成{len(schemes)}个方案：\n")
    
    for scheme in schemes:
        print(SchemeGenerator().format_scheme_for_display(scheme))
        print("\n" + "-" * 50 + "\n")
