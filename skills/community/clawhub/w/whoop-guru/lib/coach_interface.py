"""
Whoop Guru Coach - 对话接口
整合所有教练功能，提供统一的对话入口
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from lib.coach.core import CoachCore, get_coach
from lib.tracker import get_tracker, get_goal_tracker
from lib.user_profile import get_user_profile, save_user_profile, UserProfile
from lib.prompts.training import get_training_prompt


class CoachInterface:
    """
    教练对话接口
    处理用户对话，生成响应
    """
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.coach = get_coach(user_id)
        self.tracker = get_tracker()
        self.goal_tracker = get_goal_tracker()
    
    def handle_message(self, text: str) -> str:
        """
        处理用户消息，返回响应
        
        Args:
            text: 用户消息
        
        Returns:
            响应文本
        """
        text = text.strip().lower()
        
        # 命令处理
        if text in ["/start", "/coach", "开始", "教练"]:
            return self._welcome()
        
        if text in ["/plan", "今日计划", "今天练什么"]:
            return self._daily_plan()
        
        if text in ["/check", "/打卡", "打卡"]:
            return self._checkin_prompt()
        
        if text in ["/progress", "/进度", "进度"]:
            return self._progress()
        
        if text in ["/16week", "16周", "长期计划"]:
            return self._16_week_plan()
        
        if text in ["/profile", "/档案", "档案"]:
            return self._show_profile()
        
        if text.startswith("/设置"):
            return self._update_profile(text)
        
        # 对话处理
        if "不想练" in text or "惰性" in text:
            return self._motivation()
        
        if "累" in text or "恢复" in text:
            return self._recovery_question()
        
        if "膝盖" in text or "肩膀" in text or "腰" in text:
            return self._injury_question(text)
        
        if "平台" in text:
            return self._plateau_question()
        
        # 默认：生成回复
        return self._default_response(text)
    
    def _welcome(self) -> str:
        """欢迎消息"""
        return """
🏋️ **Whoop Guru 私人教练**

你好！我是你的24/7私人健身教练。

我可以帮你：
- 📋 制定每日训练计划
- 📊 追踪训练进度
- 🎯 设定并跟踪目标
- 💪 提供恢复建议

输入 `/plan` 获取今日训练计划
输入 `/16week` 获取16周长期计划
或直接告诉我你的问题！

**请先设置你的健身档案**，这样我能给出更精准的建议：
/设置 [数据]

例如：/设置 深蹲100卧推80硬拉120
"""
    
    def _daily_plan(self) -> str:
        """生成每日训练计划"""
        plan_prompt = self.coach.generate_daily_plan()
        # TODO: 调用AI生成最终计划
        # 暂时返回模板
        recovery = self.coach.whoop.get_latest_recovery()
        recovery_score = recovery.get('recovery_score', 50)
        
        if recovery_score >= 70:
            intensity = "高强度"
            exercises = "卧推、高位下拉、深蹲"
        elif recovery_score >= 50:
            intensity = "中等强度"
            exercises = "上肢训练或慢走"
        else:
            intensity = "低强度/休息"
            exercises = "拉伸、轻度活动"
        
        return f"""
📋 **今日训练计划**

基于你的恢复评分 {recovery_score}：

**推荐强度**：{intensity}
**推荐内容**：{exercises}

⚠️ 此为自动生成版本
完整计划需要AI根据你的具体情况生成。

输入 `/plan full` 获取完整AI生成计划
或告诉我你的具体情况（如：膝盖不适）
"""
    
    def _checkin_prompt(self) -> str:
        """打卡提示"""
        return """
📊 **训练打卡**

请告诉我今日训练情况：

格式：
- 训练内容：卧推、深蹲等
- 完成度：全部完成/部分完成/未完成
- 身体感受：正常/疲劳/酸痛

例如：
训练内容：卧推100kg 4x12 完成
身体感受：胸部有点酸
"""
    
    def _progress(self) -> str:
        """进度查询"""
        summary = self.tracker.get_weekly_summary(self.user_id)
        streak = self.tracker.get_streak(self.user_id)
        goals = self.goal_tracker.get_active_goals(self.user_id)
        
        msg = f"""
📊 **训练进度**

**本周** ({summary['week']})
完成：{summary['completed']}/{summary['total_checkins']}次 ({summary['completion_rate']:.0f}%)
连续打卡：{streak}天

"""
        
        if goals:
            msg += "**活跃目标**\n"
            for goal in goals[:3]:
                progress_info = self.goal_tracker.get_goal_progress(goal)
                msg += f"- {goal['type']}: {progress_info['progress']:.0f}% ({goal['current']}{goal['unit']}/{goal['target']}{goal['unit']})\n"
        
        return msg
    
    def _16_week_plan(self) -> str:
        """16周计划"""
        plan_prompt = self.coach.generate_16_week_plan()
        return f"""
🏃 **16周健身计划**

基于你的档案和WHOOP数据，我将为你生成一份完整的16周计划。

这份计划包括：
- 📅 训练方案（分阶段）
- 🍎 营养策略
- 🏃 有氧方案
- 📈 追踪协议
- ⚠️ 常见错误

正在生成中，请稍候...

（AI生成功能即将上线）
"""
    
    def _show_profile(self) -> str:
        """显示用户档案"""
        profile = self.coach.profile
        
        if not profile:
            return "📝 还没有设置档案\n\n请用 /设置 [数据] 命令设置"
        
        return f"""
👤 **健身档案**

训练年限：{profile.experience_years}年
深蹲：{profile.max_squat}kg
卧推：{profile.max_bench}kg
硬拉：{profile.max_deadlift}kg
体重：{profile.body_weight}kg
目标：{profile.goal}
每周训练：{profile.days_per_week}天

如需修改，请用 /设置 命令
"""
    
    def _update_profile(self, text: str) -> str:
        """更新档案"""
        # 简单解析：/设置 深蹲100卧推80硬拉120体重75
        try:
            parts = text.replace("/设置", "").strip()
            
            squat = 0
            bench = 0
            deadlift = 0
            weight = 0
            
            if "深蹲" in parts:
                import re
                match = re.search(r"深蹲(\d+)", parts)
                if match:
                    squat = int(match.group(1))
            
            if "卧推" in parts:
                match = re.search(r"卧推(\d+)", parts)
                if match:
                    bench = int(match.group(1))
            
            if "硬拉" in parts:
                match = re.search(r"硬拉(\d+)", parts)
                if match:
                    deadlift = int(match.group(1))
            
            if "体重" in parts:
                match = re.search(r"体重(\d+)", parts)
                if match:
                    weight = int(match.group(1))
            
            if squat or bench or deadlift or weight:
                profile = self.coach.profile
                if not profile:
                    profile = UserProfile(user_id=self.user_id)
                
                if squat:
                    profile.max_squat = squat
                if bench:
                    profile.max_bench = bench
                if deadlift:
                    profile.max_deadlift = deadlift
                if weight:
                    profile.body_weight = weight
                
                save_user_profile(profile)
                self.coach.profile = profile
                
                return f"✅ 档案已更新\n\n{self._show_profile()}"
            else:
                return "格式不正确，请用：\n/设置 深蹲100卧推80硬拉120体重75"
        
        except Exception as e:
            return f"设置失败：{e}"
    
    def _motivation(self) -> str:
        """惰性激励"""
        recovery = self.coach.whoop.get_latest_recovery()
        recovery_score = recovery.get('recovery_score', 50)
        
        if recovery_score >= 60:
            return """
😤 **不想练？**

你的恢复状态 {recovery_score}% 很好！

你知道吗？
- 不练真的浪费了这么好的恢复状态
- 今天练完明天睡得更香
- 小编建议你：哪怕只做做拉伸也好

动起来，比躺着更爽！💪
"""
        else:
            return """
😌 **确实累了**

你的恢复评分只有 {recovery_score}%，身体需要休息。

如果真的累，今天就好好休息吧。
但记得早点睡，明天又是好汉！
"""
    
    def _recovery_question(self) -> str:
        """恢复问题"""
        plan = self.coach.generate_recovery_plan()
        return f"""
💤 **恢复优化**

{plan[:500]}...

想了解更多恢复技巧？告诉我你的具体情况：
- 每周训练几天？
- 最近睡眠质量如何？
- 白天是否经常疲劳？
"""
    
    def _injury_question(self, text: str) -> str:
        """伤病问题"""
        area = ""
        if "膝盖" in text:
            area = "膝盖"
        elif "肩膀" in text:
            area = "肩膀"
        elif "腰" in text:
            area = "腰部"
        
        plan = self.coach.generate_injury_plan(area, "训练时")
        
        return f"""
⚠️ **{area}不适**

{plan[:500]}...

建议：
1. 减少该部位的高冲击动作
2. 加强该部位的辅助训练
3. 训练后做好拉伸放松

如果疼痛持续，建议就医检查。
"""
    
    def _plateau_question(self) -> str:
        """平台期问题"""
        return """
🔄 **平台期突破**

卡住了？

告诉我：
1. 哪个动作卡住了？（如：深蹲）
2. 卡了多久了？
3. 目标是多少？

我可以帮你制定突破计划！
"""
    
    def _default_response(self, text: str) -> str:
        """默认回复"""
        return f"""
🤔 **{text}**

我理解你的问题，但需要更多信息才能给出建议。

试试这些命令：
- `/plan` - 今日训练计划
- `/progress` - 查看进度
- `/16week` - 16周长期计划
- 直接告诉我你的问题（训练、恢复、伤病等）
"""


def get_coach_interface(user_id: str) -> CoachInterface:
    """获取教练接口实例"""
    return CoachInterface(user_id)
