#!/usr/bin/env python3
"""
behavior_learner.py - 智能行为学习器

通过观察用户行为，学习功能开关的最佳配置

功能：
1. 行为模式识别 - 从对话和指令中提取模式
2. 偏好学习 - 学习用户对功能开关的偏好
3. 建议生成 - 基于学习到的模式生成配置建议
4. 自动应用 - 可选的自动调整功能开关
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import Counter

sys.path.insert(0, str(Path(__file__).parent))

from feature_flag import FeatureFlag, FLAG_DIR


@dataclass
class BehaviorPattern:
    """行为模式"""
    pattern_type: str           # "command", "query", "preference", "complaint"
    trigger: str               # 触发词
    action: str               # 触发的动作
    count: int = 1            # 出现次数
    last_seen: str = ""       # 上次看到时间
    confidence: float = 0.5   # 置信度 0-1
    related_flags: List[str] = field(default_factory=list)  # 相关功能开关


@dataclass
class Preference:
    """学习到的偏好"""
    flag_name: str
    current_value: any
    learned_value: any
    evidence: List[str] = field(default_factory=list)  # 证据
    confidence: float = 0.5
    last_updated: str = ""


class BehaviorLearner:
    """智能行为学习器"""
    
    def __init__(self):
        self.patterns: Dict[str, BehaviorPattern] = {}
        self.preferences: Dict[str, Preference] = {}
        self.data_dir = FLAG_DIR / "learner"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.patterns_file = self.data_dir / "patterns.json"
        self.preferences_file = self.data_dir / "preferences.json"
        
        self._load_data()
        
        # 中文关键词 → 英文flag映射
        self.keyword_to_flag = {
            # 通用
            "自动": ["memory.auto_promote", "memory.auto_cleanup", "feedback.auto_adjust"],
            "同步": ["memory.ima_sync", "push.dual_channel"],
            "推送": ["push.meow_enabled", "push.dual_channel"],
            "安静": ["ux.silent_mode"],
            "静默": ["ux.silent_mode"],
            "提示": ["ux.show_confidence"],
            "搜索": ["search.hybrid", "search.vector_search"],
            "向量": ["search.vector_search", "memory.vector_search"],
            "模糊": ["search.fuzzy"],
            "缓存": ["search.cache"],
            "确认": ["approval.require_confirmation"],
            "安全": ["shell.whitelist_only", "security.prompt_guard"],
            "学习": ["feedback.enabled", "exp.persona_update"],
            "摘要": ["memory.summarize_daily"],
            "清理": ["memory.auto_cleanup"],
            "提升": ["memory.auto_promote"],
            "自动推送": ["push.dual_channel"],
            "详细": ["ux.detailed_errors"],
            "简洁": ["ux.silent_mode"],
        }
        
        # 行为模式关键词映射（用于模式识别）
        self.pattern_keywords = {
            # 命令类触发词 → 相关功能开关
            "快速": ["search.fast_mode", "search.cache"],
            "慢": ["search.fast_mode", "performance.optimize"],
            "详细": ["ux.detailed_errors", "search.cache"],
            "简洁": ["ux.silent_mode", "ux.show_confidence"],
            "自动": ["memory.auto_promote", "memory.auto_cleanup", "feedback.auto_adjust"],
            "手动": ["memory.auto_promote"],
            "同步": ["memory.ima_sync", "push.dual_channel"],
            "推送": ["push.meow_enabled", "push.dual_channel"],
            "安静": ["ux.silent_mode"],
            "提示": ["ux.show_confidence", "ux.silent_mode"],
            "搜索": ["search.hybrid", "search.vector_search"],
            "向量": ["search.vector_search", "memory.vector_search"],
            "模糊": ["search.fuzzy"],
            "缓存": ["search.cache", "memory.cache"],
            "忽略": ["ux.silent_mode"],
            "确认": ["approval.require_confirmation"],
            "安全": ["shell.whitelist_only", "security.prompt_guard"],
        }
        
        # 抱怨/投诉类触发词 → 需要关闭或调整
        self.complaint_keywords = {
            "太慢": ["performance.optimize", "search.cache"],
            "太快": ["search.cache"],
            "打扰": ["ux.silent_mode", "push.dual_channel"],
            "没用": ["feedback.enabled"],
            "不清楚": ["ux.detailed_errors"],
            "太吵": ["ux.silent_mode"],
            "不要提示": ["ux.silent_mode"],
            "关掉": ["ux.show_confidence"],
            "烦": ["ux.silent_mode", "push.dual_channel"],
        }
    
    def _load_data(self):
        """加载学习数据"""
        # 加载模式
        if self.patterns_file.exists():
            try:
                data = json.loads(self.patterns_file.read_text())
                self.patterns = {k: BehaviorPattern(**v) for k, v in data.items()}
            except:
                pass
        
        # 加载偏好
        if self.preferences_file.exists():
            try:
                data = json.loads(self.preferences_file.read_text())
                self.preferences = {k: Preference(**v) for k, v in data.items()}
            except:
                pass
    
    def _save_data(self):
        """保存学习数据"""
        # 保存模式
        patterns_data = {k: v.__dict__ for k, v in self.patterns.items()}
        self.patterns_file.write_text(json.dumps(patterns_data, indent=2, ensure_ascii=False))
        
        # 保存偏好
        prefs_data = {k: v.__dict__ for k, v in self.preferences.items()}
        self.preferences_file.write_text(json.dumps(prefs_data, indent=2, ensure_ascii=False))
    
    def observe(self, text: str, context: str = "conversation"):
        """
        观察用户行为
        
        Args:
            text: 用户输入的文本
            context: 上下文 ("conversation", "command", "question", "feedback")
        """
        text_lower = text.lower()
        now = datetime.now().isoformat()
        
        # 1. 检测行为模式
        for trigger, related_flags in self.pattern_keywords.items():
            if trigger in text_lower:
                pattern_key = f"{trigger}_{context}"
                
                if pattern_key in self.patterns:
                    p = self.patterns[pattern_key]
                    p.count += 1
                    p.last_seen = now
                    p.confidence = min(1.0, p.count / 10)  # 置信度随次数增加
                else:
                    self.patterns[pattern_key] = BehaviorPattern(
                        pattern_type="command" if context == "command" else "query",
                        trigger=trigger,
                        action=f"enable_{related_flags[0]}" if related_flags else "",
                        count=1,
                        last_seen=now,
                        confidence=0.3,
                        related_flags=related_flags
                    )
        
        # 2. 检测抱怨/投诉
        for complaint, related_flags in self.complaint_keywords.items():
            if complaint in text_lower:
                pattern_key = f"complaint_{complaint}"
                
                if pattern_key in self.patterns:
                    p = self.patterns[pattern_key]
                    p.count += 1
                    p.last_seen = now
                    p.confidence = min(1.0, p.count / 5)
                else:
                    self.patterns[pattern_key] = BehaviorPattern(
                        pattern_type="complaint",
                        trigger=complaint,
                        action=f"disable_{related_flags[0]}",
                        count=1,
                        last_seen=now,
                        confidence=0.3,
                        related_flags=related_flags
                    )
        
        # 3. 学习偏好
        self._learn_preferences(text, context)
        
        # 4. 保存数据
        self._save_data()
    
    def _learn_preferences(self, text: str, context: str):
        """从文本中学习偏好"""
        text_lower = text.lower()
        now = datetime.now().isoformat()
        
        # 1. 使用关键词映射表（支持中文关键词）
        for keyword, flags in self.keyword_to_flag.items():
            if keyword in text_lower:
                for flag in flags:
                    # 检测是否表示"关闭/禁用"
                    is_disable = any(kw in text_lower for kw in ['关闭', '停用', '关掉', '不用', '不要', '别', '太打扰'])
                    value = not is_disable
                    self._update_preference(flag, value, f"用户提到「{keyword}」", now)
        
        # 2. 检测"启用 XXX" → 偏好启用
        enable_match = re.search(r'(?:启用|开启|打开|用|开)\s*([\w\u4e00-\u9fff]+)', text_lower)
        if enable_match:
            feature = enable_match.group(1)
            flag = self._find_matching_flag(feature)
            if flag:
                self._update_preference(flag, True, f"用户说「启用{feature}」", now)
        
        # 3. 检测"关闭 XXX" → 偏好关闭
        disable_match = re.search(r'(?:关闭|停用|关掉|不用)\s*([\w\u4e00-\u9fff]+)', text_lower)
        if disable_match:
            feature = disable_match.group(1)
            flag = self._find_matching_flag(feature)
            if flag:
                self._update_preference(flag, False, f"用户说「关闭{feature}」", now)
        
        # 4. 检测"不要 XXX" → 偏好关闭
        avoid_match = re.search(r'(?:不要|别|不要用)\s*([\w\u4e00-\u9fff]+)', text_lower)
        if avoid_match:
            feature = avoid_match.group(1)
            flag = self._find_matching_flag(feature)
            if flag:
                self._update_preference(flag, False, f"用户说「不要{feature}」", now)
        
        # 5. 检测"喜欢 XXX" → 偏好启用
        like_match = re.search(r'(?:喜欢|想要|希望|愿意)\s*([\w\u4e00-\u9fff]+)', text_lower)
        if like_match:
            feature = like_match.group(1)
            flag = self._find_matching_flag(feature)
            if flag:
                self._update_preference(flag, True, f"用户说「喜欢{feature}」", now)
    
    def _find_matching_flag(self, keyword: str) -> Optional[str]:
        """根据关键词找到匹配的功能开关"""
        ff = FeatureFlag()
        flags_dict = ff.list()  # Returns dict, not list
        flags = list(flags_dict.keys())
        keyword_lower = keyword.lower()
        
        # 精确匹配
        for flag_name in flags:
            if keyword_lower in flag_name.lower():
                return flag_name
        
        return None
    
    def _update_preference(self, flag_name: str, value: any, evidence: str, timestamp: str):
        """更新偏好"""
        ff = FeatureFlag()
        current_value = ff.get(flag_name)  # Returns bool value directly
        
        if flag_name in self.preferences:
            p = self.preferences[flag_name]
            if p.learned_value != value:
                p.learned_value = value
                p.confidence = min(1.0, p.confidence + 0.1)
                p.evidence.append(f"{timestamp}: {evidence}")
                p.last_updated = timestamp
        else:
            self.preferences[flag_name] = Preference(
                flag_name=flag_name,
                current_value=current_value,
                learned_value=value,
                evidence=[f"{timestamp}: {evidence}"],
                confidence=0.5,
                last_updated=timestamp
            )
    
    def get_suggestions(self, limit: int = 5) -> List[Dict]:
        """
        获取配置建议
        
        Returns:
            [{"flag": "xxx", "action": "enable/disable", "reason": "...", "confidence": 0.8}]
        """
        suggestions = []
        ff = FeatureFlag()
        
        for flag_name, pref in self.preferences.items():
            if pref.confidence < 0.5:
                continue  # 置信度太低不建议
            
            current_value = ff.get(flag_name)  # Returns bool directly
            
            # 只建议有变化的
            if pref.learned_value != current_value:
                action = "enable" if pref.learned_value else "disable"
                suggestions.append({
                    "flag": flag_name,
                    "action": action,
                    "reason": pref.evidence[-1] if pref.evidence else "行为学习",
                    "confidence": pref.confidence,
                    "learned_from": len(pref.evidence)
                })
        
        # 按置信度排序
        suggestions.sort(key=lambda x: -x["confidence"])
        
        return suggestions[:limit]
    
    def apply_suggestion(self, suggestion: Dict) -> bool:
        """
        应用建议到功能开关
        
        Returns:
            True if applied successfully
        """
        flag = suggestion.get("flag")
        action = suggestion.get("action")
        ff = FeatureFlag()
        
        if action == "enable":
            return ff.enable(flag)
        elif action == "disable":
            return ff.disable(flag)
        
        return False
    
    def get_top_patterns(self, limit: int = 10) -> List[Dict]:
        """获取最常见的行为模式"""
        patterns = sorted(self.patterns.values(), key=lambda p: -p.count)
        
        return [
            {
                "type": p.pattern_type,
                "trigger": p.trigger,
                "count": p.count,
                "confidence": p.confidence,
                "related_flags": p.related_flags,
                "last_seen": p.last_seen
            }
            for p in patterns[:limit]
        ]
    
    def analyze_behavior(self) -> Dict:
        """分析用户行为，生成报告"""
        patterns = self.get_top_patterns(5)
        suggestions = self.get_suggestions(5)
        
        # 统计
        total_observations = sum(p.count for p in self.patterns.values())
        complaints = [p for p in self.patterns.values() if p.pattern_type == "complaint"]
        commands = [p for p in self.patterns.values() if p.pattern_type == "command"]
        
        return {
            "summary": {
                "total_observations": total_observations,
                "unique_patterns": len(self.patterns),
                "learned_preferences": len(self.preferences),
                "complaints": len(complaints),
                "commands": len(commands),
            },
            "top_patterns": patterns,
            "suggestions": suggestions,
            "confidence_avg": sum(p.confidence for p in self.patterns.values()) / max(len(self.patterns), 1)
        }
    
    def reset(self):
        """重置学习数据"""
        self.patterns.clear()
        self.preferences.clear()
        self._save_data()


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="智能行为学习器")
    sub = parser.add_subparsers(dest="cmd")
    
    # 观察
    observe = sub.add_parser("observe", help="观察用户行为")
    observe.add_argument("text", help="用户输入文本")
    observe.add_argument("--context", default="conversation", help="上下文")
    
    # 建议
    sub.add_parser("suggest", help="获取配置建议")
    
    # 分析
    sub.add_parser("analyze", help="分析用户行为")
    
    # 重置
    sub.add_parser("reset", help="重置学习数据")
    
    # 模式
    sub.add_parser("patterns", help="查看行为模式")
    
    args = parser.parse_args()
    
    learner = BehaviorLearner()
    
    if args.cmd == "observe":
        learner.observe(args.text, args.context)
        print(f"✅ 已记录行为: {args.text[:50]}...")
    
    elif args.cmd == "suggest":
        suggestions = learner.get_suggestions()
        if not suggestions:
            print("📝 暂无配置建议（继续使用以学习更多）")
        else:
            print("📝 配置建议：")
            for i, s in enumerate(suggestions, 1):
                print(f"  {i}. [{s['action']}] {s['flag']}")
                print(f"     原因: {s['reason']}")
                print(f"     置信度: {s['confidence']:.0%}")
    
    elif args.cmd == "analyze":
        report = learner.analyze_behavior()
        print("📊 行为分析报告：")
        print(f"  总观察数: {report['summary']['total_observations']}")
        print(f"  独立模式: {report['summary']['unique_patterns']}")
        print(f"  学习偏好: {report['summary']['learned_preferences']}")
        print(f"  投诉数: {report['summary']['complaints']}")
        print(f"  命令数: {report['summary']['commands']}")
        print(f"  平均置信度: {report['confidence_avg']:.0%}")
        
        if report['top_patterns']:
            print("\n🔥 最常见模式：")
            for p in report['top_patterns'][:3]:
                print(f"  - {p['trigger']}: {p['count']}次")
        
        if report['suggestions']:
            print("\n💡 建议：")
            for s in report['suggestions'][:3]:
                print(f"  - {s['action']} {s['flag']} ({s['confidence']:.0%})")
    
    elif args.cmd == "patterns":
        patterns = learner.get_top_patterns()
        if not patterns:
            print("📝 暂无行为模式")
        else:
            print("📝 行为模式：")
            for p in patterns:
                print(f"  [{p['type']}] {p['trigger']}: {p['count']}次, 置信度{p['confidence']:.0%}")
    
    elif args.cmd == "reset":
        learner.reset()
        print("✅ 学习数据已重置")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
