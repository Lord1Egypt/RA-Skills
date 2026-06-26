"""
种草咨询模块
处理商场购物咨询、衣橱对比
"""

import os
import shutil
from typing import Dict, List, Optional, Any
from datetime import datetime

class ShoppingConsultant:
    """购物咨询顾问"""
    
    def __init__(self, database, wardrobe_manager):
        self.db = database
        self.wardrobe = wardrobe_manager
    
    def consult(self, image_path: str, user_text: str = "") -> Dict:
        """
        处理购物咨询
        
        Returns:
            {
                "analysis": "衣服分析结果",
                "comparison": "与现有衣橱对比",
                "recommendation": "购买建议",
                "actions": ["加入种草清单", "查看搭配效果"]
            }
        """
        # 1. 分析商品图片
        item_analysis = self._analyze_shopping_item(image_path)
        
        # 2. 与现有衣橱对比
        comparison = self._compare_with_wardrobe(item_analysis)
        
        # 3. 生成购买建议
        recommendation = self._generate_purchase_advice(item_analysis, comparison)
        
        return {
            "analysis": item_analysis,
            "comparison": comparison,
            "recommendation": recommendation,
            "image_path": image_path
        }
    
    def _analyze_shopping_item(self, image_path: str) -> Dict:
        """分析商品图片（外观+吊牌）"""
        # 这里会调用 Vision API 分析
        # 返回结构化数据
        return {
            "name": "待识别商品",
            "category": "top",
            "color": "待识别",
            "material": "",
            "price": "",
            "brand": "",
            "style": "",
            "unique_features": []
        }
    
    def _compare_with_wardrobe(self, new_item: Dict) -> Dict:
        """对比新商品与现有衣橱"""
        wardrobe_items = self.db.get_all_items()
        
        similar_items = []
        complementary_items = []
        
        # 找相似款
        for item in wardrobe_items:
            similarity_score = self._calculate_similarity(new_item, item)
            if similarity_score > 0.7:
                similar_items.append({
                    "item": item,
                    "similarity": similarity_score
                })
        
        # 找可搭配的单品
        for item in wardrobe_items:
            if self._can_match(new_item, item):
                complementary_items.append(item)
        
        return {
            "similar_items": similar_items,  # 已有类似款
            "can_match_with": complementary_items[:5],  # 可搭配的单品
            "is_redundant": len(similar_items) > 0,  # 是否重复购买
            "match_score": len(complementary_items) / max(len(wardrobe_items), 1)
        }
    
    def _calculate_similarity(self, item1: Dict, item2: Dict) -> float:
        """计算两件衣服的相似度"""
        score = 0.0
        
        # 类别相同
        if item1.get('category') == item2.get('category'):
            score += 0.3
        
        # 颜色相似
        if item1.get('color') == item2.get('color'):
            score += 0.3
        
        # 风格相似
        if item1.get('style') == item2.get('style'):
            score += 0.2
        
        # 材质相似
        if item1.get('material') == item2.get('material'):
            score += 0.2
        
        return score
    
    def _can_match(self, new_item: Dict, existing_item: Dict) -> bool:
        """判断两件衣服是否可以搭配"""
        # 简单的搭配规则
        category_pair = (new_item.get('category'), existing_item.get('category'))
        
        valid_pairs = [
            ('outer', 'top'), ('top', 'bottom'), ('top', 'shoes'),
            ('outer', 'bottom'), ('outer', 'dress')
        ]
        
        return category_pair in valid_pairs or category_pair[::-1] in valid_pairs
    
    def _generate_purchase_advice(self, item: Dict, comparison: Dict) -> str:
        """生成购买建议"""
        advice_parts = []
        
        # 重复购买警告
        if comparison["is_redundant"]:
            similar = comparison["similar_items"][0]["item"]
            advice_parts.append(f"⚠️ 注意：你已有类似的{similar.get('color', '')}{similar.get('name', '衣服')}，建议考虑是否真的需要")
        
        # 搭配度评估
        match_score = comparison["match_score"]
        if match_score > 0.6:
            advice_parts.append("✅ 和你现有衣服很搭，可以搭配出多种风格")
        elif match_score > 0.3:
            advice_parts.append("🟡 可以搭配，但需要再买点其他单品")
        else:
            advice_parts.append("💡 和你现有风格不太搭，可能需要调整衣橱整体风格")
        
        # 可搭配单品
        if comparison["can_match_with"]:
            match_names = [i.get('name', '单品') for i in comparison["can_match_with"][:3]]
            advice_parts.append(f"🎯 可以搭配你的：{', '.join(match_names)}")
        
        return "\n".join(advice_parts)
    
    def add_to_wishlist(self, image_path: str, analysis: Dict, reason: str = "") -> str:
        """添加到种草清单"""
        # 保存图片到 assets 目录（使用相对路径）
        script_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        save_dir = os.path.join(script_dir, 'assets', 'images', 'wishlist')
        os.makedirs(save_dir, exist_ok=True)
        
        import uuid
        filename = f"{uuid.uuid4().hex[:8]}_wishlist.jpg"
        save_path = os.path.join(save_dir, filename)
        shutil.copy2(image_path, save_path)
        
        # 添加到数据库
        wish_item = {
            "name": analysis.get("name", "未命名商品"),
            "category": analysis.get("category", ""),
            "color": analysis.get("color", ""),
            "material": analysis.get("material", ""),
            "price": analysis.get("price", ""),
            "brand": analysis.get("brand", ""),
            "image_path": save_path,
            "reason": reason
        }
        
        item_id = self.db.add_to_wishlist(wish_item)
        return item_id
    
    def compare_wishlist_with_wardrobe(self) -> str:
        """
        对比种草清单和现有衣橱
        用户问：今天逛街看中的衣服和家里比对
        """
        wishlist = self.db.get_wishlist(purchased=False)
        
        if not wishlist:
            return "🛍️ 你的种草清单还是空的，逛街时看到喜欢的衣服可以发给我哦！"
        
        result = "🛍️ **种草清单 vs 衣橱对比**\n\n"
        
        for item in wishlist:
            name = item.get("name", "未命名")
            color = item.get("color", "")
            price = item.get("price", "")
            
            result += f"📌 **{color}{name}**\n"
            if price:
                result += f"   价格：{price}\n"
            
            # 与衣橱对比
            analysis = {
                "name": name,
                "category": item.get("category"),
                "color": color,
                "material": item.get("material")
            }
            comparison = self._compare_with_wardrobe(analysis)
            
            if comparison["is_redundant"]:
                result += "   ⚠️ 已有类似款，建议谨慎购买\n"
            else:
                result += f"   ✅ 和你衣橱搭配度：{int(comparison['match_score']*100)}%\n"
            
            if comparison["can_match_with"]:
                matches = [i.get("name", "") for i in comparison["can_match_with"][:2]]
                result += f"   🎯 可搭配：{', '.join(matches)}\n"
            
            result += "\n"
        
        result += "💡 **建议**：\n"
        result += "• 搭配度高的可以考虑入手\n"
        result += "• 已有类似款的建议放弃\n"
        result += "• 想要哪款可以告诉我，帮你加入衣橱！"
        
        return result
