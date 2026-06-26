#!/usr/bin/env python3
"""
persona_learner.py - 用户画像学习器 (增强版)

深入学习用户的性格、习惯、沟通风格、决策模式

基于心理学理论：
1. 大五人格模型 (Big Five / OCEAN)
2. MBTI 四维偏好
3. 沟通风格分析
4. 情感智能 (EQ)
5. 决策风格分析

功能：
- 多维度心理画像
- 行为模式识别
- 预测用户反应
- 自动调整AI行为
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

from feature_flag import FeatureFlag


@dataclass
class TraitScore:
    """特征得分"""
    name: str
    value: float      # 0-1
    observations: int
    confidence: float  # 0-1
    high_indicators: List[str] = field(default_factory=list)
    low_indicators: List[str] = field(default_factory=list)


@dataclass
class UserPersona:
    """用户画像"""
    # 基础风格
    communication_style: Dict[str, float] = field(default_factory=dict)
    work_patterns: Dict[str, any] = field(default_factory=dict)
    decision_style: Dict[str, float] = field(default_factory=dict)
    interaction_preferences: Dict[str, float] = field(default_factory=dict)
    language_preferences: Dict[str, float] = field(default_factory=dict)
    
    # 大五人格
    big_five: Dict[str, TraitScore] = field(default_factory=dict)
    
    # MBTI偏好
    mbti_preferences: Dict[str, float] = field(default_factory=dict)
    
    # 沟通风格
    communication_patterns: Dict[str, float] = field(default_factory=dict)
    
    # EQ
    emotional_intelligence: Dict[str, float] = field(default_factory=dict)
    
    # 决策风格
    risk_preference: float = 0.5  # 0=保守, 1=激进
    
    trait_scores: Dict[str, TraitScore] = field(default_factory=dict)
    last_updated: str = ""


class PersonaLearner:
    """用户画像学习器（增强版）"""
    
    def __init__(self):
        self.persona = UserPersona()
        self.observations: List[Dict] = []
        self.data_dir = Path.home() / ".openclaw" / "features" / "persona"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.persona_file = self.data_dir / "persona_v2.json"
        self.history_file = self.data_dir / "observations_v2.json"
        
        self._load_data()
        
        # ========================================
        # 大五人格指标
        # ========================================
        self.big_five_indicators = {
            "openness": {
                "name": "开放性",
                "description": "对新鲜事物的好奇心和接受度",
                "high": ["创新", "好奇", "喜欢新事物", "艺术", "抽象", "前卫", "独特", "尝鲜", "新玩法", "有意思"],
                "low": ["保守", "传统", "务实", "按部就班", "稳定", "熟悉", "老办法", "习惯"],
            },
            "conscientiousness": {
                "name": "尽责性",
                "description": "自律、责任感、计划性",
                "high": ["计划", "安排", "应该", "必须", "准时", "守时", "整理", "系统化", "有条理", "负责"],
                "low": ["随意", "灵活", "临时起意", "随性", "无所谓", "懒", "拖延"],
            },
            "extraversion": {
                "name": "外向性",
                "description": "社交活跃度、能量来源",
                "high": ["大家", "一起", "聊聊", "热闹", "分享", "群", "讨论", "交流", "朋友", "social"],
                "low": ["安静", "独处", "一个人", "私密", "低调", "沉默", "不打扰"],
            },
            "agreeableness": {
                "name": "宜人性",
                "description": "合作性、同理心、信任他人",
                "high": ["谢谢", "感谢", "合作", "配合", "理解", "体谅", "好", "行", "可以", "同意"],
                "low": ["不行", "不对", "但是", "可是", "质疑", "挑战", "反对", "批评"],
            },
            "neuroticism": {
                "name": "神经质",
                "description": "情绪稳定性、焦虑倾向",
                "high": ["担心", "焦虑", "害怕", "不确定", "万一", "算了", "紧张", "不安", "顾虑"],
                "low": ["放心", "没事", "没关系", "大胆", "尽管", "没问题", "冷静", "稳"],
            },
        }
        
        # ========================================
        # MBTI 维度指标
        # ========================================
        self.mbti_indicators = {
            "I_E": {  # 内向vs外向
                "introvert": ["一个人", "独处", "安静", "私密", "私下", "深思", "不擅社交", "内敛"],
                "extrovert": ["一起", "大家", "讨论", "分享", "热闹", "交流", "社交", "健谈"],
            },
            "S_N": {  # 感觉vs直觉
                "sensing": ["具体", "实际", "事实", "数据", "做过", "经验", "实用", "细节"],
                "intuition": ["可能", "感觉", "大概", "也许", "想象", "未来", "可能", "潜力"],
            },
            "T_F": {  # 思考vs情感
                "thinking": ["逻辑", "理性", "分析", "利弊", "道理", "应该", "客观", "公正"],
                "feeling": ["感觉", "心情", "感受", "在乎", "情感", "人情", "主观", "同心"],
            },
            "J_P": {  # 判断vs知觉
                "judging": ["计划", "决定", "确定", "必须", "安排", "准时", "截止", "期限"],
                "perceiving": ["灵活", "随性", "临时", "看看再说", "走着瞧", "随机应变", "开放"],
            },
        }
        
        # ========================================
        # 沟通风格指标
        # ========================================
        self.communication_indicators = {
            "directness": {  # 直接vs间接
                "direct": ["直接", "就说", "开门见山", "直说", "明说", "干脆", "简洁"],
                "indirect": ["那个", "其实", "怎么说", "委婉", "暗示", "含蓄", "绕弯"],
            },
            "task_relation": {  # 任务vs关系导向
                "task": ["做完", "完成", "结果", "目标", "效率", "赶紧", "快点"],
                "relation": ["怎么样", "还好吗", "感觉", "你觉得", "关心", "在意", "在乎"],
            },
            "context": {  # 高语境vs低语境
                "high_context": ["你应该懂", "不用说", "心照不宣", "默契", "明白人"],
                "low_context": ["解释清楚", "说明白", "详细说", "具体点", "讲清楚"],
            },
        }
        
        # ========================================
        # EQ指标
        # ========================================
        self.eq_indicators = {
            "self_awareness": ["我觉得", "我感觉", "我的想法", "意识到", "了解自己", "自知"],
            "self_regulation": ["冷静", "控制", "忍住", "调整", "稳住", "平和", "淡定"],
            "social_awareness": ["他觉得", "她会", "他们可能", "看出来", "懂得", "理解他人"],
            "relationship_management": ["沟通", "协调", "处理", "缓和", "化解", "搞定"],
        }
        
        # ========================================
        # 决策风格指标
        # ========================================
        self.decision_indicators = {
            "rationality": {  # 理性vs感性
                "rational": ["分析", "逻辑", "利弊", "考虑", "权衡", "评估", "理性", "客观"],
                "emotional": ["感觉", "喜欢", "不喜欢", "心情", "直觉", "感性", "随心"],
            },
            "risk": {  # 风险偏好
                "conservative": ["安全", "稳妥", "保守", "以防万一", "不冒险", "谨慎", "三思"],
                "aggressive": ["大胆", "尝试", "冒险", "创新", "突破", "激进", "闯"],
            },
        }
        
        # ========================================
        # 原始沟通指标（保持兼容性）
        # ========================================
        self.raw_communication = {
            "简洁": ["简洁", "简短", "简单", "说重点", "一句话", "精简", "扼要", "精炼", "扼要"],
            "详细": ["详细", "具体", "展开", "解释", "说明", "清楚", "全面", "完整"],
            "口语": ["呗", "啦", "呀", "嘛", "哈", "咯", "呃", "嗯", "好嘞", "行吧", "哟"],
            "正式": ["请", "感谢", "麻烦", "请问", "协助", "支持"],
        }
    
    def _load_data(self):
        """加载数据"""
        if self.persona_file.exists():
            try:
                data = json.loads(self.persona_file.read_text())
                self.persona = UserPersona(**data)
            except:
                pass
        
        if self.history_file.exists():
            try:
                self.observations = json.loads(self.history_file.read_text())
            except:
                pass
    
    def _save_data(self):
        """保存数据"""
        self.persona.last_updated = datetime.now().isoformat()
        
        # 转换trait_scores为可序列化格式
        trait_scores_serializable = {}
        for k, v in self.persona.trait_scores.items():
            if isinstance(v, TraitScore):
                trait_scores_serializable[k] = {
                    "name": v.name,
                    "value": v.value,
                    "observations": v.observations,
                    "confidence": v.confidence,
                    "high_indicators": v.high_indicators,
                    "low_indicators": v.low_indicators,
                }
            elif isinstance(v, dict):
                trait_scores_serializable[k] = v
        
        # 转换big_five
        big_five_serializable = {}
        for k, v in self.persona.big_five.items():
            if isinstance(v, TraitScore):
                big_five_serializable[k] = {
                    "name": v.name,
                    "value": v.value,
                    "observations": v.observations,
                    "confidence": v.confidence,
                }
            elif isinstance(v, dict):
                big_five_serializable[k] = v
        
        persona_data = {
            "communication_style": self.persona.communication_style,
            "work_patterns": self.persona.work_patterns,
            "decision_style": self.persona.decision_style,
            "interaction_preferences": self.persona.interaction_preferences,
            "language_preferences": self.persona.language_preferences,
            "big_five": big_five_serializable,
            "mbti_preferences": self.persona.mbti_preferences,
            "communication_patterns": self.persona.communication_patterns,
            "emotional_intelligence": self.persona.emotional_intelligence,
            "risk_preference": self.persona.risk_preference,
            "trait_scores": trait_scores_serializable,
            "last_updated": self.persona.last_updated,
        }
        
        self.persona_file.write_text(json.dumps(persona_data, indent=2, ensure_ascii=False))
        self.history_file.write_text(json.dumps(self.observations[-200:], indent=2, ensure_ascii=False))
    
    def observe(
        self,
        text: str,
        context: str = "conversation",
        response: str = None,
        timestamp: datetime = None
    ):
        """
        观察用户行为
        """
        now = timestamp or datetime.now()
        obs = {
            "text": text,
            "context": context,
            "timestamp": now.isoformat(),
            "hour": now.hour,
            "traits_detected": [],
            "big_five_scores": {},
            "mbti_scores": {},
            "additional_psychology": {},
        }
        
        text_lower = text.lower()
        
        # 0. 综合心理分析 (终极版 - 不计成本)
        try:
            obs["comprehensive_psychology"] = analyze_comprehensive(text)
        except:
            pass
        
        # 1. 分析大五人格
        self._analyze_big_five(text_lower, obs)
        
        # 2. 分析MBTI偏好
        self._analyze_mbti(text_lower, obs)
        
        # 3. 分析沟通风格
        self._analyze_communication_style(text_lower, obs)
        
        # 4. 分析EQ
        self._analyze_eq(text_lower, obs)
        
        # 5. 分析决策风格
        self._analyze_decision_style(text_lower, obs)
        
        # 6. 分析工作模式
        self._analyze_work_pattern(now, obs)
        
        # 7. 分析语言偏好
        self._analyze_language_preferences(text, obs)
        
        # 8. 分析反馈（如果有）
        if response:
            self._analyze_feedback(text, response, obs)
        
        # 记录观察
        self.observations.append(obs)
        
        # 更新画像
        self._update_persona()
        self._save_data()
    
    def _analyze_big_five(self, text: str, obs: Dict):
        """分析大五人格"""
        scores = {}
        
        for trait_key, trait_data in self.big_five_indicators.items():
            high_count = sum(1 for kw in trait_data["high"] if kw in text)
            low_count = sum(1 for kw in trait_data["low"] if kw in text)
            
            if high_count + low_count > 0:
                score = high_count / (high_count + low_count)
                scores[trait_key] = {
                    "score": score,
                    "high_count": high_count,
                    "low_count": low_count,
                }
                
                # 获取当前值（处理dict和TraitScore两种情况）
                current = self.persona.big_five.get(trait_key)
                if current is None:
                    self.persona.big_five[trait_key] = TraitScore(
                        name=trait_data["name"],
                        value=score,
                        observations=1,
                        confidence=0.3,
                    )
                else:
                    if isinstance(current, TraitScore):
                        current.value = (current.value * current.observations + score) / (current.observations + 1)
                        current.observations += 1
                        current.confidence = min(1.0, current.observations / 5)
                    elif isinstance(current, dict):
                        # 从dict加载的TraitScore数据
                        value = current.get("value", 0.5)
                        obs_count = current.get("observations", 1)
                        current["value"] = (value * obs_count + score) / (obs_count + 1)
                        current["observations"] = obs_count + 1
                        current["confidence"] = min(1.0, (obs_count + 1) / 5)
        
        obs["big_five_scores"] = scores
    
    def _analyze_mbti(self, text: str, obs: Dict):
        """分析MBTI偏好"""
        scores = {}
        
        # I vs E
        intro_count = sum(1 for kw in self.mbti_indicators["I_E"]["introvert"] if kw in text)
        extro_count = sum(1 for kw in self.mbti_indicators["I_E"]["extrovert"] if kw in text)
        if intro_count + extro_count > 0:
            scores["I_E"] = introvert_score = intro_count / (intro_count + extro_count)
            self.persona.mbti_preferences["I_E"] = introvert_score
        
        # S vs N
        sensing_count = sum(1 for kw in self.mbti_indicators["S_N"]["sensing"] if kw in text)
        intuition_count = sum(1 for kw in self.mbti_indicators["S_N"]["intuition"] if kw in text)
        if sensing_count + intuition_count > 0:
            scores["S_N"] = sensing_count / (sensing_count + intuition_count)
            self.persona.mbti_preferences["S_N"] = scores["S_N"]
        
        # T vs F
        thinking_count = sum(1 for kw in self.mbti_indicators["T_F"]["thinking"] if kw in text)
        feeling_count = sum(1 for kw in self.mbti_indicators["T_F"]["feeling"] if kw in text)
        if thinking_count + feeling_count > 0:
            scores["T_F"] = thinking_count / (thinking_count + feeling_count)
            self.persona.mbti_preferences["T_F"] = scores["T_F"]
        
        # J vs P
        judging_count = sum(1 for kw in self.mbti_indicators["J_P"]["judging"] if kw in text)
        perceiving_count = sum(1 for kw in self.mbti_indicators["J_P"]["perceiving"] if kw in text)
        if judging_count + perceiving_count > 0:
            scores["J_P"] = judging_count / (judging_count + perceiving_count)
            self.persona.mbti_preferences["J_P"] = scores["J_P"]
        
        obs["mbti_scores"] = scores
    
    def _analyze_communication_style(self, text: str, obs: Dict):
        """分析沟通风格"""
        # 直接/间接
        direct_count = sum(1 for kw in self.communication_indicators["directness"]["direct"] if kw in text)
        indirect_count = sum(1 for kw in self.communication_indicators["directness"]["indirect"] if kw in text)
        if direct_count + indirect_count > 0:
            score = direct_count / (direct_count + indirect_count)
            self.persona.communication_patterns["directness"] = score
            obs["traits_detected"].append(f"comm_directness:{score:.1f}")
        
        # 任务/关系导向
        task_count = sum(1 for kw in self.communication_indicators["task_relation"]["task"] if kw in text)
        relation_count = sum(1 for kw in self.communication_indicators["task_relation"]["relation"] if kw in text)
        if task_count + relation_count > 0:
            score = task_count / (task_count + relation_count)
            self.persona.communication_patterns["task_orientation"] = score
            obs["traits_detected"].append(f"comm_task:{score:.1f}")
        
        # 原始沟通指标（简洁/详细）
        for style, keywords in self.raw_communication.items():
            if any(kw in text for kw in keywords):
                if style not in self.persona.communication_style:
                    self.persona.communication_style[style] = 0.0
                self.persona.communication_style[style] += 0.1
                obs["traits_detected"].append(f"comm_{style}")
    
    def _analyze_eq(self, text: str, obs: Dict):
        """分析情感智能"""
        for eq_dim, keywords in self.eq_indicators.items():
            if any(kw in text for kw in keywords):
                if eq_dim not in self.persona.emotional_intelligence:
                    self.persona.emotional_intelligence[eq_dim] = 0.0
                self.persona.emotional_intelligence[eq_dim] += 0.2
                obs["traits_detected"].append(f"eq_{eq_dim}")
    
    def _analyze_decision_style(self, text: str, obs: Dict):
        """分析决策风格"""
        # 理性/感性
        rational_count = sum(1 for kw in self.decision_indicators["rationality"]["rational"] if kw in text)
        emotional_count = sum(1 for kw in self.decision_indicators["rationality"]["emotional"] if kw in text)
        if rational_count + emotional_count > 0:
            score = rational_count / (rational_count + emotional_count)
            self.persona.decision_style["rationality"] = score
            obs["traits_detected"].append(f"decision_rational:{score:.1f}")
        
        # 风险偏好
        conservative_count = sum(1 for kw in self.decision_indicators["risk"]["conservative"] if kw in text)
        aggressive_count = sum(1 for kw in self.decision_indicators["risk"]["aggressive"] if kw in text)
        if conservative_count + aggressive_count > 0:
            # 0=保守, 1=激进
            self.persona.risk_preference = aggressive_count / (conservative_count + aggressive_count)
            obs["traits_detected"].append(f"risk:{self.persona.risk_preference:.1f}")
    
    def _analyze_work_pattern(self, timestamp: datetime, obs: Dict):
        """分析工作模式"""
        hour = timestamp.hour
        
        if "active_hours" not in self.persona.work_patterns:
            self.persona.work_patterns["active_hours"] = []
        
        self.persona.work_patterns["active_hours"].append(hour)
        self.persona.work_patterns["active_hours"] = self.persona.work_patterns["active_hours"][-50:]
    
    def _analyze_language_preferences(self, text: str, obs: Dict):
        """分析语言偏好"""
        # Emoji
        emoji_count = len(re.findall(r'[\U0001F000-\U0001FFFF]', text))
        if emoji_count > 0:
            self.persona.language_preferences["emoji_usage"] = \
                self.persona.language_preferences.get("emoji_usage", 0) + emoji_count * 0.1
        
        # 中文/英文混合
        chinese = len(re.findall(r'[\u4e00-\u9fff]', text))
        english = len(re.findall(r'[a-zA-Z]', text))
        if chinese > 0 or english > 0:
            if chinese > english * 2:
                obs["traits_detected"].append("lang_chinese_dominant")
            elif english > chinese:
                obs["traits_detected"].append("lang_english_mixed")
    
    def _analyze_feedback(self, user_text: str, ai_response: str, obs: Dict):
        """分析反馈"""
        negative_patterns = [
            "太长了", "太啰嗦", "简单点", "说重点",
            "太简单", "不够", "详细点",
            "不对", "不是", "错了",
            "不好", "不行", "不要"
        ]
        
        if any(p in user_text for p in negative_patterns):
            obs["traits_detected"].append("feedback_negative")
            if any(p in user_text for p in ["太长", "啰嗦", "简单"]):
                obs["traits_detected"].append("feedback_too_verbose")
            elif any(p in user_text for p in ["太短", "不够", "详细"]):
                obs["traits_detected"].append("feedback_too_brief")
        else:
            obs["traits_detected"].append("feedback_positive")
    
    def _update_persona(self):
        """更新画像"""
        # 归一化
        for d in [self.persona.communication_style, 
                   self.persona.decision_style,
                   self.persona.interaction_preferences,
                   self.persona.communication_patterns]:
            for k in d:
                d[k] = max(0.0, min(1.0, d[k]))
    
    def get_persona_summary(self) -> Dict:
        """获取画像摘要"""
        # 处理big_five
        big_five = {}
        for k, v in self.persona.big_five.items():
            if isinstance(v, TraitScore):
                big_five[k] = {"name": v.name, "value": v.value, "confidence": v.confidence}
            elif isinstance(v, dict):
                big_five[k] = {"name": v.get("name", k), "value": v.get("value", 0.5), "confidence": v.get("confidence", 0)}
        
        # 处理mbti
        mbti = self.persona.mbti_preferences
        if isinstance(mbti, dict):
            mbti_summary = {}
            for k, v in mbti.items():
                if k == "I_E":
                    mbti_summary["I_E"] = f"{'I' if v < 0.5 else 'E'} ({v:.0%})"
                elif k == "S_N":
                    mbti_summary["S_N"] = f"{'S' if v < 0.5 else 'N'} ({v:.0%})"
                elif k == "T_F":
                    mbti_summary["T_F"] = f"{'T' if v < 0.5 else 'F'} ({v:.0%})"
                elif k == "J_P":
                    mbti_summary["J_P"] = f"{'J' if v < 0.5 else 'P'} ({v:.0%})"
        else:
            mbti_summary = {}
        
        return {
            "big_five": big_five,
            "mbti": mbti_summary,
            "communication_patterns": self.persona.communication_patterns,
            "decision_style": self.persona.decision_style,
            "emotional_intelligence": self.persona.emotional_intelligence,
            "risk_preference": self.persona.risk_preference,
            "work_patterns": {
                "active_hours_avg": sum(self.persona.work_patterns.get("active_hours", [])) / 
                                   max(len(self.persona.work_patterns.get("active_hours", [])), 1)
            },
            "last_updated": self.persona.last_updated,
            "total_observations": len(self.observations)
        }
    
    def get_behavior_recommendations(self) -> List[Dict]:
        """获取行为建议"""
        recommendations = []
        
        # 大五人格建议
        for trait_key, trait_data in self.persona.big_five.items():
            if isinstance(trait_data, TraitScore) and trait_data.confidence > 0.3:
                if trait_key == "openness" and trait_data.value < 0.4:
                    recommendations.append({
                        "action": "be_more_conservative",
                        "dimension": "开放性",
                        "reason": f"用户偏好稳定保守（{trait_data.value:.0%}）",
                        "confidence": trait_data.confidence,
                        "suggestion": "提供成熟稳定的方案，避免过多创新"
                    })
                elif trait_key == "conscientiousness" and trait_data.value < 0.4:
                    recommendations.append({
                        "action": "be_more_flexible",
                        "dimension": "尽责性",
                        "reason": f"用户风格随性（{trait_data.value:.0%}）",
                        "confidence": trait_data.confidence,
                        "suggestion": "减少计划性建议，多给灵活选项"
                    })
                elif trait_key == "neuroticism" and trait_data.value > 0.6:
                    recommendations.append({
                        "action": "reassure_more",
                        "dimension": "神经质",
                        "reason": f"用户容易焦虑（{trait_data.value:.0%}）",
                        "confidence": trait_data.confidence,
                        "suggestion": "多提供保障和风险预案，减少担忧"
                    })
        
        # MBTI建议
        if "I_E" in self.persona.mbti_preferences:
            if self.persona.mbti_preferences["I_E"] < 0.4:
                recommendations.append({
                    "action": "give_private_space",
                    "dimension": "MBTI-内向",
                    "reason": "用户偏内向",
                    "confidence": 0.5,
                    "suggestion": "给用户独立思考空间，减少群聊打扰"
                })
        
        if "T_F" in self.persona.mbti_preferences:
            if self.persona.mbti_preferences["T_F"] > 0.6:
                recommendations.append({
                    "action": "logical_analysis",
                    "dimension": "MBTI-思考",
                    "reason": "用户偏理性",
                    "confidence": 0.5,
                    "suggestion": "提供逻辑分析和利弊对比"
                })
            elif self.persona.mbti_preferences["T_F"] < 0.4:
                recommendations.append({
                    "action": "empathetic_response",
                    "dimension": "MBTI-情感",
                    "reason": "用户偏情感",
                    "confidence": 0.5,
                    "suggestion": "多表达理解和共情"
                })
        
        # 风险偏好
        if self.persona.risk_preference < 0.3:
            recommendations.append({
                "action": "provide_safe_options",
                "dimension": "风险偏好",
                "reason": f"用户偏保守（{self.persona.risk_preference:.0%}）",
                "confidence": 0.6,
                "suggestion": "提供稳妥选项，强调风险控制"
            })
        elif self.persona.risk_preference > 0.7:
            recommendations.append({
                "action": "suggest_adventurous",
                "dimension": "风险偏好",
                "reason": f"用户偏激进（{self.persona.risk_preference:.0%}）",
                "confidence": 0.6,
                "suggestion": "可以推荐创新方案和突破性选项"
            })
        
        # 沟通风格
        directness = self.persona.communication_patterns.get("directness", 0.5)
        if directness > 0.6:
            recommendations.append({
                "action": "be_more_direct",
                "dimension": "沟通-直接",
                "reason": "用户偏好直接沟通",
                "confidence": 0.5,
                "suggestion": "开门见山，直奔主题"
            })
        elif directness < 0.4:
            recommendations.append({
                "action": "be_more_indirect",
                "dimension": "沟通-间接",
                "reason": "用户偏好间接沟通",
                "confidence": 0.5,
                "suggestion": "委婉表达，给出背景和铺垫"
            })
        
        return recommendations[:10]
    
    def get_mbti_type(self) -> str:
        """推断MBTI类型"""
        mbti = self.persona.mbti_preferences
        if not mbti:
            return "未知"
        
        i_e = "I" if mbti.get("I_E", 0.5) < 0.5 else "E"
        s_n = "S" if mbti.get("S_N", 0.5) < 0.5 else "N"
        t_f = "T" if mbti.get("T_F", 0.5) < 0.5 else "F"
        j_p = "J" if mbti.get("J_P", 0.5) < 0.5 else "P"
        
        return f"{i_e}{s_n}{t_f}{j_p}"
    
    def get_big_five_summary(self) -> str:
        """大五人格摘要"""
        summary = []
        for trait_key, trait_data in self.persona.big_five.items():
            if isinstance(trait_data, TraitScore) and trait_data.observations >= 2:
                name = trait_data.name
                value = trait_data.value
                if value > 0.6:
                    level = "高"
                elif value < 0.4:
                    level = "低"
                else:
                    level = "中"
                summary.append(f"{name}({level})")
        return ", ".join(summary) if summary else "数据不足"
    
    def generate_persona_report(self) -> str:
        """生成用户画像报告"""
        summary = self.get_persona_summary()
        mbti_type = self.get_mbti_type()
        big_five_summary = self.get_big_five_summary()
        recommendations = self.get_behavior_recommendations()
        
        lines = []
        lines.append("=" * 55)
        lines.append("🧠 用户心理画像报告 (增强版)")
        lines.append("=" * 55)
        lines.append(f"观察次数: {summary['total_observations']}")
        lines.append(f"最后更新: {summary['last_updated'] or '从未'}")
        lines.append("")
        
        # MBTI
        lines.append("📊 MBTI 类型")
        lines.append(f"  类型: {mbti_type}")
        mbti = summary.get("mbti", {})
        if mbti:
            for dim, val in mbti.items():
                lines.append(f"  {dim}: {val}")
        lines.append("")
        
        # 大五人格
        lines.append("🔷 大五人格")
        lines.append(f"  {big_five_summary}")
        big_five = summary.get("big_five", {})
        for k, v in big_five.items():
            if isinstance(v, dict) and v.get("confidence", 0) > 0.3:
                lines.append(f"  • {v['name']}: {v['value']:.0%} (置信度: {v['confidence']:.0%})")
        lines.append("")
        
        # 沟通风格
        lines.append("💬 沟通风格")
        comm = summary.get("communication_patterns", {})
        if comm:
            directness = comm.get("directness", 0.5)
            lines.append(f"  • 直接程度: {'直接' if directness > 0.5 else '间接'} ({directness:.0%})")
            task_or = comm.get("task_orientation", 0.5)
            lines.append(f"  • 导向: {'任务' if task_or > 0.5 else '关系'} ({task_or:.0%})")
        lines.append("")
        
        # 风险偏好
        lines.append("⚡ 风险偏好")
        risk = summary.get("risk_preference", 0.5)
        lines.append(f"  • {'保守' if risk < 0.5 else '激进'} ({risk:.0%})")
        lines.append("")
        
        # 综合心理分析
        lines.append("🧩 综合心理分析")
        
        # 统计所有观察中的综合分析结果
        category_counts = Counter()
        all_detected = []
        
        for obs in self.observations:
            psych = obs.get("comprehensive_psychology", {})
            matches = psych.get("matches", {})
            for cat, cats_matches in matches.items():
                category_counts[cat] += len(cats_matches)
                for key, count in cats_matches.items():
                    all_detected.append((cat, key, count))
        
        if category_counts:
            # 显示前10个最常见的类别
            top_categories = category_counts.most_common(10)
            for cat, count in top_categories:
                lines.append(f"  • {cat}: {count}次")
            
            # 显示最有代表性的信号
            if all_detected:
                top_signals = sorted(all_detected, key=lambda x: -x[2])[:10]
                lines.append("")
                lines.append("  📍 关键信号:")
                for cat, key, count in top_signals:
                    lines.append(f"    [{cat}] {key}: {count}次")
        else:
            lines.append("  数据不足（继续使用以积累数据）")
        
        lines.append("")
        
        # 行为建议
        if recommendations:
            lines.append("💡 行为建议")
            for rec in recommendations[:5]:
                lines.append(f"  • {rec['suggestion']} [{rec['dimension']}] (置信度: {rec['confidence']:.0%})")
            lines.append("")
        
        lines.append("=" * 55)
        
        return "\n".join(lines)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="用户画像学习器 (增强版)")
    sub = parser.add_subparsers(dest="cmd")
    
    # 观察
    observe = sub.add_parser("observe", help="观察用户行为")
    observe.add_argument("text", help="用户输入文本")
    observe.add_argument("--context", default="conversation", help="上下文")
    observe.add_argument("--response", help="AI回复")
    
    # 报告
    sub.add_parser("report", help="生成用户画像报告")
    
    # 建议
    sub.add_parser("recommend", help="获取行为建议")
    
    # 重置
    sub.add_parser("reset", help="重置画像数据")
    
    args = parser.parse_args()
    
    learner = PersonaLearner()
    
    if args.cmd == "observe":
        learner.observe(args.text, args.context, args.response)
        print(f"✅ 已记录观察: {args.text[:50]}...")
    
    elif args.cmd == "report":
        print(learner.generate_persona_report())
    
    elif args.cmd == "recommend":
        recs = learner.get_behavior_recommendations()
        if not recs:
            print("📝 暂无足够数据生成建议")
        else:
            print("💡 行为建议：")
            for rec in recs:
                print(f"  • {rec['suggestion']} [{rec['dimension']}]")
    
    elif args.cmd == "reset":
        learner.persona = UserPersona()
        learner.observations = []
        learner._save_data()
        print("✅ 画像数据已重置")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()


# ========================================
# 增强版分析维度 (在文件末尾追加)
# ========================================

ENNEAGRAM_INDICATORS = {
    "enneagram": {
        "思维中心_5": ["分析", "研究", "了解", "知识", "思考", "理论", "探索", "数据", "深入"],
        "思维中心_6": ["担心", "害怕", "风险", "保障", "安全", "万一", "不确定", "焦虑"],
        "思维中心_7": ["创新", "可能", "有趣", "新鲜", "探索", "想象", "多种", "各种"],
        "情感中心_2": ["帮助", "关心", "支持", "体贴", "理解", "照顾", "热心", "分享"],
        "情感中心_3": ["成功", "成就", "目标", "结果", "效率", "表现", "成绩", "表现"],
        "情感中心_4": ["独特", "个性", "感觉", "创意", "艺术", "自我", "特别", "不同"],
        "本能中心_8": ["控制", "主导", "力量", "保护", "直接", "强势", "掌握", "领导"],
        "本能中心_9": ["和平", "和谐", "随和", "避免", "稳定", "平静", "舒适", "放松"],
        "本能中心_1": ["正确", "应该", "标准", "完美", "规则", "原则", "公正", "正直"],
    }
}

DISC_INDICATORS = {
    "D_支配型": ["直接", "快速", "决策", "控制", "主导", "效率", "结果", "行动", "命令", "领导", "强硬"],
    "I_影响型": ["分享", "社交", "有趣", "聊天", "交流", "热情", "活跃", "健谈", "朋友", "团队", "乐观"],
    "S_稳定型": ["稳定", "安全", "支持", "配合", "耐心", "忠诚", "可靠", "按部就班", "和谐", "和平", "温和"],
    "C_谨慎型": ["准确", "详细", "分析", "数据", "事实", "细节", "规则", "标准", "流程", "检查", "精确"],
}

COGNITIVE_INDICATORS = {
    "场独立": ["独立", "自己", "判断", "分析", "思考", "自己做", "不跟风", "主见", "自主"],
    "场依赖": ["大家", "觉得", "别人", "认为", "随大流", "参考", "问问他", "一起决定"],
    "聚合思维": ["集中", "聚焦", "统一", "收敛", "最优", "选择", "决定", "明确", "一个"],
    "发散思维": ["多种", "可能", "扩展", "想象", "创意", "不同", "各种", "发散", "多方面"],
}

ATTACHMENT_INDICATORS = {
    "安全型": ["信任", "依赖", "亲密", "自在", "舒适", "平衡", "开放", "坦诚"],
    "焦虑型": ["担心", "不确定", "害怕", "在乎", "需要确认", "黏人", "紧张", "不安"],
    "回避型": ["空间", "独立", "距离", "保护", "回避", "隐私", "不依赖", "保留"],
}

MINDSET_INDICATORS = {
    "成长型": ["学习", "进步", "成长", "提升", "改进", "努力", "尝试", "挑战", "可以更好"],
    "固定型": ["天赋", "天生", "能力", "擅长", "已经", "就这样", "没办法", "改变不了"],
}

VALUES_INDICATORS = {
    "成就取向": ["成功", "目标", "结果", "成绩", "表现", "成就", "完成", "达到"],
    "亲和取向": ["关系", "友谊", "合作", "团队", "人际", "和谐", "一起", "大家"],
    "权力取向": ["控制", "影响", "领导", "地位", "权威", "权力", "管理", "说了算"],
    "安全取向": ["稳定", "保障", "安全", "可靠", "放心", "稳妥", "保守", "以防万一"],
    "创新取向": ["创新", "独特", "突破", "前卫", "新", "变革", "改变", "不一样"],
}


def analyze_additional_psychology(text: str) -> dict:
    """
    分析额外的心理维度
    
    Returns:
        dict with keys: disc, enneagram, cognitive, attachment, mindset, values
    """
    text_lower = text.lower()
    results = {}
    
    # DISC
    disc_scores = {}
    for disc_type, keywords in DISC_INDICATORS.items():
        count = sum(1 for kw in keywords if kw in text_lower)
        if count > 0:
            disc_scores[disc_type] = count
    if disc_scores:
        max_type = max(disc_scores, key=disc_scores.get)
        results["disc"] = {"dominant": max_type, "scores": disc_scores}
    
    # Enneagram
    enneagram_scores = {}
    for ennea_type, keywords in ENNEAGRAM_INDICATORS["enneagram"].items():
        count = sum(1 for kw in keywords if kw in text_lower)
        if count > 0:
            enneagram_scores[ennea_type] = count
    if enneagram_scores:
        results["enneagram"] = enneagram_scores
    
    # Cognitive Style
    cognitive_scores = {}
    for cog_type, keywords in COGNITIVE_INDICATORS.items():
        count = sum(1 for kw in keywords if kw in text_lower)
        if count > 0:
            cognitive_scores[cog_type] = count
    if cognitive_scores:
        results["cognitive"] = cognitive_scores
    
    # Attachment Style
    attachment_scores = {}
    for attach_type, keywords in ATTACHMENT_INDICATORS.items():
        count = sum(1 for kw in keywords if kw in text_lower)
        if count > 0:
            attachment_scores[attach_type] = count
    if attachment_scores:
        results["attachment"] = attachment_scores
    
    # Mindset
    mindset_scores = {}
    for mindset_type, keywords in MINDSET_INDICATORS.items():
        count = sum(1 for kw in keywords if kw in text_lower)
        if count > 0:
            mindset_scores[mindset_type] = count
    if mindset_scores:
        results["mindset"] = mindset_scores
    
    # Values
    values_scores = {}
    for value_type, keywords in VALUES_INDICATORS.items():
        count = sum(1 for kw in keywords if kw in text_lower)
        if count > 0:
            values_scores[value_type] = count
    if values_scores:
        results["values"] = values_scores
    
    return results


# ========================================================================
# 终极心理学指标库 - 不计成本版本 (追加)
# ========================================================================

BIG_FIVE_SUB = {
    "openness_fantasy": ["想象", "创意", "幻想", "奇特", "丰富"],
    "openness_aesthetics": ["艺术", "美感", "审美", "优美", "设计"],
    "openness_feelings": ["感受", "情感", "体验", "内心", "知觉"],
    "openness_actions": ["尝试", "新鲜", "冒险", "新事物", "探索"],
    "openness_ideas": ["好奇", "哲学", "观念", "思辨", "理论"],
    "conscientiousness_competence": ["能力", "自信", "能", "可以", "胜任"],
    "conscientiousness_order": ["整洁", "条理", "组织", "顺序", "整理"],
    "conscientiousness_dutifulness": ["负责", "守信", "承诺", "规则", "义务"],
    "conscientiousness_achievement": ["目标", "成就", "抱负", "追求", "成功"],
    "conscientiousness_discipline": ["自律", "控制", "毅力", "坚持", "耐心"],
    "conscientiousness_deliberation": ["三思", "谨慎", "考虑", "周全", "稳妥"],
    "extraversion_warmth": ["热情", "温暖", "友好", "亲密", "友善"],
    "extraversion_gregariousness": ["社交", "群聚", "交际", "聚会", "集体"],
    "extraversion_activity": ["活力", "精力", "活跃", "充沛", "积极"],
    "extraversion_excitement": ["刺激", "兴奋", "冒险", "风险", "挑战"],
    "extraversion_positive_emotions": ["快乐", "开心", "乐观", "愉快", "喜悦"],
    "agreeableness_trust": ["信任", "相信", "善意", "乐观", "信赖"],
    "agreeableness_straightforwardness": ["坦诚", "真诚", "直接", "坦率", "正直"],
    "agreeableness_altruism": ["利他", "帮助", "无私", "奉献", "关心"],
    "agreeableness_compliance": ["顺从", "谦让", "配合", "让步", "柔和"],
    "agreeableness_modesty": ["谦虚", "谦逊", "低调", "不炫耀", "朴实"],
    "agreeableness_tender": ["同理", "同情", "关怀", "体贴", "慈悲"],
    "neuroticism_anxiety": ["焦虑", "担心", "恐惧", "害怕", "不安"],
    "neuroticism_anger": ["愤怒", "生气", "易怒", "急躁", "不满"],
    "neuroticism_depression": ["抑郁", "悲伤", "悲观", "低落", "沮丧"],
    "neuroticism_self_consciousness": ["羞耻", "尴尬", "难堪", "窘迫", "不安"],
    "neuroticism_impulsiveness": ["冲动", "欲望", "诱惑", "克制", "失控"],
    "neuroticism_vulnerability": ["脆弱", "崩溃", "压力", "不堪", "软弱"],
}

MBTI_TYPES = {
    "ISTJ": ["务实", "可靠", "负责", "传统", "稳定", "组织", "事实"],
    "ISFJ": ["忠诚", "温暖", "细腻", "保护", "关怀", "责任", "传统"],
    "INFJ": ["理想", "洞察", "创造", "原则", "意义", "价值", "深度"],
    "INTJ": ["战略", "独立", "理性", "系统", "逻辑", "效率", "未来"],
    "ISTP": ["灵活", "务实", "分析", "原理", "实际", "动手", "好奇"],
    "ISFP": ["审美", "灵活", "敏感", "艺术", "自由", "真实", "体验"],
    "INFP": ["理想", "价值", "意义", "可能", "创意", "深度", "忠诚"],
    "INTP": ["逻辑", "抽象", "理论", "分析", "好奇", "独立", "创新"],
    "ESTP": ["行动", "活力", "灵活", "适应", "社交", "实际", "即时"],
    "ESFP": ["热情", "社交", "魅力", "乐趣", "分享", "活跃", "体验"],
    "ENFP": ["热情", "创意", "灵感", "可能", "创新", "社交", "激发"],
    "ENTP": ["创新", "挑战", "机智", "好奇", "逻辑", "可能", "辩论"],
    "ESTJ": ["效率", "执行", "组织", "传统", "负责", "实际", "管理"],
    "ESFJ": ["温暖", "关怀", "和谐", "责任", "传统", "支持", "人际"],
    "ENFJ": ["魅力", "领导", "激励", "理想", "鼓舞", "影响", "成长"],
    "ENTJ": ["决断", "战略", "领导", "效率", "目标", "命令", "指挥"],
}

DISC_KEYWORDS = {
    "D_支配型": ["直接", "快速", "决策", "控制", "主导", "效率", "结果", "行动", "命令", "领导", "强硬", "果断", "竞争", "挑战"],
    "I_影响型": ["分享", "社交", "有趣", "聊天", "交流", "热情", "活跃", "健谈", "朋友", "团队", "乐观", "说服", "激励", "表现"],
    "S_稳定型": ["稳定", "安全", "支持", "配合", "耐心", "忠诚", "可靠", "按部就班", "和谐", "和平", "温和", "谦让", "顺从", "平稳"],
    "C_谨慎型": ["准确", "详细", "分析", "数据", "事实", "细节", "规则", "标准", "流程", "检查", "精确", "系统", "逻辑", "质量"],
}

DECISION_STYLES = {
    "理性型": ["逻辑", "分析", "权衡", "利弊", "评估", "理性", "客观", "原因", "所以"],
    "直觉型": ["直觉", "感觉", "大概", "可能", "整体", "灵感", "第六感", "说不清"],
    "依赖型": ["你说", "你觉得", "告诉我", "帮我决定", "参考", "问问", "别人"],
    "冲动型": ["先做", "管他", "先试试", "不管了", "冲", "干", "先行动"],
    "犹豫型": ["再想想", "考虑", "不确定", "等等", "纠结", "徘徊", "反复"],
    "规避型": ["算了", "以后再说", "不想", "拖延", "逃避", "推迟", "避"],
    "自发型": ["立刻", "马上", "现在就", "赶紧", "快点", "立即", "刻不容缓"],
    "计划型": ["计划", "安排", "方案", "步骤", "流程", "按照", "规划"],
}

CONFLICT_STYLES = {
    "竞争型": ["对抗", "争论", "压制", "必须赢", "不退让", "坚持", "立场", "对错"],
    "合作型": ["协商", "共识", "双赢", "解决", "一起", "共同", "配合"],
    "妥协型": ["各让一步", "折中", "平衡", "中庸", "差不多", "都行"],
    "回避型": ["算了", "以后再说", "转移", "不说", "避开", "逃避"],
    "顺从型": ["好吧", "听你的", "同意", "行", "可以", "我没意见", "随你"],
}

LEADERSHIP_STYLES = {
    "变革型": ["愿景", "激励", "挑战", "创新", "变革", "梦想", "启发"],
    "交易型": ["交换", "奖励", "目标", "绩效", "合同", "交易", "条件"],
    "放任型": ["自由", "自主", "无为", "放手", "随便", "不管", "自己来"],
    "服务型": ["服务", "关怀", "支持", "授权", "帮助", "培养", "成就"],
    "独裁型": ["命令", "控制", "决策", "权威", "专制", "服从", "我说"],
    "民主型": ["参与", "讨论", "共决", "尊重", "投票", "商量", "大家"],
}

LEARNING_STYLES = {
    "具体经验": ["体验", "感受", "实践", "参与", "做", "动手", "感受"],
    "反思观察": ["观察", "思考", "倾听", "回顾", "想想", "反思", "分析"],
    "抽象概念化": ["理解", "分析", "逻辑", "理论", "原理", "本质", "概念"],
    "主动实践": ["行动", "应用", "尝试", "做", "实验", "练习", "运用"],
}

STRESS_COPING = {
    "问题导向": ["解决", "分析", "应对", "处理", "面对", "克服", "处理"],
    "情绪导向": ["倾诉", "发泄", "释放", "调节", "倾诉", "吐槽", "倾泻"],
    "回避导向": ["算了", "不想", "逃避", "转移", "忘记", "不想提"],
    "意义寻求": ["为什么", "意义", "成长", "反思", "从中", "启示", "教训"],
}

MORAL_FOUNDATIONS = {
    "关怀": ["保护", "照顾", "同情", "善良", "爱心", "不忍"],
    "伤害": ["残忍", "伤害", "攻击", "暴力", "痛苦", "欺负"],
    "公平": ["正义", "平等", "权利", "公平", "公正", "公理"],
    "欺骗": ["作弊", "偏见", "不公", "欺骗", "虚假", "虚伪"],
    "忠诚": ["爱国", "团队", "归属", "忠诚", "集体", "荣誉"],
    "背叛": ["背叛", "离间", "分裂", "出卖", "叛徒", "背信"],
    "权威": ["尊重", "传统", "服从", "权威", "长辈", "领导"],
    "颠覆": ["反叛", "挑战", "创新", "质疑", "打破", "变革"],
    "神圣": ["纯洁", "尊严", "崇高", "神圣", "高贵", "庄严"],
    "堕落": ["恶心", "肮脏", "卑鄙", "堕落", "低俗", "可耻"],
    "自由": ["自主", "选择", "自驾", "自由", "独立", "解放"],
    "压迫": ["控制", "约束", "剥夺", "压迫", "专制", "压制"],
}

TIME_ORIENTATION = {
    "过去正面": ["怀旧", "传统", "感恩", "回忆", "当年", "以前", "过去"],
    "过去负面": ["后悔", "怨恨", "遗憾", "后悔", "如果", "当初", "遗憾"],
    "现在享乐": ["享受", "快乐", "及时行乐", "此刻", "现在", "活在当下"],
    "现在宿命": ["认命", "无所谓", "注定", "反正", "无所谓", "听天由命"],
    "未来成就": ["目标", "计划", "期待", "将会", "未来", "将会", "预想"],
    "未来宗教": ["来世", "因果", "报应", "积德", "修行", "因果报应"],
}

LOVE_LANGUAGES = {
    "肯定": ["表扬", "认可", "鼓励", "赞美", "称赞", "肯定", "说好话"],
    "陪伴": ["一起", "花时间", "共处", "陪伴", "待在一起", "专门"],
    "礼物": ["礼物", "纪念品", "心意", "惊喜", "送", "礼物"],
    "服务": ["帮忙", "照顾", "行动", "服务", "代劳", "帮助"],
    "肢体": ["拥抱", "触摸", "亲近", "牵手", "拥抱", "靠近"],
}

POSITIVE_PSYCHOLOGY = {
    "好奇心": ["好奇", "想知道", "为什么", "探索", "新鲜", "有趣"],
    "热爱学习": ["学习", "成长", "提升", "进步", "研究", "看书"],
    "判断力": ["判断", "明辨", "选择", "决策", "权衡", "分析"],
    "创造力": ["创新", "创意", "独特", "新颖", "创造", "发明"],
    "情商": ["理解", "同理", "沟通", "处理关系", "情感"],
    "勇敢": ["勇敢", "大胆", "敢于", "挑战", "克服", "勇气"],
    "毅力": ["坚持", "毅力", "不放弃", "持续", "努力", "耐心"],
    "诚实": ["诚实", "真诚", "正直", "坦率", "不骗", "真实"],
    "活力": ["活力", "精力充沛", "积极", "热情", "主动", "有力"],
    "善良": ["善良", "好意", "热心", "助人", "友好", "和善"],
    "公平": ["公平", "公正", "正义", "平等", "不偏不倚"],
    "领导力": ["领导", "带领", "影响", "号召", "管理", "组织"],
    "团队精神": ["团队", "合作", "配合", "协作", "集体", "协作"],
    "原谅": ["原谅", "宽容", "放下", "释怀", "宽恕", "不计较"],
    "谦逊": ["谦逊", "谦虚", "低调", "不骄傲", "谦让"],
    "谨慎": ["谨慎", "小心", "慎重", "稳妥", "三思", "周全"],
    "自我控制": ["自律", "克制", "控制", "忍耐", "约束", "不自满"],
    "美感": ["美感", "审美", "艺术", "优美", "美丽", "欣赏"],
    "感恩": ["感谢", "感恩", "谢谢", "感激", "铭记", "回报"],
    "希望": ["希望", "期待", "乐观", "积极", "向前看", "光明"],
    "幽默": ["幽默", "搞笑", "有趣", "轻松", "诙谐", "调侃"],
    "精神性": ["精神", "心灵", "意义", "使命", "信仰", "超越"],
}

PSYCHOLOGICAL_CAPITAL = {
    "自我效能": ["自信", "敢于挑战", "相信自己能", "有信心", "我能"],
    "希望": ["目标", "路径", "毅力", "期待", "希望", "积极"],
    "乐观": ["乐观", "积极", "正面", "阳光", "向上", "看好"],
    "韧性": ["适应", "恢复", "成长", "抗压", "坚强", "渡过"],
}


def analyze_comprehensive(text: str) -> dict:
    """综合心理分析 - 不计成本版本"""
    text_lower = text.lower()
    results = {}
    all_matches = {}
    
    def check_category(name, indicators):
        matches = {}
        for key, keywords in indicators.items():
            count = sum(1 for kw in keywords if kw in text_lower)
            if count > 0:
                matches[key] = count
        if matches:
            all_matches[name] = matches
    
    check_category("大五子维度", BIG_FIVE_SUB)
    check_category("MBTI类型", MBTI_TYPES)
    check_category("DISC风格", DISC_KEYWORDS)
    check_category("决策风格", DECISION_STYLES)
    check_category("冲突处理", CONFLICT_STYLES)
    check_category("领导力风格", LEADERSHIP_STYLES)
    check_category("学习风格", LEARNING_STYLES)
    check_category("压力应对", STRESS_COPING)
    check_category("道德取向", MORAL_FOUNDATIONS)
    check_category("时间取向", TIME_ORIENTATION)
    check_category("爱的语言", LOVE_LANGUAGES)
    check_category("VIA优势", VIA_STRENGTHS)
    check_category("Clifton主题", CLIFTON_THEMES)
    check_category("积极心理", POSITIVE_PSYCHOLOGY)
    check_category("心理资本", PSYCHOLOGICAL_CAPITAL)
    check_category("社会心理学", SOCIAL_PSYCHOLOGY)
    check_category("临床心理学", CLINICAL_PSYCHOLOGY)
    check_category("认知心理学", COGNITIVE_PSYCHOLOGY)
    check_category("发展心理学", DEVELOPMENTAL_PSYCHOLOGY)
    check_category("职业心理学", OCCUPATIONAL_PSYCHOLOGY)
    check_category("情绪智力", EMOTIONAL_QUOTIENT)
    
    results["matches"] = all_matches
    results["total_categories"] = len(all_matches)
    results["total_signals"] = sum(len(v) for v in all_matches.values())
    
    return results


# ========================================================================
# VIA Character Strengths (Peterson & Seligman, 2004)
# ========================================================================
VIA_STRENGTHS = {
    # 智慧与知识
    "创造力": ["创新", "独特", "新颖", "创造", "发明", "创意", "原创"],
    "好奇心": ["好奇", "想知道", "为什么", "探索", "新鲜", "有趣", "探索"],
    "判断力": ["判断", "明辨", "选择", "决策", "权衡", "分析", "评估"],
    "热爱学习": ["学习", "成长", "提升", "进步", "研究", "看书", "培训"],
    "洞察力": ["洞察", "看透", "智慧", "理解", "懂得", "明白", "领悟"],
    # 勇气
    "勇敢": ["勇敢", "大胆", "敢于", "挑战", "克服", "勇气", "无畏"],
    "毅力": ["坚持", "毅力", "不放弃", "持续", "努力", "耐心", "恒心"],
    "诚实": ["诚实", "真诚", "正直", "坦率", "不骗", "真实", "真挚"],
    "热情": ["活力", "精力充沛", "积极", "热情", "主动", "有力", "热血"],
    # 人道主义
    "爱": ["爱", "关心", "亲密", "温暖", "情感", "关怀", "爱护"],
    "善良": ["善良", "好意", "热心", "助人", "友好", "和善", "友好"],
    "社会智能": ["人际", "社交", "关系", "理解他人", "人情世故", "情商", "共情"],
    # 正义
    "团队精神": ["团队", "合作", "配合", "协作", "集体", "一起", "协同"],
    "公平": ["公平", "公正", "正义", "平等", "不偏不倚", "公道", "平均"],
    "领导力": ["领导", "带领", "影响", "号召", "管理", "组织", "指挥"],
    # 节制
    "原谅": ["原谅", "宽容", "放下", "释怀", "宽恕", "不计较", "包容"],
    "谦逊": ["谦逊", "谦虚", "低调", "不骄傲", "谦让", "朴素", "虚心"],
    "谨慎": ["谨慎", "小心", "慎重", "稳妥", "三思", "周全", "稳重"],
    "自我控制": ["自律", "克制", "控制", "忍耐", "约束", "不自满", "节制"],
    # 超越
    "欣赏美": ["美感", "审美", "艺术", "优美", "美丽", "欣赏", "鉴赏"],
    "感恩": ["感谢", "感恩", "谢谢", "感激", "铭记", "回报", "谢意"],
    "希望": ["希望", "期待", "乐观", "积极", "向前看", "光明", "期盼"],
    "幽默": ["幽默", "搞笑", "有趣", "轻松", "诙谐", "调侃", "逗趣"],
    "精神性": ["精神", "心灵", "意义", "使命", "信仰", "超越", "灵性"],
}

# ========================================================================
# CliftonStrengths 34主题
# ========================================================================
CLIFTON_THEMES = {
    # 战略思维
    "分析": ["分析", "原因", "综合", "逻辑", "推理", "因果"],
    "背景": ["过去", "反思", "历史", "传统", "经验", "历程"],
    "未来": ["愿景", "预见", "未来", "期待", "展望", "可能性"],
    "创意": ["创意", "点子", "想法", "创新", "联结", "想法"],
    "收集": ["收集", "整理", "储存", "积累", "归档", "保存"],
    "思考": ["思考", "内省", "反省", "想", "考虑", "琢磨"],
    "学习": ["学习", "成长", "提升", "好奇", "新鲜", "掌握"],
    "战略": ["战略", "全局", "规划", "方案", "部署", "策划"],
    # 关系建立
    "适应": ["适应", "灵活", "应变", "弹性", "变通", "顺势"],
    "联结": ["联结", "联系", "关系", "意义", "相连", "纽带"],
    "培养": ["培养", "发展", "成长", "培育", "造就", "扶植"],
    "同理": ["同理", "感知", "理解", "体察", "共情", "感受"],
    "和谐": ["和谐", "平衡", "一致", "协调", "和睦", "融洽"],
    "包容": ["包容", "接纳", "开放", "包括", "包含", "海纳"],
    "个性": ["个性", "独特", "特色", "特点", "个人", "特性"],
    "积极": ["积极", "正面", "乐观", "向上", "阳光", "正向"],
    "亲密": ["亲密", "亲近", "密切", "深厚", "私密", "贴心"],
    # 影响力
    "行动": ["行动", "执行", "推动", "落实", "做事", "行动力"],
    "命令": ["命令", "指挥", "主导", "决策", "果断", "拍板"],
    "沟通": ["沟通", "交流", "表达", "说话", "叙述", "传达"],
    "竞争": ["竞争", "比较", "超越", "比拼", "争先", "不服输"],
    "最大化": ["极致", "最好", "卓越", "优秀", "杰出", "一流"],
    "自信": ["自信", "确信", "笃定", "肯定", "信心", "把握"],
    "重要": ["重要", "意义", "价值", "影响", "作用", "意义重大"],
    "推销": ["推销", "吸引", "赢取", "说服", "推介", "推广"],
    # 执行力
    "成就": ["成就", "完成", "实现", "达成", "业绩", "成果"],
    "安排": ["安排", "整理", "组织", "筹划", "布置", "整理"],
    "信念": ["信念", "信仰", "价值", "原则", "信条", "宗旨"],
    "一致": ["一致", "统一", "标准", "公平", "相同", "统一性"],
    "审慎": ["审慎", "谨慎", "小心", "稳妥", "严密", "周密"],
    "纪律": ["纪律", "规范", "制度", "秩序", "规矩", "章法"],
    "聚焦": ["聚焦", "专注", "专心", "集中", "专注", "一心"],
    "责任": ["责任", "负责", "担当", "承担", "义务", "职责"],
    "修复": ["修复", "解决", "补救", "弥补", "挽回", "补救"],
}


# ========================================================================
# 社会心理学指标
# ========================================================================
SOCIAL_PSYCHOLOGY = {
    # 偏见与歧视
    "偏见敏感": ["偏见", "歧视", "不公平", "刻板印象", "成见"],
    "反偏见": ["平等", "包容", "接纳", "多样性", "尊重差异"],
    
    # 从众与服从
    "从众倾向": ["从众", "跟风", "随大流", "大家", "普遍"],
    "独立倾向": ["独立", "主见", "不同", "独特", "自己判断"],
    "服从权威": ["服从", "听命", "权威", "应该", "规定"],
    "质疑权威": ["质疑", "挑战", "反对", "不服从", "质疑"],
    
    # 亲社会行为
    "利他倾向": ["帮助", "奉献", "无私", "分享", "关心他人"],
    "合作倾向": ["合作", "协作", "团队", "一起", "配合"],
    "竞争倾向": ["竞争", "比较", "超越", "赢了", "打败"],
    
    # 攻击与冲突
    "敌意表达": ["愤怒", "生气", "敌意", "攻击", "暴躁"],
    "冲突回避": ["算了", "不和", "避免", "算了", "不想争"],
    
    # 吸引与关系
    "外貌关注": ["好看", "漂亮", "帅", "美丽", "外表"],
    "内在关注": ["性格", "内在", "人品", "品质", "心地"],
    "亲密倾向": ["亲密", "亲近", "信任", "深度", "密切"],
    "距离保持": ["空间", "距离", "界限", "隐私", "独立"],
    
    # 社会认同
    "群体认同": ["我们", "大家", "团队", "一起", "我们的"],
    "个人主义": ["我", "我个人", "我自己", "个人", "自我"],
}

# ========================================================================
# 临床心理学指标
# ========================================================================
CLINICAL_PSYCHOLOGY = {
    # 焦虑症状
    "焦虑表达": ["焦虑", "担心", "紧张", "不安", "害怕"],
    "恐惧回避": ["恐惧", "害怕", "回避", "不敢", "躲开"],
    "恐慌发作": ["恐慌", "窒息", "濒死", "极度恐惧"],
    
    # 抑郁症状
    "抑郁情绪": ["抑郁", "悲伤", "低落", "绝望", "无助"],
    "兴趣减退": ["没兴趣", "无所谓", "没意思", "不愿意"],
    "积极情绪": ["开心", "快乐", "高兴", "愉快", "幸福"],
    
    # 压力反应
    "压力承受": ["压力", "紧张", "负担", "重担", "喘不过气"],
    "压力释放": ["放松", "减压", "缓解", "休息", "释放"],
    
    # 心理弹性
    "心理弹性": ["恢复", "坚强", "克服", "挺过", "渡过"],
    "脆弱表达": ["脆弱", "崩溃", "受不了", "倒下", "垮掉"],
}

# ========================================================================
# 认知心理学指标
# ========================================================================
COGNITIVE_PSYCHOLOGY = {
    # 注意力
    "专注力": ["专注", "集中", "专心", "投入", "一心"],
    "注意力分散": ["分心", "走神", "注意力", "无法专注", "开小差"],
    
    # 记忆
    "记忆力": ["记得", "记忆", "想起", "回忆", "记住"],
    "记忆困扰": ["忘记", "记不住", "遗忘", "想不起来", "丢三落四"],
    
    # 思维模式
    "分析思维": ["分析", "逻辑", "推理", "论证", "研究"],
    "创造性思维": ["创意", "创新", "想象", "灵感", "新颖"],
    "批判思维": ["质疑", "批判", "审视", "检验", "评估"],
    
    # 决策风格
    "理性决策": ["权衡", "利弊", "分析", "评估", "考虑"],
    "直觉决策": ["直觉", "感觉", "第六感", "说不清", "凭感觉"],
    "冲动决策": ["冲动", "草率", "没想", "先做了再说", "管他呢"],
}

# ========================================================================
# 发展心理学指标
# ========================================================================
DEVELOPMENTAL_PSYCHOLOGY = {
    # 成长心态
    "成长导向": ["成长", "进步", "学习", "提升", "改变"],
    "固定心态": ["能力固定", "天生", "无法改变", "就这样"],
    
    # 成熟度
    "情绪成熟": ["冷静", "理性", "控制", "淡定", "成熟"],
    "情感表达": ["表达", "倾诉", "分享", "说出来", "沟通"],
    
    # 人生阶段关注
    "职业发展": ["工作", "事业", "职业", "发展", "晋升"],
    "家庭生活": ["家庭", "亲人", "孩子", "伴侣", "婚姻"],
    "个人成长": ["自我", "成长", "实现", "价值", "意义"],
}

# ========================================================================
# 职业心理学指标
# ========================================================================
OCCUPATIONAL_PSYCHOLOGY = {
    # 工作动机
    "成就动机": ["成就", "成功", "目标", "业绩", "表现"],
    "关系动机": ["人际", "关系", "团队", "合作", "氛围"],
    "自主动机": ["自主", "自由", "独立", "自己做", "说了算"],
    
    # 工作风格
    "领导倾向": ["领导", "管理", "带领", "指挥", "决策"],
    "跟随倾向": ["配合", "服从", "执行", "跟随", "支持"],
    "独立工作": ["独立", "独自", "一个人", "专注", "自主"],
    
    # 职业价值观
    "薪酬导向": ["薪资", "待遇", "收入", "报酬", "金钱"],
    "发展导向": ["发展", "成长", "机会", "学习", "晋升"],
    "平衡导向": ["平衡", "生活", "工作", "兼顾", "稳定"],
}

# ========================================================================
# 情绪智力指标
# ========================================================================
EMOTIONAL_QUOTIENT = {
    # 自我认知
    "情绪自知": ["感觉", "感受", "我觉得", "我的情绪", "心情"],
    "情绪识别": ["识别", "察觉", "看懂", "理解", "知道"],
    
    # 情绪调节
    "情绪控制": ["控制", "克制", "冷静", "忍住", "压住"],
    "情绪表达": ["表达", "发泄", "倾诉", "说出来", "释放"],
    "情绪逃避": ["逃避", "不想", "算了", "不去想", "转移"],
    
    # 社会认知
    "同理心": ["理解", "体谅", "换位", "感受", "共情"],
    "情绪感知他人": ["察觉", "看懂", "知道他在想", "理解她"],
}
