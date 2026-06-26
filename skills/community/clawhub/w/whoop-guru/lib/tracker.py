"""
Progress Tracker - 进度追踪系统
记录用户打卡和训练完成情况
包括跑步专项打卡追踪
"""

import os
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional


class ProgressTracker:
    """
    进度追踪器
    管理用户的训练打卡记录
    """
    
    def __init__(self, user_id: str = "default"):
        self.user_id = user_id
        self.logs_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "data", "logs"
        )
        os.makedirs(self.logs_dir, exist_ok=True)
        self.checkins_file = os.path.join(self.logs_dir, f"checkins_{user_id}.json")
        self.running_file = os.path.join(self.logs_dir, f"running_{user_id}.json")
    
    # ==================== 基础打卡 CRUD ====================
    
    def _load_checkins(self) -> Dict:
        """加载打卡记录"""
        if not os.path.exists(self.checkins_file):
            return {"checkins": []}
        try:
            with open(self.checkins_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {"checkins": []}
    
    def _save_checkins(self, data: Dict) -> bool:
        """保存打卡记录"""
        try:
            with open(self.checkins_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception:
            return False
    
    def add_checkin(
        self,
        user_id: str,
        checkin_type: str,
        completed: str,
        feedback: str,
        notes: str = ""
    ) -> str:
        """
        添加打卡记录
        
        Args:
            user_id: 用户ID
            checkin_type: 打卡类型（跑步/力量/休息/拉伸等）
            completed: 完成情况
            feedback: 身体感受
            notes: 备注
        
        Returns:
            checkin_id
        """
        checkin_id = f"checkin_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        entry = {
            "id": checkin_id,
            "user_id": user_id,
            "type": checkin_type,
            "completed": completed,
            "feedback": feedback,
            "notes": notes,
            "timestamp": datetime.now().isoformat()
        }
        
        data = self._load_checkins()
        data["checkins"].append(entry)
        self._save_checkins(data)
        
        return checkin_id
    
    def quick_checkin(
        self,
        user_id: str,
        checkin_type: str,
        notes: str = ""
    ) -> str:
        """
        快速打卡 - 简化版，无需填写完成情况和感受
        
        Args:
            user_id: 用户ID
            checkin_type: 打卡类型（跑步/力量/休息/拉伸/瑜伽等）
            notes: 备注（可包含距离、配速、重量等具体数据）
        
        Returns:
            checkin_id
        """
        checkin_id = f"checkin_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        entry = {
            "id": checkin_id,
            "user_id": user_id,
            "type": checkin_type,
            "completed": checkin_type,
            "feedback": "良好",
            "notes": notes,
            "timestamp": datetime.now().isoformat()
        }
        
        data = self._load_checkins()
        data["checkins"].append(entry)
        self._save_checkins(data)
        
        return checkin_id

    def get_checkins(self, user_id: str, limit: int = 30) -> List[Dict]:
        """获取打卡记录"""
        data = self._load_checkins()
        checkins = [c for c in data.get("checkins", []) 
                    if c.get("user_id") == user_id]
        checkins.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        return checkins[:limit]
    
    def get_streak(self, user_id: str) -> int:
        """计算连续打卡天数"""
        checkins = self.get_checkins(user_id, limit=100)
        
        if not checkins:
            return 0
        
        # 按日期分组
        dates = set()
        for c in checkins:
            ts = c.get("timestamp", "")[:10]  # YYYY-MM-DD
            if ts:
                dates.add(ts)
        
        if not dates:
            return 0
        
        # 排序并计算连续天数
        sorted_dates = sorted(dates, reverse=True)
        today = datetime.now().strftime("%Y-%m-%d")
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        
        # 如果今天和昨天都没有打卡，连续天数归零
        if sorted_dates[0] != today and sorted_dates[0] != yesterday:
            return 0
        
        streak = 1
        for i in range(len(sorted_dates) - 1):
            curr = datetime.strptime(sorted_dates[i], "%Y-%m-%d")
            next_d = datetime.strptime(sorted_dates[i+1], "%Y-%m-%d")
            if (curr - next_d).days == 1:
                streak += 1
            else:
                break
        
        return streak
    
    def get_weekly_summary(self, user_id: str) -> Dict:
        """获取周打卡汇总"""
        checkins = self.get_checkins(user_id, limit=50)
        
        today = datetime.now()
        week_start = today - timedelta(days=today.weekday())
        week_start_str = week_start.strftime("%Y-%m-%d")
        
        week_checkins = [
            c for c in checkins 
            if c.get("timestamp", "")[:10] >= week_start_str
        ]
        
        type_count = {}
        for c in week_checkins:
            t = c.get("type", "其他")
            type_count[t] = type_count.get(t, 0) + 1
        
        total = len(week_checkins)
        completion_rate = min(100, (total / 7) * 100)
        
        return {
            "total_checkins": total,
            "types": type_count,
            "completion_rate": completion_rate,
            "week_start": week_start_str
        }
    
    # ==================== 跑步打卡 CRUD ====================
    
    def _load_running(self) -> Dict:
        """加载跑步记录"""
        if not os.path.exists(self.running_file):
            return {"runs": []}
        try:
            with open(self.running_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {"runs": []}
    
    def _save_running(self, data: Dict) -> bool:
        """保存跑步记录"""
        try:
            with open(self.running_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception:
            return False
    
    def add_running_checkin(
        self,
        user_id: str,
        distance_km: float,
        duration_min: int,
        avg_pace: str,
        avg_heart_rate: int = None,
        max_heart_rate: int = None,
        feeling: str = "良好",
        terrain: str = "公路",
        notes: str = ""
    ) -> str:
        """
        添加跑步打卡
        
        Args:
            user_id: 用户ID
            distance_km: 距离（公里）
            duration_min: 时长（分钟）
            avg_pace: 平均配速（MM:SS）
            avg_heart_rate: 平均心率
            max_heart_rate: 最大心率
            feeling: 身体感受（良好/一般/疲劳/受伤）
            terrain: 地形（公路/跑道/公园/跑步机）
            notes: 备注
        
        Returns:
            run_id
        """
        run_id = f"run_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        entry = {
            "id": run_id,
            "user_id": user_id,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "timestamp": datetime.now().isoformat(),
            "distance_km": distance_km,
            "duration_min": duration_min,
            "avg_pace": avg_pace,
            "avg_heart_rate": avg_heart_rate,
            "max_heart_rate": max_heart_rate,
            "feeling": feeling,
            "terrain": terrain,
            "notes": notes
        }
        
        data = self._load_running()
        data["runs"].append(entry)
        self._save_running(data)
        
        # 同时添加到基础打卡
        self.add_checkin(
            user_id=user_id,
            checkin_type="跑步",
            completed=f"{distance_km}km",
            feedback=feeling,
            notes=f"配速{avg_pace}/km, 地形{terrain}"
        )
        
        return run_id
    
    def get_recent_runs(self, user_id: str, days: int = 7) -> List[Dict]:
        """获取最近N天的跑步记录"""
        data = self._load_running()
        cutoff = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        
        runs = [r for r in data.get("runs", [])
                if r.get("user_id") == user_id 
                and r.get("date", "") >= cutoff]
        
        runs.sort(key=lambda x: x.get("date", ""), reverse=True)
        return runs
    
    def get_weekly_distance(self, user_id: str, week_offset: int = 0) -> float:
        """
        获取某周的跑量（公里）
        
        Args:
            user_id: 用户ID
            week_offset: 周偏移（0=本周, -1=上周, 1=下周）
        
        Returns:
            总跑量（公里）
        """
        today = datetime.now()
        week_start = today - timedelta(days=today.weekday() + week_offset * 7)
        week_end = week_start + timedelta(days=6)
        
        week_start_str = week_start.strftime("%Y-%m-%d")
        week_end_str = week_end.strftime("%Y-%m-%d")
        
        data = self._load_running()
        total = 0.0
        
        for r in data.get("runs", []):
            if r.get("user_id") == user_id:
                run_date = r.get("date", "")
                if week_start_str <= run_date <= week_end_str:
                    total += r.get("distance_km", 0)
        
        return round(total, 1)
    
    def get_monthly_distance(self, user_id: str, month_offset: int = 0) -> float:
        """
        获取某月的跑量（公里）
        
        Args:
            user_id: 用户ID
            month_offset: 月偏移（0=本月, -1=上月）
        
        Returns:
            总跑量（公里）
        """
        today = datetime.now()
        month = today.month + month_offset
        year = today.year
        
        if month <= 0:
            month += 12
            year -= 1
        
        data = self._load_running()
        total = 0.0
        
        for r in data.get("runs", []):
            if r.get("user_id") == user_id:
                run_date = r.get("date", "")
                if run_date:
                    run_month = datetime.strptime(run_date, "%Y-%m-%d").month
                    run_year = datetime.strptime(run_date, "%Y-%m-%d").year
                    if run_month == month and run_year == year:
                        total += r.get("distance_km", 0)
        
        return round(total, 1)
    
    def analyze_running_pattern(self, user_id: str, days: int = 30) -> Dict:
        """
        分析跑步模式
        
        Returns:
            {
                "total_runs": int,
                "total_distance": float,
                "avg_distance": float,
                "avg_pace": str,
                "best_pace": str,
                "longest_run": float,
                "most_common_terrain": str,
                "most_common_feeling": str,
                "weekly_avg_distance": float,
                "runs_per_week": float
            }
        """
        runs = self.get_recent_runs(user_id, days=days)
        
        if not runs:
            return {
                "total_runs": 0,
                "total_distance": 0,
                "avg_distance": 0,
                "avg_pace": "0:00",
                "best_pace": "0:00",
                "longest_run": 0,
                "most_common_terrain": "未知",
                "most_common_feeling": "未知",
                "weekly_avg_distance": 0,
                "runs_per_week": 0
            }
        
        total_distance = sum(r.get("distance_km", 0) for r in runs)
        longest_run = max(r.get("distance_km", 0) for r in runs)
        
        # 计算平均配速
        pace_seconds = []
        for r in runs:
            pace = r.get("avg_pace", "0:00")
            if ":" in pace:
                parts = pace.split(":")
                seconds = int(parts[0]) * 60 + int(parts[1])
                pace_seconds.append(seconds)
        
        avg_pace = "0:00"
        if pace_seconds:
            avg_secs = sum(pace_seconds) / len(pace_seconds)
            avg_pace = f"{int(avg_secs // 60)}:{int(avg_secs % 60):02d}"
        
        best_pace = "0:00"
        if pace_seconds:
            best_secs = min(pace_seconds)
            best_pace = f"{int(best_secs // 60)}:{int(best_secs % 60):02d}"
        
        # 统计地形和感受
        terrain_count = {}
        feeling_count = {}
        for r in runs:
            t = r.get("terrain", "未知")
            f = r.get("feeling", "未知")
            terrain_count[t] = terrain_count.get(t, 0) + 1
            feeling_count[f] = feeling_count.get(f, 0) + 1
        
        most_common_terrain = max(terrain_count.items(), key=lambda x: x[1])[0] if terrain_count else "未知"
        most_common_feeling = max(feeling_count.items(), key=lambda x: x[1])[0] if feeling_count else "未知"
        
        # 计算周平均
        weeks = max(1, days // 7)
        weekly_avg = total_distance / weeks
        runs_per_week = len(runs) / weeks
        
        return {
            "total_runs": len(runs),
            "total_distance": round(total_distance, 1),
            "avg_distance": round(total_distance / len(runs), 1) if runs else 0,
            "avg_pace": avg_pace,
            "best_pace": best_pace,
            "longest_run": longest_run,
            "most_common_terrain": most_common_terrain,
            "most_common_feeling": most_common_feeling,
            "weekly_avg_distance": round(weekly_avg, 1),
            "runs_per_week": round(runs_per_week, 1)
        }
    
    def suggest_next_run(self, user_id: str, marathon_goal: Dict = None) -> Dict:
        """
        根据近期训练和马拉松目标给出下次跑步建议
        
        Args:
            user_id: 用户ID
            marathon_goal: 马拉松目标信息（可选）
                {
                    "days_until_race": int,
                    "training_phase": str,
                    "target_pace": str
                }
        
        Returns:
            {
                "suggested_distance": float,  # km
                "suggested_pace": str,  # MM:SS
                "suggested_type": str,  # 轻松跑/节奏跑/长跑等
                "reason": str,
                "pace_guide": str,
                "heart_rate_zone": str
            }
        """
        recent_runs = self.get_recent_runs(user_id, days=7)
        pattern = self.analyze_running_pattern(user_id, days=14)
        
        # 默认建议
        suggestion = {
            "suggested_distance": 8.0,
            "suggested_pace": "6:00",
            "suggested_type": "轻松跑",
            "reason": "根据近期训练情况",
            "pace_guide": "6:00-6:30/km",
            "heart_rate_zone": "Z2（轻松有氧区）"
        }
        
        # 如果有马拉松目标，根据阶段调整
        if marathon_goal:
            phase = marathon_goal.get("training_phase", "基础期")
            days_until = marathon_goal.get("days_until_race", 30)
            
            if phase == "比赛周":
                suggestion = {
                    "suggested_distance": 3.0,
                    "suggested_pace": "7:00",
                    "suggested_type": "热身跑",
                    "reason": f"赛前减量期，保持活力即可",
                    "pace_guide": "7:00-7:30/km",
                    "heart_rate_zone": "Z1-Z2"
                }
            elif phase == "减量期":
                suggestion = {
                    "suggested_distance": 6.0,
                    "suggested_pace": "6:30",
                    "suggested_type": "轻松跑",
                    "reason": f"减量期，减少训练量，保持状态",
                    "pace_guide": "6:00-6:30/km",
                    "heart_rate_zone": "Z2"
                }
            elif phase == "巅峰期":
                suggestion = {
                    "suggested_distance": 10.0,
                    "suggested_pace": "5:30",
                    "suggested_type": "节奏跑",
                    "reason": f"巅峰期，可安排高强度训练",
                    "pace_guide": "5:30-5:45/km",
                    "heart_rate_zone": "Z3-Z4"
                }
            else:  # 基础期
                suggestion = {
                    "suggested_distance": 12.0,
                    "suggested_pace": "6:00",
                    "suggested_type": "长跑",
                    "reason": f"基础期，积累跑量",
                    "pace_guide": "6:00-6:30/km",
                    "heart_rate_zone": "Z2"
                }
        
        # 根据近期训练调整
        if recent_runs:
            last_run = recent_runs[0]
            last_distance = last_run.get("distance_km", 0)
            last_feeling = last_run.get("feeling", "良好")
            
            # 如果上次感觉疲劳，减少跑量
            if last_feeling == "疲劳":
                suggestion["suggested_distance"] *= 0.7
                suggestion["reason"] = "上次感觉疲劳，减少跑量"
            
            # 如果连续跑了两天以上长跑，提醒休息
            if len(recent_runs) >= 2:
                if recent_runs[0].get("distance_km", 0) >= 10 and \
                   recent_runs[1].get("distance_km", 0) >= 10:
                    suggestion["suggested_distance"] = 5.0
                    suggestion["suggested_type"] = "恢复跑"
                    suggestion["reason"] = "连续高强度，提醒休息"
        
        # 四舍五入距离
        suggestion["suggested_distance"] = round(suggestion["suggested_distance"], 1)
        
        return suggestion
    
    def get_training_calendar(
        self, 
        user_id: str, 
        start_date: str = None, 
        end_date: str = None
    ) -> List[Dict]:
        """
        获取训练日历
        
        Args:
            user_id: 用户ID
            start_date: 开始日期（YYYY-MM-DD）
            end_date: 结束日期（YYYY-MM-DD）
        
        Returns:
            每日训练记录列表
        """
        if not start_date:
            start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")
        
        runs = self._load_running().get("runs", [])
        checkins = self._load_checkins().get("checkins", [])
        
        # 按日期组织数据
        calendar = {}
        current = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        
        while current <= end:
            date_str = current.strftime("%Y-%m-%d")
            calendar[date_str] = {
                "date": date_str,
                "runs": [],
                "checkins": [],
                "has_training": False,
                "total_distance": 0
            }
            current += timedelta(days=1)
        
        # 填充跑步数据
        for r in runs:
            if r.get("user_id") == user_id:
                date_str = r.get("date", "")
                if start_date <= date_str <= end_date and date_str in calendar:
                    calendar[date_str]["runs"].append(r)
                    calendar[date_str]["has_training"] = True
                    calendar[date_str]["total_distance"] += r.get("distance_km", 0)
        
        # 填充打卡数据
        for c in checkins:
            if c.get("user_id") == user_id:
                date_str = c.get("timestamp", "")[:10]
                if start_date <= date_str <= end_date and date_str in calendar:
                    calendar[date_str]["checkins"].append(c)
        
        return list(calendar.values())
    
    def get_distance_summary(self, user_id: str) -> Dict:
        """获取跑量汇总"""
        today = datetime.now()
        
        # 本周
        this_week = self.get_weekly_distance(user_id, week_offset=0)
        
        # 上周
        last_week = self.get_weekly_distance(user_id, week_offset=-1)
        
        # 本月
        this_month = self.get_monthly_distance(user_id, month_offset=0)
        
        # 上月
        last_month = self.get_monthly_distance(user_id, month_offset=-1)
        
        # 今年（估算）
        this_year = 0
        for week in range(52):
            dist = self.get_weekly_distance(user_id, week_offset=-week)
            if dist > 0:
                this_year += dist
            else:
                break
        
        return {
            "this_week_km": this_week,
            "last_week_km": last_week,
            "week_change": round(this_week - last_week, 1),
            "this_month_km": this_month,
            "last_month_km": last_month,
            "month_change": round(this_month - last_month, 1),
            "this_year_km": round(this_year, 1),
            "target_100km_month": 100,
            "target_500km_year": 500
        }


# ==================== 便捷函数 ====================

def add_checkin(user_id: str, checkin_type: str, completed: str, 
               feedback: str, notes: str = "") -> str:
    """添加打卡"""
    tracker = ProgressTracker(user_id)
    return tracker.add_checkin(user_id, checkin_type, completed, feedback, notes)


def quick_checkin(user_id: str, checkin_type: str, notes: str = "") -> str:
    """快速打卡 - 无需填写完成情况和感受"""
    tracker = ProgressTracker(user_id)
    return tracker.quick_checkin(user_id, checkin_type, notes)


def add_running_checkin(user_id: str, distance_km: float, duration_min: int,
                       avg_pace: str, **kwargs) -> str:
    """添加跑步打卡"""
    tracker = ProgressTracker(user_id)
    return tracker.add_running_checkin(user_id, distance_km, duration_min, avg_pace, **kwargs)


def get_checkins(user_id: str, limit: int = 30) -> List[Dict]:
    """获取打卡记录"""
    tracker = ProgressTracker(user_id)
    return tracker.get_checkins(user_id, limit)


def get_recent_runs(user_id: str, days: int = 7) -> List[Dict]:
    """获取最近跑步记录"""
    tracker = ProgressTracker(user_id)
    return tracker.get_recent_runs(user_id, days)


def get_streak(user_id: str) -> int:
    """获取连续打卡天数"""
    tracker = ProgressTracker(user_id)
    return tracker.get_streak(user_id)


def analyze_running_pattern(user_id: str, days: int = 30) -> Dict:
    """分析跑步模式"""
    tracker = ProgressTracker(user_id)
    return tracker.analyze_running_pattern(user_id, days)


# ==================== 测试 ====================

def get_tracker() -> ProgressTracker:
    """获取ProgressTracker单例"""
    return ProgressTracker()


def get_goal_tracker() -> ProgressTracker:
    """获取用于目标追踪的ProgressTracker（别名，兼容coach_interface）"""
    return ProgressTracker()


if __name__ == "__main__":
    print("=== Progress Tracker Test ===")
    
    user_id = "test_user"
    tracker = ProgressTracker(user_id)
    
    # 测试添加跑步打卡
    print("\n--- Add Running Checkin ---")
    run_id = tracker.add_running_checkin(
        user_id=user_id,
        distance_km=10.5,
        duration_min=60,
        avg_pace="5:43",
        avg_heart_rate=145,
        max_heart_rate=168,
        feeling="良好",
        terrain="跑道",
        notes="节奏跑训练"
    )
    print(f"Added run: {run_id}")
    
    # 测试获取跑步记录
    print("\n--- Recent Runs ---")
    runs = tracker.get_recent_runs(user_id, days=7)
    print(f"Recent runs: {len(runs)}")
    for r in runs:
        print(f"  {r['date']}: {r['distance_km']}km @ {r['avg_pace']}/km")
    
    # 测试跑量汇总
    print("\n--- Distance Summary ---")
    summary = tracker.get_distance_summary(user_id)
    print(f"This week: {summary['this_week_km']}km")
    print(f"This month: {summary['this_month_km']}km")
    
    # 测试跑步模式分析
    print("\n--- Running Pattern ---")
    pattern = tracker.analyze_running_pattern(user_id, days=30)
    print(f"Total runs: {pattern['total_runs']}")
    print(f"Total distance: {pattern['total_distance']}km")
    print(f"Avg pace: {pattern['avg_pace']}/km")
    print(f"Most common terrain: {pattern['most_common_terrain']}")
    
    # 测试打卡
    print("\n--- Checkins ---")
    checkin_id = tracker.add_checkin(
        user_id=user_id,
        checkin_type="力量",
        completed="胸背腿训练完成",
        feedback="肌肉酸痛",
        notes="练后拉伸15分钟"
    )
    print(f"Added checkin: {checkin_id}")
    
    streak = tracker.get_streak(user_id)
    print(f"Current streak: {streak} days")
    
    weekly = tracker.get_weekly_summary(user_id)
    print(f"Weekly summary: {weekly}")
    
    # 清理测试数据
    print("\n--- Cleanup ---")
    # 删除测试跑步记录
    data = tracker._load_running()
    data["runs"] = [r for r in data["runs"] if r.get("user_id") != user_id]
    tracker._save_running(data)
    
    # 删除测试打卡记录
    data = tracker._load_checkins()
    data["checkins"] = [c for c in data["checkins"] if c.get("user_id") != user_id]
    tracker._save_checkins(data)
    
    print("Test data cleaned up")
    print("\n✅ All tests passed!")
