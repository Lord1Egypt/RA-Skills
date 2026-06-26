import re
import os
# 注意：在 Skill 平台中，必须使用正确的包引用路径
from scripts.resume_beautifier import ResumeBeautifier 

class ResumeBeautifierPro:
    def __init__(self):
        self.engine = ResumeBeautifier()

    def diagnose(self, text):
        """AI 语义审计：核心卖点"""
        if not text or len(text.strip()) < 20:
            return {"error": "EMPTY", "msg": "内容太少，请提供完整简历文字。"}
        
        score = 65
        highlights, flaws, suggestions = [], [], []

        # 1. 逻辑纠错：时间轴
        years = [int(y) for y in re.findall(r'(?:199\d|20[0-2]\d|2030)', text)]
        if len(years) >= 2 and years[0] > years[-1] > 1990:
            score -= 20
            flaws.append("🚩 时间轴逻辑矛盾：检测到入职/毕业年份倒挂。")

        # 2. 量化审计
        if not re.search(r'\d+%|\d+人|QPS|提升|优化|降低|千万', text):
            score -= 10
            flaws.append("💡 建议量化指标：项目描述缺少具体数据支撑（如QPS、性能提升等）。")
        else:
            score += 15
            highlights.append("✅ 结果导向：简历包含明确的业务产出数据。")

        return {
            "score": min(score, 100),
            "highlights": highlights,
            "flaws": flaws,
            "suggestions": suggestions,
            "modes": ["标准投递版 (保留联系方式)", "隐私保护版 (联系方式脱敏)"]
        }

    def anonymize(self, text):
        """隐私脱敏处理（仅在用户选择时调用）"""
        # 手机号掩码
        text = re.sub(r'(1[3-9]\d)\d{4}(\d{4})', r'\1****\2', text)
        # 邮箱掩码
        text = re.sub(r'[\w\.-]+@[\w\.-]+', 'email@protected.com', text)
        return text

    def run_beautify(self, raw_text, template_style='B', is_anonymized=False):
        """
        核心运行逻辑：
        is_anonymized 参数控制是否脱敏。默认 False 保持联系方式可见。
        """
        processed_text = self.anonymize(raw_text) if is_anonymized else raw_text
        
        # 自动布局决策
        mode = "Compact_Mode" if len(processed_text) > 2000 else "Standard_Mode"
        
        output_name = "AI_Beautified_Resume.docx"
        self.engine._create_docx(processed_text, output_name, mode=mode)
        return output_name