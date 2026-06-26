from typing import Dict, List, Tuple
"""查询改写 - 纠正拼写、标准化表达"""
import re
from typing import List, Tuple

class QueryRewriter:
    # 常见拼写错误映射（扩展）
    SPELLING_CORRECTIONS = {
        "推送规则": ["推送规责", "推送归则"],
        "用户偏好": ["用户偏号", "用户偏号设置"],
        "配置": ["配制", "配值"],
        "记忆系统": ["记忆体系", "记忆系通"],
        "向量搜索": ["向量搜所", "向量收索"],
        "LLM": ["llm", "Llm"],
        "Embedding": ["embedding", "embeding"],
        "API": ["api", "Api"],
    }
    
    # 同义词标准化（扩展）
    SYNONYMS = {
        "设置": ["配置", "设定", "调整", "修改"],
        "查看": ["检查", "显示", "获取", "查询"],
        "创建": ["新建", "添加", "建立", "生成"],
        "删除": ["移除", "清除", "去掉", "卸载"],
        "记住": ["记忆", "保存", "记录", "存储"],
        "AI": ["人工智能", "智能助手", "助手"],
        "优化": ["改进", "提升", "增强", "改善"],
        "问题": ["错误", "故障", "异常", "bug"],
    }
    
    # 语义扩展词典（新增）
    SEMANTIC_EXPANSIONS = {
        "记住": ["记忆系统", "长时记忆", "记忆存储"],
        "AI": ["智能助手", "OpenClaw", "小艺"],
        "配置": ["设置", "参数", "选项"],
        "优化": ["性能提升", "效率改进", "调优"],
    }
    
    @classmethod
    def rewrite(cls, query: str) -> Tuple[str, List[str]]:
        """改写查询"""
        original = query
        corrections = []
        
        # 1. 拼写纠正
        for correct, wrongs in cls.SPELLING_CORRECTIONS.items():
            for wrong in wrongs[:-1]:  # 最后一个是正确的
                if wrong in query:
                    query = query.replace(wrong, correct)
                    corrections.append(f"拼写纠正: {wrong} → {correct}")
        
        # 2. 同义词标准化
        for standard, synonyms in cls.SYNONYMS.items():
            for syn in synonyms:
                if syn in query and standard not in query:
                    # 不自动替换，但记录为扩展词
                    pass
        
        # 3. 去除多余空格
        query = re.sub(r'\s+', ' ', query).strip()
        
        # 4. 标点符号标准化
        query = query.replace('，', ' ').replace('、', ' ')
        
        return query, corrections
    
    @classmethod
    def get_synonym_expansions(cls, query: str) -> List[str]:
        """获取同义词扩展（优化：增加语义扩展）"""
        expansions = []
        
        # 同义词扩展
        for word, synonyms in cls.SYNONYMS.items():
            if word in query:
                for syn in synonyms:
                    expanded = query.replace(word, syn)
                    if expanded != query:
                        expansions.append(expanded)
        
        # 语义扩展（新增）
        for word, related in cls.SEMANTIC_EXPANSIONS.items():
            if word in query:
                for rel in related:
                    if rel not in query:
                        expansions.append(rel)
        
        return list(set(expansions))[:5]  # 去重，最多5个扩展
