#!/usr/bin/env python3
"""
相似度检查器 - 计算技能之间的相似度
"""

from difflib import SequenceMatcher
from typing import List, Dict, Tuple

class SimilarityChecker:
    """相似度检查器"""
    
    def __init__(self, threshold: float = 0.7):
        self.threshold = threshold
    
    def text_similarity(self, text1: str, text2: str) -> float:
        """计算文本相似度 (0-1)"""
        if not text1 or not text2:
            return 0.0
        
        # 使用 SequenceMatcher 计算相似度
        return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()
    
    def check_all_pairs(self, skills: List[Dict]) -> List[Dict]:
        """检查所有技能对的相似度"""
        results = []
        
        for i in range(len(skills)):
            for j in range(i + 1, len(skills)):
                skill1 = skills[i]
                skill2 = skills[j]
                
                # 计算各项相似度
                name_sim = self.text_similarity(
                    skill1['name'], 
                    skill2['name']
                )
                desc_sim = self.text_similarity(
                    skill1['description'], 
                    skill2['description']
                )
                
                # 综合相似度 (名称 30% + 描述 70%)
                overall_sim = (name_sim * 0.3 + desc_sim * 0.7)
                
                if overall_sim >= self.threshold:
                    results.append({
                        'skill1': skill1,
                        'skill2': skill2,
                        'name_similarity': name_sim,
                        'description_similarity': desc_sim,
                        'overall_similarity': overall_sim,
                        'level': 'high' if overall_sim > 0.85 else 'medium'
                    })
        
        # 按相似度排序
        results.sort(key=lambda x: x['overall_similarity'], reverse=True)
        return results
    
    def find_most_similar(self, skills: List[Dict], target_name: str) -> List[Dict]:
        """查找与目标名称最相似的技能"""
        results = []
        
        for skill in skills:
            sim = self.text_similarity(skill['name'], target_name)
            if sim >= self.threshold:
                results.append({
                    'skill': skill,
                    'similarity': sim
                })
        
        results.sort(key=lambda x: x['similarity'], reverse=True)
        return results
