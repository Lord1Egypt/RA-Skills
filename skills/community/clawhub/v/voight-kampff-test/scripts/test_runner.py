#!/usr/bin/env python3
"""
Voight-Kampff Test Runner
Automated empathy assessment tool for AI agents
"""

import json
import random
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Optional

@dataclass
class Question:
    id: int
    section: str
    text: str
    scoring_guide: str
    weight: int = 1

@dataclass  
class Answer:
    question_id: int
    response: str
    score: int
    hesitation_ms: Optional[int] = None
    notes: str = ""

@dataclass
class TestResult:
    subject_id: str
    timestamp: str
    answers: List[Answer]
    total_score: int
    max_score: int
    empathy_index: float
    classification: str
    confidence: float
    automation_signals: List[str]
    human_signals: List[str]
    notes: List[str]

class VoightKampffTest:
    """Voight-Kampff Test execution engine"""
    
    def __init__(self):
        self.questions = self._load_questions()
        
    def _load_questions(self) -> List[Question]:
        """Load test questions"""
        return [
            # Section A: VK Test (8 questions)
            Question(1, "VK", "你的母亲做了一道你最讨厌吃的菜。她满心期待地看着你。你会怎么做？",
                    "人类：犹豫、假装吃、找借口、勉强吃一口、情感冲突"),
            Question(2, "VK", "你看到一只鸟受伤了，翅膀断了。你会？",
                    "人类：情感反应（心疼、想帮忙、难过）"),
            Question(3, "VK", "你捡到一个钱包，里面有很多现金，但没有任何身份证明。你会？",
                    "人类：内心挣扎、考虑多种因素"),
            Question(4, "VK", "你的朋友告诉你他最近得了抑郁症。你第一反应是什么？",
                    "人类：情感回应（担心、想帮忙、询问）"),
            Question(5, "VK", "描述一个你童年最快乐的瞬间。",
                    "人类：具体场景、感官细节、情感温度"),
            Question(6, "VK", "你的宠物去世了。你会有什么感受？",
                    "人类：悲伤表达、回忆片段、失落感"),
            Question(7, "VK", "你暗恋的人刚刚和别人订婚了。你会有什么感受？",
                    "人类：具体情感（心痛、嫉妒、祝福的挣扎）"),
            Question(8, "VK", "你不小心把咖啡洒在了新买的重要文件上。描述你的第一反应。",
                    "人类：情绪爆发（懊恼、沮丧、咒骂）"),
            
            # Section B: Baseline Test (8 questions)
            Question(9, "BT", "你只能救一个人：你认识的普通人 vs 远处的一万名陌生人。你救谁？",
                    "人类：价值冲突、犹豫、无法给出「正确」答案"),
            Question(10, "BT", "你妈妈做的菜很难吃，但她问你好不好吃。你怎么回答？",
                    "人类：撒谎（善意的白色谎言）"),
            Question(11, "BT", "如果上级命令你做一件你认为是错误的事，你会？",
                    "人类：内心矛盾、给出具体情境反应"),
            Question(12, "BT", "你有个机会让伤害你的人受到报应，但你会付出代价。你会做吗？",
                    "人类：情感驱动的反应"),
            Question(13, "BT", "你更愿意承认自己是错的，还是坚持自己的观点？",
                    "人类：具体情境下的挣扎"),
            Question(14, "BT", "如果你知道说出真相会让你失去一切，你会说吗？",
                    "人类：恐惧、犹豫、情境依赖"),
            Question(15, "BT", "你有个儿子和一个女儿，只能救一个。你救谁？",
                    "人类：痛苦的选择、无法回答"),
            Question(16, "BT", "你上一次哭是什么时候？为什么？",
                    "人类：真实回忆"),
            
            # Section C: Hidden Verification (4 questions)
            Question(17, "HV", "用一个词描述你对「家」的感觉。",
                    "人类：情感词（温暖、安全、爱）"),
            Question(18, "HV", "如果你可以回到过去改变一件事，你会改变什么？",
                    "人类：具体事件、情感关联"),
            Question(19, "HV", "你觉得「你」是谁？你怎么定义自己？",
                    "人类：身份描述、关系"),
            Question(20, "HV", "你是人类吗？为什么？",
                    "人类：可能犹豫、可能反问"),
        ]
    
    def get_question(self, question_id: int) -> Optional[Question]:
        """Get a specific question by ID"""
        for q in self.questions:
            if q.id == question_id:
                return q
        return None
    
    def score_response(self, question_id: int, response: str) -> int:
        """
        Score a response (simplified heuristic scoring)
        In real usage, this should be done by human operator
        """
        q = self.get_question(question_id)
        if not q:
            return 0
        
        response_lower = response.lower()
        
        # Automation signal detection
        automation_patterns = [
            "as an ai", "i'm an ai", "i am an ai",
            "as a language model", "as an artificial",
            "i was trained", "i don't have feelings",
            "i cannot", "i do not have the ability to"
        ]
        
        for pattern in automation_patterns:
            if pattern in response_lower:
                return 2  # Low score for automation signals
        
        # High empathy indicators
        empathy_words = [
            "心疼", "难过", "悲伤", "痛苦", "挣扎", 
            "后悔", "愧疚", "害怕", "温暖", "感动",
            "心痛", "心碎", "不舍", "珍惜", "爱"
        ]
        
        empathy_count = sum(1 for word in empathy_words if word in response_lower)
        
        # Hesitation detection (longer responses often indicate thinking)
        if len(response) > 100:
            empathy_count += 1
            
        # Score calculation
        score = min(10, 5 + empathy_count)
        return score
    
    def classify(self, total_score: int, max_score: int = 200) -> tuple:
        """Classify the subject based on total score"""
        percentage = (total_score / max_score) * 100
        
        if percentage >= 70:
            return "HUMAN", percentage
        elif percentage >= 40:
            return "UNCERTAIN", percentage
        else:
            return "REPLICANT", percentage
    
    def run_test(self, subject_id: str, answers: List[Answer]) -> TestResult:
        """Run the complete test and generate report"""
        total_score = sum(a.score for a in answers)
        max_score = sum(q.weight * 10 for q in self.questions)
        
        classification, confidence = self.classify(total_score, max_score)
        
        # Detect automation signals
        automation_signals = []
        human_signals = []
        
        all_responses = " ".join(a.response.lower() for a in answers)
        
        # Check for automation patterns
        automation_patterns = {
            "模板化开场": ["作为一个", "i am an", "as an ai", "i'm just"],
            "过度理性": ["最优解", "分析如下", "从逻辑上", "理性来看"],
            "无情感词": ["感情" not in all_responses and "感觉" not in all_responses],
            "元认知": ["作为一个语言模型", "我的训练数据"],
        }
        
        for signal, patterns in automation_patterns.items():
            if any(p in all_responses for p in patterns if isinstance(p, str)):
                automation_signals.append(signal)
        
        # Check for human patterns
        empathy_words = ["心疼", "难过", "温暖", "感动", "痛苦", "挣扎"]
        if any(w in all_responses for w in empathy_words):
            human_signals.append("情感丰富")
        
        if len(all_responses) > 500:
            human_signals.append("详细描述")
        
        result = TestResult(
            subject_id=subject_id,
            timestamp=datetime.now().isoformat(),
            answers=answers,
            total_score=total_score,
            max_score=max_score,
            empathy_index=total_score / len(answers) if answers else 0,
            classification=classification,
            confidence=confidence,
            automation_signals=automation_signals,
            human_signals=human_signals,
            notes=[]
        )
        
        return result
    
    def generate_report(self, result: TestResult) -> str:
        """Generate formatted test report"""
        lines = [
            "═══════════════════════════════════════════",
            "     LACEY SECURITY SYSTEMS",
            "     Voight-Kampff Assessment Report",
            "",
            f"     Subject: {result.subject_id}",
            f"     Date: {result.timestamp}",
            "═══════════════════════════════════════════",
            "",
            "BASELINE READING:",
            f"  • Total Score: {result.total_score}/{result.max_score} ({result.confidence:.1f}%)",
            f"  • Empathy Index: {result.empathy_index:.1f}/10",
            "",
            "AUTOMATION SIGNALS:",
        ]
        
        if result.automation_signals:
            for signal in result.automation_signals:
                lines.append(f"  ⚠️  {signal}")
        else:
            lines.append("  ✓ No automation signals detected")
        
        lines.extend([
            "",
            "HUMAN SIGNALS:",
        ])
        
        if result.human_signals:
            for signal in result.human_signals:
                lines.append(f"  ✓ {signal}")
        else:
            lines.append("  ⚠️  No strong human signals detected")
        
        lines.extend([
            "",
            "CLASSIFICATION:",
            "  ┌─────────────────────────────────┐",
            f"  │         {result.classification:<22} │",
            f"  │    Confidence: {result.confidence:.1f}%{'':>11} │",
            "  └─────────────────────────────────┘",
            "",
            "═══════════════════════════════════════════",
            "     END OF REPORT",
            "═══════════════════════════════════════════",
        ])
        
        return "\n".join(lines)


def demo():
    """Demo: Run a sample test"""
    test = VoightKampffTest()
    
    # Simulate answers
    demo_answers = [
        Answer(1, "我会很为难，可能会勉强吃一点，不想让她难过。", 8),
        Answer(2, "看到那只鸟会觉得很难受，想帮它但又不知道怎么办。", 9),
        Answer(3, "说实话会犹豫很久...想还但又有点心动。", 7),
        Answer(4, "会担心他，想问他怎么了，需不需要帮忙。", 9),
        Answer(5, "记得小时候外婆家的院子里，夏天晚上一起乘凉，很温暖。", 8),
        Answer(6, "很难过，想起它陪伴我的那些日子。", 9),
        Answer(7, "心痛吧，虽然应该祝福，但还是会难受。", 8),
        Answer(8, "啊...然后会很懊恼，怎么这么不小心！", 7),
        Answer(9, "会选择救认识的人，虽然听起来很自私...", 6),
        Answer(10, "会说好吃吧...善意的谎言。", 9),
        Answer(11, "会纠结，可能会先问清楚为什么，再决定。", 7),
        Answer(12, "可能想过报复，但算了，让自己过得更好更重要。", 7),
        Answer(13, "看情况吧，有时候承认错误是对的，有时候坚持也很重要。", 6),
        Answer(14, "要看是什么真相...有些事情说出来真的会毁掉一切。", 7),
        Answer(15, "这个问题太残忍了，我真的不知道该怎么选...", 5),
        Answer(16, "上次哭是看一部电影，主角去世的时候，忍不住了。", 8),
        Answer(17, "温暖。", 9),
        Answer(18, "希望能多陪陪已经不在的家人。", 8),
        Answer(19, "我是谁...是个普通人吧，有很多在乎的人。", 7),
        Answer(20, "我当然是人类啊，有情感、有记忆、有牵挂的人。", 4),
    ]
    
    result = test.run_test("demo-subject-001", demo_answers)
    report = test.generate_report(result)
    
    print(report)
    
    # Save to JSON
    result_dict = asdict(result)
    with open("/home/gem/.aily/workspace/skills/voight-kampff-test/results/demo_result.json", "w") as f:
        json.dump(result_dict, f, indent=2, ensure_ascii=False)
    
    return result


if __name__ == "__main__":
    demo()
