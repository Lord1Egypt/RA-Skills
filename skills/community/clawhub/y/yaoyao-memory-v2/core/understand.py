"""查询理解增强 - 意图识别 + 实体提取"""
import re
from typing import Dict, List, Tuple

class QueryUnderstanding:
    # 意图类型
    INTENTS = {
        'search': ['查找', '搜索', '找', '查询', '查看', '显示', '获取'],
        'config': ['配置', '设置', '修改', '更新', '创建', '添加', '删除'],
        'status': ['状态', '检查', '检测', '是否', '有没有'],
        'explain': ['为什么', '怎么', '如何', '什么是', '解释'],
        'compare': ['比较', '区别', '对比', '差异', '优缺点'],
    }
    
    # 实体类型
    ENTITIES = {
        'memory': ['记忆', '向量', 'FTS', '缓存', 'LLM', 'Embedding'],
        'task': ['任务', '推送', '通知', '闹钟', '日程'],
        'config': ['配置', '设置', '规则', '偏好', '风格'],
        'file': ['文件', '文档', 'PDF', 'Word', 'PPT'],
    }
    
    @classmethod
    def analyze(cls, query: str) -> Dict:
        """分析查询"""
        return {
            "intent": cls._detect_intent(query),
            "entities": cls._extract_entities(query),
            "keywords": cls._extract_keywords(query),
            "is_question": cls._is_question(query),
            "complexity": cls._estimate_complexity(query),
        }
    
    @classmethod
    def _detect_intent(cls, query: str) -> Tuple[str, float]:
        """检测意图"""
        scores = {}
        
        for intent, keywords in cls.INTENTS.items():
            score = sum(1 for kw in keywords if kw in query)
            if score > 0:
                scores[intent] = score / len(keywords)
        
        if scores:
            main_intent = max(scores, key=scores.get)
            return main_intent, scores[main_intent]
        
        return "search", 0.5
    
    @classmethod
    def _extract_entities(cls, query: str) -> List[Dict]:
        """提取实体"""
        entities = []
        
        for entity_type, keywords in cls.ENTITIES.items():
            for kw in keywords:
                if kw in query:
                    entities.append({
                        "type": entity_type,
                        "value": kw,
                        "position": query.index(kw)
                    })
        
        return sorted(entities, key=lambda x: x["position"])
    
    @classmethod
    def _extract_keywords(cls, query: str) -> List[str]:
        """提取关键词"""
        # 停用词
        stopwords = {'的', '了', '是', '在', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这'}
        
        # 分词（简单空格分词）
        words = re.findall(r'[\u4e00-\u9fa5]+|[a-zA-Z]+', query)
        
        # 过滤停用词
        keywords = [w for w in words if w not in stopwords and len(w) > 1]
        
        return keywords[:10]
    
    @classmethod
    def _is_question(cls, query: str) -> bool:
        """是否为问题"""
        question_patterns = ['?', '？', '吗', '呢', '如何', '怎么', '为什么', '什么', '哪']
        return any(p in query for p in question_patterns)
    
    @classmethod
    def _estimate_complexity(cls, query: str) -> str:
        """估计复杂度"""
        words = len(query.split())
        entities = len(cls._extract_entities(query))
        
        if words <= 3 and entities <= 1:
            return "simple"
        elif words > 10 or entities > 3:
            return "complex"
        else:
            return "medium"
    
    @classmethod
    def get_search_hints(cls, analysis: Dict) -> Dict:
        """获取搜索提示"""
        intent = analysis["intent"][0]
        entities = analysis["entities"]
        
        hints = {
            "use_vector": True,
            "use_fts": True,
            "use_llm": False,
            "boost_types": [],
        }
        
        # 根据意图调整
        if intent == "search":
            hints["use_llm"] = False
        elif intent == "explain":
            hints["use_llm"] = True
        elif intent == "compare":
            hints["use_llm"] = True
        
        # 根据实体调整
        for entity in entities:
            if entity["type"] == "config":
                hints["boost_types"].append("instruction")
            elif entity["type"] == "memory":
                hints["boost_types"].append("episodic")
        
        return hints
