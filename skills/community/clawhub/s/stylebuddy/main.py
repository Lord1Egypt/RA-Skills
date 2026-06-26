"""
StyleBuddy - AI 穿搭助手
主入口文件
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.core.router import CapabilityRouter
from src.storage.database import Database
from src.core.recommender import OutfitRecommender
from src.core.analyzer import WardrobeAnalyzer
from src.services.visualizer import OutfitVisualizer
from src.services.weather import WeatherService
from src.models.wardrobe import WardrobeManager
from src.services.shopping import ShoppingConsultant
import json

class StyleBuddy:
    """StyleBuddy 主类"""
    
    def __init__(self):
        self.db = Database()
        self.router = CapabilityRouter()
        self.recommender = OutfitRecommender(self.db)
        self.analyzer = WardrobeAnalyzer(self.db)
        self.visualizer = OutfitVisualizer()
        self.weather = WeatherService()
        self.wardrobe = WardrobeManager(self.db)
        self.shopping = ShoppingConsultant(self.db, self.wardrobe)
        self.capabilities = self.router.detect()
        
    def _is_first_time(self) -> bool:
        """检查是否是首次使用"""
        items = self.db.get_all_items()
        return len(items) == 0
    
    def _get_welcome_message(self) -> str:
        """首次使用欢迎语"""
        return """🌸 **欢迎使用 StyleBuddy！**

我是你的 AI 穿搭闺蜜，帮你管理衣橱、智能搭配，让穿搭变得更简单～

━━━━━━━━━━━━━━━━━━━━━━
📸 **录入衣服**
   拍照或文字描述，我会自动识别材质、颜色、风格
   👉 试试：拍张照片发给我，或说"录入一件蓝色卫衣"

👗 **查看衣橱**  
   随时了解你有什么衣服
   👉 试试："我有什么衣服"

✨ **智能搭配**
   根据天气、场合推荐穿搭
   👉 试试："今天穿什么" 或 "明天约会怎么搭"

🛍️ **种草咨询**
   逛街看中衣服？发给我，帮你对比衣橱、给建议
   👉 试试：拍商场衣服照片

📊 **衣橱分析**
   分析你的穿衣习惯，优化衣橱
   👉 试试："帮我分析衣橱"

━━━━━━━━━━━━━━━━━━━━━━
💡 **小技巧**
   • 拍照时带上吊牌，我能识别材质和价格
   • 逛街种草 vs 录入衣橱，我会自动判断或询问你

**现在，录入你的第一件衣服吧！** 📸"""
    
    def _detect_intent(self, user_input: str, has_image: bool) -> str:
        """
        检测用户意图
        
        Returns:
            "wardrobe_add" - 录入衣橱
            "shopping_consult" - 种草咨询
            "ask_clarification" - 需要询问
        """
        user_input_lower = user_input.lower().strip()
        
        # 录入衣橱关键词
        wardrobe_keywords = ["录入", "添加", "新买", "我的", "已有", "这件是", "入库"]
        # 种草咨询关键词
        shopping_keywords = ["好看吗", "建议", "值不值", "怎么样", "适合", "搭配吗", 
                           "买吗", "种草", "纠结", "要不要", "选哪个"]
        
        # 明确说录入 → 录入衣橱
        if any(kw in user_input_lower for kw in wardrobe_keywords):
            return "wardrobe_add"
        
        # 明确咨询 → 种草咨询
        if any(kw in user_input_lower for kw in shopping_keywords):
            return "shopping_consult"
        
        # 只发图没说文字 → 默认种草咨询（逛街随手拍场景）
        if has_image and not user_input:
            return "shopping_consult"
        
        # 不确定 → 询问
        return "ask_clarification"
    
    def _ask_intent_clarification(self) -> str:
        """询问用户意图"""
        return "🤔 看起来你发了一张衣服照片！\n\n这是在：\n📸 [录入我的衣橱] - 已经买的衣服，录入管理\n🛍️ [种草咨询] - 逛街看中，给购买建议\n\n请告诉我你的意图，或点击上面的选项！"
    
    def _handle_shopping_consult(self, context: dict) -> str:
        """处理种草咨询"""
        image_path = context.get('image')
        if not image_path:
            return "请发送衣服照片，我来帮你分析！"
        
        # 进行分析
        result = self.shopping.consult(image_path)
        
        # 格式化输出
        output = """🛍️ **种草咨询分析**

📸 **衣服识别**
   名称：{name}
   颜色：{color}
   材质：{material}
   价格：{price}

💡 **购买建议**
{advice}

📋 **操作**
[加入种草清单] [查看衣橱对比] [算了不买了]""".format(
            name=result['analysis'].get('name', '待识别'),
            color=result['analysis'].get('color', '待识别'),
            material=result['analysis'].get('material', '待识别'),
            price=result['analysis'].get('price', '未知'),
            advice=result['recommendation']
        )
        
        return output
    
    def _handle_wishlist_query(self, user_input: str) -> str:
        """处理种草清单相关查询"""
        # 对比种草和衣橱
        if any(kw in user_input for kw in ["对比", "比对", "和家里"]):
            return self.shopping.compare_wishlist_with_wardrobe()
        
        # 查看种草清单
        wishlist = self.db.get_wishlist(purchased=False)
        if not wishlist:
            return "🛍️ 你的种草清单是空的，逛街看到喜欢的可以发给我！"
        
        result = "🛍️ **你的种草清单**\n\n"
        for i, item in enumerate(wishlist[:5], 1):
            name = item.get('name', '未命名')
            color = item.get('color', '')
            price = item.get('price', '')
            result += f"{i}. {color}{name}"
            if price:
                result += f" ({price})"
            result += "\n"
        
        result += "\n💡 说'种草清单对比衣橱'查看购买建议！"
        return output
    
    def process(self, user_input: str, context: dict = None):
        """处理用户输入"""
        # 首次使用检测
        if self._is_first_time() and user_input in ["开始", "你好", "hi", "hello", "?", "帮助", "怎么用"]:
            return self._get_welcome_message()
        
        # 检测是否有图片
        has_image = context and 'image' in context
        
        # 种草清单相关
        if any(kw in user_input for kw in ["种草", "逛街", "看中", "清单"]):
            return self._handle_wishlist_query(user_input)
        
        # 如果有图片，进行意图识别
        if has_image:
            intent = self._detect_intent(user_input, has_image)
            
            if intent == "wardrobe_add":
                return self._handle_add_item(user_input, context)
            elif intent == "shopping_consult":
                return self._handle_shopping_consult(context)
            else:
                # 询问用户意图
                return self._ask_intent_clarification()
        
        user_input_lower = user_input.lower().strip()
        
        # 路由到不同功能 - 更精确的关键词匹配
        if any(kw in user_input_lower for kw in ["录入", "添加", "新买", "我有件", "买了件", "买了", "买了双"]) and \
           (any(kw in user_input_lower for kw in ["件", "条", "双", "个", "套"]) or \
            any(kw in user_input_lower for kw in ["风衣", "外套", "t恤", "衬衫", "卫衣", "毛衣", "牛仔裤", "裤子", "裙子", "鞋", "大衣", "西装"])):
            return self._handle_add_item(user_input, context)
        
        elif any(kw in user_input_lower for kw in ["衣橱", "有什么衣服", "我的衣服", "查看衣服"]):
            return self._handle_wardrobe_view()
        
        elif any(kw in user_input for kw in ["今天穿", "推荐", "搭配", "明天穿"]):
            return self._handle_recommendation(user_input, context)
        
        elif any(kw in user_input for kw in ["记录", "今天穿", "穿了"]):
            return self._handle_record_outfit(user_input, context)
        
        elif any(kw in user_input for kw in ["分析", "诊断", "统计"]):
            return self._handle_analysis()
        
        elif any(kw in user_input for kw in ["一衣多穿", "怎么搭"]):
            return self._handle_item_styling(user_input)
        
        elif any(kw in user_input for kw in ["备份", "恢复", "导出", "导入"]):
            return self._handle_backup(user_input)
        
        else:
            return self._handle_help()
    
    def _handle_add_item(self, user_input, context):
        """处理添加单品"""
        # 简单解析
        result = self.wardrobe.parse_and_add(user_input, context)
        return result
    
    def _handle_wardrobe_view(self):
        """查看衣橱"""
        return self.wardrobe.get_wardrobe_summary()
    
    def _handle_recommendation(self, user_input, context):
        """处理搭配推荐"""
        # 获取天气
        weather = None
        if self.capabilities.get("weather_api"):
            weather = self.weather.get_current()
        
        # 获取场合
        occasion = self._extract_occasion(user_input)
        
        # 生成推荐
        recommendations = self.recommender.recommend(
            occasion=occasion,
            weather=weather,
            count=3
        )
        
        return self._format_recommendations(recommendations, weather)
    
    def _handle_record_outfit(self, user_input, context):
        """记录今日穿搭"""
        return self.wardrobe.record_today_outfit(context)
    
    def _handle_analysis(self):
        """衣橱分析"""
        return self.analyzer.generate_report()
    
    def _handle_item_styling(self, user_input):
        """一衣多穿"""
        item_name = self._extract_item_name(user_input)
        if item_name:
            styles = self.recommender.get_item_styles(item_name)
            return self._format_styles(item_name, styles)
        return "请告诉我你想怎么搭配哪件单品？比如：'这件风衣怎么搭'"
    
    def _handle_backup(self, user_input):
        """备份/恢复"""
        if "恢复" in user_input or "导入" in user_input:
            return self.wardrobe.restore_data()
        return self.wardrobe.backup_data()
    
    def _handle_help(self):
        """帮助信息"""
        return """🌸 StyleBuddy - 你的 AI 穿搭助手

我可以帮你：
• 录入衣服 - "录入一件米色风衣"
• 查看衣橱 - "我有什么衣服"
• 搭配推荐 - "今天穿什么" / "明天约会穿什么"
• 记录穿搭 - "记录今日穿搭"
• 衣橱分析 - "帮我分析衣橱"
• 一衣多穿 - "这件风衣怎么搭"
• 数据备份 - "备份衣橱数据"

有什么穿搭问题随时问我！"""
    
    def _extract_occasion(self, user_input):
        """提取场合"""
        occasions = {
            "约会": "约会", "见面": "约会", "date": "约会",
            "上班": "职场", "工作": "职场", "职场": "职场", "面试": "职场",
            "运动": "运动", "健身": "运动", "跑步": "运动",
            "逛街": "休闲", "日常": "休闲", "周末": "休闲", "休闲": "休闲",
            "聚会": "聚会", "party": "聚会", "派对": "聚会",
            "旅行": "旅行", "旅游": "旅行", "度假": "旅行"
        }
        for key, value in occasions.items():
            if key in user_input:
                return value
        return "日常"
    
    def _extract_item_name(self, user_input):
        """提取单品名称"""
        # 简单提取
        prefixes = ["这件", "这件", "我的", "那个", "那件"]
        for p in prefixes:
            if p in user_input:
                start = user_input.find(p) + len(p)
                end = user_input.find("怎么", start)
                if end == -1:
                    end = len(user_input)
                return user_input[start:end].strip()
        return None
    
    def _format_recommendations(self, recommendations, weather):
        """格式化推荐结果"""
        if not recommendations:
            return "还没有足够的单品来推荐搭配，先录入一些衣服吧！"
        
        weather_info = ""
        if weather:
            weather_info = f"\n🌤️ 今日天气：{weather.get('temp', '?')}°C {weather.get('condition', '')}\n"
        
        result = f"🌸 为你准备了 {len(recommendations)} 套搭配方案{weather_info}\n"
        image_paths = []
        
        for i, outfit in enumerate(recommendations, 1):
            result += f"\n--- 方案 {i} ---\n"
            result += f"{outfit.get('name', '未命名搭配')}\n"
            items = outfit.get('items', [])
            if items:
                result += "搭配：" + " + ".join(items) + "\n"
            result += f"💡 {outfit.get('tips', '')}\n"
            
            # 收集图片路径
            img_path = outfit.get('image_path')
            if img_path:
                image_paths.append(img_path)
        
        # 返回文本和图片路径
        return {
            "text": result,
            "images": image_paths
        }
    
    def process_with_images(self, user_input: str, context: dict = None):
        """处理用户输入并返回文本+图片"""
        result = self.process(user_input, context)
        
        # 如果结果是字典（包含图片），直接返回
        if isinstance(result, dict):
            return result
        
        # 否则包装成字典
        return {"text": result, "images": []}
    
    def _format_styles(self, item_name, styles):
        """格式化一衣多穿结果"""
        if not styles:
            return f"暂无 '{item_name}' 的搭配方案"
        
        result = f"🌸 '{item_name}' 的 {len(styles)} 种搭配方式\n\n"
        for i, style in enumerate(styles, 1):
            result += f"{i}. {style.get('name', '未命名')}\n"
            items = style.get('items', [])
            if items:
                result += f"   搭配：{' + '.join(items)}\n"
            result += f"   💡 {style.get('tips', '')}\n\n"
        
        return result


def main():
    """主函数 - 供 OpenClaw 调用"""
    buddy = StyleBuddy()
    
    # 如果是命令行测试
    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
        result = buddy.process(user_input)
        print(result)
        return result
    
    return buddy


if __name__ == "__main__":
    main()
