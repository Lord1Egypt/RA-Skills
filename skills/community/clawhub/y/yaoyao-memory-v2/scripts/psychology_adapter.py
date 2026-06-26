#!/usr/bin/env python3
"""
psychology_adapter.py - 心理学适配器

整合用户心理学画像与功能开关系统，实现智能开关推荐：
1. 读取用户心理学画像（persona.md）
2. 分析用户心理特征
3. 基于心理特征推荐功能开关
4. 观察用户行为，学习开关偏好

用法：
    python3 psychology_adapter.py recommend     # 推荐开关
    python3 psychology_adapter.py analyze        # 分析心理学画像
    python3 psychology_adapter.py learn <action> # 学习用户行为
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime

# 心理学特征 → 功能开关映射
PSYCHOLOGY_TO_FLAGS = {
    # 开放性高 → 启用实验性功能
    "openness": {
        "high": [
            ("feature.new_features", True, "开放性高，喜欢探索新功能"),
            ("search.hybrid", True, "开放性高，接受混合搜索"),
            ("psychology.integration", True, "开放性高，追求心理学整合"),
        ],
        "low": [
            ("feature.new_features", False, "开放性低，偏好稳定"),
            ("search.hybrid", False, "偏好简单搜索"),
        ],
    },
    
    # 尽责性高 → 启用自动备份、安全功能
    "conscientiousness": {
        "high": [
            ("memory.auto_backup", True, "尽责性高，重视数据安全"),
            ("feature.safety_check", True, "尽责性高，关注安全"),
            ("shell.confirm_destructive", True, "尽责性高，谨慎操作"),
            ("notification.redundancy", True, "尽责性高，需要冗余备份"),
        ],
        "low": [
            ("memory.auto_backup", False, "尽责性低，简化操作"),
            ("shell.confirm_destructive", False, "尽责性低，快速执行"),
        ],
    },
    
    # 外向性 → 推送偏好
    "extraversion": {
        "high": [
            ("notification.verbose", True, "外向，喜欢互动"),
            ("notification.auto_push", True, "外向，接受主动互动"),
        ],
        "low": [
            ("notification.verbose", False, "内向，减少打扰"),
            ("notification.auto_push", False, "内向，不喜欢主动打扰"),
        ],
    },
    
    # 情绪稳定性 → 全时透明度需求
    "neuroticism": {
        "high": [
            ("notification.full_transparency", True, "需要全时透明度"),
            ("status.always_show", True, "需要知道系统状态"),
            ("response.consume_report", True, "需要消耗报告"),
        ],
        "low": [
            ("notification.full_transparency", False, "情绪稳定，不需要过度透明"),
        ],
    },
    
    # 决策风格 - 激进探索 + 审慎执行
    "cautious_decision": [
        ("analysis.detailed", True, "谨慎决策，需要详细信息"),
        ("search.explain", True, "谨慎决策，需要解释"),
        ("response.show_reasoning", True, "谨慎决策，想看推理过程"),
        ("confirm.before_execute", True, "先确认再执行"),
    ],
    "fast_decision": [
        ("analysis.detailed", False, "快速决策，简短回复"),
        ("search.explain", False, "快速决策，不需要解释"),
        ("response.concise", True, "快速决策，简洁优先"),
    ],
    
    # 风险偏好 - 探索激进 + 执行保守
    "risk_seeking": [
        ("feature.experimental", True, "探索激进，启用实验功能"),
        ("search.broad", True, "探索激进，搜索范围更广"),
    ],
    "cautious_execution": [
        ("confirm.before_execute", True, "执行保守，需要确认"),
        ("shell.safe_mode", True, "执行保守，安全模式"),
        ("test.before_production", True, "执行保守，需要测试验证"),
    ],
    "risk_profile": {
        "exploratory": [
            ("feature.experimental", True, "探索激进"),
        ],
        "conservative": [
            ("feature.experimental", False, "执行保守"),
            ("shell.safe_mode", True, "安全模式"),
        ],
    },
    
    # 成长导向
    "growth_oriented": [
        ("feature.learning_mode", True, "成长导向，启用学习模式"),
        ("memory.promote_important", True, "成长导向，重视知识积累"),
    ],
    
    # 成就导向
    "achievement_oriented": [
        ("progress.tracking", True, "成就导向，关注进度"),
        ("status.show_metrics", True, "成就导向，喜欢看指标"),
    ],
    
    # 促进导向（追求收益）
    "promotion_focus": [
        ("message.positive_framing", True, "促进导向，喜欢积极框架"),
        ("feedback.encouraging", True, "促进导向，喜欢鼓励"),
    ],
    
    # 简洁沟通
    "concise_communication": [
        ("response.concise", True, "偏好简洁"),
        ("analysis.brief", True, "不需要详细分析"),
        ("notification.summary_only", True, "通知只发摘要"),
    ],
    
    # 详细沟通 + 全时透明
    "detailed_communication": [
        ("response.concise", False, "偏好详细"),
        ("analysis.detailed", True, "需要详细分析"),
        ("notification.full_detail", True, "通知要完整"),
    ],
    
    # 夜猫子
    "night_owl": [
        ("ui.dark_mode", True, "深夜模式"),
        ("notification.quiet_hours", True, "深夜勿扰"),
    ],
    
    # 安全意识
    "security_focus": [
        ("feature.safety_check", True, "安全优先"),
        ("shell.confirm_destructive", True, "危险操作需要确认"),
        ("backup.before_change", True, "变更前自动备份"),
    ],
}

# 用户行为 → 开关偏好映射
BEHAVIOR_TO_FLAGS = {
    # 频繁修改配置 → 启用高级功能
    "frequent_config_changes": [
        ("feature.advanced_mode", True, "经常修改配置"),
    ],
    # 经常搜索 → 启用搜索优化
    "frequent_search": [
        ("search.cache", True, "经常搜索，启用缓存"),
        ("search.personalized", True, "搜索习惯已形成"),
    ],
    # 经常查看状态 → 启用详细状态
    "frequent_status_check": [
        ("status.detailed", True, "经常查看状态"),
        ("notification.status_changes", True, "关注状态变化"),
    ],
    # 深夜活动 → 启用深夜模式
    "night_owl": [
        ("ui.dark_mode", True, "深夜活动模式"),
        ("notification.quiet_hours", True, "深夜勿扰"),
    ],
    # 快速回复 → 简洁模式
    "quick_responses": [
        ("response.concise", True, "偏好快速简洁回复"),
        ("analysis.brief", True, "不需要详细分析"),
    ],
}


class PsychologyAdapter:
    """心理学适配器"""
    
    def __init__(self):
        self.persona_file = Path.home() / ".openclaw" / "memory-tdai" / "persona.md"
        self.behavior_file = Path.home() / ".openclaw" / ".openclaw" / "behavior_cache.json"
        self.recommendations = {}
        
    def load_persona(self) -> str:
        """加载用户画像"""
        if self.persona_file.exists():
            return self.persona_file.read_text(encoding='utf-8')
        return ""
    
    def analyze_persona(self) -> Dict[str, any]:
        """分析用户心理学画像"""
        content = self.load_persona()
        if not content:
            return {"traits": {}, "recommendations": []}
        
        traits = {}
        
        # Big Five 特征提取（支持多种格式）
        big_five_patterns = {
            "openness": {
                "high": ["开放性", "极高", "极高"],
                "markers": ["不计成本", "持续探索", "心理学", "深夜工作"]
            },
            "conscientiousness": {
                "high": ["尽责性", "极高", "极高"],
                "markers": ["多渠道", "冗余", "备份", "安全架构", "整洁癖", "系统化"]
            },
            "extraversion": {
                "high": ["外向性", "极高"],
                "low": ["内向"],
                "markers": ["深夜工作", "任务导向"]
            },
            "agreeableness": {
                "high": ["宜人性", "极高"],
                "markers": ["信任AI"]
            },
            "neuroticism": {
                "high": ["情绪稳定性", "高"],  # 高神经质 = 情绪波动
                "markers": ["全时透明", "变更可控", "审核权"]
            },
        }
        
        for trait, config in big_five_patterns.items():
            markers = config.get("markers", [])
            high_names = config.get("high", [])
            low_names = config.get("low", [])
            
            # 检查标记词
            marker_count = sum(1 for m in markers if m in content)
            
            if any(name in content for name in high_names):
                traits[trait] = "high"
            elif any(name in content for name in low_names):
                traits[trait] = "low"
            elif marker_count >= 2:
                traits[trait] = "high"
            elif marker_count == 1:
                traits[trait] = "medium"
            else:
                traits[trait] = "unknown"
        
        # 动机分析
        if "成长导向" in content or "促进导向" in content:
            traits["growth_oriented"] = True
        if "成就导向" in content:
            traits["achievement_oriented"] = True
            
        # 文化维度
        if "独立自我" in content:
            traits["independent_self"] = True
        if "互依自我" in content:
            traits["interdependent_self"] = True
            
        # 决策风格 - 激进探索 + 审慎执行 并存
        if "激进" in content or "探索" in content:
            traits["risk_seeking"] = True
        if "保守" in content or "谨慎" in content or "审核" in content:
            traits["cautious_execution"] = True
        if "先评估" in content or "先评估后决策" in content:
            traits["cautious_decision"] = True
            
        # 风险偏好
        if "探索激进" in content:
            traits["risk_profile"] = "exploratory"
        elif "执行保守" in content:
            traits["risk_profile"] = "conservative"
        
        # 沟通偏好
        if "简洁" in content or "直接" in content or "不废话" in content:
            traits["concise_communication"] = True
        if "详细" in content or "全时透明" in content:
            traits["detailed_communication"] = True
            
        # 心理需求
        if "自主性" in content:
            traits["autonomy_need"] = "high"
        if "胜任感" in content:
            traits["competence_need"] = "high"
        if "意义感" in content:
            traits["meaning_need"] = "high"
            
        # 工作时间偏好
        if "深夜" in content or "凌晨" in content:
            traits["night_owl"] = True
            
        # 安全意识
        if "安全" in content and ("架构" in content or "优先" in content):
            traits["security_focus"] = True
            
        return traits
    
    def get_flag_recommendations(self, traits: Dict) -> List[Dict]:
        """基于心理学特征获取功能开关推荐"""
        recommendations = []
        seen = set()  # 去重
        
        for trait_key, trait_value in traits.items():
            if trait_key in PSYCHOLOGY_TO_FLAGS:
                mapping = PSYCHOLOGY_TO_FLAGS[trait_key]
                
                # 嵌套格式 (Big Five)
                if isinstance(mapping, dict):
                    if trait_value in mapping:
                        for flag, value, reason in mapping[trait_value]:
                            if flag not in seen:
                                seen.add(flag)
                                recommendations.append({
                                    "flag": flag,
                                    "value": value,
                                    "reason": reason,
                                    "source": f"psychology.{trait_key}"
                                })
                # 列表格式 (其他特征)
                elif isinstance(mapping, list):
                    if trait_value:  # True 或非空
                        for flag, value, reason in mapping:
                            if flag not in seen:
                                seen.add(flag)
                                recommendations.append({
                                    "flag": flag,
                                    "value": value,
                                    "reason": reason,
                                    "source": f"psychology.{trait_key}"
                                })
                        
        return recommendations
    
    def analyze_behavior(self, action: str, context: Dict = None) -> List[Dict]:
        """分析用户行为，推荐开关"""
        recommendations = []
        
        # 行为模式匹配
        behavior_patterns = {
            "config_change": ["配置", "设置", "开关", "设置"],
            "search": ["搜索", "查找", "query"],
            "status_check": ["状态", "健康", "检查"],
            "quick_reply": ["继续", "简单", "快"],
            "night_activity": ["深夜", "凌晨", "晚上"],
        }
        
        for behavior, keywords in behavior_patterns.items():
            if any(kw in action for kw in keywords):
                if behavior in BEHAVIOR_TO_FLAGS:
                    for flag, value, reason in BEHAVIOR_TO_FLAGS[behavior]:
                        recommendations.append({
                            "flag": flag,
                            "value": value,
                            "reason": reason,
                            "source": "behavior"
                        })
                        
        return recommendations
    
    def generate_recommendations(self) -> Dict:
        """生成完整的推荐"""
        traits = self.analyze_persona()
        flag_recs = self.get_flag_recommendations(traits)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "traits": traits,
            "flag_recommendations": flag_recs,
            "summary": self._summarize(traits)
        }
    
    def _summarize(self, traits: Dict) -> str:
        """生成心理学画像摘要"""
        lines = []
        
        trait_names = {
            "openness": "开放性",
            "conscientiousness": "尽责性",
            "extraversion": "外向性",
            "agreeableness": "宜人性",
            "neuroticism": "情绪稳定性"
        }
        
        for trait, name in trait_names.items():
            value = traits.get(trait, "unknown")
            if value != "unknown":
                symbol = "⬆️" if value == "high" else "⬇️"
                lines.append(f"{symbol} {name}: {value}")
                
        if traits.get("growth_oriented"):
            lines.append("📈 成长导向")
        if traits.get("cautious_decision"):
            lines.append("⚖️ 谨慎决策")
        if traits.get("fast_decision"):
            lines.append("⚡ 快速决策")
            
        return ", ".join(lines) if lines else "画像数据不足"
    
    def display_recommendations(self):
        """显示推荐结果"""
        recs = self.generate_recommendations()
        
        print("=" * 50)
        print("🧠 心理学适配 - 智能开关推荐")
        print("=" * 50)
        print()
        
        # 心理学画像
        print("📊 用户心理学画像:")
        print(f"   {recs['summary']}")
        print()
        
        # 推荐开关
        if recs['flag_recommendations']:
            print("⚙️ 功能开关推荐:")
            seen = set()
            for rec in recs['flag_recommendations']:
                key = rec['flag']
                if key not in seen:
                    seen.add(key)
                    status = "✅ 启用" if rec['value'] else "❌ 禁用"
                    print(f"   {status} {rec['flag']}")
                    print(f"      原因: {rec['reason']}")
                    print(f"      来源: {rec['source']}")
                    print()
        else:
            print("暂无推荐")
            
        return recs


def main():
    import sys
    
    adapter = PsychologyAdapter()
    
    if len(sys.argv) < 2:
        adapter.display_recommendations()
        return
        
    cmd = sys.argv[1]
    
    if cmd == "recommend":
        adapter.display_recommendations()
    elif cmd == "analyze":
        traits = adapter.analyze_persona()
        print("心理学特征:", json.dumps(traits, ensure_ascii=False, indent=2))
    elif cmd == "learn" and len(sys.argv) > 2:
        action = " ".join(sys.argv[2:])
        recs = adapter.analyze_behavior(action)
        if recs:
            print("基于行为的推荐:")
            for rec in recs:
                print(f"  {rec['flag']} = {rec['value']} ({rec['reason']})")
        else:
            print("未识别到需要学习的模式")
    else:
        print("用法:")
        print("  python3 psychology_adapter.py recommend   # 显示推荐")
        print("  python3 psychology_adapter.py analyze    # 分析画像")
        print("  python3 psychology_adapter.py learn <动作>  # 学习行为")


if __name__ == "__main__":
    main()
