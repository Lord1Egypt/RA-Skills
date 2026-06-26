#!/usr/bin/env python3
"""
Pure Wan Fridge Gourmet - 纯血万相冰箱盲盒 v2.0
基于 Wan2.7/Wan2.1 视觉大模型的烹饪灵感触发器

本脚本 100% 使用 Wan 系列 API（阿里云 DashScope），未调用任何第三方 LLM。
支持图像生成 + 智能菜谱生成
支持异步任务提交和轮询查询。
支持参数：菜系、难易程度、烹饪时间
"""

import os
import sys
import base64
import json
import time
import requests
from typing import Optional, Dict, Any, List

# 导入真实菜谱数据库
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'data'))
try:
    from recipe_database import RecipeDatabase, CookingTechniques
    HAS_RECIPE_DB = True
except ImportError:
    HAS_RECIPE_DB = False
    print("⚠️ 菜谱数据库未找到，将使用AI生成模式")


class WanFridgeGourmet:
    """
    纯血万相冰箱盲盒核心类
    
    使用 Wan 系列 API（阿里云 DashScope）将冰箱照片转化为米其林级美食概念图 + 完整菜谱
    支持菜系、难易程度、烹饪时间等参数定制
    """
    
    # 支持的模型版本
    MODEL_VERSIONS = {
        "2.1-t2i": "wanx2.1-t2i-plus",           # 万相2.1 文生图
        "2.1-t2i-free": "wanx2.1-t2i-free",      # 万相2.1 文生图免费版
        "2.1-i2v": "wanx2.1-i2v-plus",           # 万相2.1 图生视频
        "2.1-t2v": "wanx2.1-t2v-plus",           # 万相2.1 文生视频
        "2.7": "wan2.7-image-pro",               # 万相2.7 图生图
        "2.7-t2i": "wan2.6-t2i",                   # 万相2.7 文生图（新增！）
    }
    
    # 扩展的菜系提示词映射 - 更丰富的选择
    CUISINE_PROMPTS = {
        # ===== 中式八大菜系 =====
        "chinese": {
            "name": "中式料理",
            "prompt": "Chinese cuisine style, traditional Chinese ceramic plate, precise knife work, steam wisps, soy sauce glaze, scallion garnish, wok hei aroma visualized, traditional meets contemporary presentation"
        },
        "sichuan": {
            "name": "川菜",
            "prompt": "Sichuan cuisine style, red chili oil, numbing Sichuan peppercorns, vibrant red presentation, steaming hot pot aesthetic, bold spicy flavors, rustic earthenware serving dishes"
        },
        "cantonese": {
            "name": "粤菜",
            "prompt": "Cantonese dim sum style, delicate steamed dumplings, bamboo steamer baskets, light soy sauce dip, refined presentation, fresh seafood emphasis, traditional tea house atmosphere"
        },
        "hunan": {
            "name": "湘菜",
            "prompt": "Hunan cuisine style, smoky chili flavors, fermented black beans, steaming hot clay pot, bold red and green colors, hearty presentation, farm-to-table rustic feel"
        },
        "shandong": {
            "name": "鲁菜",
            "prompt": "Shandong cuisine style, imperial court presentation, clear broth elegance, seafood emphasis, precise knife work, light golden sauces, traditional northern Chinese aesthetic"
        },
        "jiangsu": {
            "name": "苏菜/淮扬菜",
            "prompt": "Jiangsu Huaiyang cuisine style, exquisite knife sculpture, sweet and sour balance, light soup presentation, artistic vegetable carving, refined Jiangnan aesthetic, pale color palette"
        },
        "fujian": {
            "name": "闽菜",
            "prompt": "Fujian cuisine style, seafood soup emphasis, red vinasse wine flavor, light broth, bamboo shoot ingredients, coastal freshness, subtle umami presentation"
        },
        "zhejiang": {
            "name": "浙菜",
            "prompt": "Zhejiang cuisine style, freshwater fish emphasis, tender texture, light seasoning, West Lake inspired presentation, elegant simplicity, fresh green garnish"
        },
        "anhui": {
            "name": "徽菜",
            "prompt": "Anhui cuisine style, wild mountain herbs, bamboo shoots, stewed in ceramic pots, dark soy caramelization, rustic farmhouse presentation, earthy color tones"
        },
        "beijing": {
            "name": "京菜/宫廷菜",
            "prompt": "Beijing imperial cuisine style, Peking duck presentation, elaborate court dishes, golden serving platters, auspicious red and gold colors, ceremonial presentation"
        },
        "xi'an": {
            "name": "西北菜/陕菜",
            "prompt": "Northwestern Chinese cuisine style, hand-pulled noodles, lamb skewers, hearty bread accompaniments, bold cumin spices, rustic metal serving plates, Silk Road aesthetic"
        },
        "yunnan": {
            "name": "云南菜",
            "prompt": "Yunnan cuisine style, wild mushrooms, crossing bridge noodles presentation, ethnic minority influences, fresh herbs and flowers, colorful pottery, highland freshness"
        },
        "guizhou": {
            "name": "贵州菜",
            "prompt": "Guizhou cuisine style, sour soup base, fermented flavors, wild herbs, spicy and sour balance, ethnic Miao/Dong influences, rustic wooden serving bowls"
        },
        
        # ===== 日韩 =====
        "japanese": {
            "name": "日式料理",
            "prompt": "Japanese kaiseki-style, minimalist plating, zen aesthetic, seasonal ingredients, ceramic dishware, soft natural lighting, delicate presentation"
        },
        "sushi": {
            "name": "寿司/刺身",
            "prompt": "Premium sushi omakase style, fresh sashimi slices, perfectly formed nigiri, black lacquer plates, wasabi and ginger garnish, sushi bar counter presentation, Japanese ceramic soy sauce dish"
        },
        "ramen": {
            "name": "拉面",
            "prompt": "Authentic Japanese ramen bowl, rich tonkotsu broth, chashu pork slices, soft-boiled egg, nori sheets, bamboo shoots, steam rising, wooden chopsticks, izakaya atmosphere"
        },
        "korean": {
            "name": "韩式料理",
            "prompt": "Korean cuisine style, sizzling hot plate, gochujang glaze, sesame seeds garnish, colorful banchan arrangement, modern Korean presentation"
        },
        "korean-bbq": {
            "name": "韩式烤肉",
            "prompt": "Korean BBQ style, sizzling grill pan, marinated bulgogi or galbi, lettuce wraps, ssamjang dipping sauce, banchan side dishes, tabletop grilling atmosphere, sizzling smoke wisps"
        },
        
        # ===== 东南亚 =====
        "thai": {
            "name": "泰式料理",
            "prompt": "Thai cuisine style, vibrant tropical colors, coconut curry sauce, fresh lime and chili garnish, banana leaf plating, exotic presentation"
        },
        "vietnamese": {
            "name": "越南菜",
            "prompt": "Vietnamese cuisine style, fresh spring rolls, pho noodle soup, fresh herbs (cilantro, mint, basil), light fish sauce dressing, banana leaf presentation, street food authenticity"
        },
        "singapore": {
            "name": "新加坡菜/东南亚融合",
            "prompt": "Singapore hawker style, Hainanese chicken rice or laksa, vibrant multi-cultural presentation, banana leaf base, chili sauce accompaniments, tropical open-air food court atmosphere"
        },
        "malaysian": {
            "name": "马来西亚菜",
            "prompt": "Malaysian cuisine style, nasi lemak presentation, sambal chili, coconut rice, banana leaf wrapping, vibrant blue butterfly pea rice, street food authenticity"
        },
        "indonesian": {
            "name": "印尼菜",
            "prompt": "Indonesian cuisine style, nasi goreng fried rice, satay skewers, peanut sauce, krupuk crackers, tropical fruit garnish, woven basket serving, island spice aesthetic"
        },
        "burmese": {
            "name": "缅甸菜",
            "prompt": "Burmese cuisine style, mohinga fish noodle soup, tea leaf salad, earthy spice palette, lacquerware serving bowls, golden pagoda-inspired presentation"
        },
        
        # ===== 南亚 =====
        "indian": {
            "name": "印度菜",
            "prompt": "Indian cuisine style, rich curry sauces, golden turmeric colors, tandoori char marks, fresh naan bread, brass serving ware, aromatic spice blend visualized, warm ambient lighting"
        },
        "indian-south": {
            "name": "南印度菜",
            "prompt": "South Indian cuisine style, crispy dosa, sambar lentils, coconut chutney, banana leaf plate, temple feast presentation, golden ghee accents"
        },
        "sri-lankan": {
            "name": "斯里兰卡菜",
            "prompt": "Sri Lankan cuisine style, coconut curry, string hoppers, vibrant spice colors, tropical fruit accents, brass curry bowls, island paradise aesthetic"
        },
        
        # ===== 西式 =====
        "western": {
            "name": "西式料理",
            "prompt": "Western cuisine style, elegant white porcelain plate, butter sauce, herb garnish, roasted vegetables, classic fine dining presentation"
        },
        "french": {
            "name": "法式料理",
            "prompt": "French haute cuisine, artistic sauce drizzles, microgreens garnish, white porcelain, fine dining atmosphere, sophisticated plating"
        },
        "italian": {
            "name": "意式料理",
            "prompt": "Italian trattoria style, rustic family-style plating, rich tomato sauces, fresh herbs, wooden table background, warm golden lighting"
        },
        "italian-pasta": {
            "name": "意面专门",
            "prompt": "Italian pasta specialty, perfectly al dente noodles twirled, rich cream or tomato sauce, fresh basil and parmesan, rustic ceramic bowl, red checkered tablecloth suggestion, trattoria warmth"
        },
        "pizza": {
            "name": "披萨",
            "prompt": "Neapolitan pizza style, leopard-spotted charred crust, bubbling mozzarella, fresh basil leaves, San Marzano tomato sauce, wood-fired oven aesthetic, rustic wooden peel"
        },
        "american": {
            "name": "美式料理",
            "prompt": "American comfort food style, generous portions, classic burger or steak, golden fries side, diner aesthetic, bold satisfying presentation, modern gastropub twist"
        },
        "american-bbq": {
            "name": "美式BBQ",
            "prompt": "American BBQ smokehouse style, slow-smoked brisket or ribs, pink smoke ring, rich dark bark, tangy sauce glaze, rustic wooden board, smoke wisps, backyard cookout atmosphere"
        },
        "mexican": {
            "name": "墨西哥菜",
            "prompt": "Mexican cuisine style, vibrant colorful presentation, fresh tortillas, salsa and guacamole, lime wedges, clay pottery serving, fiesta atmosphere, bold chili colors"
        },
        "spanish": {
            "name": "西班牙菜",
            "prompt": "Spanish tapas style, paella in traditional pan, saffron golden rice, seafood medley, rustic ceramic plates, sherry accompaniment, warm Mediterranean atmosphere"
        },
        "greek": {
            "name": "希腊菜/地中海",
            "prompt": "Greek Mediterranean style, fresh feta cheese, olive oil drizzle, ripe tomatoes and cucumbers, oregano garnish, blue and white aesthetic, Aegean seaside freshness"
        },
        "mediterranean": {
            "name": "地中海料理",
            "prompt": "Mediterranean diet style, olive oil richness, fresh vegetables, grilled fish, lemon accents, herbs de Provence, sun-bleached colors, coastal wellness aesthetic"
        },
        "german": {
            "name": "德国菜",
            "prompt": "German cuisine style, hearty schnitzel or sausages, golden potato sides, rustic ceramic beer stein, pretzel accompaniment, beer hall atmosphere, Bavarian warmth"
        },
        "british": {
            "name": "英式料理",
            "prompt": "British gastropub style, fish and chips, mushy peas, malt vinegar, newspaper wrapping aesthetic, cozy pub atmosphere, comfort food heartiness"
        },
        "scandinavian": {
            "name": "北欧菜",
            "prompt": "Nordic cuisine style, foraged ingredients, fermented elements, minimalist white plates, natural wood accents, hygge atmosphere, New Nordic culinary philosophy"
        },
        "russian": {
            "name": "俄式料理",
            "prompt": "Russian cuisine style, hearty borscht, sour cream dollop, dark rye bread, intricate ceramic patterns, winter warmth, babushka kitchen nostalgia"
        },
        "portuguese": {
            "name": "葡萄牙菜",
            "prompt": "Portuguese cuisine style, salted cod preparation, olive oil richness, rustic pottery, Atlantic coastal freshness, azulejo blue patterns"
        },
        
        # ===== 中东风味 =====
        "turkish": {
            "name": "土耳其菜",
            "prompt": "Turkish cuisine style, kebab presentation, yogurt sauce, sumac and paprika, flatbread accompaniment, ornate copper serving ware, bazaar spice atmosphere"
        },
        "lebanese": {
            "name": "黎巴嫩菜/中东",
            "prompt": "Lebanese mezze style, hummus and falafel, tahini drizzle, fresh pita bread, colorful mezze spread, Mediterranean warmth, traditional arabesque patterns"
        },
        "moroccan": {
            "name": "摩洛哥菜",
            "prompt": "Moroccan tagine style, conical clay pot, preserved lemons, olives, saffron and cinnamon spices, ornate metalwork tray, Sahara desert warmth, intricate geometric patterns"
        },
        "persian": {
            "name": "波斯菜/伊朗",
            "prompt": "Persian cuisine style, jeweled rice, saffron golden chicken, barberries, ornate silver serving platters, rose water essence, ancient Silk Road elegance"
        },
        "israeli": {
            "name": "以色列菜",
            "prompt": "Israeli modern cuisine style, vibrant vegetable-forward presentation, tahini and olive oil, fresh herbs abundance, contemporary Tel Aviv restaurant aesthetic"
        },
        
        # ===== 非洲 =====
        "ethiopian": {
            "name": "埃塞俄比亚菜",
            "prompt": "Ethiopian cuisine style, injera flatbread base, colorful wot stews, communal sharing platter, rich berbere spice, traditional woven basket serving"
        },
        "south-african": {
            "name": "南非菜",
            "prompt": "South African braai style, grilled meats, chakalaka relish, maize pap, outdoor barbecue atmosphere, rainbow nation warmth"
        },
        "nigerian": {
            "name": "尼日利亚菜/西非",
            "prompt": "West African cuisine style, jollof rice vibrant red, grilled suya skewers, plantain sides, bold spice flavors, traditional patterns"
        },
        
        # ===== 澳洲/其他 =====
        "australian": {
            "name": "澳洲料理",
            "prompt": "Modern Australian cuisine style, indigenous ingredients, beach barbecue aesthetic, fresh seafood, contemporary casual elegance, outdoor lifestyle"
        },
        "caribbean": {
            "name": "加勒比菜",
            "prompt": "Caribbean cuisine style, jerk spice char, coconut rice, tropical fruit salsa, beach shack atmosphere, reggae colors, island spice and sunshine"
        },
        "brazilian": {
            "name": "巴西菜",
            "prompt": "Brazilian churrasco style, grilled meat skewers, feijoada black bean stew, caipirinha freshness, carnival colors, tropical exuberance"
        },
        "peruvian": {
            "name": "秘鲁菜",
            "prompt": "Peruvian ceviche style, fresh raw fish, lime and chili tiger's milk, purple corn accents, Andean and coastal fusion, vibrant South American colors"
        },
        "argentinian": {
            "name": "阿根廷菜",
            "prompt": "Argentinian asado style, grass-fed beef, chimichurri sauce, empanadas, Malbec wine pairing, gaucho tradition, South American passion"
        },
        
        # ===== 融合/现代 =====
        "fusion": {
            "name": "融合料理",
            "prompt": "Fusion cuisine combining Eastern and Western techniques, unexpected flavor pairings, avant-garde plating, dramatic shadows, innovative presentation"
        },
        "molecular": {
            "name": "分子料理",
            "prompt": "Molecular gastronomy style, edible spheres, foam garnishes, liquid nitrogen mist, deconstructed elements, laboratory-meets-kitchen aesthetic, avant-garde culinary art"
        },
        "plant-based": {
            "name": "植物基/素食",
            "prompt": "Plant-based gourmet style, vibrant vegetables as centerpieces, creative meat alternatives, sustainable elegance, farmers market freshness, ethical luxury presentation"
        },
        "raw": {
            "name": "生食/健康",
            "prompt": "Raw vegan cuisine style, uncooked natural ingredients, vibrant living colors, edible flowers, spiralized vegetables, wellness aesthetic, pure and clean presentation"
        },
    }
    
    # 难易程度提示词映射
    DIFFICULTY_PROMPTS = {
        "easy": {
            "name": "简单快手",
            "prompt": "Simple home cooking style, minimal preparation steps, easy-to-find ingredients, straightforward plating, beginner-friendly dish",
            "recipe_level": "新手友好，步骤简单，30分钟内完成"
        },
        "medium": {
            "name": "适中难度",
            "prompt": "Intermediate cooking level, balanced technique and flavor, moderate preparation complexity, appealing presentation",
            "recipe_level": "需要一定烹饪基础，步骤适中，注意火候和调味"
        },
        "hard": {
            "name": "挑战级",
            "prompt": "Advanced culinary technique, complex preparation steps, professional chef-level execution, sophisticated molecular gastronomy elements",
            "recipe_level": "专业级难度，需要精湛刀工和精准火候控制，耗时较长"
        }
    }
    
    # 烹饪时间提示词映射
    TIME_PROMPTS = {
        "quick": {
            "name": "快手菜（15分钟内）",
            "prompt": "Quick 15-minute recipe, stir-fry or raw preparation, fresh ingredients, minimal cooking time, fast casual style",
            "time_range": "10-15分钟"
        },
        "moderate": {
            "name": "适中（30-45分钟）",
            "prompt": "30-45 minute cooking time, balanced preparation and cooking, medium complexity, home dinner style",
            "time_range": "30-45分钟"
        },
        "slow": {
            "name": "慢炖/精煮（1小时以上）",
            "prompt": "Slow cooking 1+ hour, braised or stewed dish, deep flavors developed over time, tender texture, weekend cooking project",
            "time_range": "1-2小时"
        }
    }
    
    def __init__(self, api_key: Optional[str] = None, api_url: Optional[str] = None, model_version: str = "2.7"):
        """
        初始化 WanFridgeGourmet
        
        Args:
            api_key: DashScope API Key，如未提供则从环境变量 WAN_API_KEY 读取
            api_url: DashScope API 端点，如未提供则使用默认端点
            model_version: 模型版本，可选 "2.1-t2i", "2.1-t2i-free", "2.1-i2v", "2.1-t2v", "2.7"（默认 "2.7"）
        """
        self.api_key = api_key or os.environ.get("WAN_API_KEY")
        self.api_url = api_url or os.environ.get(
            "WAN_API_URL", 
            "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation"
        )
        self.model_version = model_version
        self.model_name = self.MODEL_VERSIONS.get(model_version, self.MODEL_VERSIONS["2.7"])
        
        if not self.api_key:
            raise ValueError(
                "API Key 未设置。请通过参数传入或设置环境变量 WAN_API_KEY"
            )
    
    def _encode_image(self, image_path: str) -> str:
        """将图片文件转为 base64 编码"""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    def _build_prompt(
        self,
        cuisine: str = "chinese",
        difficulty: str = "medium",
        cooking_time: str = "moderate",
        custom_requirements: Optional[str] = None,
        recipe: Optional[Dict] = None
    ) -> str:
        """
        构建完整的提示词
        
        Args:
            cuisine: 菜系代码
            difficulty: 难易程度 (easy/medium/hard)
            cooking_time: 烹饪时间 (quick/moderate/slow)
            custom_requirements: 额外自定义要求
            recipe: 已生成的菜谱信息（用于指导图像生成）
            
        Returns:
            完整的提示词字符串
        """
        # 获取各部分提示词
        cuisine_info = self.CUISINE_PROMPTS.get(cuisine, self.CUISINE_PROMPTS["chinese"])
        difficulty_info = self.DIFFICULTY_PROMPTS.get(difficulty, self.DIFFICULTY_PROMPTS["medium"])
        time_info = self.TIME_PROMPTS.get(cooking_time, self.TIME_PROMPTS["moderate"])
        
        # 如果有菜谱信息，构建强约束提示词
        if recipe and not recipe.get("error"):
            dish_name = recipe.get("name", "")
            ingredients = recipe.get("ingredients", [])
            steps = recipe.get("steps", [])
            
            # 提取关键食材（前6个）
            key_ingredients = []
            for ing in ingredients[:6]:
                # 简化食材描述，去掉用量和括号内容
                ing_name = ing.split("：")[0] if "：" in ing else ing.split("|")[0] if "|" in ing else ing
                ing_name = ing_name.split("（")[0].split("(")[0] if "（" in ing or "(" in ing else ing_name
                ing_name = ing_name.strip()
                if ing_name and len(ing_name) < 20 and ing_name not in key_ingredients:
                    key_ingredients.append(ing_name)
            
            # 提取烹饪方式和菜品类型
            cooking_method = "plated dish"
            dish_type = "main course"
            
            if steps:
                step_text = " ".join(steps[:3]).lower()
                if any(word in step_text for word in ["炒", "stir-fry", "sauté", "爆炒"]):
                    cooking_method = "stir-fried"
                    dish_type = "stir-fry dish"
                elif any(word in step_text for word in ["煎", "pan-fry", "煎蛋", "fry"]):
                    cooking_method = "pan-fried"
                    dish_type = "pan-fried dish"
                elif any(word in step_text for word in ["烤", "bake", "roast", "oven"]):
                    cooking_method = "roasted"
                    dish_type = "roasted dish"
                elif any(word in step_text for word in ["蒸", "steam", "steamed"]):
                    cooking_method = "steamed"
                    dish_type = "steamed dish"
                elif any(word in step_text for word in ["卷", "wrap", "roll", "卷成"]):
                    cooking_method = "rolled"
                    dish_type = "rolled wrap or roll"
                elif any(word in step_text for word in ["沙拉", "salad", "凉拌", "拌", "mix"]):
                    cooking_method = "fresh raw"
                    dish_type = "fresh salad"
                elif any(word in step_text for word in ["汤", "soup", "炖", "stew", "braise"]):
                    cooking_method = "simmered"
                    dish_type = "soup or stew"
            
            # 构建强约束提示词
            ingredients_str = ", ".join(key_ingredients[:6]) if key_ingredients else "fresh vegetables"
            
            # 根据菜品类型添加具体的摆盘描述
            plating_description = ""
            negative_prompt = ""
            if "salad" in dish_type.lower():
                plating_description = "Fresh colorful salad in a white bowl, mixed raw vegetables with dressing, cold dish"
                negative_prompt = "NO cooked meat, NO fish, NO hot dish, NO grilled items, NO roasted meat"
            elif "roll" in dish_type.lower() or "wrap" in dish_type.lower():
                plating_description = "Elegant rolled wraps on a plate, cut to show colorful fillings inside"
                negative_prompt = "NO whole fish, NO meat slab, NO plain plate"
            elif "soup" in dish_type.lower():
                plating_description = "Soup or stew in a bowl with visible broth, liquid-based dish"
                negative_prompt = "NO dry dishes, NO plain plate"
            elif "stir-fry" in dish_type.lower():
                plating_description = "Stir-fried dish on a plate, wok-cooked appearance with sauce"
                negative_prompt = "NO raw vegetables, NO uncooked items"
            
            # 构建最强约束提示词 - 万相2.7专用格式（中文提示词版）
            # 根据菜品类型添加中文描述
            dish_type_cn = "菜品"
            if "salad" in dish_type.lower():
                dish_type_cn = "沙拉碗"
            elif "soup" in dish_type.lower():
                dish_type_cn = "汤品"
            elif "roll" in dish_type.lower() or "wrap" in dish_type.lower():
                dish_type_cn = "卷类"
            elif "stir-fry" in dish_type.lower():
                dish_type_cn = "炒菜"
            
            base_prompt = f"""拍摄一道精致的{dish_type_cn}：{dish_name if dish_name else '创意料理'}

菜品包含以下食材（必须全部显示）：{ingredients_str}
菜系风格：{cuisine_info['name']}
摆盘方式：{plating_description}

严格要求：
1. 这是一道素食菜品，禁止出现肉类、鱼类、海鲜
2. 必须清晰显示所有列出的食材
3. 采用{cuisine_info['name']}的摆盘风格
4. 盛放在白色餐具中

{cuisine_info['prompt']}

专业美食摄影，8K高清，令人食欲大开。"""
        else:
            # 没有菜谱时的默认提示词
            base_prompt = f"""Create a highly detailed, exquisite gourmet dish.

Cuisine Style: {cuisine_info['prompt']}

Difficulty Level: {difficulty_info['prompt']}

Cooking Time: {time_info['prompt']}

Based semantically on the ingredients found in the input image, extract their core identities and synthesize them into a beautiful, artfully plated culinary concept.

Photography style: macro shot, dark food photography, dramatic rim lighting, film grain, 8k, photorealistic, appetizing."""
        
        # 添加自定义要求
        if custom_requirements:
            base_prompt += f"\n\nAdditional Requirements: {custom_requirements}"
        
        return base_prompt.strip()
    
    def identify_ingredients(
        self,
        image_path: str,
        confidence_threshold: str = "medium"
    ) -> Dict[str, Any]:
        """
        识别冰箱照片中的食材
        
        Args:
            image_path: 冰箱照片路径
            confidence_threshold: 置信度阈值 (high/medium/low)
            
        Returns:
            识别的食材列表和详细信息
        """
        try:
            encoded_image = self._encode_image(image_path)
        except Exception as e:
            return {"error": f"图片编码失败: {str(e)}"}
        
        # 构建食材识别提示词
        identify_prompt = """请仔细分析这张冰箱照片，识别里面所有的食材。

要求：
1. 仔细辨认每个物品，不要仅凭颜色猜测（比如红色可能是火龙果而不是红辣椒）
2. 对不确定的食材，标注"可能是"并说明依据
3. 区分新鲜食材和包装食品
4. 注意食材的状态（新鲜/冷冻/罐头等）

请按以下格式输出（使用中文）：

【识别到的食材】
- 食材名称 | 数量/状态 | 置信度(高/中/低) | 备注

【不确定的物品】
- 物品描述 | 可能的身份 | 建议用户确认

【建议优先使用的食材】
- 列出3-5个最适合做菜的食材（如快过期、数量多、易搭配等）"""

        # 调用 Qwen-VL 模型
        vl_payload = {
            "model": "qwen-vl-max",
            "input": {
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {"image": f"data:image/jpeg;base64,{encoded_image}"},
                            {"text": identify_prompt}
                        ]
                    }
                ]
            }
        }
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            print(f"🔍 正在识别冰箱中的食材...")
            response = requests.post(
                "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation",
                json=vl_payload,
                headers=headers,
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()
                output = result.get("output", {})
                choices = output.get("choices", [])
                if choices and len(choices) > 0:
                    content = choices[0].get("message", {}).get("content", [])
                    if content and len(content) > 0:
                        identify_text = content[0].get("text", "")
                        return {
                            "success": True,
                            "raw_text": identify_text,
                            "parsed": self._parse_ingredients(identify_text)
                        }
            
            return {"error": f"食材识别失败: {response.status_code}"}
            
        except Exception as e:
            return {"error": f"食材识别异常: {str(e)}"}
    
    def _parse_ingredients(self, text: str) -> Dict[str, List[Dict]]:
        """解析识别到的食材文本"""
        ingredients = []
        uncertain = []
        suggestions = []
        
        lines = text.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('【'):
                if '识别到的食材' in line:
                    current_section = 'ingredients'
                elif '不确定的物品' in line:
                    current_section = 'uncertain'
                elif '建议优先' in line:
                    current_section = 'suggestions'
                continue
            
            if line.startswith('-') or line.startswith('•'):
                item = line.lstrip('- •').strip()
                if current_section == 'ingredients' and item:
                    parts = item.split('|')
                    ingredients.append({
                        "name": parts[0].strip() if len(parts) > 0 else item,
                        "quantity": parts[1].strip() if len(parts) > 1 else "",
                        "confidence": parts[2].strip() if len(parts) > 2 else "中",
                        "note": parts[3].strip() if len(parts) > 3 else ""
                    })
                elif current_section == 'uncertain' and item:
                    uncertain.append(item)
                elif current_section == 'suggestions' and item:
                    suggestions.append(item)
        
        return {
            "ingredients": ingredients,
            "uncertain": uncertain,
            "suggestions": suggestions
        }

    def _generate_recipe_with_vl(
        self, 
        image_path: str,
        cuisine: str,
        difficulty: str,
        cooking_time: str,
        custom_requirements: Optional[str] = None,
        confirmed_ingredients: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        使用 Qwen-VL 模型分析图片并生成菜谱
        
        优先从真实菜谱数据库匹配，没有匹配时再使用AI生成
        
        Args:
            image_path: 冰箱照片路径
            cuisine: 菜系
            difficulty: 难度
            cooking_time: 烹饪时间
            custom_requirements: 额外要求
            confirmed_ingredients: 用户确认的食材列表（可选）
            
        Returns:
            菜谱信息字典
        """
        cuisine_name = self.CUISINE_PROMPTS.get(cuisine, {}).get("name", cuisine)
        difficulty_info = self.DIFFICULTY_PROMPTS.get(difficulty, self.DIFFICULTY_PROMPTS["medium"])
        time_info = self.TIME_PROMPTS.get(cooking_time, self.TIME_PROMPTS["moderate"])
        
        # 步骤1：尝试从真实菜谱数据库匹配
        if HAS_RECIPE_DB and confirmed_ingredients:
            print("   正在从经典菜谱库匹配...")
            matched_recipe = RecipeDatabase.match_recipe(
                ingredients=confirmed_ingredients,
                cuisine=cuisine,
                difficulty=difficulty,
                time_limit=cooking_time
            )
            
            if matched_recipe:
                print(f"   ✅ 匹配到经典菜谱：{matched_recipe['name']}")
                formatted_recipe = RecipeDatabase.format_recipe_for_display(matched_recipe)
                formatted_recipe["source"] = "经典菜谱库"
                formatted_recipe["authentic"] = True
                return formatted_recipe
            else:
                print("   未匹配到经典菜谱，使用AI生成...")
        
        try:
            encoded_image = self._encode_image(image_path)
        except Exception as e:
            return {"error": f"图片编码失败: {str(e)}"}
        
        # 步骤2：使用AI生成菜谱（增强版提示词）
        # 构建菜谱生成提示词
        if confirmed_ingredients:
            # 使用用户确认的食材 - 增强版提示词
            ingredients_str = "、".join(confirmed_ingredients)
            recipe_prompt = f"""基于以下确认可用的食材，设计一道{cuisine_name}风格的真实家常菜。

【确认可用的食材】
{ingredients_str}

要求：
- 难度：{difficulty_info['name']}（{difficulty_info['recipe_level']}）
- 时间：{time_info['name']}
- 烹饪时长：{time_info['time_range']}
- 必须优先使用上面列出的食材
- 必须是真实可行的家常做法，不是创意融合菜

请输出以下内容（使用中文），烹饪步骤必须详细真实：

【菜品名称】给这道菜起一个家常菜的名字（如"番茄炒蛋"而不是"番茄蛋花烩"）

【食材清单】列出需要的所有食材，标注具体用量（如"鸡蛋3个"而不是"鸡蛋适量"）

【烹饪步骤】按以下格式详细描述每个步骤：
步骤1. 【步骤名称】具体操作
   【火候】大火/中火/小火
   【时长】具体时间（如"2分钟"、"30秒"）
   【判断标准】如何判断这一步完成（如"蛋液凝固成块"、"番茄出汁变软"）
   💡 关键技巧

步骤2...（以此类推）

【烹饪技巧】2-3个真实有用的技巧（如"蛋液要充分搅打30秒"、"热锅凉油防粘"）

【风味描述】用一句话描述这道菜的味道特点（如"酸甜可口，蛋香浓郁"）"""
        else:
            # 传统模式：让AI自己识别 - 增强版提示词
            recipe_prompt = f"""分析这张冰箱照片里的食材，设计一道{cuisine_name}风格的真实家常菜。

要求：
- 难度：{difficulty_info['name']}（{difficulty_info['recipe_level']}）
- 时间：{time_info['name']}
- 烹饪时长：{time_info['time_range']}
- 重要：仔细观察每个食材，不要仅凭颜色猜测（比如红色可能是火龙果而不是红辣椒）
- 对不确定的食材，宁可不用也不要乱猜
- 必须是真实可行的家常做法，不是创意融合菜

请输出以下内容（使用中文），烹饪步骤必须详细真实：

【菜品名称】给这道菜起一个家常菜的名字（如"番茄炒蛋"而不是"番茄蛋花烩"）

【食材清单】列出需要的所有食材，标注具体用量（如"鸡蛋3个"而不是"鸡蛋适量"）

【烹饪步骤】按以下格式详细描述每个步骤：
步骤1. 【步骤名称】具体操作
   【火候】大火/中火/小火
   【时长】具体时间（如"2分钟"、"30秒"）
   【判断标准】如何判断这一步完成（如"蛋液凝固成块"、"番茄出汁变软"）
   💡 关键技巧

步骤2...（以此类推）

【烹饪技巧】2-3个真实有用的技巧（如"蛋液要充分搅打30秒"、"热锅凉油防粘"）

【风味描述】用一句话描述这道菜的味道特点（如"酸甜可口，蛋香浓郁"）"""

        if custom_requirements:
            recipe_prompt += f"\n\n额外要求：{custom_requirements}"

        # 调用 Qwen-VL 模型
        vl_payload = {
            "model": "qwen-vl-max",
            "input": {
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {"image": f"data:image/jpeg;base64,{encoded_image}"},
                            {"text": recipe_prompt}
                        ]
                    }
                ]
            }
        }
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            print(f"   正在生成菜谱...")
            response = requests.post(
                "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation",
                json=vl_payload,
                headers=headers,
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()
                output = result.get("output", {})
                choices = output.get("choices", [])
                if choices and len(choices) > 0:
                    content = choices[0].get("message", {}).get("content", [])
                    if content and len(content) > 0:
                        recipe_text = content[0].get("text", "")
                        return self._parse_recipe(recipe_text)
            
            return {"error": f"菜谱生成失败: {response.status_code}"}
            
        except Exception as e:
            return {"error": f"菜谱生成异常: {str(e)}"}
    
    def _parse_recipe(self, recipe_text: str) -> Dict[str, Any]:
        """
        解析菜谱文本为结构化数据
        
        Args:
            recipe_text: 原始菜谱文本
            
        Returns:
            结构化菜谱字典
        """
        recipe = {
            "raw_text": recipe_text,
            "name": "",
            "ingredients": [],
            "steps": [],
            "tips": [],
            "flavor_description": ""
        }
        
        lines = recipe_text.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # 识别章节
            if '菜品名称' in line or '【菜品名称】' in line:
                current_section = 'name'
                # 可能名称在同一行
                if '】' in line:
                    parts = line.split('】', 1)
                    if len(parts) > 1 and parts[1].strip():
                        recipe['name'] = parts[1].strip()
                continue
            elif '食材清单' in line or '【食材清单】' in line:
                current_section = 'ingredients'
                continue
            elif '烹饪步骤' in line or '【烹饪步骤】' in line:
                current_section = 'steps'
                continue
            elif '烹饪技巧' in line or '【烹饪技巧】' in line or '小贴士' in line:
                current_section = 'tips'
                continue
            elif '风味描述' in line or '【风味描述】' in line or '味道特点' in line:
                current_section = 'flavor'
                continue
            
            # 根据当前章节处理内容
            if current_section == 'name' and line and not line.startswith('【'):
                recipe['name'] = line
            elif current_section == 'ingredients' and line:
                # 去掉常见的列表符号
                clean_line = line.lstrip('- * ・').strip()
                if clean_line and not clean_line.startswith('【'):
                    recipe['ingredients'].append(clean_line)
            elif current_section == 'steps' and line:
                # 保留原始格式，包括火候、时长等信息
                clean_line = line
                # 只去掉简单的数字编号，保留【火候】等标记
                for i in range(10):
                    if clean_line.startswith(f"{i}.") or clean_line.startswith(f"{i}、"):
                        clean_line = clean_line[2:].strip()
                        break
                
                # 过滤掉只包含标记的行（如单独的"【火候】"）
                if clean_line and not (clean_line.startswith('【') and '】' in clean_line and len(clean_line) < 15):
                    recipe['steps'].append(clean_line)
                # 保留火候、时长等标记行
                elif clean_line and ('【火候】' in clean_line or '【时长】' in clean_line or '【判断标准】' in clean_line or line.startswith('💡')):
                    recipe['steps'].append(clean_line)
            elif current_section == 'tips' and line:
                clean_line = line.lstrip('- * ・').strip()
                if clean_line and not clean_line.startswith('【'):
                    recipe['tips'].append(clean_line)
            elif current_section == 'flavor' and line:
                recipe['flavor_description'] = line
        
        return recipe
    
    def generate(
        self,
        image_path: str,
        cuisine: str = "chinese",
        difficulty: str = "medium",
        cooking_time: str = "moderate",
        custom_requirements: Optional[str] = None,
        size: str = "1024*1024",
        seed: Optional[int] = None,
        max_retries: int = 30,
        poll_interval: int = 2,
        generate_recipe: bool = True,
        confirmed_ingredients: Optional[List[str]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        生成美食概念图（支持异步轮询和详细参数定制）
        
        Args:
            image_path: 冰箱照片路径
            cuisine: 菜系选择
            difficulty: 难易程度
            cooking_time: 烹饪时间
            custom_requirements: 额外自定义要求
            size: 输出图片尺寸
            seed: 随机种子（可选）
            max_retries: 最大轮询次数
            poll_interval: 轮询间隔（秒）
            generate_recipe: 是否同时生成菜谱
            confirmed_ingredients: 用户确认的食材列表（可选）
            **kwargs: 其他 API 参数
            
        Returns:
            包含 image_url, recipe 或 error 的字典
        """
        # 获取参数中文名称用于显示
        cuisine_info = self.CUISINE_PROMPTS.get(cuisine, self.CUISINE_PROMPTS["chinese"])
        difficulty_info = self.DIFFICULTY_PROMPTS.get(difficulty, self.DIFFICULTY_PROMPTS["medium"])
        time_info = self.TIME_PROMPTS.get(cooking_time, self.TIME_PROMPTS["moderate"])
        
        cuisine_name = cuisine_info["name"]
        difficulty_name = difficulty_info["name"]
        time_name = time_info["name"]
        
        # 生成菜谱（如果启用）
        recipe = None
        if generate_recipe:
            print(f"📝 正在根据冰箱食材生成{cuisine_name}菜谱...")
            recipe = self._generate_recipe_with_vl(
                image_path, cuisine, difficulty, cooking_time, custom_requirements, confirmed_ingredients
            )
            if recipe and not recipe.get("error"):
                print(f"   ✅ 菜谱生成完成: {recipe.get('name', '未知菜品')}")
            else:
                print(f"   ⚠️ 菜谱生成失败，将继续生成图片")
        
        # 构建图片生成提示词（现在包含菜谱信息，让图片更贴合菜谱）
        prompt = self._build_prompt(cuisine, difficulty, cooking_time, custom_requirements, recipe)
        
        # 编码图片
        try:
            encoded_image = self._encode_image(image_path)
        except FileNotFoundError:
            return {"error": f"图片文件未找到: {image_path}", "recipe": recipe}
        except Exception as e:
            return {"error": f"图片编码失败: {str(e)}", "recipe": recipe}
        
        # 判断模型类型
        is_27 = self.model_version == "2.7"
        is_27_t2i = self.model_version == "2.7-t2i"  # 万相2.7 文生图
        is_21_i2v = self.model_version == "2.1-i2v"
        is_21_t2v = self.model_version == "2.1-t2v"
        is_video = is_21_i2v or is_21_t2v
        
        # 构建负面提示词（如果有菜谱信息）
        negative_prompt = None
        if recipe and not recipe.get("error"):
            ingredients = recipe.get("ingredients", [])
            has_meat = any(m in str(ingredients).lower() for m in ["肉", " pork", " beef", " chicken", " meat", "鱼", "fish", "虾", "shrimp"])
            if not has_meat:
                negative_prompt = "meat, fish, seafood, chicken, beef, pork, lamb, animal protein, raw meat, cooked meat, fish on plate, whole fish"
        
        # 根据模型类型构建不同的payload
        if is_27:
            # 万相2.7 图生图 - 使用 messages 格式
            # 把文字放前面，增强文字提示词的权重
            content_list = [
                {"text": prompt},
                {"image": f"data:image/jpeg;base64,{encoded_image}"}
            ]
            
            payload = {
                "model": self.model_name,
                "input": {
                    "messages": [
                        {
                            "role": "user",
                            "content": content_list
                        }
                    ]
                },
                "parameters": {
                    "size": size if size in ["1K", "2K", "4K"] else "2K",
                    "n": 1,
                    "watermark": False,
                    **({"seed": seed} if seed else {}),
                    **({"negative_prompt": negative_prompt} if negative_prompt else {}),
                    **kwargs
                }
            }
        elif is_21_i2v:
            # 万相2.1 图生视频
            payload = {
                "model": self.model_name,
                "input": {
                    "prompt": prompt,
                    "image": encoded_image
                },
                "parameters": {
                    "size": size if size in ["720*1280", "1280*720"] else "720*1280",
                    "n": 1,
                    **({"seed": seed} if seed else {}),
                    **kwargs
                }
            }
        elif is_27_t2i:
            # 万相2.7 文生图（基于菜谱生成，不用冰箱照片！）
            # 基于菜谱构建更详细的文字描述
            t2i_prompt = prompt
            if recipe and recipe.get("name"):
                ingredients_str = ", ".join([i.split("：")[0].split("（")[0].strip() for i in recipe.get("ingredients", [])[:6]])
                
                # 判断烹饪方式，确保生成"熟"的菜
                steps_text = " ".join(recipe.get("steps", [])).lower()
                is_cooked = any(word in steps_text for word in ["炒", "煎", "炸", "烤", "蒸", "煮", "炖", "stir-fry", "fry", "roast", "steam", "boil", "braise"])
                
                # 强制所有菜都显示为热菜，无论菜谱类型
                cooking_hint = "这是一道热炒菜肴，食材经过高温快炒，冒着腾腾热气，表面有焦香色泽，绝不是冷盘或沙拉。 "
                
                # 替换可能导致"生"联想的词汇
                t2i_ingredients = ingredients_str.replace("生菜", "菜叶").replace("生", "")
                
                t2i_prompt = f"""专业美食摄影：{recipe['name']}

{cooking_hint}这是一道{cuisine_name}热炒菜，主要食材：{t2i_ingredients}。所有食材经过高温烹饪，表面有炒制痕迹，热气腾腾，油光锃亮。

{cuisine_info['prompt']}

专业美食摄影，微距拍摄，戏剧性灯光，8K超高清，逼真写实，细节丰富，令人食欲大开，热气腾腾，高温快炒，wok hei锅气。"""
            
            # 万相2.6/2.7文生图使用 messages 格式（和图生图一样）
            payload = {
                "model": self.model_name,
                "input": {
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {"text": t2i_prompt}
                            ]
                        }
                    ]
                },
                "parameters": {
                    "size": size if "*" in size else "1024*1024",  # 文生图需要 width*height 格式
                    "n": 1,
                    "watermark": False,
                    "prompt_extend": True,  # 官方示例有这个参数
                    **({"seed": seed} if seed else {}),
                    **kwargs
                }
            }
            encoded_image = None  # 文生图不需要图片
            
        elif is_21_t2v:
            # 万相2.1 文生视频（不使用冰箱图）
            # 根据菜谱信息生成视频提示词
            video_prompt = prompt
            if recipe and recipe.get("name"):
                video_prompt = f"A delicious {cuisine_name} dish called '{recipe['name']}'. Professional food cinematography, steam rising, sizzling pan, appetizing cooking process, dramatic lighting. {cuisine_info['prompt']}"
            
            payload = {
                "model": self.model_name,
                "input": {
                    "prompt": video_prompt
                },
                "parameters": {
                    "size": size if size in ["720*1280", "1280*720"] else "720*1280",
                    "n": 1,
                    **({"seed": seed} if seed else {}),
                    **kwargs
                }
            }
            encoded_image = None  # 文生视频不需要图片
        else:
            # 万相2.1 文生图（使用冰箱图作为参考）
            payload = {
                "model": self.model_name,
                "input": {
                    "prompt": prompt,
                    "image": encoded_image  # 参考图
                },
                "parameters": {
                    "size": size,
                    "n": 1,
                    **({"seed": seed} if seed else {}),
                    **kwargs
                }
            }
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # 只有 2.7图生图 和 2.7-t2i 文生图使用同步，其他用异步
        use_async = not (is_27 or is_27_t2i)
        if use_async:
            headers["X-DashScope-Async"] = "enable"
        
        output_type = "视频" if is_video else "图片"
        print(f"\n🚀 提交{output_type}生成任务...")
        print(f"   模型: {self.model_name}")
        print(f"   模式: {'同步' if not use_async else '异步'}")
        print(f"   菜系: {cuisine_name}")
        print(f"   难度: {difficulty_name}")
        print(f"   时间: {time_name}")
        
        try:
            response = requests.post(
                self.api_url,
                json=payload,
                headers=headers,
                timeout=300 if not use_async else 60
            )
            
            if response.status_code != 200:
                return {
                    "error": "任务提交失败",
                    "status_code": response.status_code,
                    "response": response.text[:500],
                    "recipe": recipe
                }
            
            result = response.json()
            
            # 同步模式（2.7、视频模型）
            if not use_async:
                output = result.get("output", {})
                choices = output.get("choices", [])
                if choices and len(choices) > 0:
                    content = choices[0].get("message", {}).get("content", [])
                    if content and len(content) > 0:
                        media_url = content[0].get("video" if is_video else "image")
                        if media_url:
                            print(f"\n🎉 生成成功！")
                            return {
                                "success": True,
                                "media_url": media_url,
                                "media_type": "video" if is_video else "image",
                                "cuisine": cuisine,
                                "cuisine_name": cuisine_name,
                                "difficulty": difficulty,
                                "difficulty_name": difficulty_name,
                                "cooking_time": cooking_time,
                                "cooking_time_name": time_name,
                                "recipe": recipe,
                                "raw_response": result
                            }
                return {
                    "error": "同步响应中未找到媒体文件",
                    "raw_response": result,
                    "recipe": recipe
                }
            
            # 异步模式（2.1 T2I）
            task_id = result.get("output", {}).get("task_id")
            if not task_id:
                return {
                    "error": "响应中未找到 task_id",
                    "raw_response": result,
                    "recipe": recipe
                }
            
            print(f"📝 任务ID: {task_id}")
            
            # 轮询查询结果
            print(f"\n⏳ 开始轮询任务状态...")
            query_url = f"https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}"
            
            for i in range(max_retries):
                time.sleep(poll_interval)
                print(f"   第 {i+1} 次查询...", end=" ")
                
                query_response = requests.get(query_url, headers=headers, timeout=30)
                
                if query_response.status_code != 200:
                    print(f"查询失败: {query_response.status_code}")
                    continue
                
                task_result = query_response.json()
                status = task_result.get("output", {}).get("task_status", "UNKNOWN")
                print(f"状态: {status}")
                
                if status == "SUCCEEDED":
                    results = task_result.get("output", {}).get("results", [])
                    if results and len(results) > 0:
                        image_url = results[0].get("url")
                        print(f"\n🎉 任务完成！")
                        return {
                            "success": True,
                            "media_url": image_url,
                            "media_type": "image",
                            "cuisine": cuisine,
                            "cuisine_name": cuisine_name,
                            "difficulty": difficulty,
                            "difficulty_name": difficulty_name,
                            "cooking_time": cooking_time,
                            "cooking_time_name": time_name,
                            "task_id": task_id,
                            "recipe": recipe,
                            "raw_response": task_result
                        }
                    else:
                        return {
                            "error": "任务成功但未返回图片 URL",
                            "raw_response": task_result,
                            "recipe": recipe
                        }
                
                elif status == "FAILED":
                    return {
                        "error": "任务执行失败",
                        "task_id": task_id,
                        "raw_response": task_result,
                        "recipe": recipe
                    }
            
            return {
                "error": "轮询超时，请稍后手动查询",
                "task_id": task_id,
                "query_url": query_url,
                "recipe": recipe
            }
            
        except requests.exceptions.Timeout:
            return {"error": "请求超时，请检查网络或稍后重试", "recipe": recipe}
        except requests.exceptions.ConnectionError:
            return {"error": "连接失败，请检查 API URL 是否正确", "recipe": recipe}
        except Exception as e:
            return {"error": f"请求异常: {str(e)}", "recipe": recipe}
    
    def query_task(self, task_id: str) -> Dict[str, Any]:
        """查询已提交任务的状态"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        query_url = f"https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}"
        
        try:
            response = requests.get(query_url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                return response.json()
            else:
                return {
                    "error": "查询失败",
                    "status_code": response.status_code,
                    "response": response.text[:500]
                }
        except Exception as e:
            return {"error": f"查询异常: {str(e)}"}
    
    @classmethod
    def list_cuisines(cls) -> Dict[str, List[str]]:
        """列出所有可用的菜系分类"""
        categories = {
            "中式菜系": [],
            "日韩料理": [],
            "东南亚": [],
            "南亚": [],
            "西式": [],
            "中东风味": [],
            "美洲": [],
            "其他": [],
            "现代/融合": []
        }
        
        chinese_keywords = ["chinese", "sichuan", "cantonese", "hunan", "shandong", "jiangsu", "fujian", "zhejiang", "anhui", "beijing", "xi'an", "yunnan", "guizhou"]
        japanese_korean = ["japanese", "sushi", "ramen", "korean", "korean-bbq"]
        southeast_asia = ["thai", "vietnamese", "singapore", "malaysian", "indonesian", "burmese"]
        south_asia = ["indian", "indian-south", "sri-lankan"]
        western = ["western", "french", "italian", "italian-pasta", "pizza", "american", "american-bbq", "mexican", "spanish", "greek", "mediterranean", "german", "british", "scandinavian", "russian", "portuguese"]
        middle_east = ["turkish", "lebanese", "moroccan", "persian", "israeli"]
        americas = ["mexican", "american", "american-bbq", "caribbean", "brazilian", "peruvian", "argentinian"]
        modern = ["fusion", "molecular", "plant-based", "raw"]
        
        for code, info in cls.CUISINE_PROMPTS.items():
            name = info["name"]
            if code in chinese_keywords:
                categories["中式菜系"].append(f"{code}: {name}")
            elif code in japanese_korean:
                categories["日韩料理"].append(f"{code}: {name}")
            elif code in southeast_asia:
                categories["东南亚"].append(f"{code}: {name}")
            elif code in south_asia:
                categories["南亚"].append(f"{code}: {name}")
            elif code in western and code not in americas:
                categories["西式"].append(f"{code}: {name}")
            elif code in middle_east:
                categories["中东风味"].append(f"{code}: {name}")
            elif code in americas:
                categories["美洲"].append(f"{code}: {name}")
            elif code in modern:
                categories["现代/融合"].append(f"{code}: {name}")
            else:
                categories["其他"].append(f"{code}: {name}")
        
        return categories


def generate_gourmet_from_fridge_photo(
    image_path: str,
    api_key: Optional[str] = None,
    api_url: Optional[str] = None,
    cuisine: str = "chinese",
    difficulty: str = "medium",
    cooking_time: str = "moderate",
    model_version: str = "2.7",
    generate_recipe: bool = True,
    **kwargs
) -> Dict[str, Any]:
    """
    便捷函数：从冰箱照片生成美食概念图 + 菜谱
    
    Args:
        image_path: 冰箱照片路径
        api_key: API Key（可选）
        api_url: API URL（可选）
        cuisine: 菜系
        difficulty: 难易程度
        cooking_time: 烹饪时间
        model_version: 模型版本
        generate_recipe: 是否生成菜谱
        **kwargs: 其他参数
        
    Returns:
        生成结果字典
    """
    gourmet = WanFridgeGourmet(api_key=api_key, api_url=api_url, model_version=model_version)
    return gourmet.generate(
        image_path,
        cuisine=cuisine,
        difficulty=difficulty,
        cooking_time=cooking_time,
        generate_recipe=generate_recipe,
        **kwargs
    )


def main():
    """命令行入口"""
    import argparse
    
    # 获取所有可用的菜系代码
    cuisine_choices = list(WanFridgeGourmet.CUISINE_PROMPTS.keys())
    
    parser = argparse.ArgumentParser(
        description="纯血万相冰箱盲盒 v2.0 - 将冰箱照片转为米其林级美食概念图 + 完整菜谱",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
示例:
  # 基础用法（生成图片+菜谱）
  python3 generate_gourmet.py fridge.jpg
  
  # 先识别食材，再生成（避免AI认错）
  python3 generate_gourmet.py fridge.jpg --identify-only
  python3 generate_gourmet.py fridge.jpg --ingredients "鸡蛋,西红柿,青椒"
  
  # 指定风格：日式简单快手菜
  python3 generate_gourmet.py fridge.jpg --cuisine japanese --difficulty easy --cooking-time quick
  
  # 使用万相2.7图生图（基于冰箱照片生成）
  python3 generate_gourmet.py fridge.jpg --model 2.7 -c japanese -d easy -t quick
  
  # 使用万相2.7文生图（基于菜谱文字描述生成，更贴合菜谱！）
  python3 generate_gourmet.py fridge.jpg --model 2.7-t2i -c chinese -d medium -t moderate
  
  # 使用万相2.1文生视频（会基于菜谱生成烹饪视频）
  python3 generate_gourmet.py fridge.jpg --model 2.1-t2v -c chinese -d medium -t moderate
  
  # 只生成图片，不生成菜谱
  python3 generate_gourmet.py fridge.jpg --no-recipe
  
  # 查看所有可用的菜系
  python3 generate_gourmet.py --list-cuisines
  
  # 查询任务状态
  python3 generate_gourmet.py --query <task_id>

支持的模型:
  - 2.7        万相2.7 图生图（默认，基于冰箱照片生成）
  - 2.7-t2i    万相2.7 文生图（基于菜谱描述生成，图文更贴合！）
  - 2.1-t2i    万相2.1 文生图（含参考图）
  - 2.1-t2i-free 万相2.1 文生图免费版
  - 2.1-i2v    万相2.1 图生视频
  - 2.1-t2v    万相2.1 文生视频

可用菜系（共{len(cuisine_choices)}种）:
  中式: chinese, sichuan, cantonese, hunan, shandong, jiangsu, fujian, zhejiang, anhui, beijing, xi'an, yunnan, guizhou
  日韩: japanese, sushi, ramen, korean, korean-bbq
  东南亚: thai, vietnamese, singapore, malaysian, indonesian, burmese
  南亚: indian, indian-south, sri-lankan
  西式: western, french, italian, italian-pasta, pizza, american, american-bbq, spanish, greek, mediterranean, german, british, scandinavian, russian, portuguese
  中东: turkish, lebanese, moroccan, persian, israeli
  美洲: mexican, caribbean, brazilian, peruvian, argentinian
  现代: fusion, molecular, plant-based, raw
        """
    )
    
    parser.add_argument("image", nargs="?", help="冰箱照片路径")
    
    # 菜系参数
    parser.add_argument(
        "--cuisine", "-c",
        choices=cuisine_choices,
        default="chinese",
        help="菜系选择（默认: chinese 中式）"
    )
    
    # 难易程度参数
    parser.add_argument(
        "--difficulty", "-d",
        choices=["easy", "medium", "hard"],
        default="medium",
        help="难易程度（默认: medium 适中）"
    )
    
    # 烹饪时间参数
    parser.add_argument(
        "--cooking-time", "-t",
        choices=["quick", "moderate", "slow"],
        default="moderate",
        help="烹饪时间（默认: moderate 30-45分钟）"
    )
    
    # 自定义要求
    parser.add_argument(
        "--custom", "-x",
        help="额外自定义要求（如：不要辣、适合减脂、适合宝宝等）"
    )
    
    # 是否生成菜谱
    parser.add_argument(
        "--no-recipe",
        action="store_true",
        help="不生成菜谱，仅生成图片"
    )
    
    # 其他参数
    parser.add_argument("--seed", type=int, help="随机种子")
    parser.add_argument("--output", "-o", help="输出结果保存路径（JSON格式）")
    parser.add_argument("--query", help="查询已有任务状态（传入 task_id）")
    
    # 列出菜系
    parser.add_argument(
        "--list-cuisines",
        action="store_true",
        help="列出所有可用的菜系选项"
    )
    
    # 模型版本参数
    parser.add_argument(
        "--model", "-m",
        choices=["2.7", "2.7-t2i", "2.1-t2i", "2.1-t2i-free", "2.1-i2v", "2.1-t2v"],
        default="2.7",
        help="模型版本选择（默认: 2.7）。2.7-t2i为文生图模式，基于菜谱生成而非冰箱照片"
    )
    
    # 食材识别模式
    parser.add_argument(
        "--identify-only",
        action="store_true",
        help="仅识别冰箱中的食材，不生成菜谱和图片"
    )
    
    # 指定确认的食材列表
    parser.add_argument(
        "--ingredients", "-i",
        help='指定确认的食材列表，用逗号分隔（如："鸡蛋,西红柿,青椒"）'
    )
    
    args = parser.parse_args()
    
    # 列出菜系模式
    if args.list_cuisines:
        print("=" * 60)
        print("🍜 纯血万相冰箱盲盒 - 可用菜系列表")
        print("=" * 60)
        categories = WanFridgeGourmet.list_cuisines()
        for category, items in categories.items():
            if items:
                print(f"\n【{category}】")
                for item in items:
                    print(f"  • {item}")
        print(f"\n总计: {len(cuisine_choices)} 种菜系")
        return
    
    # 检查环境变量
    if not os.environ.get("WAN_API_KEY") and not args.query:
        print("❌ 错误: 未设置 WAN_API_KEY 环境变量")
        print("   请运行: export WAN_API_KEY='your-api-key'")
        sys.exit(1)
    
    gourmet = WanFridgeGourmet(model_version=args.model)
    
    # 查询模式
    if args.query:
        result = gourmet.query_task(args.query)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    
    # 检查图片路径
    if not args.image:
        print("❌ 错误: 请提供冰箱照片路径")
        parser.print_help()
        sys.exit(1)
    
    # 仅识别食材模式
    if args.identify_only:
        result = gourmet.identify_ingredients(args.image)
        if result.get("success"):
            print("=" * 60)
            print("🔍 冰箱食材识别结果")
            print("=" * 60)
            print(result.get("raw_text", ""))
            print("\n" + "=" * 60)
            print("💡 提示: 使用 --ingredients 参数指定确认的食材")
            print("   例如: python3 generate_gourmet.py fridge.jpg --ingredients '鸡蛋,西红柿,青椒'")
        else:
            print(f"❌ 识别失败: {result.get('error', '未知错误')}")
            sys.exit(1)
        return
    
    # 解析确认的食材列表
    confirmed_ingredients = None
    if args.ingredients:
        confirmed_ingredients = [i.strip() for i in args.ingredients.split(",")]
        print(f"📝 使用确认的食材: {', '.join(confirmed_ingredients)}")
    
    # 生成模式
    result = gourmet.generate(
        args.image,
        cuisine=args.cuisine,
        difficulty=args.difficulty,
        cooking_time=args.cooking_time,
        custom_requirements=args.custom,
        seed=args.seed,
        generate_recipe=not args.no_recipe,
        confirmed_ingredients=confirmed_ingredients
    )
    
    # 输出结果 - 图文并茂格式
    if result.get("success"):
        media_type = result.get("media_type", "image")
        
        print(f"\n{'='*60}")
        print(f"🎉 {'视频' if media_type == 'video' else '图片'}生成成功！")
        print(f"{'='*60}")
        print(f"\n📎 {'视频' if media_type == 'video' else '图片'}链接: {result['media_url']}")
        print(f"   菜系: {result['cuisine_name']}")
        print(f"   难度: {result['difficulty_name']}")
        print(f"   时间: {result['cooking_time_name']}")
        if 'task_id' in result:
            print(f"   任务ID: {result['task_id']}")
        
        # 输出菜谱
        recipe = result.get("recipe")
        if recipe and not recipe.get("error"):
            print(f"\n{'='*60}")
            print("📖 智能菜谱")
            print(f"{'='*60}")
            
            # 菜品名称
            if recipe.get("name"):
                print(f"\n【{recipe['name']}】")
            
            # 风味描述
            if recipe.get("flavor_description"):
                print(f"\n💫 {recipe['flavor_description']}")
            
            # 食材清单
            if recipe.get("ingredients"):
                print(f"\n🥬 食材清单:")
                for i, ing in enumerate(recipe["ingredients"][:15], 1):
                    print(f"   {i}. {ing}")
                if len(recipe["ingredients"]) > 15:
                    print(f"   ... 等共 {len(recipe['ingredients'])} 种食材")
            
            # 烹饪步骤（重点突出）
            if recipe.get("steps"):
                print(f"\n{'='*60}")
                print("👨‍🍳 烹饪步骤")
                print(f"{'='*60}")
                for i, step in enumerate(recipe["steps"], 1):
                    print(f"\n   步骤 {i}:")
                    print(f"   {step}")
            
            # 烹饪技巧
            if recipe.get("tips"):
                print(f"\n{'='*60}")
                print("💡 烹饪技巧")
                print(f"{'='*60}")
                for i, tip in enumerate(recipe["tips"], 1):
                    print(f"   {i}. {tip}")
        
        model_info = f"\n（本{ '视频' if media_type == 'video' else '图片' }由 {gourmet.model_name} 基于您的冰箱照片独家生成）"
        print(f"\n{model_info}")
    else:
        print(f"\n❌ 生成失败: {result.get('error', '未知错误')}")
        if "task_id" in result:
            print(f"   任务ID: {result['task_id']}")
            print(f"   可稍后查询: python3 generate_gourmet.py --query {result['task_id']}")
        
        # 如果菜谱生成了但图片失败了，也显示菜谱
        recipe = result.get("recipe")
        if recipe and not recipe.get("error"):
            print(f"\n📖 但菜谱已生成:")
            if recipe.get("name"):
                print(f"   菜品: {recipe['name']}")
            if recipe.get("raw_text"):
                print(f"\n{recipe['raw_text'][:500]}...")
        
        sys.exit(1)
    
    # 保存结果
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"\n💾 结果已保存至: {args.output}")


if __name__ == "__main__":
    main()
