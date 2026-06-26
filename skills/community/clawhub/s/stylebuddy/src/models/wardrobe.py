"""
衣橱模型模块
管理衣橱数据操作
"""

import os
import re
import shutil
from typing import Dict, List, Optional, Any
from datetime import datetime

class WardrobeManager:
    """衣橱管理器"""
    
    CATEGORIES = {
        "外套": "outer",
        "outer": "outer",
        "上衣": "top",
        "top": "top",
        "下装": "bottom",
        "裤子": "bottom",
        "裙子": "bottom",
        "bottom": "bottom",
        "鞋": "shoes",
        "鞋子": "shoes",
        "shoes": "shoes",
        "配饰": "accessory",
        "包包": "accessory",
        "帽子": "accessory",
        "围巾": "accessory",
        "accessory": "accessory"
    }
    
    COLORS = ["黑", "白", "灰", "米", "卡其", "棕", "驼", "红", "粉", "橙", "黄", "绿", "蓝", "紫", "条纹", "格", "花"]
    
    def __init__(self, database):
        self.db = database
    
    def parse_and_add(self, user_input: str, context: Dict = None) -> str:
        """
        解析用户输入并添加单品
        
        示例:
        - "录入一件米色风衣"
        - "添加黑色牛仔裤"
        - "新买白色T恤"
        """
        # 解析名称
        name = self._extract_item_name(user_input)
        
        # 解析类别
        category = self._extract_category(user_input, name)
        
        # 解析颜色
        color = self._extract_color(user_input, name)
        
        # 解析风格
        style = self._extract_style(user_input)
        
        # 检查是否有图片
        image_path = None
        if context and 'image' in context:
            image_path = self._save_item_image(context['image'], name)
        
        # 创建单品记录
        item = {
            "name": name,
            "category": category,
            "color": color,
            "style": style,
            "season": self._guess_season(name, category),
            "image_path": image_path,
            "tags": [color, style] if style else [color]
        }
        
        # 检查是否已存在
        existing_item = self._find_item_by_name_color(name, color, category)
        if existing_item:
            # 更新现有单品
            item_id = existing_item['id']
            self.db.update_item(item_id, item)
            action = "更新"
        else:
            # 添加新单品
            item_id = self.db.add_item(item)
            action = "添加"
        
        # 返回结果
        display_name = name
        if color and color != "其他" and not name.startswith(color):
            display_name = f"{color}{name}"
        
        result = f"✅ 已{action}单品：{display_name}\n"
        result += f"   类别：{self._cat_to_chinese(category)}\n"
        result += f"   颜色：{color}\n"
        if style:
            result += f"   风格：{style}\n"
        if image_path:
            result += f"   图片：已保存\n"
        if action == "更新":
            result += f"   💡 该单品已存在，已更新信息"
        
        return result
    
    def _find_item_by_name_color(self, name: str, color: str, category: str) -> Optional[Dict]:
        """根据名称、颜色、类别查找单品"""
        items = self.db.get_all_items()
        for item in items:
            if (item.get('name') == name and 
                item.get('color') == color and 
                item.get('category') == category):
                return item
        return None
    
    def _extract_item_name(self, text: str) -> str:
        """提取单品名称"""
        # 去掉常见前缀
        prefixes = ["录入", "添加", "新买", "我有", "一件", "一条", "一双", "一个", "套"]
        name = text
        for p in prefixes:
            name = name.replace(p, "")
        
        # 去掉类别词，保留完整名称
        category_words = ["外套", "上衣", "裤子", "裙子", "鞋", "包包", "围巾"]
        for cw in category_words:
            if cw in name:
                # 找到了类别词，保留它
                pass
        
        name = name.strip()
        
        # 如果没提取到，取后几个字
        if not name and len(text) > 2:
            name = text[-4:].strip()
        
        return name or "未命名单品"
    
    def _extract_category(self, text: str, name: str) -> str:
        """提取类别"""
        # 根据关键词判断
        category_map = {
            "outer": ["风衣", "大衣", "外套", "西装", "夹克", "羽绒服", "棉衣", "皮衣"],
            "top": ["T恤", "t恤", "衬衫", "卫衣", "毛衣", "针织衫", "背心", "吊带", "打底"],
            "bottom": ["牛仔裤", "休闲裤", "西裤", "短裤", "裙子", "连衣裙", "半裙", "阔腿裤", "运动裤"],
            "shoes": ["鞋", "靴", "拖", "sneaker", "boots"],
            "accessory": ["包", "围巾", "帽子", "项链", "耳环", "手链", "腰带", "眼镜"]
        }
        
        for cat, keywords in category_map.items():
            for kw in keywords:
                if kw in text or kw in name:
                    return cat
        
        # 默认根据量词判断
        if any(w in text for w in ["双", "只"]):
            return "shoes"
        if any(w in text for w in ["条"]):
            return "bottom"
        
        return "top"  # 默认上衣
    
    def _extract_color(self, text: str, name: str) -> str:
        """提取颜色"""
        color_map = {
            "黑": "黑色", "白": "白色", "灰": "灰色",
            "米": "米色", "杏": "杏色", "卡其": "卡其色",
            "棕": "棕色", "驼": "驼色", "咖": "咖啡色",
            "红": "红色", "粉": "粉色", "玫红": "玫红",
            "橙": "橙色", "黄": "黄色",
            "绿": "绿色", "蓝": "蓝色", "藏青": "藏青",
            "紫": "紫色", "条纹": "条纹", "格": "格纹", "花": "花色"
        }
        
        for short, full in color_map.items():
            if short in text or short in name:
                return full
        
        return "其他"
    
    def _extract_style(self, text: str) -> Optional[str]:
        """提取风格"""
        styles = {
            "休闲": ["休闲", "随性", "日常", "舒适"],
            "职场": ["职场", "通勤", "正式", "OL", "干练"],
            "优雅": ["优雅", "气质", "淑女", "精致"],
            "运动": ["运动", "健身", "活力"],
            "街头": ["街头", "潮", "酷", "个性"],
            "简约": ["简约", "极简", "基础", "百搭"]
        }
        
        for style, keywords in styles.items():
            for kw in keywords:
                if kw in text:
                    return style
        
        return None
    
    def _guess_season(self, name: str, category: str) -> str:
        """猜测适用季节"""
        if any(w in name for w in ["羽绒服", "棉衣", "大衣", "毛衣", "靴"]):
            return "秋冬"
        if any(w in name for w in ["T恤", "短裤", "裙子", "凉", "背心", "吊带"]):
            return "春夏"
        if category == "outer":
            return "春秋"
        return "四季"
    
    def _cat_to_chinese(self, cat: str) -> str:
        """类别转中文"""
        mapping = {
            "outer": "外套", "top": "上衣",
            "bottom": "下装", "shoes": "鞋子",
            "accessory": "配饰"
        }
        return mapping.get(cat, cat)
    
    def parse_and_add_with_image(self, image_path: str, user_text: str = "") -> str:
        """通过图片识别录入单品（支持吊牌识别）"""
        import json
        
        # 调用 Vision API 分析图片（外观 + 吊牌）
        analysis = self._analyze_clothing_image(image_path)
        
        # 创建单品记录
        item = {
            "name": analysis.get("name", user_text or "未命名单品"),
            "category": analysis.get("category", "top"),
            "color": analysis.get("color", "其他"),
            "material": analysis.get("material", ""),
            "price": analysis.get("price", ""),
            "brand": analysis.get("brand", ""),
            "season": analysis.get("season", "四季"),
            "style": analysis.get("style", ""),
            "image_path": image_path,
            "tags": [analysis.get("color", ""), analysis.get("style", "")] if analysis.get("style") else [analysis.get("color", "")]
        }
        
        # 添加记录
        item_id = self.db.add_item(item)
        
        # 返回结果
        result = f"✅ 已添加单品：{item['name']}\n"
        result += f"   类别：{self._cat_to_chinese(item['category'])}\n"
        result += f"   颜色：{item['color']}\n"
        if item['material']:
            result += f"   材质：{item['material']}\n"
        if item['brand']:
            result += f"   品牌：{item['brand']}\n"
        if item['price']:
            result += f"   价格：{item['price']}\n"
        result += f"   图片：已保存 📸\n"
        
        # 添加穿搭建议
        if analysis.get("styling_tips"):
            result += f"\n💡 搭配建议：{analysis['styling_tips']}"
        
        return result
    
    def _analyze_clothing_image(self, image_path: str) -> dict:
        """分析衣服图片（外观 + 吊牌）"""
        # 这里实际会调用 Vision API
        # 返回结构化数据
        return {
            "name": "待识别",
            "category": "top",
            "color": "待识别",
            "material": "",
            "price": "",
            "brand": "",
            "season": "四季",
            "style": "",
            "styling_tips": ""
        }
    
    def _save_item_image(self, image_data, item_name: str):
        """保存单品图片"""
        try:
            import shutil
            import uuid
            
            # 创建保存目录（使用相对路径）
            script_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            save_dir = os.path.join(script_dir, 'assets', 'images', 'items')
            os.makedirs(save_dir, exist_ok=True)
            
            # 如果是文件路径
            if isinstance(image_data, str) and os.path.exists(image_data):
                ext = os.path.splitext(image_data)[1] or ".jpg"
                filename = f"{uuid.uuid4().hex[:8]}_{item_name[:10]}{ext}"
                save_path = os.path.join(save_dir, filename)
                shutil.copy2(image_data, save_path)
                return save_path
            
            # 如果是 bytes 数据
            elif isinstance(image_data, bytes):
                filename = f"{uuid.uuid4().hex[:8]}_{item_name[:10]}.jpg"
                save_path = os.path.join(save_dir, filename)
                with open(save_path, 'wb') as f:
                    f.write(image_data)
                return save_path
                
        except Exception as e:
            print(f"保存图片失败: {e}")
        
        return None
    
    def get_wardrobe_summary(self) -> str:
        """获取衣橱概览"""
        stats = self.db.get_stats()
        items = self.db.get_all_items()
        
        if not items:
            return "👗 你的衣橱还是空的，先录入一些衣服吧！\n\n比如：\n• '录入一件米色风衣'\n• '添加黑色牛仔裤'\n• '新买白色T恤'"
        
        result = "👗 你的衣橱\n"
        result += f"共 {stats['total_items']} 件单品\n\n"
        
        # 按类别分组
        by_cat = stats.get('by_category', {})
        cat_names = {"outer": "外套", "top": "上衣", "bottom": "下装", "shoes": "鞋子", "accessory": "配饰"}
        
        for cat, name in cat_names.items():
            count = by_cat.get(cat, 0)
            if count > 0:
                result += f"{name}：{count} 件\n"
        
        # 显示最近添加的
        result += "\n📌 最近添加：\n"
        for item in items[:5]:
            color = item.get('color', '') or ''
            name = item.get('name', '')
            # 避免颜色重复
            if color and name.startswith(color):
                result += f"• {name}\n"
            else:
                result += f"• {color}{name}\n"
        
        return result
    
    def record_today_outfit(self, context: Dict = None) -> str:
        """记录今日穿搭"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        # 检查是否已记录
        existing = self.db.get_outfits(date=today)
        if existing:
            return f"今天已经记录过穿搭啦！\n\n已记录的单品：{', '.join(existing[0].get('items', []))}"
        
        # 从 context 或推荐中获取
        items = []
        if context and 'outfit_items' in context:
            items = context['outfit_items']
        
        if not items:
            # 提示用户先获取推荐
            return "还没有今天的穿搭推荐，先问我'今天穿什么'获取搭配方案吧！"
        
        # 记录
        outfit = {
            "date": today,
            "items": items,
            "occasion": context.get('occasion', '日常') if context else '日常',
            "notes": context.get('notes', '') if context else ''
        }
        
        self.db.add_outfit(outfit)
        return f"✅ 已记录今日穿搭！\n\n穿着：{', '.join(items)}\n\n明天见~"
    
    def backup_data(self) -> str:
        """备份数据"""
        import json
        
        data = self.db.export_data()
        backup_path = f"./assets/data/backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        os.makedirs(os.path.dirname(backup_path), exist_ok=True)
        
        with open(backup_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return f"✅ 数据已备份到：{backup_path}\n\n包含 {len(data.get('items', []))} 件单品，{len(data.get('outfits', []))} 条穿搭记录"
    
    def restore_data(self, backup_path: str = None) -> str:
        """恢复数据"""
        import json
        import glob
        
        if not backup_path:
            # 找最新的备份
            backups = glob.glob("./assets/data/backup_*.json")
            if not backups:
                return "没有找到备份文件"
            backup_path = max(backups, key=os.path.getctime)
        
        if not os.path.exists(backup_path):
            return f"备份文件不存在：{backup_path}"
        
        with open(backup_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        counts = self.db.import_data(data)
        
        return f"✅ 数据已恢复！\n\n导入了 {counts['items']} 件单品，{counts['outfits']} 条穿搭记录"
