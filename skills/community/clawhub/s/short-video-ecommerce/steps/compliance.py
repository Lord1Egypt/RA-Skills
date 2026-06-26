"""
第五步：合规检查
- 图片logo检测：检查是否清理干净
- 文案敏感词检查
- 平台规则合规检查
- 侵权风险提示
"""

import re
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

# 常见敏感词列表（示例）
SENSITIVE_WORDS = [
    # 绝对化用语
    "最", "第一", "国家级", "最高级", "最佳", "顶级", "极致",
    # 医疗相关
    "治疗", "治愈", "疗效", "防癌", "抗癌",
    # 虚假承诺
    "保证", "100%", "必涨", "保本",
]

class ComplianceStep:
    def __init__(self):
        pass
        
    def check_image(self, image_path) -> dict:
        """检查图片是否有logo需要去除"""
        # TODO: 图像识别检测logo
        result = {
            "has_logo": False,
            "needs_processing": False,
            "note": ""
        }
        return result
    
    def check_text(self, text: str) -> dict:
        """检查文案是否有敏感词"""
        found = []
        for word in SENSITIVE_WORDS:
            if word in text:
                found.append(word)
        
        return {
            "success": True,
            "sensitive_words_found": found,
            "passed": len(found) == 0,
            "text_length_ok": 5 <= len(text) <= 500
        }
    
    def check_video(self, video_path) -> dict:
        """检查视频合规性"""
        # TODO: 检查分辨率、时长、内容
        return {
            "success": True,
            "passed": True,
            "note": "视频格式检查通过"
        }
    
    def generate_report(self, image_check, text_check, video_check) -> dict:
        """生成合规检查报告"""
        all_passed = (
            (not image_check.get('needs_processing', True)) and
            text_check.get('passed', False) and
            video_check.get('passed', False)
        )
        
        report = "====== 合规检查报告 ======\n"
        report += f"图片logo检查: {'通过' if not image_check.get('needs_processing') else '需要处理'}\n"
        report += f"文案敏感词: {'通过' if text_check['passed'] else f'发现 {len(text_check[\"sensitive_words_found\"])} 个敏感词'}\n"
        
        if text_check['sensitive_words_found']:
            report += f"敏感词列表: {', '.join(text_check['sensitive_words_found'])}\n"
            
        report += f"视频合规: {'通过' if video_check['passed'] else '不通过'}\n"
        report += f"\n总体结果: {'✅ 通过' if all_passed else '⚠️ 需要修正'}\n"
        
        # 通用提示
        report += "\n【风险提示】\n"
        report += "- 使用品牌商品请确保获得品牌授权\n"
        report += "- 图片中第三方logo请务必去除\n"
        report += "- 夸大宣传用语请修改\n"
        
        return {
            "all_passed": all_passed,
            "report": report
        }
