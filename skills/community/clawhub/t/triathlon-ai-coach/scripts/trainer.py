# ⚠️ DEPRECATED MODULE
# 本文件已拆分为三个模块：
#   - plan_engine.py  : 计划生成逻辑
#   - formatter.py     : 格式化输出
#   - notifier.py      : 推送
# 请优先使用以上三个模块，本文件仅作向后兼容保留。
#
# 建议迁移：from plan_engine import get_daily_plan, generate_weekly_plan
#
# ─────────────────────────────────────────────────────────────
#!/usr/bin/env python3
"""
AI 智能训练教练 - 核心引擎 v4
整合 TrainingPeaks 数据同步
"""

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


# Garmin 数据缓存（同一天内只拉一次）
_GARMIN_CACHE = {"date": None, "data": None}

def get_garmin_health():
    """获取 Garmin 健康数据（睡眠/压力/训练准备度）
    同一天内缓存结果，避免重复调用 API
    """
    import datetime as _dt

    today = _dt.date.today().isoformat()
    if _GARMIN_CACHE["date"] == today and _GARMIN_CACHE["data"]:
        return _GARMIN_CACHE["data"]

    try:
        import garminconnect

        TOKEN_DIR = os.path.expanduser("~/.garmin_tokens")
        config = load_config()
        garmin_email = config.get("garmin_email", os.environ.get("GARMIN_EMAIL", ""))
        garmin_pass = config.get("garmin_password", os.environ.get("GARMIN_PASSWORD", ""))
        if not garmin_email or not garmin_pass:
            raise ValueError("请在 user_config.json 中设置 garmin_email/garmin_password 或设置环境变量 GARMIN_EMAIL/GARMIN_PASSWORD")
        client = garminconnect.Garmin(
            garmin_email, garmin_pass, is_cn=False
        )
        client.garth.load(TOKEN_DIR)

        # 睡眠
        sleep_data = client.get_sleep_data(today)
        dto = sleep_data.get("dailySleepDTO", {})
        scores = dto.get("sleepScores", {})
        overall = scores.get("overall", {})
        total_s = dto.get("sleepTimeSeconds", 0)
        deep_s = dto.get("deepSleepSeconds", 0)
        rem_s = dto.get("remSleepSeconds", 0)

        # 训练准备度
        readiness_list = client.get_training_readiness(today)
        readiness_data = readiness_list[0] if readiness_list else {}
        hrv = readiness_data.get("hrvWeeklyAverage", 0)
        hrv_feedback = readiness_data.get("hrvFactorFeedback", "")

        # 压力
        stress_data = client.get_stress_data(today)
        avg_stress = stress_data.get("avgStressLevel", 0)

        result = {
            "sleep_score": str(overall.get("value", 0)),
            "sleep_hours": f"{total_s // 3600}h{(total_s % 3600) // 60}m",
            "deep_sleep": f"{deep_s // 3600}h{deep_s % 3600 // 60}m",
            "rem_sleep": f"{rem_s // 3600}h{rem_s % 3600 // 60}m",
            "readiness_score": str(readiness_data.get("score", 0)),
            "readiness_level": readiness_data.get("level", "N/A"),
            "hrv": f"{hrv} ms（{hrv_feedback}）",
            "avg_stress": float(avg_stress),
        }

        _GARMIN_CACHE["date"] = today
        _GARMIN_CACHE["data"] = result
        return result

    except Exception as e:
        print(f"Garmin健康数据获取失败: {e}")
        # 如果有缓存，即使过期也返回（容错）
        if _GARMIN_CACHE["data"]:
            return _GARMIN_CACHE["data"]
        return {}


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


def format_daily_plan(plan):
    """格式化训练计划"""
    config = load_config()
    zones = get_training_zones(config)
    session = plan['session']
    fitness = plan.get('fitness', {})
    recent = plan.get('recent_stats', {})
    weather = plan.get('weather', {})
    weather_adjustment = plan.get('weather_adjustment')
    
    # 加载游泳法则（2026版）
    try:
        from swimming_rules import RULES_2026, get_all_rules, get_critical_rules, PHILOSOPHY_EVOLUTION
        has_swimming_rules = True
    except:
        has_swimming_rules = False
    
    content = f"""📅 **{plan['weekday']} {plan['date']}**

🎯 **本期主题：** {plan['focus']}
"""
    
    # 天气信息
    if weather:
        temp = weather.get('temp', '?')
        feels = weather.get('feels_like', temp)
        desc = weather.get('weather_desc', '未知')
        humidity = weather.get('humidity', '?')
        wind = weather.get('wind_speed', 0)
        sunrise = weather.get('sunrise', '?')
        sunset = weather.get('sunset', '?')
        
        # 天气图标
        weather_icon = "☀️"
        code = weather.get('weather_code', 113)
        if code in [200, 201, 202, 210, 211, 212, 221, 230, 231, 232]:
            weather_icon = "⛈️"
        elif code in [300, 301, 302, 310, 311, 312, 313, 314, 321, 500, 501, 502, 503, 504, 511, 520, 521, 522, 531]:
            weather_icon = "🌧️"
        elif code in [600, 601, 602, 611, 612, 613, 615, 616, 620, 621, 622]:
            weather_icon = "❄️"
        elif code in [116, 119, 122]:
            weather_icon = "☁️"
        
        content += f"""
{weather_icon} **天气：** {desc} | {temp}°C（体感{feels}°C）
🌬️ **风力：** {wind}km/h | 💧 **湿度：** {humidity}%
🌅 **日出/日落：** {sunrise} / {sunset}
"""
        
        # 天气调整提示
        if weather_adjustment:
            content += f"""
{weather_adjustment}
"""
    
    # 体能状态
    if fitness:
        ctl_val = float(fitness.get('ctl', 0) or 0)
        tsb_val = float(fitness.get('tsb', 0) or 0)
        status = "疲劳积累" if tsb_val < -10 else "状态良好"
        content += f"""
📊 **体能状态：** CTL {ctl_val:.1f} | TSB {tsb_val:.1f} | {status}
"""
    
    # Garmin 健康数据
    garmin_health = plan.get('garmin_health', {})
    garmin_note = plan.get('garmin_note')
    if garmin_health:
        sleep_score = garmin_health.get('sleep_score', '-')
        sleep_hours = garmin_health.get('sleep_hours', '-')
        readiness = garmin_health.get('readiness_score', '-')
        readiness_level = garmin_health.get('readiness_level', '-')
        hrv = garmin_health.get('hrv', '-')
        avg_stress = garmin_health.get('avg_stress', '-')
        emoji = "LOW" if isinstance(readiness, str) and int(readiness or 0) < 40 else ("NORMAL" if isinstance(readiness, str) and int(readiness or 0) < 60 else "GOOD")
        content += f"""
💓 **Garmin健康：** 睡眠 {sleep_score}/100（{sleep_hours}）| 准备度 {emoji} {readiness}/100（{readiness_level}）| HRV {hrv} | 压力 {avg_stress}
"""
    
    # Garmin 调整说明
    if garmin_note:
        content += f"\n{garmin_note}\n"
    
    # 最近训练
    if recent:
        content += f"""📈 **本周训练：** {recent['total_workouts']}次 | 游{recent['swim_count']}骑{recent['bike_count']}跑{recent['run_count']}
"""
    
    content += f"""
{'='*25}
"""
    
    # 根据训练类型显示不同内容
    session_type = session['type']
    
    if session_type == 'rest':
        content += f"""
🏖️ **休息日**

📝 {session.get('detail', '完全休息')}

💡 建议：充足睡眠，可做全身拉伸/瑜伽

"""
    elif session_type == 'swim':
        # 游泳训练融入技术法则
        # Joe Filliol 2026 更新版：体能至上，技术是体能支撑下的自然产物
        content += f"""
🏊 **游泳训练** - {session['focus']}

⏱️ 时长：约 {session['duration']} 小时
📝 {session.get('detail', '')}

"""
        
        # Joe Filliol 2026 核心原则
        content += f"""
🏊 **Joe Filliol 2026 游泳原则**

**核心理念：体能 > 技术**
> "给我一个有体能没技术的运动员，我能让他游得很快；
> 给我一个技术完美但体能不足的，他在铁三比赛中会崩溃。"

**训练原则：**
• **体能是基础** - 胶衣提供浮力，体能更关键
• **频次 > 单次时长** - 更频繁地游
• **长距离主菜** - 短距离≥2km，大铁≥4km
• **短间歇保质量** - 如 50×50m，积累更多"好划"
• **别过度思考** - 过度分析会让技术变差
• **重复是朋友** - 变化干扰学习

"""
        
        # 技术要点（简化版）
        content += f"""
**技术要点（简化）：**

**绑脚练习** ⭐
- 最好的练习，从短距离开始（25m）
- 让身体自己找到正确位置

**划手掌** 
- 感受背阔肌发力（主要动力肌）
- 保持腋下打开

**呼吸**
- 头低一点，抬头腿就沉
- 快速吸气，充分呼气

**踢腿**
- 只关乎身体位置，不是推进
- 别花太多时间练踢腿

**划频**
- 别数划次，目标是更快
- 学会高划频（人群和风浪中有用）

"""
        
        # 特别提醒
        content += f"""
**💡 Joe Filliol 提醒：**
• 每次游泳都要有质量（即使轻松游也加技术刺激）
• 累了就用工具（保持技术质量）
• 课表要简单（能记住才是好课表）
• 游泳体能会转化到骑跑（铁三是一个运动）
• 爱上游泳 — 耐心、坚持

**2026 更新：** 所有规则验证有效，体能是核心，简化技术细节

"""
        
    elif session_type == 'progression_run' or session_type == 'treadmill':
        zone_level = session.get('zones', '初级')
        is_indoor = session_type == 'treadmill'
        title = "跑步机渐进跑" if is_indoor else f"渐进式长跑 - {zone_level}版"
        
        content += f"""
🏃 **{title}**

⏱️ 时长：约 {session['duration']} 小时
📝 {session.get('detail', '')}

📊 **三区训练法：**

**Zone 1** | {zones['run']['zone1_pace']}/km | 体感 1/10
**Zone 2** | {zones['run']['zone2_pace']}/km | 体感 2-3/10
**Zone 3** | {zones['run']['zone3_pace']}/km | 体感 5-7/10

💡 以身体感受为主，不依赖手表！

"""
    elif session_type == 'bike' or session_type == 'trainer':
        is_indoor = session_type == 'trainer'
        title = "骑行台训练" if is_indoor else f"骑行 - {session['focus']}"
        
        content += f"""
🚴 **{title}**

⏱️ 时长：约 {session['duration']} 小时
📝 {session.get('detail', '')}

💡 FTP训练：保持目标功率稳定输出

"""
    elif session_type == 'run':
        content += f"""
🏃 **跑步** - {session['focus']}

⏱️ 时长：约 {session['duration']} 小时
📝 {session.get('detail', '')}

"""
    elif session_type == 'brick':
        content += f"""
🔄 **骑跑两项 (Bricks)**

⏱️ 时长：约 {session['duration']} 小时
📝 {session.get('detail', '')}

💡 先骑后跑，模拟比赛转换

"""
    
    content += """
---
💡 提示：训练前热身10分钟，结束后拉伸放松

"""
    
    return content


def log_daily_plan(date, plan_type, session):
    """记录每天的计划
    plan_type: 'scheduled'(定时推送) / 'temp'(临时) / 'extra'(额外加练)
    """
    log_path = Path(__file__).parent / "daily_plans.json"
    
    if log_path.exists():
        with open(log_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = {"daily_plans": {}}
    
    date_str = date.isoformat() if hasattr(date, 'isoformat') else str(date)
    
    if date_str not in data["daily_plans"]:
        data["daily_plans"][date_str] = {
            "scheduled": [],
            "temp": [],
            "extra": []
        }
    
    # 添加计划
    session_with_type = session.copy() if isinstance(session, dict) else session
    if isinstance(session_with_type, dict):
        session_with_type['plan_type'] = plan_type
        session_with_type['logged_at'] = datetime.now().isoformat()
    
    data["daily_plans"][date_str][plan_type].append(session_with_type)
    
    with open(log_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_today_all_plans():
    """获取今天的所有计划（三个维度）"""
    log_path = Path(__file__).parent / "daily_plans.json"
    today_str = datetime.now().date().isoformat()
    
    if log_path.exists():
        with open(log_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            plans = data.get("daily_plans", {}).get(today_str, {})
            return {
                "scheduled": plans.get("scheduled", []),
                "temp": plans.get("temp", []),
                "extra": plans.get("extra", [])
            }
    
    return {"scheduled": [], "temp": [], "extra": []}


def get_tp_today_workout():
    """从 TrainingPeaks 获取今天的训练"""
    workouts = sync_trainingpeaks_data()
    today = datetime.now().date().isoformat()
    
    # 返回今天的所有训练（可能有多个）
    today_workouts = [w for w in workouts if w.get('workoutDay', '')[:10] == today]
    return today_workouts if today_workouts else None


def analyze_today_training(planned_sessions, actual_tp_list):
    """分析今天的训练完成情况（支持多个计划）"""
    review = {
        "planned": planned_sessions,
        "actual": actual_tp_list,
        "completion_status": {},
        "highlights": [],
        "issues": [],
        "gains": [],
        "advice": []
    }
    
    if not actual_tp_list:
        review["issues"].append("今天没有训练记录")
        return review
    
    # 计算实际训练统计
    total_distance = 0
    total_time = 0
    total_tss = 0
    swim_distance = 0
    bike_distance = 0
    run_distance = 0
    avg_hr = 0
    hr_count = 0
    
    for w in actual_tp_list:
        distance = w.get('distance', 0) / 1000
        time = w.get('totalTime', 0)
        title = w.get('title', '').lower()
        hr = w.get('heartRateAverage', 0)
        tss = w.get('tssActual', 0) or w.get('tss', 0)
        
        total_distance += distance
        total_time += time
        total_tss += tss
        
        if hr:
            avg_hr += hr
            hr_count += 1
        
        # 根据 title 判断运动类型
        if 'swim' in title:
            swim_distance += distance
        elif 'bike' in title or 'cycl' in title or 'road' in title:
            bike_distance += distance
        elif 'run' in title:
            run_distance += distance
    
    if hr_count > 0:
        avg_hr = avg_hr / hr_count
    
    # 对比计划
    for plan in planned_sessions:
        plan_type = plan.get('type', '')
        plan_focus = plan.get('focus', '')
        plan_duration = plan.get('duration', 0)
        
        # 检查是否完成
        if plan_type == 'swim':
            if swim_distance > 0:
                review["completion_status"][plan_focus] = "✅ 完成"
            else:
                review["completion_status"][plan_focus] = "❌ 未完成"
                review["issues"].append(f"游泳计划未完成")
        
        elif plan_type == 'bike':
            if bike_distance > 0:
                review["completion_status"][plan_focus] = "✅ 完成"
            else:
                review["completion_status"][plan_focus] = "❌ 未完成"
                review["issues"].append(f"骑行计划未完成")
        
        elif plan_type == 'run' or plan_type == 'progression_run':
            if run_distance > 0:
                review["completion_status"][plan_focus] = "✅ 完成"
            else:
                review["completion_status"][plan_focus] = "❌ 未完成"
                review["issues"].append(f"跑步计划未完成")
        
        elif plan_type == 'rest':
            review["completion_status"][plan_focus] = "✅ 休息"
    
    # 总体统计
    review["highlights"].append(f"📊 **今日总计：**")
    review["highlights"].append(f"总距离: {total_distance:.1f}km")
    review["highlights"].append(f"总时长: {total_time:.2f}h ({int(total_time*60)}分钟)")
    if avg_hr:
        review["highlights"].append(f"平均心率: {int(avg_hr)}bpm")
    if total_tss:
        review["highlights"].append(f"TSS: {int(total_tss)}")
    
    # 计算实际消耗的能量
    from nutrition_manager import NutritionManager
    nm = NutritionManager()
    total_calories = 0
    for w in actual_tp_list:
        title = w.get('title', '').lower()
        time = w.get('totalTime', 0)
        hr = w.get('heartRateAverage', 0)
        
        # 判断训练类型
        if 'swim' in title:
            training_type = 'swim'
        elif 'bike' in title or 'cycl' in title or 'road' in title:
            training_type = 'bike'
        elif 'run' in title:
            training_type = 'run'
        else:
            training_type = 'bike'
        
        calories = nm.calculate_training_calories(training_type, time, 'moderate', hr)
        total_calories += calories
    
    if total_calories > 0:
        review["highlights"].append(f"🔥 能量消耗: {total_calories} kcal")
    
    # 分项统计
    if swim_distance > 0:
        review["highlights"].append(f"🏊 游泳: {swim_distance:.1f}km")
    if bike_distance > 0:
        review["highlights"].append(f"🚴 骑行: {bike_distance:.1f}km")
    if run_distance > 0:
        review["highlights"].append(f"🏃 跑步: {run_distance:.1f}km")
    
    # 生成建议
    if not review["issues"]:
        review["advice"].append("💪 今天训练完成很好，保持这个节奏！")
    else:
        if len(review["issues"]) == 1:
            review["advice"].append("🔄 注意调整，明天补上未完成的训练")
        else:
            review["advice"].append("⚠️ 多个计划未完成，注意恢复")
    
    # 检查是否有额外训练
    planned_types = [p.get('type', '') for p in planned_sessions]
    actual_types = set()
    for w in actual_tp_list:
        title = w.get('title', '').lower()
        if 'swim' in title:
            actual_types.add('swim')
        elif 'bike' in title or 'cycl' in title or 'road' in title:
            actual_types.add('bike')
        elif 'run' in title:
            actual_types.add('run')
    
    extra_types = actual_types - set(planned_types)
    if extra_types:
        extra_str = []
        if 'swim' in extra_types and swim_distance > 0:
            extra_str.append(f"游泳 {swim_distance:.1f}km")
        if 'bike' in extra_types and bike_distance > 0:
            extra_str.append(f"骑行 {bike_distance:.1f}km")
        if 'run' in extra_types and run_distance > 0:
            extra_str.append(f"跑步 {run_distance:.1f}km")
        
        if extra_str:
            review["gains"].append(f"✨ 额外训练: {', '.join(extra_str)}")
    
    return review
def format_today_review_message(review):
    """格式化今日复盘消息 - 精简版"""
    if not review:
        return None
    
    today = datetime.now()
    weekday_map = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
    weekday = weekday_map[today.weekday()]
    date_str = today.strftime('%Y-%m-%d')
    
    parts = []
    parts.append('=' * 25)
    parts.append('📋 今日训练复盘（数据来源：TrainingPeaks）')
    parts.append(f'📅 {weekday} {date_str}')
    parts.append('')
    
    # 完成概览
    completed = sum(1 for s in review.get("completion_status", {}).values() if "完成" in s)
    total = len(review.get("completion_status", {}))
    if total > 0:
        parts.append(f'✅ 完成 {completed}/{total} 项计划')
    
    # 实际训练（一行一条）
    actual_list = review.get("actual", [])
    planned = review.get("planned", [])
    planned_types = [p.get('type', '') for p in planned]
    
    if actual_list:
        planned_workouts, extra_workouts = [], []
        for w in actual_list:
            title = w.get('title', '未知')
            title_lower = title.lower()
            is_planned = any(
                (ptype == 'swim' and 'swim' in title_lower) or
                (ptype == 'bike' and any(k in title_lower for k in ['bike', 'cycl', 'road'])) or
                (ptype == 'run' and 'run' in title_lower)
                for ptype in planned_types
            )
            (planned_workouts if is_planned else extra_workouts).append(w)
        
        for w in planned_workouts:
            dist = w.get('distance', 0) / 1000
            t = w.get('totalTime', 0)
            hr = w.get('heartRateAverage', 0)
            tss = w.get('tssActual', 0) or w.get('tss', 0)
            s = f"{w.get('title', '')} {dist:.1f}km {int(t*60)}min"
            if hr: s += f" HR{int(hr)}"
            if tss: s += f" TSS{int(tss)}"
            parts.append(s)
        
        for w in extra_workouts:
            dist = w.get('distance', 0) / 1000
            t = w.get('totalTime', 0)
            hr = w.get('heartRateAverage', 0)
            tss = w.get('tssActual', 0) or w.get('tss', 0)
            s = f"➕ 额外训练 {w.get('title', '')} {dist:.1f}km {int(t*60)}min"
            if hr: s += f" HR{int(hr)}"
            if tss: s += f" TSS{int(tss)}"
            parts.append(s)
    else:
        parts.append('（无训练记录）')
    
    # 精简总计（跳过标题行，只取数据）
    for h in review.get("highlights", []):
        if any(k in h for k in ["总", "TSS", "能量"]):
            clean = h.replace("**", "")
            if "今日总计" not in clean and "总计" not in clean:
                parts.append(clean)
    
    # 建议
    if review.get("advice"):
        parts.append('')
        parts.append(review["advice"][0])
    
    return "\n".join(parts)



def _format_workout_detail(w):
    """格式化单个训练的详细信息"""
    title = w.get('title', '未知')
    distance = w.get('distance', 0) / 1000
    time = w.get('totalTime', 0)
    hr = w.get('heartRateAverage', 0)
    tss = w.get('tssActual', 0) or w.get('tss', 0)
    
    msg = f"\n\n{title}"
    msg += f"\n  📏 距离: {distance:.2f}km"
    msg += f"\n  ⏱️ 时长: {time:.2f}h ({int(time*60)}分钟)"
    
    # 计算配速
    if distance > 0 and time > 0:
        pace_sec = (time * 3600) / distance
        pace_min = int(pace_sec // 60)
        pace_sec = int(pace_sec % 60)
        msg += f"\n  🏃 配速: {pace_min}:{pace_sec:02d}/km"
    
    if hr:
        msg += f"\n  ❤️ 心率: {int(hr)}bpm"
    if tss:
        msg += f"\n  📊 TSS: {int(tss)}"
    
    # 对标目标
    if 'swim' in title.lower():
        msg += f"\n  🎯 目标: 配速 <1:45/100m"
        msg += f"\n  📈 当前: {distance*10:.1f}m/min"
    elif 'bike' in title.lower() or 'road' in title.lower():
        msg += f"\n  🎯 目标: FTP 250W"
    elif 'run' in title.lower():
        msg += f"\n  🎯 目标配速: 4:45/km"
    
    return msg
    """从 TrainingPeaks 获取今天的训练"""
    workouts = sync_trainingpeaks_data()
    today = datetime.now().date().isoformat()
    
    # 返回今天的所有训练（可能有多个）
    today_workouts = [w for w in workouts if w.get('workoutDay', '')[:10] == today]
    return today_workouts if today_workouts else None


def analyze_training_performance(planned, actual_tp):
    """分析训练完成情况（基于 TP 数据）"""
    review = {
        "completion": "完成",
        "highlights": [],
        "issues": [],
        "gains": [],
        "advice": []
    }
    
    if not actual_tp:
        return None
    
    planned_type = planned.get('type', '')
    planned_duration = planned.get('duration', 0)
    
    # 从 TP 获取数据
    actual_duration = actual_tp.get('totalTime', 0) / 3600 if actual_tp.get('totalTime') else 0
    sport = actual_tp.get('sport', '').lower()
    distance = actual_tp.get('distance', 0)
    tss = actual_tp.get('tss', 0)
    avg_hr = actual_tp.get('avgHr', 0)
    title = actual_tp.get('title', sport)
    
    # 时长对比
    if actual_duration >= planned_duration * 0.9:
        review["highlights"].append(f"✅ 完成计划时长 ({actual_duration:.1f}h vs 计划{planned_duration}h)")
    elif actual_duration >= planned_duration * 0.7:
        review["highlights"].append(f"⚠️ 完成 {actual_duration/planned_duration*100:.0f}% 时长")
    else:
        review["issues"].append(f"完成时长: {actual_duration:.1f}h（计划{planned_duration}h）")
    
    # 训练类型分析
    if 'swim' in sport:
        if distance:
            review["highlights"].append(f"🏊 距离: {distance/1000:.1f}km")
        if avg_hr:
            review["highlights"].append(f"❤️ 平均心率: {avg_hr}bpm")
        if tss:
            review["highlights"].append(f"📊 TSS: {tss}")
        if avg_hr and avg_hr < 130:
            review["gains"].append("💪 有氧基础扎实，心率控制良好")
    
    elif 'bike' in sport or 'cycl' in sport:
        if distance:
            review["highlights"].append(f"🚴 距离: {distance:.1f}km")
        if tss:
            review["highlights"].append(f"📊 TSS: {tss}")
        if tss and tss > 80:
            review["gains"].append("⚡ 高强度训练，FTP训练效果良好")
        elif tss and tss < 50:
            review["gains"].append("🧘 轻松恢复骑行")
    
    elif 'run' in sport:
        if distance:
            pace = (actual_duration * 60 * 60 / distance) if distance else 0
            pace_str = f"{int(pace//60)}:{int(pace%60):02d}" if pace else "-"
            review["highlights"].append(f"🏃 距离: {distance:.1f}km | 配速: {pace_str}/km")
        if avg_hr:
            review["highlights"].append(f"❤️ 平均心率: {avg_hr}bpm")
        if tss:
            review["highlights"].append(f"📊 TSS: {tss}")
        # 分析跑步配速
        if distance and distance >= 10:
            pace = (actual_duration * 60 * 60 / distance) if distance else 0
            target_pace = 285  # 4:45/km = 285秒
            if pace > 0 and pace < target_pace * 1.1:
                review["gains"].append("🏆 配速达标，状态良好！")
            elif pace > 0:
                review["issues"].append(f"配速偏慢（目标4:45/km，当前{pace_str}/km）")
    
    # TSS 分析
    if tss:
        if tss > 100:
            review["issues"].append("⚠️ 训练负荷较大，注意恢复")
        elif tss < 30 and actual_duration > 0.5:
            review["issues"].append("训练强度偏低")
    
    # 生成建议
    if review["completion"] == "完成":
        if not review["issues"]:
            review["advice"].append("💪 训练状态良好，保持这个节奏！")
        else:
            review["advice"].append("🔄 注意调整，下次争取更好")
    
    return review


def format_review_message(review, planned_session, actual_tp):
    """格式化复盘消息"""
    if not review or not actual_tp:
        return None
    
    session_type = planned_session.get('type', '')
    sport = actual_tp.get('sport', '训练').lower()
    
    type_emoji = {"swim": "🏊", "bike": "🚴", "run": "🏃", 
                  "progression_run": "🏃", "brick": "🔄", "rest": "🏖️"}.get(session_type, "📋")
    
    title = actual_tp.get('title', sport)
    
    msg = f"""
{'='*25}
📋 **昨日训练复盘**（数据来源：TrainingPeaks）

{type_emoji} **计划：** {planned_session.get('focus', '休息')}
📋 **实际：** {title}
"""
    
    if review.get("highlights"):
        for h in review["highlights"]:
            msg += f"\n{h}"
    
    if review.get("issues"):
        msg += """
⚠️ **待改进：**"""
        for i in review["issues"]:
            msg += f"\n{i}"
    
    if review.get("gains"):
        msg += """
✨ **收益：**"""
        for g in review["gains"]:
            msg += f"\n{g}"
    
    if review.get("advice"):
        msg += """
🎯 **建议：**"""
        for a in review["advice"]:
            msg += f"\n{a}"
    
    return msg


def generate_tomorrow_plan():
    """生成明天的训练计划"""
    config = load_config()
    tomorrow = datetime.now().date() + timedelta(days=1)
    plan = get_daily_plan(config, tomorrow)
    
    # 从 TP 获取今天实际训练
    actual_tp_list = get_tp_today_workout()
    
    # 获取今天的所有计划（三个维度）
    today_all_plans = get_today_all_plans()
    all_planned = today_all_plans.get("scheduled", []) + today_all_plans.get("temp", []) + today_all_plans.get("extra", [])
    
    # 生成复盘
    review_msg = None
    if actual_tp_list and all_planned:
        review = analyze_today_training(all_planned, actual_tp_list)
        review_msg = format_today_review_message(review)
    
    # 获取格式化后的计划
    plan_msg = format_daily_plan(plan)
    
    # 生成营养推荐
    from nutrition_manager import NutritionManager
    nm = NutritionManager()
    session = plan.get('session', {})
    training_type = session.get('type', 'rest')
    duration = session.get('duration', 0)
    intensity = session.get('intensity', 'moderate')
    
    nutrition_msg = None
    if training_type != 'rest' and duration > 0:
        nutrition_msg = nm.format_nutrition_message(training_type, duration, intensity)
    
    # 记录明天的定时推送计划
    tomorrow_session = plan.get('session', {})
    tomorrow_session['plan_type'] = 'scheduled'
    log_daily_plan(tomorrow, 'scheduled', tomorrow_session)
    
    # 合并复盘、计划和营养推荐
    result = ""
    if review_msg:
        result += review_msg + "\n\n"
    result += plan_msg
    if nutrition_msg:
        result += "\n\n" + nutrition_msg
    
    return result


def generate_today_plan():
    """生成今天的训练计划"""
    config = load_config()
    today = datetime.now().date()
    plan = get_daily_plan(config, today)
    return format_daily_plan(plan)


if __name__ == "__main__":
    print(generate_tomorrow_plan())
