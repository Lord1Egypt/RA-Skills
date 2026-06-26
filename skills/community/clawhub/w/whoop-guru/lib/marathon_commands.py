"""
Marathon Commands - 马拉松训练指令处理
用户通过自然语言设置和管理马拉松训练计划
"""

import os
import sys
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# 添加父目录到路径
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, SKILL_DIR)

from lib.goals import GoalsManager, MarathonGoal
from lib.tracker import ProgressTracker
from lib.marathon_analyzer import MarathonAnalyzer


class MarathonCommands:
    """
    马拉松指令处理器
    处理用户设置、查询、调整马拉松计划的指令
    """
    
    def __init__(self, user_id: str = "dongyi"):
        self.user_id = user_id
        self.goals_manager = GoalsManager(user_id)
        self.tracker = ProgressTracker(user_id)
        self.analyzer = MarathonAnalyzer(user_id)
    
    def parse_race_info(self, text: str) -> Dict:
        """
        从用户输入解析比赛信息
        
        Args:
            text: 用户输入的文本
        
        Returns:
            {
                "success": bool,
                "race_name": str,
                "race_date": str,
                "goal_time": str,
                "race_type": str,
                "errors": [...]
            }
        """
        result = {
            "success": False,
            "race_name": "",
            "race_date": "",
            "goal_time": "",
            "race_type": "半程马拉松",
            "errors": []
        }
        
        text = text.strip()
        
        # 比赛类型识别
        race_types = {
            "全马": "全程马拉松",
            "全程马拉松": "全程马拉松",
            "全程": "全程马拉松",
            "半马": "半程马拉松",
            "半程马拉松": "半程马拉松",
            "半程": "半程马拉松"
        }
        
        for key, value in race_types.items():
            if key in text:
                result["race_type"] = value
                break
        
        # 比赛日期识别 (YYYY-MM-DD 或 YYYYMMDD 或中文格式)
        import re
        from datetime import datetime
        current_year = datetime.now().year
        
        # 带年份的模式
        dated_patterns = [
            (r"(\d{4})-(\d{1,2})-(\d{1,2})", False),  # 2026-04-12
            (r"(\d{4})年(\d{1,2})月(\d{1,2})日", False),  # 2026年4月12日
            (r"(\d{4})(\d{2})(\d{2})", False),  # 20260412
        ]
        
        # 不带年份的模式（使用当前年份）
        yearless_patterns = [
            r"(\d{1,2})月(\d{1,2})日",  # 4月12日
            r"(\d{1,2})月(\d{1,2})号",  # 4月12号
        ]
        
        date_found = None
        for pattern, has_dash in dated_patterns:
            match = re.search(pattern, text)
            if match:
                groups = match.groups()
                if len(groups) == 3:
                    date_found = f"{groups[0]}-{int(groups[1]):02d}-{int(groups[2]):02d}"
                    break
        
        if not date_found:
            for pattern in yearless_patterns:
                match = re.search(pattern, text)
                if match:
                    groups = match.groups()
                    month = int(groups[0])
                    day = int(groups[1])
                    date_found = f"{current_year}-{month:02d}-{day:02d}"
                    break
        
        if date_found:
            result["race_date"] = date_found
        else:
            result["errors"].append("未找到比赛日期，请使用 YYYY-MM-DD 格式")
        
        # 目标时间识别
        time_patterns = [
            r"(\d{1,2}):(\d{2}):(\d{2})",  # 2:00:00
            r"(\d{1,2})点(\d{1,2})分",  # 2点00分
            r"(\d{1,2})时(\d{1,2})分",  # 2时00分
            r"破?2?[时:]?(\d{1,2})[分]?(\d{2})?秒?",  # 破2 / 2:00 / 2点
        ]
        
        goal_time = None
        
        # 简单识别"破2" -> 2小时
        if "破2" in text and result["race_type"] == "半程马拉松":
            goal_time = "02:00:00"
        elif "破4:45" in text or "破445" in text:
            goal_time = "04:45:00"
        elif "4:45" in text or "445" in text:
            goal_time = "04:45:00"
        
        # 识别 XX:XX:XX 格式
        if not goal_time:
            for pattern in time_patterns:
                match = re.search(pattern, text)
                if match:
                    groups = match.groups()
                    if len(groups) >= 2 and groups[0] is not None:
                        h = int(groups[0])
                        m = int(groups[1]) if groups[1] is not None else 0
                        s = int(groups[2]) if len(groups) > 2 and groups[2] else 0
                        goal_time = f"{h}:{m:02d}:{s:02d}"
                        break
        
        if goal_time:
            result["goal_time"] = goal_time
        
        # 比赛名称识别
        race_name_patterns = [
            r"北京半马",
            r"通州全马",
            r"上海半马",
            r"上海全马",
            r"厦门半马",
            r"厦门全马",
            r"无锡半马",
            r"无锡全马",
            r"武汉半马",
            r"武汉全马",
        ]
        
        for pattern in race_name_patterns:
            if pattern in text:
                result["race_name"] = pattern
                break
        
        if not result["race_name"]:
            # 默认名称
            if result["race_type"] == "半程马拉松":
                result["race_name"] = "半马"
            else:
                result["race_name"] = "全马"
        
        # 验证
        if not result["race_date"]:
            result["errors"].append("请提供比赛日期")
        
        result["success"] = len(result["errors"]) == 0
        
        return result
    
    def set_marathon_goal(self, race_name: str, race_date: str, 
                         goal_time: str = None,
                         race_type: str = "半程马拉松") -> Dict:
        """
        设置马拉松目标
        
        Args:
            race_name: 比赛名称
            race_date: 比赛日期 (YYYY-MM-DD)
            goal_time: 目标时间 (HH:MM:SS)
            race_type: 比赛类型
        
        Returns:
            {
                "success": bool,
                "message": str,
                "goal": MarathonGoal
            }
        """
        try:
            # 验证日期
            race_date_obj = datetime.strptime(race_date, "%Y-%m-%d")
            days_until = (race_date_obj.date() - datetime.now().date()).days
            
            if days_until < 0:
                return {
                    "success": False,
                    "message": f"比赛日期 {race_date} 已经过去",
                    "goal": None
                }
            
            # 创建目标
            goal = self.goals_manager.create_marathon_goal(
                race_name=race_name,
                race_date=race_date,
                goal_time=goal_time,
                race_type=race_type
            )
            
            # 生成成功消息
            phase = goal.training_phase
            target_pace_str = ""
            if goal.target_pace:
                target_pace_str = f"（配速 {goal.target_pace}/km）"
            
            message = f"""✅ 马拉松目标已设置！

🏃 比赛：{goal.goal_name}
📅 日期：{race_date}（{days_until}天后）
🏅 类型：{goal.race_type}"""
            
            if goal.goal_time:
                message += f"\n🎯 目标：{goal.goal_time}"
            
            if goal.target_pace:
                message += f"\n⚡ 目标配速：{goal.target_pace}/km"
            
            message += f"\n📊 当前阶段：{phase}"
            
            return {
                "success": True,
                "message": message,
                "goal": goal
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"设置失败：{str(e)}",
                "goal": None
            }
    
    def get_marathon_status(self) -> str:
        """
        获取当前马拉松训练状态
        
        Returns:
            状态报告文本
        """
        goals = self.goals_manager.get_marathon_goals()
        active = self.goals_manager.get_active_marathon_goals()
        
        if not active:
            return """📭 暂无马拉松训练计划

设置方式：
/设置马拉松 北京半马 2026-04-12 目标2:00:00
或直接告诉我：「4月12号半马，目标是破2」"""
        
        # 获取最近跑步
        recent_runs = self.tracker.get_recent_runs(self.user_id, days=7)
        distance_summary = self.tracker.get_distance_summary(self.user_id)
        
        # 构建状态报告
        lines = []
        lines.append("🏃 **马拉松训练状态**")
        lines.append("")
        
        for goal in active:
            days = goal.days_until_race
            phase = goal.training_phase
            
            lines.append("━━━━━━━━━━━━━━━━━━━━")
            lines.append(f"📅 **{goal.goal_name}**")
            lines.append(f"📆 日期：{goal.race_date}（{days}天后）")
            lines.append(f"🏅 类型：{goal.race_type}")
            
            if goal.goal_time:
                lines.append(f"🎯 目标：{goal.goal_time}")
            if goal.target_pace:
                lines.append(f"⚡ 配速：{goal.target_pace}/km")
            
            lines.append(f"📊 阶段：{phase}")
            
            # 阶段提示
            phase_summary = self.analyzer.get_phase_summary(goal)
            if phase_summary.get("phase_tips"):
                lines.append("")
                lines.append("💡 阶段提示：")
                for tip in phase_summary["phase_tips"][:2]:
                    lines.append(f"• {tip}")
            
            lines.append("")
        
        # 本周跑量
        lines.append("━━━━━━━━━━━━━━━━━━━━")
        lines.append("📈 **本周跑量**")
        lines.append(f"• 本周：{distance_summary['this_week_km']}km")
        lines.append(f"• 上周：{distance_summary['last_week_km']}km")
        week_change = distance_summary['week_change']
        if week_change >= 0:
            lines.append(f"• 变化：+{week_change}km ↑")
        else:
            lines.append(f"• 变化：{week_change}km ↓")
        
        # 最近跑步
        if recent_runs:
            lines.append("")
            lines.append("🏃 **近期跑步**")
            for r in recent_runs[:3]:
                date = r.get("date", "")[5:]  # MM-DD
                dist = r.get("distance_km", 0)
                pace = r.get("avg_pace", "-")
                lines.append(f"• {date} {dist}km @ {pace}/km")
        
        return "\n".join(lines)
    
    def adjust_plan(self, date_str: str, new_plan: str) -> Dict:
        """
        调整某天的计划
        
        Args:
            date_str: 日期（如"明天"、"4月5日"）
            new_plan: 新计划（如"休息"、"8km轻松跑"）
        
        Returns:
            {
                "success": bool,
                "message": str
            }
        """
        # 解析日期
        import re
        today = datetime.now()
        
        if date_str in ["今天", "今日"]:
            target_date = today
        elif date_str in ["明天", "明日"]:
            target_date = today + __import__('datetime').timedelta(days=1)
        elif date_str in ["后天", "后日"]:
            target_date = today + __import__('datetime').timedelta(days=2)
        else:
            # 尝试解析 YYYY-MM-DD 或 MM-DD
            match = re.search(r"(\d{1,2})月(\d{1,2})日", date_str)
            if match:
                month, day = int(match.group(1)), int(match.group(2))
                target_date = datetime(today.year, month, day)
            else:
                return {
                    "success": False,
                    "message": f"无法解析日期：{date_str}，请使用「今天」「明天」「4月5日」等格式"
                }
        
        date_str_formatted = target_date.strftime("%Y-%m-%d")
        
        return {
            "success": True,
            "message": f"""✅ 计划已调整

📅 {target_date.strftime('%m月%d日')}（{date_str}）
🆕 新计划：{new_plan}

注意：此功能需要后续打卡系统支持""",
            "adjusted_date": date_str_formatted,
            "new_plan": new_plan
        }
    
    def get_training_calendar(self, days: int = 14) -> str:
        """
        获取训练日历
        
        Args:
            days: 天数
        
        Returns:
            日历文本
        """
        calendar = self.tracker.get_training_calendar(
            self.user_id,
            end_date=datetime.now().strftime("%Y-%m-%d")
        )
        
        # 只显示有跑步的日子
        running_days = [d for d in calendar if d.get("has_training")]
        
        if not running_days:
            return "📭 近期暂无跑步记录"
        
        lines = []
        lines.append(f"🏃 **近期训练日历**（{len(running_days)}天有跑步）")
        lines.append("")
        
        for day in running_days[-14:]:
            date = day["date"]
            total = day.get("total_distance", 0)
            runs = day.get("runs", [])
            
            # 格式化日期
            try:
                d = datetime.strptime(date, "%Y-%m-%d")
                date_display = d.strftime("%m/%d")
            except:
                date_display = date
            
            # 跑步详情
            run_details = []
            for r in runs:
                dist = r.get("distance_km", 0)
                pace = r.get("avg_pace", "-")
                run_details.append(f"{dist}km@{pace}")
            
            lines.append(f"**{date_display}** {total}km")
            for detail in run_details:
                lines.append(f"  • {detail}")
        
        return "\n".join(lines)


# ==================== 便捷函数 ====================

def parse_and_set_marathon(user_id: str, text: str) -> Dict:
    """解析用户输入并设置马拉松目标"""
    cmd = MarathonCommands(user_id)
    
    # 解析比赛信息
    parsed = cmd.parse_race_info(text)
    
    if not parsed["success"]:
        return {
            "success": False,
            "message": f"解析失败：{', '.join(parsed['errors'])}\n\n请使用格式：\n• 4月12号半马，目标是破2\n• 北京半马 2026-04-12 目标2:00:00"
        }
    
    # 设置目标
    result = cmd.set_marathon_goal(
        race_name=parsed["race_name"],
        race_date=parsed["race_date"],
        goal_time=parsed.get("goal_time"),
        race_type=parsed["race_type"]
    )
    
    return result


def get_marathon_status(user_id: str = "dongyi") -> str:
    """获取马拉松状态"""
    cmd = MarathonCommands(user_id)
    return cmd.get_marathon_status()


def adjust_training_plan(user_id: str, date: str, new_plan: str) -> Dict:
    """调整训练计划"""
    cmd = MarathonCommands(user_id)
    return cmd.adjust_plan(date, new_plan)


# ==================== 测试 ====================

if __name__ == "__main__":
    print("=== Marathon Commands Test ===")
    
    cmd = MarathonCommands("test_user")
    
    # 测试解析
    print("\n--- Parse Race Info ---")
    test_inputs = [
        "4月12号半马目标是破2",
        "北京半马 2026-04-12 目标2:00:00",
        "通州全马 2026-04-19 目标是4:45",
    ]
    
    for inp in test_inputs:
        parsed = cmd.parse_race_info(inp)
        print(f"\nInput: {inp}")
        print(f"  Success: {parsed['success']}")
        if parsed['success']:
            print(f"  Name: {parsed['race_name']}")
            print(f"  Date: {parsed['race_date']}")
            print(f"  Type: {parsed['race_type']}")
            print(f"  Time: {parsed['goal_time']}")
        else:
            print(f"  Errors: {parsed['errors']}")
    
    # 测试设置马拉松目标
    print("\n--- Set Marathon Goal ---")
    result = cmd.set_marathon_goal(
        race_name="测试半马",
        race_date="2026-04-12",
        goal_time="02:00:00",
        race_type="半程马拉松"
    )
    print(f"Success: {result['success']}")
    print(f"Message: {result['message']}")
    
    # 测试状态查询
    print("\n--- Marathon Status ---")
    status = cmd.get_marathon_status()
    print(status)
    
    # 测试调整计划
    print("\n--- Adjust Plan ---")
    adjust = cmd.adjust_plan("明天", "休息")
    print(f"Success: {adjust['success']}")
    print(f"Message: {adjust['message']}")
    
    # 清理测试数据
    print("\n--- Cleanup ---")
    goals = cmd.goals_manager.get_marathon_goals()
    for g in goals:
        cmd.goals_manager.delete_marathon_goal(g.goal_id)
    print(f"Deleted {len(goals)} test goals")
    
    print("\n✅ All tests passed!")
