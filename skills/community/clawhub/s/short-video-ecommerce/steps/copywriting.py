"""
第二步：文案脚本生成
对标爆款分析，生成15秒三段式分镜脚本（每段5秒）
"""

from typing import List
import logging

logger = logging.getLogger(__name__)

class CopywritingStep:
    def __init__(self):
        pass
        
    def generate_script(self, product_name: str, product_features: List[str], category: str) -> Dict:
        """
        生成15秒分镜脚本
        返回三段文案：[开场痛点, 产品卖点, 引导下单]
        """
        logger.info(f"为 {product_name} 生成文案脚本")
        
        # TODO: 对标该类目头部爆款，分析结构后生成
        # 三段式结构：0-5s / 5-10s / 10-15s
        
        script_sections = {
            "opening": "",   # 0-5s 开场痛点
            "middle": "",    # 5-10s 产品卖点
            "closing": ""    # 10-15s 引导下单
        }
        
        # 模板框架（实际由AI生成）
        script_template = self._get_template(category)
        
        return {
            "success": True,
            "product": product_name,
            "sections": script_sections,
            "full_script": self._format_script(script_sections),
            "template_used": script_template
        }
    
    def _get_template(self, category: str) -> str:
        """根据类目获取模板"""
        templates = {
            "food": "美食：痛点（饿了/嘴馋）→ 产品展示 → 赶紧下单",
            "clothing": "女装：身材痛点 → 展示效果 → 点击购买",
            "home": "家居：生活麻烦 → 产品解决 → 改善生活",
            "beauty": "美妆：皮肤问题 → 产品效果 → 赶紧入手",
        }
        return templates.get(category.lower(), "通用：场景痛点 → 产品优势 → 引导下单")
    
    def _format_script(self, sections: Dict) -> str:
        """格式化完整脚本"""
        return f"""【0-5秒 开场痛点】
{sections['opening']}

【5-10秒 产品卖点】
{sections['middle']}

【10-15秒 引导下单】
{sections['closing']}
"""
