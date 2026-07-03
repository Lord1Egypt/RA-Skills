#!/usr/bin/env python3
"""
运动卡路里计算引擎 + 运动日记管理
- 基于MET值的卡路里消耗计算
- 运动日记持久化存储
- 用户档案管理
- 趋势分析
"""

import json
import re
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Optional
try:
    from .motion_db import search_exercise, get_food_equivalent
except ImportError:
    from motion_db import search_exercise, get_food_equivalent

DATA_DIR = Path(__file__).parent.parent / "user_data"
DIARY_DIR = DATA_DIR / "diary"
PROFILE_PATH = DATA_DIR / "profile.json"


class CalorieCalc:
    def __init__(self):
        DIARY_DIR.mkdir(parents=True, exist_ok=True)

    # ---- 用户档案 ----

    def load_profile(self) -> Optional[dict]:
        if PROFILE_PATH.exists():
            with open(PROFILE_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        return None

    def save_profile(self, profile: dict):
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        with open(PROFILE_PATH, "w", encoding="utf-8") as f:
            json.dump(profile, f, ensure_ascii=False, indent=2)

    def get_weight(self) -> float:
        """获取用户体重(kg)，未设置则默认70kg"""
        profile = self.load_profile()
        if profile and "body" in profile:
            return profile["body"].get("weight_kg", 70.0)
        return 70.0

    # ---- 运动解析 ----

    def parse_exercise_text(self, text: str) -> list:
        """
        自然语言解析运动记录
        支持: "跑了5公里30分钟"、"游了40分钟泳"、"做了3组深蹲"
        返回: [{exercise_type, met, duration_min, distance_km, reps_sets, intensity}]
        """
        exercises = []
        text_clean = text.strip()

        # 尝试分割多个运动（按逗号、然后、接着、之后 等）
        parts = re.split(r'[,，]|然后|接着|之后|还|又|也|和|与|及|再', text_clean)
        
        for part in parts:
            part = part.strip()
            if not part or len(part) < 2:
                continue

            result = self._parse_single_exercise(part)
            if result:
                exercises.append(result)

        return exercises

    def _parse_single_exercise(self, text: str) -> Optional[dict]:
        """解析单个运动记录"""
        # 去除前缀
        text = re.sub(r'^(今天|昨天|上午|下午|晚上|早上|我)?(做了?|去|进行了?|完成了?)?', '', text).strip()
        if not text:
            return None

        # 查找运动类型
        exercise_info = search_exercise(text)
        if not exercise_info:
            return None

        # 提取时长 (分钟)
        duration_min = 30  # 默认30分钟
        dur_match = re.search(r'(\d+)\s*(分钟|分|min|mins)', text)
        if dur_match:
            duration_min = int(dur_match.group(1))
        else:
            hour_match = re.search(r'(\d+(?:\.\d+)?)\s*(小时|h|hr|hrs|个钟)', text)
            if hour_match:
                duration_min = int(float(hour_match.group(1)) * 60)
            elif re.search(r'半小时|0\.5小时|半个钟', text):
                duration_min = 30
            elif re.search(r'1个?半小时|一个半钟|1\.5小时', text):
                duration_min = 90

        # 提取距离 (公里)
        distance_km = None
        dist_match = re.search(r'(\d+(?:\.\d+)?)\s*(公里|千米|km|K)', text)
        if dist_match:
            distance_km = float(dist_match.group(1))
        else:
            m_match = re.search(r'(\d+)\s*[米m](?!饭|粉|线|粥)', text)
            if m_match:
                distance_km = int(m_match.group(1)) / 1000.0

        # 从距离推断时长（如果有距离没时长，用默认速度推断）
        if distance_km and not dur_match and exercise_info.get("default_speed") and exercise_info["default_speed"] != "-":
            try:
                speed = float(exercise_info["default_speed"].split()[0])
                duration_min = int(distance_km / speed * 60)
            except (ValueError, IndexError):
                pass

        # 提取组数/次数（力量训练）
        reps = None
        sets = None
        rep_match = re.search(r'(\d+)\s*[组set]', text)
        if rep_match:
            sets = int(rep_match.group(1))
        num_match = re.search(r'(\d+)\s*[次个rep]', text)
        if num_match:
            reps = int(num_match.group(1))

        # 提取强度
        intensity = "moderate"
        if any(kw in text for kw in ["快", "冲刺", "高强度", "全力", "暴汗", "猛"]):
            intensity = "high"
        elif any(kw in text for kw in ["慢", "轻松", "休闲", "缓", "放松"]):
            intensity = "low"

        # 强度调整MET
        met = exercise_info["met"]
        if intensity == "low":
            met *= 0.8
        elif intensity == "high":
            met *= 1.2

        # 力量训练如果有组数，只记录组数时间
        if exercise_info.get("category") == "力量" and sets:
            duration_min = sets * 3  # 每组约3分钟含休息
        elif re.search(r'平板支撑|plank', text, re.IGNORECASE):
            # 平板支撑特殊处理
            sec_match = re.search(r'(\d+)\s*(秒|s|sec)', text)
            if sec_match:
                duration_min = int(sec_match.group(1)) / 60.0

        result = {
            "exercise_type": exercise_info.get("alias", [text])[0],
            "met": round(met, 1),
            "duration_min": max(duration_min, 1),
            "distance_km": distance_km,
            "category": exercise_info.get("category", "其他"),
            "intensity": intensity,
        }

        if reps is not None:
            result["reps"] = reps
        if sets is not None:
            result["sets"] = sets

        return result

    # ---- 卡路里计算 ----

    def calc_calories(self, exercise: dict, weight_kg: float = None) -> dict:
        """
        计算卡路里消耗
        公式: Calories = MET × weight(kg) × duration(hours)
        """
        if weight_kg is None:
            weight_kg = self.get_weight()
        
        duration_h = exercise["duration_min"] / 60.0
        calories = exercise["met"] * weight_kg * duration_h
        
        food_eq = get_food_equivalent(calories)
        
        return {
            "calories": round(calories, 0),
            "weight_kg": weight_kg,
            "met": exercise["met"],
            "duration_min": exercise["duration_min"],
            "duration_h": round(duration_h, 2),
            "food_equivalent": food_eq,
        }

    # ---- 日记管理 ----

    def save_exercise(self, exercise: dict, cal_result: dict, dt: date = None, note: str = ""):
        """保存运动记录"""
        if dt is None:
            dt = date.today()

        day_file = DIARY_DIR / f"{dt.isoformat()}.json"

        if day_file.exists():
            with open(day_file, "r", encoding="utf-8") as f:
                entries = json.load(f)
        else:
            entries = []

        entries.append({
            "time": datetime.now().strftime("%H:%M"),
            "exercise": exercise,
            "calories": cal_result,
            "note": note,
            "timestamp": datetime.now().isoformat(),
        })

        with open(day_file, "w", encoding="utf-8") as f:
            json.dump(entries, f, ensure_ascii=False, indent=2)

    def calc_daily(self, dt: date = None) -> dict:
        """计算某天运动总计"""
        if dt is None:
            dt = date.today()

        day_file = DIARY_DIR / f"{dt.isoformat()}.json"
        result = {
            "date": dt.isoformat(),
            "total_calories": 0,
            "total_duration_min": 0,
            "exercise_count": 0,
            "exercises": [],
            "categories": {},
        }

        if day_file.exists():
            with open(day_file, "r", encoding="utf-8") as f:
                entries = json.load(f)
                result["exercise_count"] = len(entries)
                for entry in entries:
                    cal = entry.get("calories", {})
                    ex = entry.get("exercise", {})
                    result["total_calories"] += cal.get("calories", 0)
                    result["total_duration_min"] += ex.get("duration_min", 0)
                    
                    cat = ex.get("category", "其他")
                    if cat not in result["categories"]:
                        result["categories"][cat] = 0
                    result["categories"][cat] += cal.get("calories", 0)
                    
                    result["exercises"].append({
                        "type": ex.get("exercise_type", "未知"),
                        "duration_min": ex.get("duration_min", 0),
                        "calories": cal.get("calories", 0),
                        "category": cat,
                        "time": entry.get("time", ""),
                    })

        result["total_calories"] = round(result["total_calories"], 0)
        result["total_duration_min"] = round(result["total_duration_min"], 1)
        return result

    def calc_trend(self, days: int = 7) -> dict:
        """计算多日运动趋势"""
        trend = {
            "dates": [],
            "calories": [],
            "durations": [],
            "exercise_counts": [],
            "categories": {},
        }

        for i in range(days - 1, -1, -1):
            dt = date.today() - timedelta(days=i)
            daily = self.calc_daily(dt)
            trend["dates"].append(dt.strftime("%m/%d"))
            trend["calories"].append(daily["total_calories"])
            trend["durations"].append(daily["total_duration_min"])
            trend["exercise_counts"].append(daily["exercise_count"])
            
            for cat, cal in daily["categories"].items():
                if cat not in trend["categories"]:
                    trend["categories"][cat] = [0] * days
                trend["categories"][cat][-len(trend["dates"]):] = [cal]

        return trend

    def calc_weekly_stats(self) -> dict:
        """周统计摘要"""
        trend = self.calc_trend(7)
        active_days = sum(1 for c in trend["calories"] if c > 0)
        total_cal = sum(trend["calories"])
        total_dur = sum(trend["durations"])
        avg_cal = total_cal / max(active_days, 1)
        
        # 进度评估
        guideline_target = 150  # WHO 建议每周 150 分钟中等强度
        progress_pct = min(int(total_dur / guideline_target * 100), 100)
        
        # 连续运动天数
        streak = 0
        for i in range(6, -1, -1):
            dt = date.today() - timedelta(days=i)
            if self.calc_daily(dt)["exercise_count"] > 0:
                streak += 1
            else:
                break

        return {
            "active_days": active_days,
            "total_calories": round(total_cal, 0),
            "total_duration_min": round(total_dur, 0),
            "avg_calories_per_day": round(avg_cal, 0),
            "who_progress_pct": progress_pct,
            "streak_days": streak,
            "guideline_status": "达标 ✅" if progress_pct >= 100 else f"还差 {guideline_target - int(total_dur)} 分钟",
        }

    def get_streak(self) -> int:
        """获取当前连续运动天数"""
        streak = 0
        for i in range(30):
            dt = date.today() - timedelta(days=i)
            daily = self.calc_daily(dt)
            if daily["exercise_count"] > 0:
                streak += 1
            else:
                break
        return streak
