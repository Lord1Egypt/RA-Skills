from typing import Dict, List, Tuple
"""动态权重调整"""
from typing import Dict, Tuple

class DynamicWeights:
    @staticmethod
    def calculate(query: str) -> Tuple[float, float]:
        """计算向量搜索和FTS搜索的权重"""
        # 默认权重
        vector_weight = 0.7
        fts_weight = 0.3
        
        # 查询特征分析
        features = DynamicWeights._analyze_query(query)
        
        # 精确匹配倾向（短词、专有名词）
        if features['has_exact_terms']:
            fts_weight += 0.2
            vector_weight -= 0.2
        
        # 语义匹配倾向（长句、描述性）
        if features['is_descriptive']:
            vector_weight += 0.15
            fts_weight -= 0.15
        
        # 问题类查询（语义更重要）
        if features['is_question']:
            vector_weight += 0.1
            fts_weight -= 0.1
        
        # 确保权重在合理范围
        vector_weight = max(0.3, min(0.9, vector_weight))
        fts_weight = max(0.1, min(0.7, fts_weight))
        
        return vector_weight, fts_weight
    
    @staticmethod
    def _analyze_query(query: str) -> Dict:
        """分析查询特征"""
        words = query.split()
        
        return {
            'length': len(query),
            'word_count': len(words),
            'has_exact_terms': any(w in query for w in ['配置', '设置', '规则', '状态', 'ID', '名称']),
            'is_descriptive': len(query) > 20 or any(w in query for w in ['如何', '为什么', '怎样', '什么']),
            'is_question': '?' in query or '？' in query or any(w in query for w in ['如何', '为什么', '怎样', '什么', '吗']),
            'has_numbers': any(c.isdigit() for c in query),
        }
    
    @staticmethod
    def apply_weights(vector_results: list, fts_results: list, 
                       vector_weight: float, fts_weight: float) -> list:
        """应用权重到结果"""
        # 为向量结果添加权重分数
        for r in vector_results:
            r['weighted_score'] = r.get('score', 0) * vector_weight
        
        # 为FTS结果添加权重分数
        for r in fts_results:
            # FTS 结果没有相似度分数，使用固定值
            r['weighted_score'] = 0.5 * fts_weight
        
        # 合并并按加权分数排序
        all_results = vector_results + fts_results
        all_results.sort(key=lambda x: x.get('weighted_score', 0), reverse=True)
        
        return all_results
