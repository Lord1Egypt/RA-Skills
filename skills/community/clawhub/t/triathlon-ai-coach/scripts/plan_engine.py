# coding: utf-8
# plan_engine.py - 计划生成逻辑模块
# 从 trainer.py 拆分出来
# ⚠️ 本模块为 trainer.py 的拆分备份，原有函数已迁移至此

import json
import os
import subprocess
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path

CONFIG_PATH = Path(__file__).parent / "config.json"
TP_SKILL_DIR = Path(__file__).parent.parent / "trainingpeaks-skill"

# 天气相关常量
WEATHER_API = "https://wttr.in/Beijing?format=j1"
BAD_WEATHER_CODES = [200, 201, 202, 210, 211, 212, 221, 230, 231, 232,  # 雷雨
                     300, 301, 302, 310, 311, 312, 313, 314, 321,  # 毛毛雨
                     500, 501, 502, 503, 504, 511, 520, 521, 522, 531,  # 雨
                     600, 601, 602, 611, 612, 613, 615, 616, 620, 621, 622]  # 雪

# 训练类型
TRAINING_TYPES = {
    "swim": "游泳",
    "bike": "骑行", 
    "run": "跑步",
    "progression_run": "渐进式长跑",
    "brick": "骑跑两项",
    "rest": "休息"
}

INTENSITY = {
    "easy": "轻松",
    "moderate": "中等",
    "hard": "高强度",
    "race": "比赛强度"
}


def load_config():
    """加载配置"""
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def sync_trainingpeaks_data():
    """同步 TrainingPeaks 数据"""
    try:
        python_path = os.path.expanduser("~/.miniconda3/bin/python3")
        result = subprocess.run(
            [python_path, str(TP_SKILL_DIR / "scripts/tp.py"), "workouts", 
             (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d"),
             datetime.now().strftime("%Y-%m-%d"), "--json"],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            return json.loads(result.stdout)
    except Exception as e:
        print(f"TP 同步失败: {e}")
    return []


def get_fitness_status():
    """获取体能状态"""
    try:
        python_path = os.path.expanduser("~/.miniconda3/bin/python3")
        result = subprocess.run(
            [python_path, str(TP_SKILL_DIR / "scripts/tp.py"), "fitness", "--json"],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return data[-1] if data and isinstance(data, list) and len(data) > 0 else {}
    except Exception as e:
        print(f"体能状态获取失败: {e}")
    return {}


# Garmin 数据缓存（同一天内只拉一次）+ 文件持久化
import os as _os
_GARMIN_CACHE = {"date": None, "data": None}
_CACHE_FILE = _os.path.expanduser("~/.openclaw/workspace/skills/self-evolution/scripts/.garmin_health_cache.json")

def _load_cache():
    """从文件加载缓存（进程重启后依然有效）"""
    try:
        if _os.path.exists(_CACHE_FILE):
            with open(_CACHE_FILE) as f:
                return json.loads(f.read())
    except:
        pass
    return {"date": None, "data": None}

def _save_cache(date, data):
    """保存缓存到文件"""
    try:
        with open(_CACHE_FILE, "w") as f:
            json.dump({"date": date, "data": data}, f)
    except:
        pass

def get_garmin_health():
    """获取 Garmin 健康数据（睡眠/压力/训练准备度）
    - 同一天内缓存结果
    - 支持进程重启后从文件恢复缓存
    - 永远不主动重新登录（避免 429）
    """
    import datetime as _dt

    today = _dt.date.today().isoformat()

    # 优先用内存缓存
    if _GARMIN_CACHE["date"] == today and _GARMIN_CACHE["data"]:
        return _GARMIN_CACHE["data"]

    # 尝试从文件恢复
    file_cache = _load_cache()
    if file_cache.get("date") == today and file_cache.get("data"):
        _GARMIN_CACHE["date"] = today
        _GARMIN_CACHE["data"] = file_cache["data"]
        return _GARMIN_CACHE["data"]

    # 文件缓存也不可用，返回空（不尝试登录）
    return {}


def get_garmin_health_fetch():
    """真正获取 Garmin 数据（仅当确认 token 有效时调用）"""
    import datetime as _dt
    import garminconnect

    TOKEN = "/tmp/garmin_test_token"
    config = _json.loads(Path("user_config.json").read_text()) if Path("user_config.json").exists() else {}
    garmin_email = config.get("garmin_email", os.environ.get("GARMIN_EMAIL", ""))
    garmin_pass = config.get("garmin_password", os.environ.get("GARMIN_PASSWORD", ""))
    if not garmin_email or not garmin_pass:
        raise ValueError("请在 user_config.json 中设置 garmin_email/garmin_password 或设置环境变量 GARMIN_EMAIL/GARMIN_PASSWORD")
    client = garminconnect.Garmin(garmin_email, garmin_pass, is_cn=False)
    client.garth.load(TOKEN)
    today = _dt.date.today().isoformat()

    sleep_data = client.get_sleep_data(today)
    dto = sleep_data.get("dailySleepDTO", {})
    scores = dto.get("sleepScores", {})
    overall = scores.get("overall", {})
    total_s = dto.get("sleepTimeSeconds") or 0
    deep_s = dto.get("deepSleepSeconds") or 0
    rem_s = dto.get("remSleepSeconds") or 0

    readiness_list = client.get_training_readiness(today)
    readiness_data = readiness_list[0] if readiness_list else {}
    hrv = readiness_data.get("hrvWeeklyAverage") or 0
    hrv_feedback = readiness_data.get("hrvFactorFeedback") or ""

    stress_data = client.get_stress_data(today)
    avg_stress = stress_data.get("avgStressLevel") or 0

    result = {
        "sleep_score": str(overall.get("value", 0)),
        "sleep_hours": f"{total_s // 3600}h{(total_s % 3600) // 60}m",
        "deep_sleep": f"{deep_s // 3600}h{deep_s % 3600 // 60}m",
        "rem_sleep": f"{rem_s // 3600}h{rem_s % 3600 // 60}m",
        "readiness_score": str(readiness_data.get("score", 0)),
        "readiness_level": readiness_data.get("level", "N/A"),
        "hrv": f"{hrv} ms（{hrv_feedback}）",
        "avg_stress": float(avg_stress or 0),
    }

    _GARMIN_CACHE["date"] = today
    _GARMIN_CACHE["data"] = result
    _save_cache(today, result)
    return result


def get_weather():
    """获取当地天气"""
    try:
        req = urllib.request.Request(WEATHER_API)
        req.add_header('User-Agent', 'curl')
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            current = data.get('current_condition', [{}])[0]
            weather_data = data.get('weather', [{}])[0]
            
            return {
                "temp": int(current.get('temp_C', 20)),
                "feels_like": int(current.get('FeelsLikeC', 20)),
                "humidity": int(current.get('humidity', 50)),
                "weather_code": int(current.get('weatherCode', 113)),
                "weather_desc": current.get('weatherDesc', [{}])[0].get('value', '未知'),
                "visibility": int(current.get('visibility', 10)),
                "wind_speed": int(current.get('windspeedKmph', 0)),
                "chance_of_rain": int(weather_data.get('hourly', [{}])[0].get('chanceofrain', 0)) if weather_data.get('hourly') else 0,
                "sunrise": weather_data.get('astronomy', [{}])[0].get('sunrise', '06:00') if weather_data.get('astronomy') else '06:00',
                "sunset": weather_data.get('astronomy', [{}])[0].get('sunset', '18:00') if weather_data.get('astronomy') else '18:00'
            }
    except Exception as e:
        print(f"获取天气失败: {e}")
        return None


def is_bad_weather(weather):
    """判断是否恶劣天气"""
    if not weather:
        return False, "天气未知"
    
    code = weather.get('weather_code', 113)
    visibility = weather.get('visibility', 10)
    humidity = weather.get('humidity', 50)
    temp = weather.get('temp', 20)
    
    reasons = []
    
    # 下雨/下雪
    if code in BAD_WEATHER_CODES:
        reasons.append("降水")
    
    # 雾霾（能见度<5km且湿度>70%）
    if visibility < 5 and humidity > 70:
        reasons.append("雾霾")
    
    # 极端温度
    if temp < -5:
        reasons.append("极寒")
    if temp > 35:
        reasons.append("高温")
    
    if reasons:
        return True, "、".join(reasons)
    return False, ""


def adjust_for_weather(session, weather):
    """根据天气调整训练"""
    if not weather:
        return session, None
    
    is_bad, reason = is_bad_weather(weather)
    
    if not is_bad:
        return session, None
    
    # 根据原始训练类型调整
    original_type = session.get('type', '')
    adjusted = session.copy()
    adjustment_note = f"⚠️ 天气调整（{reason}）："
    
    if original_type == 'run':
        # 室外跑步 → 室内跑步机
        adjusted['type'] = 'treadmill'
        adjusted['focus'] = '跑步机训练'
        adjusted['detail'] = f"室内跑步机替代：{session.get('detail', '')}"
        adjustment_note += "室外跑步→跑步机"
    
    elif original_type == 'bike':
        # 室外骑行 → 骑行台
        adjusted['type'] = 'trainer'
        adjusted['focus'] = '骑行台训练'
        adjusted['detail'] = f"室内骑行台替代：{session.get('detail', '')}"
        adjustment_note += "室外骑行→骑行台"
    
    elif original_type == 'progression_run':
        # 渐进式长跑 → 室内调整
        adjusted['type'] = 'treadmill'
        adjusted['focus'] = '跑步机渐进跑'
        adjusted['detail'] = f"室内跑步机替代：{session.get('detail', '')}"
        adjustment_note += "室外跑步→跑步机"
    
    elif original_type == 'brick':
        # 骑跑两项 → 全室内
        adjusted['detail'] = f"骑行台 + 跑步机：{session.get('detail', '')}"
        adjustment_note += "室外→室内训练"
    
    # 游泳不受天气影响
    elif original_type == 'swim':
        adjustment_note = None  # 游泳不需要调整
    
    else:
        adjustment_note = None
    
    return adjusted, adjustment_note


def analyze_recent_training(workouts):
    """分析最近训练状态"""
    if not workouts:
        return None
    
    # 最近7天统计
    now = datetime.now()
    week_ago = now - timedelta(days=7)
    
    recent = [w for w in workouts if datetime.strptime(w.get('workoutDay', '1970-01-01')[:10], '%Y-%m-%d') >= week_ago]
    
    stats = {
        "total_workouts": len(recent),
        "swim_count": 0,
        "bike_count": 0,
        "run_count": 0,
        "total_duration": 0,
        "total_tss": 0
    }
    
    for w in recent:
        tags = (w.get('userTags', '') or '').lower()
        sport = (w.get('sport', '') or '').lower()
        stats["total_duration"] += w.get('totalTime', 0) or 0
        stats["total_tss"] += w.get('tssActual', 0) or 0
        
        if 'swim' in tags or 'swim' in sport:
            stats["swim_count"] += 1
        elif 'bike' in tags or 'cycl' in tags or 'bike' in sport or 'cycl' in sport:
            stats["bike_count"] += 1
        elif 'run' in tags or 'run' in sport:
            stats["run_count"] += 1
    
    return stats


def get_days_until_race(race_date):
    """计算距离比赛的天数"""
    today = datetime.now().date()
    race = datetime.strptime(race_date, "%Y-%m-%d").date()
    return (race - today).days


def format_pace(seconds_per_km):
    """格式化配速"""
    mins = int(seconds_per_km // 60)
    secs = int(seconds_per_km % 60)
    return f"{mins}:{secs:02d}"


def get_training_zones(config):
    """计算训练区间"""
    half_marathon_seconds = 100 * 60
    half_marathon_pace = half_marathon_seconds / 21
    max_hr = 172  # 220-48
    
    return {
        "run": {
            "zone1_pace": format_pace(half_marathon_pace * 1.35),
            "zone2_pace": format_pace(half_marathon_pace * 1.15),
            "zone3_pace": format_pace(half_marathon_pace),
            "zone1_hr": int(max_hr * 0.60),
            "zone2_hr": int(max_hr * 0.75),
            "zone3_hr": int(max_hr * 0.88),
        },
        "swim": {"easy_pace": "2:10", "moderate_pace": "1:55", "hard_pace": "1:50"},
        "bike": {"easy_watts": 162, "moderate_watts": 200, "hard_watts": 237}
    }


def generate_weekly_plan(config, fitness=None, recent_stats=None):
    """生成一周训练计划"""
    races = config['training']['races']
    zones = get_training_zones(config)
    
    upcoming_races = [r for r in races if get_days_until_race(r['date']) > 0]
    
    # 根据体能状态调整
    ctl = fitness.get('ctl', 15) if fitness else 15
    tsb = fitness.get('tsb', 0) if fitness else 0
    
    # 如果 TSB < -15，说明疲劳积累，需要减量
    recovery_mode = tsb < -15
    
    if not upcoming_races:
        weekly_plan = {
            "focus": "基础耐力 + 渐进式长跑",
            "schedule": [
                {"day": 1, "type": "swim", "focus": "技术训练", "duration": 1.5, "intensity": "easy", "detail": "2000m轻松游"},
                {"day": 2, "type": "progression_run", "focus": "渐进式长跑", "duration": 1.5, "intensity": "moderate", "detail": "初级版：20min Zone1 → 20min Zone2 → 20min Zone3", "zones": "初级"},
                {"day": 3, "type": "bike", "focus": "耐力骑行", "duration": 2.0, "intensity": "easy", "detail": "50km有氧骑行"},
                {"day": 4, "type": "rest", "focus": "休息", "duration": 0, "intensity": "rest", "detail": "休息或拉伸"},
                {"day": 5, "type": "swim", "focus": "间歇训练", "duration": 1.5, "intensity": "hard", "detail": "10x200m间歇"},
                {"day": 6, "type": "progression_run", "focus": "渐进式长跑", "duration": 2.0, "intensity": "moderate", "detail": "中级版：25min Zone1 → 25min Zone2 → 25min Zone3", "zones": "中级"},
                {"day": 7, "type": "bike", "focus": "FTP训练", "duration": 2.0, "intensity": "hard", "detail": "4x15min阈值训练"},
            ]
        }
    else:
        next_race = min(upcoming_races, key=lambda x: get_days_until_race(x['date']))
        days_left = get_days_until_race(next_race['date'])
        
        if days_left < 30:
            weekly_plan = {
                "focus": f"赛前减量 - {next_race['name']} ({days_left}天)",
                "schedule": [
                    {"day": 1, "type": "swim", "focus": "放松游", "duration": 1.0, "intensity": "easy", "detail": "1500m放松游"},
                    {"day": 2, "type": "progression_run", "focus": "马拉松配速", "duration": 1.0, "intensity": "moderate", "detail": "15min Zone1 → 15min Zone2 → 15min Zone3", "zones": "赛前"},
                    {"day": 3, "type": "rest", "focus": "休息", "duration": 0, "intensity": "rest", "detail": "休息"},
                    {"day": 4, "type": "swim", "focus": "比赛配速", "duration": 0.8, "intensity": "race", "detail": f"{next_race.get('swim_distance', 2000)}m"},
                    {"day": 5, "type": "bike", "focus": "放松骑", "duration": 1.0, "intensity": "easy", "detail": "30km放松骑"},
                    {"day": 6, "type": "run", "focus": "比赛配速", "duration": 0.8, "intensity": "race", "detail": f"{next_race.get('run_distance', 10)}km"},
                    {"day": 7, "type": "rest", "focus": "休息", "duration": 0, "intensity": "rest", "detail": "休息"},
                ]
            }
        else:
            weekly_plan = {
                "focus": f"赛前冲刺 - {next_race['name']} ({days_left}天)",
                "schedule": [
                    {"day": 1, "type": "swim", "focus": "间歇训练", "duration": 1.5, "intensity": "hard", "detail": "12x150m间歇"},
                    {"day": 2, "type": "progression_run", "focus": "渐进式长跑", "duration": 1.5, "intensity": "hard", "detail": "高级版：30min Zone1 → 30min Zone2 → 30min Zone3", "zones": "高级"},
                    {"day": 3, "type": "rest", "focus": "休息", "duration": 0, "intensity": "rest", "detail": "休息"},
                    {"day": 4, "type": "bike", "focus": "阈值训练", "duration": 1.5, "intensity": "hard", "detail": "3x20min阈值"},
                    {"day": 5, "type": "swim", "focus": "长距离游", "duration": 1.5, "intensity": "moderate", "detail": "2500m有氧游"},
                    {"day": 6, "type": "brick", "focus": "骑跑两项", "duration": 2.5, "intensity": "moderate", "detail": "骑60km + 跑8km"},
                    {"day": 7, "type": "progression_run", "focus": "渐进式长跑", "duration": 1.8, "intensity": "moderate", "detail": "中级版", "zones": "中级"},
                ]
            }
    
    # 如果疲劳度高，增加休息
    if recovery_mode:
        for i, s in enumerate(weekly_plan["schedule"]):
            if s["type"] != "rest" and s["intensity"] == "hard":
                weekly_plan["schedule"][i] = {"day": s["day"], "type": "rest", "focus": "恢复休息", "duration": 0, "intensity": "rest", "detail": "疲劳恢复"}
                break
    
    return weekly_plan


def get_daily_plan(config, date=None):
    """生成指定日期的训练计划"""
    # 先同步数据
    workouts = sync_trainingpeaks_data()
    fitness = get_fitness_status()
    garmin_health = get_garmin_health()
    recent_stats = analyze_recent_training(workouts)
    weather = get_weather()
    
    # 根据 Garmin 健康数据调整训练强度
    garmin_adjustment = None
    if garmin_health:
        ready = garmin_health.get("readiness_score", "50")
        try:
            ready_val = int(ready)
            if ready_val < 30:
                garmin_adjustment = "garmin_low_readiness"
            elif ready_val < 50:
                garmin_adjustment = "garmin_moderate_readiness"
        except:
            pass
    
    if date is None:
        date = datetime.now().date()
    
    weekday = date.weekday()
    weekly = generate_weekly_plan(config, fitness, recent_stats)
    
    for session in weekly['schedule']:
        if session['day'] == weekday + 1:
            # 根据 Garmin 健康数据调整训练
            adjusted_session = session.copy()
            garmin_note = None
            if garmin_adjustment == "garmin_low_readiness":
                adjusted_session = {"day": session['day'], "type": "rest", "focus": "Garmin建议休息", "duration": 0, "intensity": "rest", "detail": "训练准备度过低（Garmin建议休息）"}
                garmin_note = "⚠️ Garmin训练准备度过低，自动调整为休息"
            elif garmin_adjustment == "garmin_moderate_readiness":
                if session.get("intensity") == "hard":
                    adjusted_session["intensity"] = "moderate"
                    adjusted_session["detail"] = session.get("detail", "") + "（强度下调：准备度不足）"
                    garmin_note = "⚠️ Garmin准备度偏低，高强度训练降为中等"
            # 根据天气调整训练
            adjusted_session, weather_note = adjust_for_weather(adjusted_session, weather)
            return {
                "date": date.strftime("%Y-%m-%d"),
                "weekday": ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][weekday],
                "focus": weekly['focus'],
                "session": adjusted_session,
                "fitness": fitness,
                "garmin_health": garmin_health,
                "garmin_adjustment": garmin_adjustment,
                "garmin_note": garmin_note,
                "recent_stats": recent_stats,
                "weather": weather,
                "weather_adjustment": weather_note
            }
    
    return {
        "date": date.strftime("%Y-%m-%d"),
        "weekday": ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][weekday],
        "focus": weekly['focus'],
        "session": {"day": weekday+1, "type": "rest", "focus": "休息", "duration": 0, "intensity": "rest", "detail": "休息"},
        "fitness": fitness,
        "garmin_health": garmin_health,
        "garmin_adjustment": garmin_adjustment,
        "garmin_note": None,
        "recent_stats": recent_stats,
        "weather": weather,
        "weather_adjustment": None
    }


# ── 教练理念和用户偏好 ──────────────────────────────────────────────

def get_coach_principles():
    """返回关键教练理念（用于计划说明）"""
    return {
        "joe_friel": {
            "name": "Joe Friel",
            "quote": "80% 低强度训练，20% 高强度训练",
            "application": "确保大多数训练是有氧 Zone 2，间歇训练不超过总量 20%"
        },
        "brett_sutton": {
            "name": "Brett Sutton",
            "quote": "有氧基础上发展速度",
            "application": "先打好游泳有氧耐力，再加速度和乳酸阈值训练"
        },
        "mark_allen": {
            "name": "Mark Allen",
            "quote": "比赛中 50% 是心理，50% 是身体",
            "application": "训练中穿插心理建设，穿泳裤跑等比赛模拟"
        },
        "joe_filliol": {
            "name": "Joe Filliol",
            "quote": "体能 > 技术（铁三游泳）",
            "application": "游泳以长距离有氧为主，技术练习穿插而非单独大段时间"
        }
    }

def get_user_preferences():
    """读取用户训练偏好（来自 feedback_manager）"""
    try:
        import sys, os
        sys.path.insert(0, str(os.path.dirname(__file__)))
        from feedback_manager import get_session_type_preference, get_preferences
        prefs = get_preferences()
        return {
            "satisfaction_rate": prefs.get("satisfaction_rate", 0),
            "session_likes": {
                "swim": get_session_type_preference("swim"),
                "bike": get_session_type_preference("bike"),
                "run": get_session_type_preference("run"),
                "rest": get_session_type_preference("rest"),
            }
        }
    except:
        return {"satisfaction_rate": 0, "session_likes": {}}

def get_coach_tip_for_plan(daily_plan):
    """根据当前状态，给出一条教练建议"""
    import datetime as dt
    
    # 获取状态
    fitness = daily_plan.get("fitness", {})
    garmin = daily_plan.get("garmin_health", {})
    session = daily_plan.get("session", {})
    recent_stats = daily_plan.get("recent_stats", {})
    
    tsb = float(fitness.get("tsb", 0) or 0)
    ready = float(garmin.get("readiness_score", 50) or 50)
    sleep_score = float(garmin.get("sleep_score", 50) or 50)
    week_tss = float(recent_stats.get("total_tss", 0) or 0)
    session_type = session.get("type", "")
    
    principles = get_coach_principles()
    tips = []
    
    # TSB 建议
    if tsb < -30:
        tips.append(f"【Joe Friel】TSB {tsb:.0f} = 极度疲劳，优先恢复，不要追训练量")
    elif tsb < -15:
        tips.append(f"【Joe Friel】TSB {tsb:.0f} = 疲劳积累，减少高强度，保持轻松有氧")
    elif tsb > 15:
        tips.append(f"【Joe Friel】TSB {tsb:.0f} = 状态超量，可以挑战更高强度")
    else:
        tips.append(f"【Joe Friel】TSB {tsb:.0f} = 状态平衡，维持现有训练节奏")
    
    # Garmin 建议
    if ready < 30:
        tips.append(f"【Mark Allen】Garmin准备度 {ready:.0f} = 身体未恢复，今天完全休息最佳")
    elif sleep_score < 50:
        tips.append(f"【Joe Filliol】睡眠评分 {sleep_score:.0f} = 睡眠不足，训练强度保守一点")
    else:
        tips.append(f"【Brett Sutton】身体状态良好，按计划执行，有氧为基础")
    
    # 本周训练量
    if week_tss > 500:
        tips.append(f"【Joe Friel】本周 TSS {week_tss:.0f} = 训练量大，注意恢复")
    elif week_tss < 200:
        tips.append(f"【Brett Sutton】本周 TSS {week_tss:.0f} = 训练量偏低，适当增加")
    
    # 加入学习到的个性化建议（优先级最高）
    from feedback_manager import get_learned_coach_tip
    learned_tip = get_learned_coach_tip()
    if learned_tip:
        tips.insert(0, learned_tip)

    return tips if tips else []
