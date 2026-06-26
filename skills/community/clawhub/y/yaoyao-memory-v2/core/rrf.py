"""RRF (Reciprocal Rank Fusion) 混合检索"""
from typing import List, Dict

class RRFFusion:
    """RRF 算法实现"""
    
    def __init__(self, k: int = 60):
        """
        Args:
            k: RRF 参数，默认60
        """
        self.k = k
    
    def fuse(self, vector_results: List[Dict], fts_results: List[Dict]) -> List[Dict]:
        """
        RRF 融合
        
        公式: RRF(d) = Σ 1/(k + rank(d))
        """
        # 计算每个结果的 RRF 分数
        scores = {}
        
        # 向量结果排名
        for rank, result in enumerate(vector_results, 1):
            rid = result.get("record_id")
            if rid not in scores:
                scores[rid] = {
                    "record_id": rid,
                    "content": result.get("content", ""),
                    "type": result.get("type", ""),
                    "scene": result.get("scene", ""),
                    "vector_rank": rank,
                    "fts_rank": None,
                    "rrf_score": 0,
                    "source": "vector"
                }
            scores[rid]["rrf_score"] += 1 / (self.k + rank)
        
        # FTS 结果排名
        for rank, result in enumerate(fts_results, 1):
            rid = result.get("record_id")
            if rid not in scores:
                scores[rid] = {
                    "record_id": rid,
                    "content": result.get("content", ""),
                    "type": result.get("type", ""),
                    "scene": result.get("scene", ""),
                    "vector_rank": None,
                    "fts_rank": rank,
                    "rrf_score": 0,
                    "source": "fts"
                }
            else:
                scores[rid]["fts_rank"] = rank
                scores[rid]["source"] = "hybrid"
            scores[rid]["rrf_score"] += 1 / (self.k + rank)
        
        # 按 RRF 分数排序
        results = list(scores.values())
        results.sort(key=lambda x: x["rrf_score"], reverse=True)
        
        return results
    
    @staticmethod
    def explain_rank(vector_rank: int, fts_rank: int, k: int = 60) -> str:
        """解释排名"""
        vec_score = 1 / (k + vector_rank) if vector_rank else 0
        fts_score = 1 / (k + fts_rank) if fts_rank else 0
        total = vec_score + fts_score
        
        parts = []
        if vector_rank:
            parts.append(f"向量排名#{vector_rank}={vec_score:.4f}")
        if fts_rank:
            parts.append(f"FTS排名#{fts_rank}={fts_score:.4f}")
        
        return f"RRF={total:.4f} ({' + '.join(parts)})"
