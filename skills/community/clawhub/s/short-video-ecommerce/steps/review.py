"""
第七步：生成复盘模板
预留数据填写位置，方便后续跟踪优化
"""

from datetime import datetime

class ReviewStep:
    def __init__(self):
        pass
        
    def generate_template(self, keyword: str, product_name: str) -> dict:
        """生成复盘模板"""
        
        template = self._build_template(keyword, product_name)
        
        return {
            "success": True,
            "template": template
        }
    
    def _build_template(self, keyword: str, product_name: str) -> str:
        """构建复盘模板"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        return f"""

====== 数据复盘模板 ======

商品：{product_name}
关键词：{keyword}
发布日期：{today}

【数据填写】
发布时间：____________
3 天播放量：__________
7 天播放量：__________
1 周出单量：__________
ROI：________________

【爆点分析】
这个商品为什么爆了 / 为什么没爆：


【优化建议】
下一个版本可以改进哪些地方：


【后续动作】


--- 填写完成，长期跟踪 ---
"""
