#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分镜规划模块
预设分镜模板，支持自定义编辑
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field


@dataclass
class Shot:
    """单个分镜"""
    id: int
    name: str           # 分镜名称
    name_en: str        # 英文名称
    description: str    # 场景描述
    composition: str    # 构图说明
    lighting: str       # 光线要求
    angle: str          # 拍摄角度
    copywriting: str    # 文案内容
    copywriting_en: str # 英文文案


class CompositionPlanner:
    """分镜规划器"""
    
    # 预设分镜模板
    SHOT_TEMPLATES = {
        'main': {
            'name': '首页主图',
            'name_en': 'Main Hero Shot',
            'description': '产品完整展示，突出整体外观',
            'composition': '产品居中，完整展示，适当留白',
            'lighting': '主光+辅光，突出产品轮廓',
            'angle': '平视或45度角，展示最佳视角'
        },
        'detail': {
            'name': '细节特写',
            'name_en': 'Detail Close-up',
            'description': '产品细节特写，展示材质工艺',
            'composition': '局部放大，占据画面70%',
            'lighting': '侧光或顶光，强调纹理质感',
            'angle': '微距视角，展示细节'
        },
        'scene': {
            'name': '场景图',
            'name_en': 'Lifestyle Scene',
            'description': '产品在实际使用场景中展示',
            'composition': '环境+产品，产品占30-40%',
            'lighting': '自然光或环境光，营造氛围',
            'angle': '广角视角，展示空间关系'
        },
        'comparison': {
            'name': '对比图',
            'name_en': 'Size Comparison',
            'description': '展示产品尺寸或与其他物品对比',
            'composition': '产品+参照物，左右或上下排列',
            'lighting': '均匀光线，避免阴影干扰',
            'angle': '平视，确保比例准确'
        },
        'feature': {
            'name': '功能展示',
            'name_en': 'Feature Highlight',
            'description': '展示产品功能或使用方式',
            'composition': '动作捕捉或功能部位特写',
            'lighting': '定向光源，突出功能点',
            'angle': '根据功能选择最佳角度'
        },
        'package': {
            'name': '包装展示',
            'name_en': 'Package Display',
            'description': '展示产品包装，适合礼品场景',
            'composition': '包装完整展示，可带开箱状态',
            'lighting': '柔和光线，突出包装质感',
            'angle': '45度角，展示包装立体感'
        }
    }
    
    # 文案模板
    COPYWRITING_TEMPLATES = {
        'healing_warm': {
            'main': {'zh': '自然清新，点缀生活', 'en': 'Natural & Fresh, Decorate Your Life'},
            'detail': {'zh': '精选品质，匠心工艺', 'en': 'Selected Quality, Crafted with Care'},
            'scene': {'zh': '温馨相伴，生活美学', 'en': 'Warm Companion, Life Aesthetics'},
            'comparison': {'zh': '恰到好处，尺寸适中', 'en': 'Perfect Size, Just Right'},
            'feature': {'zh': '用心设计，贴心功能', 'en': 'Thoughtful Design, Caring Features'},
            'package': {'zh': '精美包装，送礼佳品', 'en': 'Elegant Package, Perfect Gift'}
        },
        'minimal_business': {
            'main': {'zh': '品质之选，专业保障', 'en': 'Quality Choice, Professional Guarantee'},
            'detail': {'zh': '精工细作，品质可见', 'en': 'Exquisite Craftsmanship, Visible Quality'},
            'scene': {'zh': '高效实用，商务首选', 'en': 'Efficient & Practical, Business First'},
            'comparison': {'zh': '标准规格，精准尺寸', 'en': 'Standard Specs, Precise Dimensions'},
            'feature': {'zh': '功能强大，效率提升', 'en': 'Powerful Features, Boost Efficiency'},
            'package': {'zh': '专业包装，安全送达', 'en': 'Professional Package, Safe Delivery'}
        },
        'fashion_trendy': {
            'main': {'zh': '潮流先锋，个性表达', 'en': 'Trend Pioneer, Personal Expression'},
            'detail': {'zh': '独特设计，彰显品味', 'en': 'Unique Design, Show Your Taste'},
            'scene': {'zh': '时尚生活，态度之选', 'en': 'Fashion Life, Choice of Attitude'},
            'comparison': {'zh': '完美比例，潮流尺寸', 'en': 'Perfect Proportion, Trendy Size'},
            'feature': {'zh': '酷感功能，玩转创意', 'en': 'Cool Features, Play with Creativity'},
            'package': {'zh': '潮酷包装，开箱惊喜', 'en': 'Cool Package, Unboxing Surprise'}
        }
    }
    
    def __init__(self, style_key: str = 'healing_warm'):
        self.style_key = style_key
        self.shots: List[Shot] = []
    
    def create_default_plan(self, num_shots: int = 3) -> List[Shot]:
        """
        创建默认分镜规划
        
        Args:
            num_shots: 分镜数量（默认3张）
        
        Returns:
            分镜列表
        """
        # 默认使用：主图、细节、场景
        default_order = ['main', 'detail', 'scene', 'comparison', 'feature', 'package']
        selected = default_order[:num_shots]
        
        shots = []
        for idx, shot_key in enumerate(selected, start=1):
            template = self.SHOT_TEMPLATES[shot_key]
            copywriting = self.COPYWRITING_TEMPLATES[self.style_key][shot_key]
            
            shot = Shot(
                id=idx,
                name=template['name'],
                name_en=template['name_en'],
                description=template['description'],
                composition=template['composition'],
                lighting=template['lighting'],
                angle=template['angle'],
                copywriting=copywriting['zh'],
                copywriting_en=copywriting['en']
            )
            shots.append(shot)
        
        self.shots = shots
        return shots
    
    def update_shot_copywriting(self, shot_id: int, new_copywriting: str) -> bool:
        """更新分镜文案"""
        for shot in self.shots:
            if shot.id == shot_id:
                shot.copywriting = new_copywriting
                return True
        return False
    
    def add_shot(self, shot_type: str, position: int = -1) -> Optional[Shot]:
        """添加分镜"""
        if shot_type not in self.SHOT_TEMPLATES:
            return None
        
        template = self.SHOT_TEMPLATES[shot_type]
        copywriting = self.COPYWRITING_TEMPLATES[self.style_key].get(
            shot_type, 
            {'zh': '产品展示', 'en': 'Product Display'}
        )
        
        new_id = len(self.shots) + 1
        shot = Shot(
            id=new_id,
            name=template['name'],
            name_en=template['name_en'],
            description=template['description'],
            composition=template['composition'],
            lighting=template['lighting'],
            angle=template['angle'],
            copywriting=copywriting['zh'],
            copywriting_en=copywriting['en']
        )
        
        if position == -1:
            self.shots.append(shot)
        else:
            self.shots.insert(position - 1, shot)
            # 重新编号
            for i, s in enumerate(self.shots, start=1):
                s.id = i
        
        return shot
    
    def remove_shot(self, shot_id: int) -> bool:
        """删除分镜"""
        for i, shot in enumerate(self.shots):
            if shot.id == shot_id:
                self.shots.pop(i)
                # 重新编号
                for j, s in enumerate(self.shots, start=1):
                    s.id = j
                return True
        return False
    
    def reorder_shots(self, new_order: List[int]) -> bool:
        """重新排序分镜"""
        if len(new_order) != len(self.shots):
            return False
        
        try:
            new_shots = [self.shots[i-1] for i in new_order]
            self.shots = new_shots
            # 重新编号
            for i, shot in enumerate(self.shots, start=1):
                shot.id = i
            return True
        except IndexError:
            return False
    
    def format_plan_for_display(self) -> str:
        """格式化分镜规划用于显示"""
        lines = ["📋 分镜规划：\n"]
        
        for shot in self.shots:
            lines.append(f"图{shot.id}：{shot.name}")
            lines.append(f"  📖 {shot.description}")
            lines.append(f"  🎨 {shot.composition}")
            lines.append(f"  💡 {shot.lighting}")
            lines.append(f"  📝 文案：{shot.copywriting}")
            lines.append("")
        
        return '\n'.join(lines)


# 便捷函数
def create_composition_plan(style_key: str = 'healing_warm', num_shots: int = 3) -> CompositionPlanner:
    """便捷函数：创建分镜规划"""
    planner = CompositionPlanner(style_key)
    planner.create_default_plan(num_shots)
    return planner


if __name__ == '__main__':
    # 测试
    print("🎬 分镜规划器 - 测试")
    print("=" * 50)
    
    # 创建规划
    planner = create_composition_plan('healing_warm', 3)
    print(planner.format_plan_for_display())
    
    # 测试更新文案
    print("\n更新图1文案...")
    planner.update_shot_copywriting(1, "新品上市，限时优惠！")
    print(planner.format_plan_for_display())
