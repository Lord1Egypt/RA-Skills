import jieba.analyse
import re

class TextAnalyzer:
    @staticmethod
    def extract_keywords(text, top_k=50):
        """提取文本中的前 K 个关键名词"""
        if not text:
            return []
            
        # 预处理：移除多余空白和非文字字符
        clean_text = re.sub(r'[^\w\s]', ' ', text)
        
        # 使用 jieba 提取名词 (n, nr, nz, nt, nw, v)
        # 这里主要关注名词相关词性
        allow_pos = ('n', 'nr', 'nz', 'nt', 'nw', 'v')
        keywords = jieba.analyse.extract_tags(
            text, 
            topK=top_k, 
            withWeight=False, 
            allowPOS=allow_pos
        )
        return keywords

    @staticmethod
    def get_context_prompt(keywords):
        """将关键词转化为提示词，帮助翻译引擎精确匹配专业领域"""
        if not keywords:
            return ""
        return f"The text contains these key technical/domain terms: {', '.join(keywords)}. Please ensure professional and accurate translation of these terms."
