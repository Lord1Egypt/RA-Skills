#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
产品分析模块
分析上传的产品图片，提取特征和卖点
"""

import os
import base64
from typing import Dict, List, Any, Optional
from dataclasses import dataclass


@dataclass
class ProductFeatures:
    """产品特征"""
    product_type: str  # 产品类型（绿植/工艺品/家居等）
    material: str      # 材质（陶瓷/金属/布料等）
    color: str         # 主要颜色
    shape: str         # 形状描述
    texture: str       # 质感（光滑/粗糙/细腻等）
    size: str          # 尺寸感知（大/中/小）
    style: str         # 风格（现代/复古/简约等）
    usage: str         # 用途（装饰/实用/礼品等）


@dataclass
class ProductSellingPoints:
    """产品卖点"""
    main_selling_point: str    # 主要卖点
    secondary_points: List[str] # 次要卖点
    target_audience: str       # 目标人群
    usage_scenarios: List[str] # 使用场景


class ImageAnalyzer:
    """图片分析器"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('DASHSCOPE_API_KEY')
        self.api_base = "https://dashscope.aliyuncs.com/api/v1"
    
    def analyze_image(self, image_path: str) -> Dict[str, Any]:
        """
        分析单张产品图片
        
        Args:
            image_path: 图片路径
        
        Returns:
            分析结果字典
        """
        # 检查图片是否存在
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"图片不存在: {image_path}")
        
        # 读取图片并转为base64
        with open(image_path, 'rb') as f:
            image_base64 = base64.b64encode(f.read()).decode('utf-8')
        
        # 这里应该调用多模态API（GPT-4V/Qwen-VL）
        # 现在先用模拟数据演示
        return self._mock_analyze(image_path)
    
    def analyze_multiple(self, image_paths: List[str]) -> Dict[str, Any]:
        """
        分析多张产品图片
        
        Args:
            image_paths: 图片路径列表
        
        Returns:
            综合分析结果
        """
        if not image_paths:
            raise ValueError("至少需要一张图片")
        
        # 分析每张图片
        analyses = []
        for path in image_paths:
            try:
                result = self.analyze_image(path)
                analyses.append(result)
            except Exception as e:
                print(f"⚠️  分析图片失败 {path}: {e}")
        
        # 综合所有分析结果
        return self._merge_analyses(analyses)
    
    def _mock_analyze(self, image_path: str) -> Dict[str, Any]:
        """模拟分析结果（实际使用时替换为真实API调用）"""
        # 根据文件名关键词模拟不同类型
        filename = os.path.basename(image_path).lower()
        
        if 'plant' in filename or 'green' in filename or 'leaf' in filename:
            return {
                'product_type': '绿植盆栽',
                'material': '植物+陶瓷盆',
                'color': '翠绿、棕色',
                'shape': '叶片舒展，自然形态',
                'texture': '叶片光滑，盆土粗糙',
                'size': '中型',
                'style': '自然清新',
                'usage': '家居装饰、空气净化',
                'main_selling_point': '自然清新，点缀生活空间',
                'secondary_points': [
                    '净化空气，改善环境',
                    '易于养护，适合新手',
                    '提升家居格调'
                ],
                'target_audience': '25-40岁都市白领、家居爱好者',
                'usage_scenarios': ['客厅摆放', '书房装饰', '办公室绿化']
            }
        elif 'vase' in filename or 'ceramic' in filename:
            return {
                'product_type': '陶瓷花瓶',
                'material': '手工陶瓷',
                'color': '米白、浅蓝',
                'shape': '流线型瓶身，优雅曲线',
                'texture': '釉面光滑，温润细腻',
                'size': '中大型',
                'style': '新中式/北欧风',
                'usage': '插花装饰、摆件',
                'main_selling_point': '手工制作，独一无二',
                'secondary_points': [
                    '釉色温润，质感高级',
                    '适合多种花材',
                    '提升空间艺术感'
                ],
                'target_audience': '30-50岁中产、花艺爱好者、室内设计师',
                'usage_scenarios': ['客厅装饰', '餐厅 centerpiece', '玄关摆件']
            }
        else:
            return {
                'product_type': '家居工艺品',
                'material': '复合材料',
                'color': '原木色、金属色',
                'shape': '几何造型',
                'texture': '质感丰富',
                'size': '中型',
                'style': '现代简约',
                'usage': '装饰摆件',
                'main_selling_point': '设计感强，提升空间品味',
                'secondary_points': [
                    '精工细作，品质保证',
                    '百搭风格，适配多种场景',
                    '送礼自用两相宜'
                ],
                'target_audience': '25-45岁都市人群',
                'usage_scenarios': ['客厅装饰', '书房摆件', '礼品赠送']
            }
    
    def _merge_analyses(self, analyses: List[Dict]) -> Dict[str, Any]:
        """合并多个分析结果"""
        if not analyses:
            return {}
        
        # 以第一个为主，后续补充
        merged = analyses[0].copy()
        
        # 合并卖点（去重）
        all_points = set()
        for a in analyses:
            all_points.add(a.get('main_selling_point', ''))
            all_points.update(a.get('secondary_points', []))
        
        merged['all_selling_points'] = list(all_points)[:5]  # 最多5个
        
        return merged


# 便捷函数
def analyze_product(image_paths: List[str]) -> Dict[str, Any]:
    """便捷函数：分析产品图片"""
    analyzer = ImageAnalyzer()
    return analyzer.analyze_multiple(image_paths)


if __name__ == '__main__':
    # 测试
    print("🖼️  产品图片分析器 - 测试")
    print("=" * 50)
    
    # 模拟测试
    test_images = ['/tmp/plant_001.jpg', '/tmp/vase_002.jpg']
    
    for img in test_images:
        print(f"\n分析: {img}")
        result = analyze_product([img])
        print(f"  产品类型: {result.get('product_type')}")
        print(f"  材质: {result.get('material')}")
        print(f"  主要卖点: {result.get('main_selling_point')}")
        print(f"  目标人群: {result.get('target_audience')}")
