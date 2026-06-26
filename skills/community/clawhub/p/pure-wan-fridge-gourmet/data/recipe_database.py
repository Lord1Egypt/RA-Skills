#!/usr/bin/env python3
"""
真实经典菜谱数据库
基于真实中餐/西餐经典菜谱，而非AI随意生成
"""

from typing import List, Dict, Any, Optional
import random

class RecipeDatabase:
    """
    真实菜谱数据库
    收录经过验证的经典家常菜做法
    """
    
    # 中式经典菜谱库
    CHINESE_RECIPES = [
        {
            "name": "番茄炒蛋",
            "name_en": "Tomato and Egg Stir-fry",
            "cuisine": "chinese",
            "difficulty": "easy",
            "time": "quick",
            "tags": ["家常", "快手菜", "下饭"],
            "ingredients": [
                {"name": "鸡蛋", "amount": "3个", "essential": True},
                {"name": "番茄", "amount": "2个中等大小", "essential": True},
                {"name": "葱花", "amount": "1根", "essential": False},
                {"name": "盐", "amount": "1/2茶匙", "essential": True},
                {"name": "白糖", "amount": "1茶匙", "essential": True},
                {"name": "食用油", "amount": "2汤匙", "essential": True}
            ],
            "steps": [
                {
                    "step": 1,
                    "title": "准备食材",
                    "content": "番茄洗净，顶部划十字，用开水烫10秒后去皮（也可不去皮），切成滚刀块。鸡蛋打入碗中，加1/4茶匙盐，用筷子充分搅打至起泡（约30秒）。",
                    "heat": "无",
                    "duration": "3分钟",
                    "tips": "蛋液充分搅打炒出来更蓬松"
                },
                {
                    "step": 2,
                    "title": "炒鸡蛋",
                    "content": "热锅凉油，大火烧至油温六成热（约160°C，油面微微波动），倒入蛋液。待蛋液底部凝固，用铲子轻轻推动，炒至七分熟（表面还有少许液态）盛出备用。",
                    "heat": "大火",
                    "duration": "30秒",
                    "tips": "不要炒太老，七分熟就要盛出"
                },
                {
                    "step": 3,
                    "title": "炒番茄",
                    "content": "锅中再加少许油，中火下番茄块翻炒。加1/4茶匙盐，炒至番茄出汁变软（约2分钟）。",
                    "heat": "中火",
                    "duration": "2分钟",
                    "tips": "加盐能加速番茄出汁"
                },
                {
                    "step": 4,
                    "title": "合炒调味",
                    "content": "倒入炒好的鸡蛋，加白糖提鲜，快速翻炒均匀。撒葱花，关火盛出。",
                    "heat": "中火",
                    "duration": "30秒",
                    "tips": "糖能中和番茄酸味，提鲜关键"
                }
            ],
            "cooking_tips": [
                "蛋液要充分搅打，炒出来才蓬松",
                "番茄去皮口感更好，但不去皮营养更丰富",
                "炒鸡蛋时油温要高，这样蛋才嫩滑"
            ],
            "flavor": "酸甜可口，蛋香浓郁，经典家常菜",
            "matching_ingredients": ["鸡蛋", "番茄", "西红柿"]
        },
        {
            "name": "青椒炒蛋",
            "name_en": "Green Pepper and Egg Stir-fry",
            "cuisine": "chinese",
            "difficulty": "easy",
            "time": "quick",
            "tags": ["家常", "快手菜", "下饭"],
            "ingredients": [
                {"name": "鸡蛋", "amount": "3个", "essential": True},
                {"name": "青椒", "amount": "2个", "essential": True},
                {"name": "盐", "amount": "1/2茶匙", "essential": True},
                {"name": "生抽", "amount": "1茶匙", "essential": False},
                {"name": "食用油", "amount": "2汤匙", "essential": True}
            ],
            "steps": [
                {
                    "step": 1,
                    "title": "准备食材",
                    "content": "青椒去蒂去籽，切成细丝或小块。鸡蛋打入碗中，加少许盐，充分搅打均匀。",
                    "heat": "无",
                    "duration": "3分钟",
                    "tips": "青椒去籽后不会太辣，口感更好"
                },
                {
                    "step": 2,
                    "title": "炒鸡蛋",
                    "content": "热锅倒油，大火烧至七成热，倒入蛋液。快速划散炒至凝固，呈块状盛出。",
                    "heat": "大火",
                    "duration": "40秒",
                    "tips": "油温要高，蛋液才能快速凝固蓬松"
                },
                {
                    "step": 3,
                    "title": "炒青椒",
                    "content": "锅中再加少许油，大火下青椒丝翻炒至断生（边缘微微透明，约1分钟）。",
                    "heat": "大火",
                    "duration": "1分钟",
                    "tips": "大火快炒保持青椒脆嫩"
                },
                {
                    "step": 4,
                    "title": "合炒出锅",
                    "content": "倒入炒好的鸡蛋，加少许生抽提鲜，快速翻炒均匀即可出锅。",
                    "heat": "大火",
                    "duration": "30秒",
                    "tips": "生抽从锅边淋入，激发香气"
                }
            ],
            "cooking_tips": [
                "青椒选薄皮的更嫩，厚皮的口感偏硬",
                "全程大火快炒，保持青椒脆嫩",
                "加一点点生抽能提鲜增色"
            ],
            "flavor": "青椒爽脆，蛋香浓郁，清淡下饭",
            "matching_ingredients": ["鸡蛋", "青椒", "辣椒"]
        },
        {
            "name": "黄瓜炒蛋",
            "name_en": "Cucumber and Egg Stir-fry",
            "cuisine": "chinese",
            "difficulty": "easy",
            "time": "quick",
            "tags": ["家常", "快手菜", "清淡"],
            "ingredients": [
                {"name": "鸡蛋", "amount": "2-3个", "essential": True},
                {"name": "黄瓜", "amount": "1根", "essential": True},
                {"name": "盐", "amount": "1/2茶匙", "essential": True},
                {"name": "食用油", "amount": "2汤匙", "essential": True},
                {"name": "葱花", "amount": "少许", "essential": False}
            ],
            "steps": [
                {
                    "step": 1,
                    "title": "准备食材",
                    "content": "黄瓜洗净，切成薄片或菱形片（不要太薄，炒后会缩水）。鸡蛋打散，加少许盐搅匀。",
                    "heat": "无",
                    "duration": "3分钟",
                    "tips": "黄瓜切稍厚一点，炒后口感更好"
                },
                {
                    "step": 2,
                    "title": "炒鸡蛋",
                    "content": "热锅倒油，中大火烧至六成热，倒入蛋液。炒至凝固成块，盛出备用。",
                    "heat": "中大火",
                    "duration": "40秒",
                    "tips": "油温不要太高，以免蛋焦"
                },
                {
                    "step": 3,
                    "title": "炒黄瓜",
                    "content": "锅中余油，大火下黄瓜片快速翻炒约1分钟至断生（边缘微微透明）。",
                    "heat": "大火",
                    "duration": "1分钟",
                    "tips": "大火快炒保持黄瓜脆嫩"
                },
                {
                    "step": 4,
                    "title": "合炒调味",
                    "content": "倒入鸡蛋，加盐调味，快速翻炒均匀。撒葱花，出锅。",
                    "heat": "大火",
                    "duration": "30秒",
                    "tips": "不要炒太久，黄瓜要保持脆爽"
                }
            ],
            "cooking_tips": [
                "黄瓜不要切太薄，炒后会缩水变软",
                "全程大火快炒，黄瓜才脆嫩",
                "不要加水，黄瓜本身会出水"
            ],
            "flavor": "黄瓜清脆，蛋香淡雅，清爽解腻",
            "matching_ingredients": ["鸡蛋", "黄瓜"]
        },
        {
            "name": "胡萝卜炒蛋",
            "name_en": "Carrot and Egg Stir-fry",
            "cuisine": "chinese",
            "difficulty": "easy",
            "time": "quick",
            "tags": ["家常", "快手菜", "营养"],
            "ingredients": [
                {"name": "鸡蛋", "amount": "2-3个", "essential": True},
                {"name": "胡萝卜", "amount": "1根", "essential": True},
                {"name": "盐", "amount": "1/2茶匙", "essential": True},
                {"name": "食用油", "amount": "2汤匙", "essential": True},
                {"name": "葱花", "amount": "少许", "essential": False}
            ],
            "steps": [
                {
                    "step": 1,
                    "title": "准备食材",
                    "content": "胡萝卜去皮，先切片再切丝（或用擦丝器）。鸡蛋打散，加少许盐搅匀。",
                    "heat": "无",
                    "duration": "4分钟",
                    "tips": "胡萝卜丝切细一点，熟得快"
                },
                {
                    "step": 2,
                    "title": "炒鸡蛋",
                    "content": "热锅倒油，中火烧至六成热，倒入蛋液。炒至凝固成块，盛出备用。",
                    "heat": "中火",
                    "duration": "40秒",
                    "tips": "油温不要太高，中火慢炒蛋更嫩"
                },
                {
                    "step": 3,
                    "title": "炒胡萝卜",
                    "content": "锅中再加少许油，中火下胡萝卜丝翻炒2-3分钟至变软（可以尝一下，不生硬即可）。",
                    "heat": "中火",
                    "duration": "3分钟",
                    "tips": "胡萝卜要炒软才好吃，多炒一会儿"
                },
                {
                    "step": 4,
                    "title": "合炒出锅",
                    "content": "倒入炒好的鸡蛋，加盐调味，翻炒均匀。撒葱花，出锅。",
                    "heat": "中火",
                    "duration": "30秒",
                    "tips": "调味简单，突出食材本味"
                }
            ],
            "cooking_tips": [
                "胡萝卜丝要切细，熟得快",
                "胡萝卜要炒软才好吃，不生硬",
                "可以加一点点糖，激发胡萝卜的甜味"
            ],
            "flavor": "胡萝卜甜软，蛋香浓郁，营养丰富",
            "matching_ingredients": ["鸡蛋", "胡萝卜"]
        },
        {
            "name": "洋葱炒蛋",
            "name_en": "Onion and Egg Stir-fry",
            "cuisine": "chinese",
            "difficulty": "easy",
            "time": "quick",
            "tags": ["家常", "快手菜", "香甜"],
            "ingredients": [
                {"name": "鸡蛋", "amount": "3个", "essential": True},
                {"name": "洋葱", "amount": "1个中等大小", "essential": True},
                {"name": "盐", "amount": "1/2茶匙", "essential": True},
                {"name": "食用油", "amount": "2汤匙", "essential": True},
                {"name": "生抽", "amount": "1茶匙", "essential": False}
            ],
            "steps": [
                {
                    "step": 1,
                    "title": "准备食材",
                    "content": "洋葱去皮，切成细丝（切的时候刀上沾点水，减少刺激）。鸡蛋打散，加少许盐搅匀。",
                    "heat": "无",
                    "duration": "4分钟",
                    "tips": "切洋葱时刀沾水，减少流泪"
                },
                {
                    "step": 2,
                    "title": "炒鸡蛋",
                    "content": "热锅倒油，中火烧至六成热，倒入蛋液。炒至凝固成块，盛出备用。",
                    "heat": "中火",
                    "duration": "40秒",
                    "tips": "不要炒太老，嫩一点更好吃"
                },
                {
                    "step": 3,
                    "title": "炒洋葱",
                    "content": "锅中再加少许油，中火下洋葱丝翻炒2-3分钟至变软变透明，边缘微焦出香味。",
                    "heat": "中火",
                    "duration": "3分钟",
                    "tips": "洋葱要炒软，甜味才能出来"
                },
                {
                    "step": 4,
                    "title": "合炒调味",
                    "content": "倒入炒好的鸡蛋，加少许生抽（可选），加盐调味，翻炒均匀出锅。",
                    "heat": "中火",
                    "duration": "30秒",
                    "tips": "洋葱本身有甜味，不用加糖"
                }
            ],
            "cooking_tips": [
                "洋葱要炒软才甜，不要急",
                "紫洋葱比白洋葱更适合炒菜",
                "洋葱炒蛋可以加少许胡椒粉，更香"
            ],
            "flavor": "洋葱甜软，蛋香浓郁，略带甜味",
            "matching_ingredients": ["鸡蛋", "洋葱"]
        },
        {
            "name": "时蔬杂炒",
            "name_en": "Mixed Vegetable Stir-fry",
            "cuisine": "chinese",
            "difficulty": "easy",
            "time": "quick",
            "tags": ["家常", "快手菜", "健康"],
            "ingredients": [
                {"name": "鸡蛋", "amount": "2个", "essential": True},
                {"name": "时令蔬菜", "amount": "300克", "essential": True, "note": "黄瓜、胡萝卜、青椒、洋葱等随意搭配"},
                {"name": "大蒜", "amount": "2瓣", "essential": False},
                {"name": "盐", "amount": "1/2茶匙", "essential": True},
                {"name": "食用油", "amount": "2汤匙", "essential": True},
                {"name": "生抽", "amount": "1茶匙", "essential": False}
            ],
            "steps": [
                {
                    "step": 1,
                    "title": "准备食材",
                    "content": "各种蔬菜洗净，切成大小均匀的片或丝（黄瓜切片、胡萝卜切丝、青椒切块、洋葱切丝）。鸡蛋打散备用。大蒜拍碎切末。",
                    "heat": "无",
                    "duration": "5分钟",
                    "tips": "蔬菜切均匀，熟成度一致"
                },
                {
                    "step": 2,
                    "title": "炒鸡蛋",
                    "content": "热锅倒油，大火烧至七成热，倒入蛋液。快速炒散至凝固，盛出备用。",
                    "heat": "大火",
                    "duration": "30秒",
                    "tips": "油温要高，蛋才蓬松"
                },
                {
                    "step": 3,
                    "title": "炒蔬菜",
                    "content": "锅中再加少许油，大火爆香蒜末。先下胡萝卜丝炒1分钟，再下青椒、洋葱炒1分钟，最后下黄瓜片炒30秒。",
                    "heat": "大火",
                    "duration": "2分30秒",
                    "tips": "按蔬菜熟成度依次下锅，胡萝卜最先，黄瓜最后"
                },
                {
                    "step": 4,
                    "title": "合炒调味",
                    "content": "倒入炒好的鸡蛋，加少许生抽和盐，快速翻炒均匀即可出锅。",
                    "heat": "大火",
                    "duration": "30秒",
                    "tips": "大火快炒保持蔬菜脆嫩"
                }
            ],
            "cooking_tips": [
                "蔬菜按熟成度先后下锅：胡萝卜>青椒/洋葱>黄瓜",
                "全程大火快炒，保持蔬菜脆嫩和颜色",
                "调味料简单，突出蔬菜本味"
            ],
            "flavor": "蔬菜脆嫩，色彩缤纷，清淡健康",
            "matching_ingredients": ["鸡蛋", "黄瓜", "胡萝卜", "青椒", "洋葱"]
        }
    ]
    
    @classmethod
    def match_recipe(cls, ingredients: List[str], cuisine: str = "chinese", 
                     difficulty: str = "easy", time_limit: str = "quick") -> Optional[Dict[str, Any]]:
        """
        根据食材匹配菜谱
        
        Args:
            ingredients: 用户拥有的食材列表
            cuisine: 菜系偏好
            difficulty: 难度要求
            time_limit: 时间要求
            
        Returns:
            匹配的菜谱，如果没有则返回None
        """
        # 标准化食材名称
        normalized_ingredients = set()
        for ing in ingredients:
            ing = ing.lower().strip()
            # 常见同义词映射
            if ing in ["西红柿", "番茄"]:
                normalized_ingredients.add("番茄")
            elif ing in ["青辣椒", "青椒", "尖椒"]:
                normalized_ingredients.add("青椒")
            else:
                normalized_ingredients.add(ing)
        
        matched_recipes = []
        
        # 遍历菜谱库匹配
        for recipe in cls.CHINESE_RECIPES:
            # 检查菜系匹配
            if recipe["cuisine"] != cuisine and cuisine != "chinese":
                continue
                
            # 检查难度和时间
            if recipe["difficulty"] != difficulty and difficulty != "easy":
                continue
            if recipe["time"] != time_limit and time_limit != "quick":
                continue
            
            # 计算食材匹配度
            essential_ings = [ing["name"] for ing in recipe["ingredients"] if ing.get("essential", False)]
            matching_count = sum(1 for ing in essential_ings if any(
                ing in user_ing or user_ing in ing 
                for user_ing in normalized_ingredients
            ))
            
            # 如果主要食材都匹配，加入候选
            if matching_count >= len(essential_ings) * 0.8:  # 80%的主要食材匹配即可
                matched_recipes.append({
                    "recipe": recipe,
                    "match_score": matching_count / len(essential_ings)
                })
        
        # 按匹配度排序，返回最佳匹配
        if matched_recipes:
            matched_recipes.sort(key=lambda x: x["match_score"], reverse=True)
            return matched_recipes[0]["recipe"]
        
        return None
    
    @classmethod
    def get_random_recipe(cls, cuisine: str = "chinese") -> Dict[str, Any]:
        """随机获取一个菜谱（用于展示）"""
        recipes = [r for r in cls.CHINESE_RECIPES if r["cuisine"] == cuisine or cuisine == "chinese"]
        return random.choice(recipes) if recipes else None
    
    @classmethod
    def format_recipe_for_display(cls, recipe: Dict[str, Any]) -> Dict[str, Any]:
        """将数据库菜谱格式化为显示格式"""
        return {
            "name": recipe["name"],
            "flavor_description": recipe["flavor"],
            "ingredients": [f"{ing['name']}：{ing['amount']}" + (f"（{ing.get('note', '')}）" if ing.get('note') else "") 
                          for ing in recipe["ingredients"]],
            "steps": [f"{step['step']}. {step['title']}：{step['content']}\n   【火候】{step['heat']} | 【时长】{step['duration']}\n   💡 {step['tips']}" 
                     for step in recipe["steps"]],
            "tips": recipe["cooking_tips"],
            "source": "经典菜谱库",
            "is_authentic": True
        }


# 烹饪技法知识库
class CookingTechniques:
    """中式烹饪技法详解"""
    
    HEAT_LEVELS = {
        "大火": {
            "temperature": "180-200°C",
            "description": "油面有大量青烟，食材入锅有剧烈滋滋声",
            "use_case": "爆炒、快炒、焯水、油炸",
            "tips": "动作要快，不断翻动，防止焦糊"
        },
        "中火": {
            "temperature": "140-160°C", 
            "description": "油面微微波动，有少量青烟",
            "use_case": "煎、炒、煮、焖",
            "tips": "适合大多数炒菜，能均匀受热"
        },
        "小火": {
            "temperature": "80-100°C",
            "description": "油面平静，偶有细小气泡",
            "use_case": "慢炖、煨、保温、熬酱",
            "tips": "长时间烹饪，保持汤汁微沸即可"
        },
        "文火": {
            "temperature": "60-80°C",
            "description": "几乎看不到油动，只有细微涟漪",
            "use_case": "炖汤、熬膏、保温",
            "tips": "最小火力，保持温度不沸腾"
        }
    }
    
    SEASONING_ORDER = {
        "基础调味": ["盐", "糖", "鸡精/味精"],
        "提鲜调味": ["生抽", "蚝油", "蒸鱼豉油"],
        "增香调味": ["料酒", "醋", "香油"],
        "风味调味": ["豆瓣酱", "辣椒酱", "花椒粉", "五香粉"]
    }
    
    DONENESS_SIGNS = {
        "断生": "蔬菜边缘变透明，无生硬口感，但仍有脆度",
        "七成熟": "食材表面变色定型，内部还有少许生色",
        "全熟": "食材完全变色，质地变软，无生硬感",
        "焦香": "表面微黄有焦色斑点，散发香气"
    }
