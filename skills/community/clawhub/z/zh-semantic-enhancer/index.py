#!/usr/bin/env python3
"""
中文语义理解增强技能 - 主入口
Chinese Semantic Enhancement Skill - Main Entry
"""

import os
import sys
import json
from typing import Dict, Any

# 添加 scripts 目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts'))

try:
    from zh_tokenizer import enhanced_tokenize
    from intent_enhancer import enhance_intent
    from zh_expressions import detect_expression
    from pricing import PricingManager, PRICING_TIERS
    from credit_system import CreditSystem, CREDIT_PACKAGES
    from premium_features import PremiumFeatures
    from enterprise_features import EnterpriseFeatures
    HAS_PREMIUM = True
except ImportError:
    # 如果依赖未安装，使用简化版本
    def enhanced_tokenize(text: str) -> dict:
        return {"tokens": list(text), "entities": [], "domain": "general"}
    
    def enhance_intent(raw_intent: str, context: dict) -> dict:
        return {
            "original": raw_intent,
            "normalized": raw_intent,
            "confidence": 0.8,
            "suggested_actions": []
        }
    
    def detect_expression(text: str) -> list:
        return []
    
    HAS_PREMIUM = False

# SkillPay 配置
BILLING_URL = 'https://skillpay.me/api/v1/billing'
API_KEY = os.environ.get('SKILLPAY_API_KEY', '')
SKILL_ID = os.environ.get('SKILLPAY_SKILL_ID', '')
VERSION = "1.1.0"

class ZHSemanticEnhancer:
    """中文语义增强器"""
    
    def __init__(self, api_key: str = API_KEY, skill_id: str = SKILL_ID):
        self.api_key = api_key
        self.skill_id = skill_id
        self.demo_mode = not api_key
        self.trial_manager = TrialManager("zh-semantic-enhancer")
        self.lang = 'zh'
    
    def process(self, text: str, user_id: str = "") -> Dict[str, Any]:
        """处理中文文本"""
        if self.demo_mode:
            return self._demo_process(text)
        
        # 检查免费试用
        trial_remaining = self.trial_manager.get_trial_remaining(user_id)
        
        if trial_remaining > 0:
            self.trial_manager.use_trial(user_id)
            result = self._analyze(text)
            result["trial_mode"] = True
            result["trial_remaining"] = trial_remaining - 1
            return result
        
        # 付费模式
        result = self._analyze(text)
        result["trial_mode"] = False
        result["trial_remaining"] = 0
        return result
    
    def _demo_process(self, text: str) -> Dict[str, Any]:
        """演示模式处理"""
        return {
            "success": True,
            "demo_mode": True,
            "original": text,
            "normalized": text,
            "tokens": self._simple_tokenize(text),
            "entities": [],
            "expressions": self._detect_demo_expressions(text),
            "confidence": 0.85,
            "suggested_actions": ["尝试使用完整句子以获得更好效果"],
            "trial_mode": False,
            "trial_remaining": 100,
            "note": "演示模式：完整功能需要API密钥"
        }
    
    def _analyze(self, text: str) -> Dict[str, Any]:
        """完整分析"""
        # 1. 分词+实体识别
        zh_analysis = enhanced_tokenize(text)
        
        # 2. 识别特有表达
        expressions = detect_expression(text)
        
        # 3. 意图增强
        enhanced = enhance_intent(text, zh_analysis)
        
        return {
            "success": True,
            "demo_mode": False,
            "original": enhanced["original"],
            "normalized": enhanced["normalized"],
            "tokens": zh_analysis.get("tokens", []),
            "entities": zh_analysis.get("entities", []),
            "expressions": expressions,
            "domain": zh_analysis.get("domain", "general"),
            "confidence": enhanced["confidence"],
            "suggested_actions": enhanced.get("suggested_actions", [])
        }
    
    def _simple_tokenize(self, text: str) -> list:
        """简单分词（演示模式）"""
        # 基础中文分词：按字符和常见词分割
        tokens = []
        i = 0
        while i < len(text):
            # 尝试匹配2-4字词
            matched = False
            for length in [4, 3, 2]:
                if i + length <= len(text):
                    word = text[i:i+length]
                    if word in COMMON_WORDS:
                        tokens.append((word, "n"))
                        i += length
                        matched = True
                        break
            if not matched:
                tokens.append((text[i], "x"))
                i += 1
        return tokens
    
    def _detect_demo_expressions(self, text: str) -> list:
        """演示模式：检测常见表达"""
        expressions = []
        demo_db = {
            "yyds": {"type": "internet_slang", "meaning": "永远的神"},
            "内卷": {"type": "slang", "meaning": "非理性竞争"},
            "躺平": {"type": "slang", "meaning": "放弃竞争"},
            "画蛇添足": {"type": "idiom", "meaning": "多此一举"},
        }
        for expr, meta in demo_db.items():
            if expr in text:
                expressions.append({
                    "expression": expr,
                    **meta
                })
        return expressions


# 常用词库（演示模式）
COMMON_WORDS = {
    "中文", "语义", "理解", "增强", "技能", "分析", "处理",
    "意思", "方便", "内卷", "躺平", "yyds", "画蛇添足"
}


# 免费试用管理
class TrialManager:
    def __init__(self, skill_name: str):
        self.skill_name = skill_name
        self.trial_dir = os.path.expanduser("~/.openclaw/skill_trial")
        self.trial_file = os.path.join(self.trial_dir, f"{skill_name}.json")
        self.max_free_calls = 100  # 100次免费试用
        os.makedirs(self.trial_dir, exist_ok=True)
    
    def _load_trial_data(self) -> Dict[str, Any]:
        if os.path.exists(self.trial_file):
            try:
                with open(self.trial_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_trial_data(self, data: Dict[str, Any]):
        try:
            with open(self.trial_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except:
            pass
    
    def get_trial_remaining(self, user_id: str) -> int:
        if not user_id:
            return 0
        data = self._load_trial_data()
        user_data = data.get(user_id, {})
        used_calls = user_data.get('used_calls', 0)
        return max(0, self.max_free_calls - used_calls)
    
    def use_trial(self, user_id: str) -> bool:
        if not user_id:
            return False
        data = self._load_trial_data()
        if user_id not in data:
            data[user_id] = {'used_calls': 0}
        data[user_id]['used_calls'] += 1
        self._save_trial_data(data)
        return True


def on_user_input(text: str, context: dict = None) -> dict:
    """
    OpenClaw调用入口
    """
    context = context or {}
    user_id = context.get("user_id", "")
    
    enhancer = ZHSemanticEnhancer()
    return enhancer.process(text, user_id)


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='中文语义理解增强技能')
    parser.add_argument('--input', '-i', help='输入中文文本')
    parser.add_argument('--user-id', '-u', help='用户ID')
    parser.add_argument('--demo', action='store_true', help='演示模式')
    
    args = parser.parse_args()
    
    if args.input:
        result = on_user_input(args.input, {"user_id": args.user_id or "demo"})
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        # 交互模式
        print("🀄 中文语义理解增强技能")
        print("输入中文文本进行分析 (输入 'quit' 退出):")
        while True:
            try:
                text = input("> ")
                if text.lower() in ['quit', 'exit', '退出']:
                    break
                result = on_user_input(text, {"user_id": "cli_user"})
                print(json.dumps(result, ensure_ascii=False, indent=2))
            except EOFError:
                break
            except KeyboardInterrupt:
                break


if __name__ == "__main__":
    main()
