#!/usr/bin/env python3
"""
情绪分析器 - 识别情绪类型、强度和触发因素
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional

class EmotionAnalyzer:
    def __init__(self):
        self.emotion_data = self._load_emotion_data()
    
    def _load_emotion_data(self):
        """加载情绪数据"""
        refs_path = Path(__file__).parent.parent / "references" / "emotions.json"
        with open(refs_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def analyze(self, text: str) -> dict:
        """
        分析文本中的情绪
        
        Returns:
            dict: {
                "emotions": list,  # 识别到的情绪
                "primary_emotion": str,  # 主要情绪
                "intensity": int,  # 强度 1-10
                "triggers": list,  # 可能的触发因素
                "analysis": str  # 分析说明
            }
        """
        emotions = self._detect_emotions(text)
        
        result = {
            "emotions": emotions,
            "primary_emotion": emotions[0]["name"] if emotions else "未知",
            "intensity": self._estimate_intensity(text),
            "triggers": self._extract_triggers(text),
            "analysis": self._generate_analysis(emotions)
        }
        
        return result
    
    def _detect_emotions(self, text: str) -> List[dict]:
        """检测情绪"""
        text = text.lower()
        detected = []
        
        # 检查正面情绪
        for emotion in self.emotion_data.get("emotions", {}).get("positive", []):
            if any(alias in text for alias in emotion.get("aliases", [])):
                detected.append({
                    "name": emotion["name"],
                    "type": "positive",
                    "confidence": 0.9
                })
        
        # 检查负面情绪
        for emotion in self.emotion_data.get("emotions", {}).get("negative", []):
            if any(alias in text for alias in emotion.get("aliases", [])):
                detected.append({
                    "name": emotion["name"],
                    "type": "negative",
                    "confidence": 0.9
                })
        
        # 基于关键词推断情绪
        if not detected:
            detected = self._infer_emotions(text)
        
        return detected[:3]  # 最多返回3个情绪
    
    def _infer_emotions(self, text: str) -> List[dict]:
        """基于文本推断情绪"""
        inferred = []
        
        # 焦虑推断
        if any(word in text for word in ["担心", "紧张", "害怕", "不安", "烦"]):
            inferred.append({"name": "焦虑", "type": "negative", "confidence": 0.6})
        
        # 失落推断
        if any(word in text for word in ["累", "疲惫", "无力", "疲倦"]):
            inferred.append({"name": "疲惫", "type": "negative", "confidence": 0.6})
        
        # 烦躁推断
        if any(word in text for word in ["烦", "躁", "恼火", "不顺"]):
            inferred.append({"name": "烦躁", "type": "negative", "confidence": 0.5})
        
        return inferred
    
    def _estimate_intensity(self, text: str) -> int:
        """估算情绪强度"""
        intensity_keywords = {
            9: ["非常", "极度", "极其", "十分", "太"],
            7: ["很", "比较", "相当"],
            5: ["有点", "略微", "轻微"],
            3: ["稍微", "有一点"]
        }
        
        for level, keywords in intensity_keywords.items():
            if any(kw in text for kw in keywords):
                return level
        
        # 默认中等强度
        return 5
    
    def _extract_triggers(self, text: str) -> List[str]:
        """提取可能的触发因素"""
        triggers = []
        trigger_categories = self.emotion_data.get("trigger_categories", [])
        
        for trigger in trigger_categories:
            if trigger in text:
                triggers.append(trigger)
        
        return triggers
    
    def _generate_analysis(self, emotions: List[dict]) -> str:
        """生成分析说明"""
        if not emotions:
            return "我感受到一些情绪，但不太确定具体是什么。你能更具体地描述一下吗？"
        
        primary = emotions[0]
        
        if primary.get("type") == "positive":
            return f"你现在的情绪主要是{primary['name']}，这很好！"
        else:
            intensity = self.emotion_data.get("intensity_levels", {}).get(
                str(self._get_last_intensity()), "中等"
            )
            return f"你现在的情绪主要是{primary['name']}，强度大概{intensity}。想聊聊是什么让你有这样的感受吗？"
    
    def _get_last_intensity(self) -> int:
        """获取默认强度（需要从上下文中获取）"""
        return 5
    
    def format_emotion_report(self, analysis: dict) -> str:
        """格式化情绪分析报告"""
        lines = []
        
        lines.append("📊 **情绪分析报告**")
        lines.append("")
        
        if analysis.get("emotions"):
            lines.append("**识别到的情绪：**")
            for e in analysis["emotions"]:
                emoji = "😊" if e.get("type") == "positive" else "😔"
                lines.append(f"- {emoji} {e['name']}")
            lines.append("")
        
        if analysis.get("triggers"):
            lines.append("**可能的触发因素：**")
            lines.append(", ".join(analysis["triggers"]))
            lines.append("")
        
        if analysis.get("analysis"):
            lines.append(analysis["analysis"])
        
        return "\n".join(lines)


if __name__ == "__main__":
    # 测试用例
    analyzer = EmotionAnalyzer()
    
    test_cases = [
        "今天工作压力好大，焦虑得睡不着",
        "终于完成了项目，特别开心满足",
        "和男朋友吵架了，很生气",
        "最近失眠，疲惫不堪"
    ]
    
    print("=== 情绪分析测试 ===\n")
    for text in test_cases:
        result = analyzer.analyze(text)
        print(f"输入: {text}")
        print(f"情绪: {result['emotions']}")
        print(f"主要: {result['primary_emotion']}")
        print(f"强度: {result['intensity']}")
        print(f"触发: {result['triggers']}")
        print("-" * 40)