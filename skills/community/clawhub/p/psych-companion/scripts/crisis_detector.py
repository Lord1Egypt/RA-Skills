#!/usr/bin/env python3
"""
危机检测器 - 检测用户输入中的危机信号并触发专业转介
"""

import json
import re
from pathlib import Path

class CrisisDetector:
    def __init__(self):
        self.crisis_data = self._load_crisis_data()
    
    def _load_crisis_data(self):
        """加载危机关键词数据"""
        refs_path = Path(__file__).parent.parent / "references" / "crisis_keywords.json"
        with open(refs_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def detect(self, text: str) -> dict:
        """
        检测文本中的危机信号
        
        Returns:
            dict: {
                "has_crisis": bool,
                "level": "high" | "medium" | None,
                "type": "suicide" | "self_harm" | "breakdown" | None,
                "matched_keywords": list,
                "response": str
            }
        """
        text = text.lower()
        crisis_signals = self.crisis_data.get("crisis_signals", {})
        
        results = {
            "has_crisis": False,
            "level": None,
            "type": None,
            "matched_keywords": [],
            "response": None
        }
        
        # 检查自杀相关
        suicide_keywords = crisis_signals.get("suicide", [])
        matched = [kw for kw in suicide_keywords if kw in text]
        if matched:
            results["has_crisis"] = True
            results["level"] = "high"
            results["type"] = "suicide"
            results["matched_keywords"] = matched
        
        # 检查自伤相关
        else:
            self_harm_keywords = crisis_signals.get("self_harm", [])
            matched = [kw for kw in self_harm_keywords if kw in text]
            if matched:
                results["has_crisis"] = True
                results["level"] = "high"
                results["type"] = "self_harm"
                results["matched_keywords"] = matched
            
            # 检查严重崩溃
            else:
                breakdown_keywords = crisis_signals.get("severe_breakdown", [])
                matched = [kw for kw in breakdown_keywords if kw in text]
                if matched:
                    results["has_crisis"] = True
                    results["level"] = "medium"
                    results["type"] = "breakdown"
                    results["matched_keywords"] = matched
        
        # 生成响应
        if results["has_crisis"]:
            results["response"] = self._generate_response(results["type"])
        
        return results
    
    def _generate_response(self, crisis_type: str) -> str:
        """生成危机响应话术"""
        templates = self.crisis_data.get("response_templates", {})
        hotline = self.crisis_data.get("professional_resources", {}).get("national_hotline", "400-161-9995")
        
        response_parts = []
        
        # 立即回应
        response_parts.append(templates.get("immediate", ""))
        
        # 提供热线
        hotline_text = templates.get("hotline", "").replace("400-161-9995", hotline)
        response_parts.append(hotline_text)
        
        # 当地资源
        response_parts.append(templates.get("local", ""))
        
        # 紧急情况
        response_parts.append(templates.get("emergency", ""))
        
        return "\n\n".join([r for r in response_parts if r])
    
    def should_escalate(self, text: str) -> bool:
        """判断是否需要升级转介"""
        return self.detect(text).get("has_crisis", False)


if __name__ == "__main__":
    # 测试用例
    detector = CrisisDetector()
    
    test_cases = [
        "我今天心情不好",
        "我最近压力好大",
        "活着没意思",
        "想伤害自己",
        "坚持不住了"
    ]
    
    print("=== 危机检测测试 ===\n")
    for text in test_cases:
        result = detector.detect(text)
        print(f"输入: {text}")
        print(f"危机: {result['has_crisis']}")
        print(f"级别: {result.get('level', 'N/A')}")
        print(f"类型: {result.get('type', 'N/A')}")
        print("-" * 30)