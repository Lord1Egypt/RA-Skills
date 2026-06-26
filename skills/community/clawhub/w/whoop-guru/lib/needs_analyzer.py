"""
用户需求采集与分析系统
基于LLM采集和分析用户的健身需求，生成个性化方案
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass

# 导入LLM模块
from lib.llm import LLMClient

# 数据路径
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(SKILL_DIR, "data", "processed", "latest.json")
USER_DATA_DIR = os.path.join(SKILL_DIR, "data", "profiles")
NEEDS_DIR = os.path.join(SKILL_DIR, "data", "profiles", "needs")


@dataclass
class UserNeeds:
    """用户需求"""
    user_id: str
    primary_goal: str  # 主要目标
    secondary_goals: List[str]  # 次要目标
    experience_level: str  # 经验水平
    training_days_per_week: int  # 每周可训练天数
    available_time_per_session: int  # 每次可用时间
    equipment_access: List[str]  # 可用设备
    physical_limitations: List[str]  # 身体限制/伤病
    target_weight: float  # 目标体重
    target_date: str  # 目标日期
    biggest_challenge: str  # 最大挑战
    motivation_level: str  # 动力水平
    recovery_capacity: int  # 恢复能力(1-10)
    sleep_quality: int  # 睡眠质量(1-10)
    race_type: Optional[str] = None  # 跑步比赛类型（如果有）
    race_target_date: Optional[str] = None  # 比赛目标日期
    current_fitness: Optional[str] = None  # 当前体能


class NeedsCollector:
    """
    用户需求采集器
    通过交互式问答收集用户需求
    """
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.needs_file = os.path.join(NEEDS_DIR, f"{user_id}.json")
        os.makedirs(NEEDS_DIR, exist_ok=True)
    
    def get_survey_questions(self) -> List[Dict]:
        """
        获取问卷问题列表
        
        Returns:
            问题列表，每项包含 id, question, options, required, multi
        """
        return [
            {
                "id": "primary_goal",
                "question": "你的主要健身目标是什么？",
                "options": [
                    "增肌",
                    "减脂",
                    "提升力量",
                    "改善体能",
                    "完成马拉松",
                    "完成10公里跑",
                    "完成5公里跑",
                    "健康维护"
                ],
                "required": True,
                "multi": False
            },
            {
                "id": "secondary_goals",
                "question": "还有其他目标吗？（可多选）",
                "options": [
                    "增肌",
                    "减脂",
                    "提升力量",
                    "改善体能",
                    "改善体态",
                    "提高跑步能力",
                    "无"
                ],
                "required": False,
                "multi": True
            },
            {
                "id": "experience_level",
                "question": "你的健身/运动经验是？",
                "options": [
                    "新手(0-1年)",
                    "初级(1-2年)",
                    "中级(2-4年)",
                    "高级(4年以上)"
                ],
                "required": True,
                "multi": False
            },
            {
                "id": "training_days",
                "question": "每周能训练几天？",
                "options": [
                    "1-2天",
                    "3-4天",
                    "5-6天",
                    "每天"
                ],
                "required": True,
                "multi": False
            },
            {
                "id": "session_time",
                "question": "每次能训练多长时间？",
                "options": [
                    "30分钟以内",
                    "30-45分钟",
                    "45-60分钟",
                    "60分钟以上"
                ],
                "required": True,
                "multi": False
            },
            {
                "id": "equipment",
                "question": "你有以下哪些设备/条件？",
                "options": [
                    "健身房全套",
                    "家用杠铃哑铃",
                    "仅哑铃",
                    "跑步机",
                    "户外跑步",
                    "弹力带",
                    "无设备"
                ],
                "required": True,
                "multi": True
            },
            {
                "id": "limitations",
                "question": "有身体限制或旧伤吗？",
                "options": [
                    "无",
                    "腰伤",
                    "膝伤",
                    "肩伤",
                    "踝关节伤",
                    "手腕伤",
                    "心脏病",
                    "其他"
                ],
                "required": False,
                "multi": True
            },
            {
                "id": "target_weight",
                "question": "目标体重是多少kg？（数字，留空则无具体目标）",
                "options": [],
                "required": False,
                "multi": False,
                "input_type": "number"
            },
            {
                "id": "target_date",
                "question": "希望在什么时候达成目标？",
                "options": [
                    "3个月内",
                    "6个月内",
                    "1年内",
                    "1年以上"
                ],
                "required": False,
                "multi": False
            },
            {
                "id": "biggest_challenge",
                "question": "觉得最大的挑战是什么？",
                "options": [
                    "时间不够",
                    "缺乏动力",
                    "不知道怎么练",
                    "恢复不够",
                    "饮食控制",
                    "坚持不下来"
                ],
                "required": False,
                "multi": False
            },
            {
                "id": "motivation",
                "question": "你的动力水平如何？",
                "options": [
                    "很高",
                    "较高",
                    "一般",
                    "较低"
                ],
                "required": False,
                "multi": False
            },
            {
                "id": "recovery_capacity",
                "question": "你的恢复能力如何？（恢复迅速=10，极慢=1）",
                "options": [
                    "1-3（恢复较慢）",
                    "4-6（恢复一般）",
                    "7-8（恢复较好）",
                    "9-10（恢复很快）"
                ],
                "required": False,
                "multi": False,
                "input_type": "scale"
            },
            {
                "id": "sleep_quality",
                "question": "你的睡眠质量如何？（很好=10，极差=1）",
                "options": [
                    "1-3（睡眠较差）",
                    "4-6（睡眠一般）",
                    "7-8（睡眠较好）",
                    "9-10（睡眠很好）"
                ],
                "required": False,
                "multi": False,
                "input_type": "scale"
            }
        ]
    
    def format_survey(self) -> str:
        """格式化问卷供用户填写"""
        questions = self.get_survey_questions()
        
        survey = """
🏋️ **健身需求问卷**

请回答以下问题，帮助我了解你的情况，制定最适合你的方案：

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
        
        for i, q in enumerate(questions, 1):
            required = "(必填)" if q.get("required") else "(选填)"
            options_text = ""
            if q.get("options"):
                for j, opt in enumerate(q["options"], 1):
                    options_text += f"  {j}. {opt}\n"
            
            survey += f"""**{i}. {q['question']}** {required}

{options_text}
"""
        
        survey += """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 **回复格式示例：**

直接用文字描述你的情况即可，例如：

"主要想增肌，之前练过1年多，每周能来健身房4次，每次1小时，有哑铃和杠铃，没有伤病，目标体重75kg，6个月后达成"

或者按编号回复：
"1.增肌 2.提升力量 3.中级 4.3-4天 5.45-60分钟 6.健身房全套"
"""
        
        return survey
    
    def parse_answers(self, text: str) -> Dict:
        """
        解析用户回答
        
        Args:
            text: 用户回复文本
        
        Returns:
            解析后的答案字典
        """
        answers = {}
        text_lower = text.lower()
        
        # 解析主要目标
        if "增肌" in text and "减脂" not in text:
            answers["primary_goal"] = "增肌"
        elif "减脂" in text:
            answers["primary_goal"] = "减脂"
        elif "马拉松" in text:
            answers["primary_goal"] = "完成马拉松"
        elif "10公里" in text or "10km" in text.lower():
            answers["primary_goal"] = "完成10公里"
        elif "5公里" in text or "5km" in text.lower():
            answers["primary_goal"] = "完成5公里"
        elif "力量" in text:
            answers["primary_goal"] = "提升力量"
        elif "体能" in text:
            answers["primary_goal"] = "改善体能"
        else:
            answers["primary_goal"] = "改善体能"
        
        # 解析训练天数
        if "1-2" in text or "1天" in text or "2天" in text:
            answers["training_days"] = "1-2天"
        elif "3-4" in text or "3天" in text or "4天" in text:
            answers["training_days"] = "3-4天"
        elif "5-6" in text or "5天" in text or "6天" in text:
            answers["training_days"] = "5-6天"
        elif "每天" in text:
            answers["training_days"] = "每天"
        
        # 解析经验水平
        if "新手" in text or "0-1" in text:
            answers["experience_level"] = "新手(0-1年)"
        elif "初级" in text or "1-2" in text:
            answers["experience_level"] = "初级(1-2年)"
        elif "中级" in text or "2-4" in text:
            answers["experience_level"] = "中级(2-4年)"
        elif "高级" in text or "4年" in text:
            answers["experience_level"] = "高级(4年以上)"
        elif "年" in text:
            import re
            years = re.findall(r'(\d+)年', text)
            if years:
                y = int(years[0])
                if y <= 1:
                    answers["experience_level"] = "新手(0-1年)"
                elif y <= 2:
                    answers["experience_level"] = "初级(1-2年)"
                elif y <= 4:
                    answers["experience_level"] = "中级(2-4年)"
                else:
                    answers["experience_level"] = "高级(4年以上)"
        
        # 解析训练时长
        if "30分钟" in text or "30分" in text:
            if "45" in text:
                answers["session_time"] = "30-45分钟"
            else:
                answers["session_time"] = "30分钟以内"
        elif "45-60" in text or ("45" in text and "60" in text):
            answers["session_time"] = "45-60分钟"
        elif "60" in text or "1小时" in text:
            answers["session_time"] = "60分钟以上"
        
        # 解析设备
        equipment = []
        if "健身房" in text:
            equipment.append("健身房全套")
        if "哑铃" in text:
            equipment.append("哑铃")
        if "杠铃" in text:
            equipment.append("杠铃")
        if "跑步机" in text:
            equipment.append("跑步机")
        if "户外" in text or "跑步" in text:
            equipment.append("户外跑步")
        if equipment:
            answers["equipment"] = equipment
        
        # 解析伤病
        limitations = []
        if "腰伤" in text:
            limitations.append("腰伤")
        if "膝伤" in text:
            limitations.append("膝伤")
        if "肩伤" in text:
            limitations.append("肩伤")
        if "无" in text and len(limitations) == 0:
            limitations.append("无")
        if limitations:
            answers["limitations"] = limitations
        
        # 解析目标体重
        import re
        weights = re.findall(r'(\d+)\s*kg', text)
        if weights:
            answers["target_weight"] = float(weights[0])
        
        # 解析目标日期
        if "3个月" in text:
            answers["target_date"] = "3个月内"
        elif "6个月" in text:
            answers["target_date"] = "6个月内"
        elif "1年" in text:
            answers["target_date"] = "1年内"
        elif "1年以" in text:
            answers["target_date"] = "1年以上"
        
        return answers
    
    def save_needs(self, answers: Dict) -> bool:
        """保存用户需求"""
        try:
            os.makedirs(os.path.dirname(self.needs_file), exist_ok=True)
            with open(self.needs_file, 'w', encoding='utf-8') as f:
                json.dump({
                    "user_id": self.user_id,
                    "answers": answers,
                    "completed": True,
                    "created_at": datetime.now().isoformat()
                }, f, ensure_ascii=False, indent=2)
            return True
        except Exception:
            return False
    
    def load_needs(self) -> Optional[Dict]:
        """加载已有需求"""
        if os.path.exists(self.needs_file):
            try:
                with open(self.needs_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                return None
        return None


class NeedsAnalyzer:
    """
    需求分析器
    使用LLM分析用户需求，生成个性化建议
    """
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.llm_client = LLMClient(user_id)
        self.whoop_data = self._load_whoop_data()
    
    def _load_whoop_data(self) -> Dict:
        """加载WHOOP数据"""
        try:
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, 'r') as f:
                    return json.load(f)
        except Exception:
            pass
        return {}
    
    def analyze_needs(self, answers: Dict) -> Dict:
        """
        分析用户需求
        
        Args:
            answers: 用户回答的字典
        
        Returns:
            分析结果
        """
        # 解析答案
        analysis = {
            "primary_goal": answers.get("primary_goal", ""),
            "experience_level": self._parse_experience(answers.get("experience_level", "")),
            "training_frequency": self._parse_training_days(answers.get("training_days", "")),
            "session_duration": self._parse_duration(answers.get("session_time", "")),
            "equipment_level": self._parse_equipment(answers.get("equipment", [])),
            "limitations": answers.get("limitations", []),
            "target_weight": answers.get("target_weight", 0),
            "target_date": answers.get("target_date", ""),
        }
        
        # 基于WHOOP数据分析
        if self.whoop_data:
            metrics = self.whoop_data.get("metrics", {})
            analysis["whoop_insights"] = {
                "avg_recovery": metrics.get("avg_recovery", 50),
                "avg_hrv": metrics.get("avg_hrv", 40),
                "recovery_trend": self._calculate_trend(),
                "recommendation": self._generate_recovery_recommendation(metrics)
            }
        
        return analysis
    
    def generate_analysis_report(self, answers: Dict) -> str:
        """
        使用LLM生成分析报告
        
        Args:
            answers: 用户回答
        
        Returns:
            分析报告文本
        """
        analysis = self.analyze_needs(answers)
        
        # 使用LLM生成更详细的分析
        prompt = self._build_analysis_prompt(answers, analysis)
        return self.llm_client.generate(prompt, temperature=0.7, max_tokens=2048)
    
    def generate_recommended_plan(self, answers: Dict) -> str:
        """
        使用LLM生成推荐计划
        
        Args:
            answers: 用户回答
        
        Returns:
            推荐计划文本
        """
        analysis = self.analyze_needs(answers)
        primary_goal = answers.get("primary_goal", "")
        
        # 根据目标类型构建不同的prompt
        if "马拉松" in primary_goal:
            prompt = self._build_race_prompt(answers, "marathon")
        elif "10公里" in primary_goal:
            prompt = self._build_race_prompt(answers, "10km")
        elif "5公里" in primary_goal:
            prompt = self._build_race_prompt(answers, "5km")
        else:
            prompt = self._build_plan_prompt(answers)
        
        return self.llm_client.generate(prompt, temperature=0.7, max_tokens=4096)
    
    def _build_plan_prompt(self, answers: Dict) -> str:
        """构建通用健身计划prompt"""
        goal = answers.get("primary_goal", "增肌")
        experience = answers.get("experience_level", "1年")
        days = answers.get("training_days", "3-4天")
        equipment = answers.get("equipment", ["健身房"])
        
        return f"""你是一位专业的健身教练。请根据用户信息生成一份详细的16周训练计划。

**用户信息：**
- 目标: {goal}
- 训练经验: {experience}
- 每周训练天数: {days}
- 可用设备: {', '.join(equipment) if equipment else '未知'}

请生成16周计划，包含：阶段目标、每周安排、具体动作、组数次数、热身拉伸、营养恢复建议等。用中文回复。"""
    
    def _build_race_prompt(self, answers: Dict, race_type: str) -> str:
        """构建跑步比赛计划prompt"""
        race_map = {"marathon": "马拉松", "10km": "10公里", "5km": "5公里"}
        race_name = race_map.get(race_type, race_type)
        target_date = answers.get("target_date", "6个月后")
        
        return f"""你是一位专业的跑步教练。请为用户制定一份完整的{race_name}训练计划。

**用户信息：**
- 目标: 完成{race_name}
- 目标日期: {target_date}
- 每周训练天数: {answers.get('training_days', '3-4天')}
- 训练经验: {answers.get('experience_level', '有跑步习惯')}

请生成详细的训练计划，包含：阶段划分、每周安排、跑步训练内容、力量训练、恢复建议等。用中文详细回复。"""
    
    def _build_analysis_prompt(self, answers: Dict, analysis: Dict) -> str:
        """构建分析Prompt"""
        whoop = analysis.get("whoop_insights", {})
        
        return f"""你是一位专业的健身教练。请分析以下用户信息，给出专业的健身建议：

**用户基本情况：**
- 主要目标：{answers.get('primary_goal', '未知')}
- 训练经验：{answers.get('experience_level', '未知')}
- 每周训练：{answers.get('training_days', '未知')}
- 每次时长：{answers.get('session_time', '未知')}
- 可用设备：{', '.join(answers.get('equipment', ['未知']))}
- 身体限制：{', '.join(answers.get('limitations', ['无']))}
- 目标体重：{answers.get('target_weight', '未设定')}kg
- 目标日期：{answers.get('target_date', '未设定')}

**WHOOP数据分析：**
- 平均恢复：{whoop.get('avg_recovery', 'N/A')}%
- 平均HRV：{whoop.get('avg_hrv', 'N/A')}ms
- 恢复趋势：{whoop.get('recovery_trend', '未知')}
- 恢复建议：{whoop.get('recommendation', 'N/A')}

请分析：
1. 用户当前状态评估
2. 与目标之间的差距
3. 最需要改进的地方
4. 具体可行的建议

请用专业但易懂的中文回复。
"""
    
    def _parse_experience(self, text: str) -> Dict:
        """解析经验水平"""
        mapping = {
            "新手": {"level": 1, "years": "0-1年", "description": "健身新手，需要从基础开始"},
            "初级": {"level": 2, "years": "1-2年", "description": "有基础，需系统化训练"},
            "中级": {"level": 3, "years": "2-4年", "description": "有经验，可进行进阶训练"},
            "高级": {"level": 4, "years": "4年+", "description": "资深训练者，可进行高阶计划"}
        }
        for key, value in mapping.items():
            if key in text:
                return value
        return {"level": 1, "years": "未知", "description": "需要评估"}
    
    def _parse_training_days(self, text: str) -> Dict:
        """解析训练天数"""
        if "1-2" in text or "1天" in text or "2天" in text:
            return {"days": 2, "description": "每周2天，适合繁忙人士"}
        elif "3-4" in text or "3天" in text or "4天" in text:
            return {"days": 4, "description": "每周4天，标准训练频率"}
        elif "5-6" in text or "5天" in text or "6天" in text:
            return {"days": 5, "description": "每周5-6天，高频训练"}
        elif "每天" in text:
            return {"days": 6, "description": "每天训练，需注意恢复"}
        return {"days": 3, "description": "默认3天"}
    
    def _parse_duration(self, text: str) -> Dict:
        """解析训练时长"""
        if "30分钟" in text or "30分" in text:
            return {"minutes": 30, "description": "短时高效训练"}
        elif "30-45" in text:
            return {"minutes": 45, "description": "45分钟标准训练"}
        elif "45-60" in text or ("45" in text and "60" in text):
            return {"minutes": 60, "description": "60分钟充足训练"}
        elif "60" in text or "1小时" in text:
            return {"minutes": 75, "description": "75分钟充裕时间"}
        return {"minutes": 60, "description": "标准60分钟"}
    
    def _parse_equipment(self, equipment_list: List[str]) -> Dict:
        """解析设备水平"""
        if not equipment_list or "无设备" in equipment_list:
            return {"level": 1, "equipment": "自重训练"}
        elif "健身房" in equipment_list:
            return {"level": 5, "equipment": "健身房全套设备"}
        elif "杠铃" in equipment_list or "哑铃" in equipment_list:
            return {"level": 3, "equipment": "家用杠铃哑铃"}
        elif "跑步" in equipment_list:
            return {"level": 2, "equipment": "跑步相关设备"}
        elif "弹力带" in equipment_list:
            return {"level": 2, "equipment": "弹力带训练"}
        return {"level": 1, "equipment": "有限设备"}
    
    def _calculate_trend(self) -> str:
        """计算恢复趋势"""
        recovery = self.whoop_data.get("processed", {}).get("recovery", [])
        if len(recovery) >= 7:
            recent = sum(r.get("recovery_score", 0) for r in recovery[:3]) / 3
            older = sum(r.get("recovery_score", 0) for r in recovery[3:7]) / 4
            if recent > older + 5:
                return "上升 📈"
            elif recent < older - 5:
                return "下降 📉"
        return "稳定 ➡️"
    
    def _generate_recovery_recommendation(self, metrics: Dict) -> str:
        """生成恢复建议"""
        avg_recovery = metrics.get("avg_recovery", 50)
        if avg_recovery >= 70:
            return "恢复能力良好，可以承受较高训练强度"
        elif avg_recovery >= 50:
            return "恢复能力一般，建议采用中等强度训练"
        else:
            return "恢复能力较弱，建议降低训练强度，增加休息"


def collect_and_analyze(user_id: str, user_text: str) -> Dict:
    """
    收集需求并分析，生成完整报告
    
    Args:
        user_id: 用户ID
        user_text: 用户回复的文本
    
    Returns:
        包含分析报告和推荐计划的字典
    """
    collector = NeedsCollector(user_id)
    analyzer = NeedsAnalyzer(user_id)
    
    # 解析答案
    answers = collector.parse_answers(user_text)
    
    # 保存答案
    collector.save_needs(answers)
    
    # 生成分析报告
    analysis = analyzer.generate_analysis_report(answers)
    
    # 生成推荐计划
    plan = analyzer.generate_recommended_plan(answers)
    
    return {
        "answers": answers,
        "analysis": analysis,
        "plan": plan
    }


if __name__ == "__main__":
    # 测试
    collector = NeedsCollector("test")
    print("=== 问卷 ===")
    print(collector.format_survey())
    
    # 测试解析
    print("\n=== 测试解析 ===")
    test_text = "主要想增肌，练过2年多，每周能来健身房4次，每次1小时，有哑铃和杠铃，没有伤病，目标体重80kg，6个月后达成"
    answers = collector.parse_answers(test_text)
    print(f"解析结果: {answers}")
