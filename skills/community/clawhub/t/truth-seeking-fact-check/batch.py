#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Truth (求真) v1.3 - 批量处理模块
功能：批量文本核查，并发控制适配2核2G，最大并发=2
"""

from typing import List, Dict
import concurrent.futures
from preprocess import TextPreprocessor
from checker import FactChecker, CheckResult


class BatchProcessor:
    """批量处理器"""
    
    def __init__(self, checker: FactChecker, max_concurrency: int = 2):
        self.checker = checker
        self.max_concurrency = max_concurrency  # 适配2核2G，不超过CPU核心数
    
    def process_single(self, text: str, weights = None) -> CheckResult:
        """处理单个文本，支持自定义权重"""
        if text.startswith("【违规内容已拦截】"):
            # 已被合规拦截，直接返回错误结果
            from preprocess import TextPreprocessor
            result = CheckResult(text, [], weights)
            result.credibility_score = 0.0
            result.conclusion = text
            return result
        
        sentences = TextPreprocessor().split_sentences(text)
        return self.checker.check(text, sentences, weights)
    
    def process_batch(self, texts: List[str], weights = None) -> List[CheckResult]:
        """批量处理，控制并发，支持自定义权重"""
        results = []
        
        # 并发不超过最大限制，适配2核2G
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_concurrency) as executor:
            futures = [executor.submit(self.process_single, text, weights) for text in texts]
            for future in concurrent.futures.as_completed(futures):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    # 处理异常，返回错误结果
                    from checker import CheckResult
                    result = CheckResult("", [], weights)
                    result.credibility_score = 0.0
                    result.conclusion = f"处理异常: {str(e)}"
                    results.append(result)
        
        return results


class BatchSummary:
    """批量结果汇总统计"""
    
    def __init__(self, results: List[CheckResult]):
        self.total_count = len(results)
        self.problem_count = sum(1 for r in results if len(r.problematic_sentences) > 0)
        if self.total_count > 0:
            self.average_score = round(sum(r.credibility_score for r in results) / self.total_count, 1)
            self.problem_ratio = round(self.problem_count / self.total_count * 100, 1)
        else:
            self.average_score = 0
            self.problem_ratio = 0
    
    def to_dict(self) -> Dict:
        return {
            "total_count": self.total_count,
            "average_score": self.average_score,
            "problem_count": self.problem_count,
            "problem_ratio": self.problem_ratio
        }
