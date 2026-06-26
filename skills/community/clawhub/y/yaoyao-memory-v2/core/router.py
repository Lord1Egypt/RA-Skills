"""智能路由 - 根据查询复杂度选择模式"""

class QueryRouter:
    @staticmethod
    def analyze(query: str) -> str:
        """分析查询复杂度"""
        # 简单特征
        simple_score = sum([
            len(query) < 10,
            len(query.split()) <= 2,
            any(kw in query for kw in ["推送", "配置", "设置", "状态", "规则"]),
        ])
        
        # 复杂特征
        complex_score = sum([
            len(query) > 30,
            "或者" in query or "和" in query,
            "?" in query or "？" in query,
            any(kw in query for kw in ["比较", "分析", "为什么", "如何", "区别"]),
        ])
        
        if complex_score > simple_score:
            return "full"
        elif simple_score >= 2:
            return "fast"
        else:
            return "balanced"
    
    @staticmethod
    def select_mode(query: str, use_llm: bool) -> str:
        """选择搜索模式"""
        if not use_llm:
            return "fast"
        
        complexity = QueryRouter.analyze(query)
        
        if complexity == "simple":
            return "fast"
        elif complexity == "complex":
            return "full"
        else:
            return "balanced"
