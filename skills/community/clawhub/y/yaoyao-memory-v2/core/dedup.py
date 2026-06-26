from typing import Dict, List
"""结果去重增强 - 语义去重"""
from typing import List, Dict
import hashlib

class SemanticDeduplicator:
    def __init__(self, similarity_threshold: float = 0.85):
        self.threshold = similarity_threshold
    
    @staticmethod
    def content_hash(content: str) -> str:
        """内容哈希"""
        # 标准化内容
        normalized = content.lower().strip()
        return hashlib.md5(normalized.encode()).hexdigest()[:8]
    
    @staticmethod
    def simple_similarity(text1: str, text2: str) -> float:
        """简单相似度计算（基于词重叠）"""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        
        return intersection / union if union > 0 else 0.0
    
    def deduplicate(self, results: List[Dict]) -> List[Dict]:
        """语义去重"""
        if not results:
            return results
        
        deduplicated = []
        seen_hashes = set()
        
        for result in results:
            content = result.get('content', '')
            content_hash = self.content_hash(content)
            
            # 完全重复检查
            if content_hash in seen_hashes:
                continue
            
            # 语义相似检查
            is_duplicate = False
            for existing in deduplicated:
                existing_content = existing.get('content', '')
                similarity = self.simple_similarity(content, existing_content)
                
                if similarity >= self.threshold:
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                deduplicated.append(result)
                seen_hashes.add(content_hash)
        
        return deduplicated
