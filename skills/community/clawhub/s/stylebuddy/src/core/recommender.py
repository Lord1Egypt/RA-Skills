"""
推荐引擎模块
智能搭配推荐核心逻辑
"""

import json
import random
from typing import List, Dict, Optional, Any
from datetime import datetime
import re
import os

class OutfitRecommender:
    """搭配推荐引擎"""
    
    def __init__(self, database):
        self.db = database
        self.templates = self._load_templates()
        self.color_schemes = self._load_color_schemes()
    
    def _load_templates(self) -> List[Dict]:
        """加载搭配模板"""
        template_path = "./assets/data/templates.json"
        if os.path.exists(template_path):
            with open(template_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return self._get_default_templates()
    
    def _load_color_schemes(self) -> List[Dict]:
        """加载配色方案"""
        color_path = "./assets/data/color_schemes.json"
        if os.path.exists(color_path):
            with open(color_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return self._get_default_colors()
    
    def _get_default_templates(self) -> List[Dict]:
        """默认模板数据"""
        return [
            {
                "id": "t_casual_001",
                "name": "基础休闲搭配",
                "category": "休闲",
                "gender": "female",
                "occasions": ["日常", "逛街"],
                "items": {"outer": ["风衣"], "top": ["T恤"], "bottom": ["牛仔裤"], "shoes": ["小白鞋"]},
                "colors": {"primary": ["米色"], "accent": ["白色", "蓝色"]},
                "tips": "敞开穿更休闲，内搭塞进去显腿长"
            },
            {
                "id": "t_work_001",
                "name": "职场通勤搭配",
                "category": "职场",
                "gender": "female",
                "occasions": ["上班", "面试"],
                "items": {"outer": ["西装"], "top": ["衬衫"], "bottom": ["西裤"], "shoes": ["高跟鞋"]},
                "colors": {"primary": ["黑色", "白色"], "accent": ["藏青"]},
                "tips": "合身剪裁更显专业，配饰选择简约款"
            },
            {
                "id": "t_date_001",
                "name": "约会温柔搭配",
                "category": "约会",
                "gender": "female",
                "occasions": ["约会", "聚会"],
                "items": {"outer": ["针织开衫"], "top": ["连衣裙"], "bottom": [], "shoes": ["低跟鞋"]},
                "colors": {"primary": ["粉色", "米色"], "accent": ["白色"]},
                "tips": "柔和色调更有亲和力，适当露肤增加女人味"
            }
        ]
    
    def _get_default_colors(self) -> List[Dict]:
        """默认配色方案"""
        return [
            {"name": "经典黑白", "colors": ["黑色", "白色"], "style": "简约", "occasions": ["职场", "日常"]},
            {"name": "大地色系", "colors": ["米色", "卡其色", "棕色", "驼色"], "style": "优雅", "occasions": ["通勤", "休闲"]},
            {"name": "莫兰迪色", "colors": ["雾霾蓝", "灰粉", "豆绿", "燕麦"], "style": "温柔", "occasions": ["约会", "日常"]},
            {"name": "海军蓝白", "colors": ["藏青", "白色", "条纹"], "style": "清爽", "occasions": ["休闲", "度假"]}
        ]
    
    def recommend(self, occasion: str = "日常", weather: Dict = None, count: int = 3) -> List[Dict]:
        """
        生成搭配推荐
        
        Args:
            occasion: 场合
            weather: 天气信息
            count: 推荐数量
        
        Returns:
            推荐方案列表
        """
        # 获取用户衣橱
        items = self.db.get_all_items()
        
        if not items:
            # 没有单品，返回纯模板推荐
            return self._get_template_recommendations(occasion, count)
        
        # 有单品，基于模板+实际单品生成
        return self._generate_personalized_recommendations(items, occasion, weather, count)
    
    def _get_template_recommendations(self, occasion: str, count: int) -> List[Dict]:
        """纯模板推荐（无单品时）"""
        # 过滤适合该场合的模板
        matching = [t for t in self.templates if occasion in t.get('occasions', [])]
        
        if not matching:
            matching = self.templates
        
        # 随机选择
        selected = random.sample(matching, min(count, len(matching)))
        
        # 格式化输出 - 确保使用中文名称
        return [self._format_template(t) for t in selected]
    
    def _generate_personalized_recommendations(self, items: List[Dict], occasion: str, 
                                                 weather: Dict, count: int) -> List[Dict]:
        """个性化推荐"""
        recommendations = []
        
        # 按类别分组
        by_category = {"outer": [], "top": [], "bottom": [], "shoes": [], "accessory": []}
        for item in items:
            cat = item.get('category', 'top')
            if cat in by_category:
                by_category[cat].append(item)
        
        # 根据天气调整
        temp = weather.get('temp', 20) if weather else 20
        need_outer = temp < 20
        need_warm = temp < 10
        
        # 生成方案 - 获取原始模板进行匹配
        matching_templates = [t for t in self.templates if occasion in t.get('occasions', [])]
        if not matching_templates:
            matching_templates = self.templates
        
        selected_templates = random.sample(matching_templates, min(count * 2, len(matching_templates)))
        
        for template in selected_templates[:count]:
            outfit = self._match_items_to_template(template, by_category, need_outer)
            if outfit:
                recommendations.append(outfit)
        
        # 如果匹配不够，补充纯模板
        while len(recommendations) < count:
            recommendations.append(random.choice(templates))
        
        return recommendations[:count]
    
    def _match_items_to_template(self, template: Dict, by_category: Dict, need_outer: bool) -> Optional[Dict]:
        """将模板与用户单品匹配"""
        template_items = template.get('items', {})
        matched_items = []
        
        for cat, keywords in template_items.items():
            if not keywords:
                continue
            
            # 跳过外套如果不需要
            if cat == 'outer' and not need_outer:
                continue
            
            # 在用户单品中找匹配的
            user_items = by_category.get(cat, [])
            matched = self._find_matching_item(user_items, keywords, template.get('colors', {}))
            
            if matched:
                color = matched.get('color', '') or ''
                name = matched.get('name', '')
                # 避免颜色重复
                if color and name.startswith(color):
                    matched_items.append(name)
                else:
                    matched_items.append(f"{color}{name}")
            elif cat in ['top', 'bottom']:
                # 核心单品必须匹配到
                return None
        
        if len(matched_items) >= 2:
            # 获取友好的名称
            name = template.get('name', '')
            if not name or name.startswith('t_') or re.match(r'^.+搭配\s+\d+$', name):
                category = template.get('category', '搭配')
                occasions = template.get('occasions', ['日常'])
                occasion = occasions[0]
                # 避免重复（如类别和场合都是'其他'）
                if category == occasion or category in occasion:
                    name = f"{occasion}风"
                else:
                    name = f"{occasion}{category}风"
            
            # 获取参考图片
            image_path = self._get_outfit_image(template)
            
            return {
                "name": name,
                "items": matched_items,
                "tips": template.get('tips', ''),
                "template_id": template.get('id'),
                "matched": True,
                "image_path": image_path
            }
        
        return None
    
    def _find_matching_item(self, items: List[Dict], keywords: List[str], colors: Dict) -> Optional[Dict]:
        """根据关键词和颜色找匹配单品"""
        target_colors = colors.get('primary', []) + colors.get('accent', [])
        
        # 优先颜色匹配
        for item in items:
            item_color = item.get('color', '')
            if any(c in item_color for c in target_colors):
                return item
        
        # 其次关键词匹配
        for item in items:
            name = item.get('name', '')
            for kw in keywords:
                if kw in name:
                    return item
        
        # 随机选一个同类别
        return random.choice(items) if items else None
    
    def _format_template(self, template: Dict) -> Dict:
        """格式化模板为推荐格式"""
        items = []
        template_items = template.get('items', {})
        
        for cat, keywords in template_items.items():
            if keywords:
                items.append(keywords[0])
        
        # 获取中文名称
        name = template.get('name', '')
        # 如果名称是通用格式（如'休闲搭配 32'），生成更友好的名称
        if not name or name.startswith('t_') or re.match(r'^.+搭配\s+\d+$', name):
            category = template.get('category', '搭配')
            occasions = template.get('occasions', ['日常'])
            occasion = occasions[0]
            # 避免重复
            if category == occasion or category in occasion:
                name = f"{occasion}风"
            else:
                name = f"{occasion}{category}风"
        
        return {
            "name": name,
            "items": items,
            "tips": template.get('tips', ''),
            "template_id": template.get('id'),
            "matched": False
        }
    
    def get_item_styles(self, item_name: str) -> List[Dict]:
        """
        一衣多穿 - 获取某件单品的多种搭配方式
        """
        # 找包含该单品的模板
        matching_templates = []
        
        for template in self.templates:
            items = template.get('items', {})
            for cat, keywords in items.items():
                for kw in keywords:
                    if kw in item_name or item_name in kw:
                        matching_templates.append(template)
                        break
        
        # 如果没找到，基于类别推荐
        if not matching_templates:
            # 判断单品类别
            category = self._guess_category(item_name)
            matching_templates = [t for t in self.templates 
                                 if category in str(t.get('items', {}))]
        
        return [self._format_template(t) for t in matching_templates[:5]]
    
    def _guess_category(self, item_name: str) -> str:
        """猜测单品类别"""
        keywords = {
            "outer": ["风衣", "大衣", "外套", "西装", "夹克", "羽绒服"],
            "top": ["T恤", "衬衫", "卫衣", "毛衣", "针织衫"],
            "bottom": ["裤", "裙", "牛仔裤", "休闲裤"],
            "shoes": ["鞋", "靴", "拖"],
            "accessory": ["包", "围巾", "帽子", "项链"]
        }
        
        for cat, words in keywords.items():
            for w in words:
                if w in item_name:
                    return cat
        
        return "top"
    def _get_outfit_image(self, template: Dict) -> Optional[str]:
        """根据模板获取对应的参考图片路径（返回 workspace 可访问路径）"""
        import glob
        import random
        import shutil
        
        category = template.get('category', '休闲')
        
        category_map = {
            '休闲': 'casual', '职场': 'business', '约会': 'date',
            '聚会': 'party', '运动': 'sport', '旅行': 'travel', '其他': 'casual'
        }
        
        prefix = category_map.get(category, 'casual')
        skill_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        image_dir = os.path.join(skill_dir, 'assets', 'images', 'outfits')
        
        images = glob.glob(os.path.join(image_dir, f'{prefix}_*.jpg'))
        if not images:
            images = glob.glob(os.path.join(image_dir, '*.jpg'))
        
        if images:
            selected = random.choice(images)
            # 使用相对路径存储图片
            workspace_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets', 'images', 'outfits')
            os.makedirs(workspace_dir, exist_ok=True)
            filename = os.path.basename(selected)
            workspace_path = os.path.join(workspace_dir, filename)
            if not os.path.exists(workspace_path):
                shutil.copy2(selected, workspace_path)
            return workspace_path
        
        return None
