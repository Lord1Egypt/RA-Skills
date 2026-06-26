#!/usr/bin/env python3
"""
Enhanced health daily report generator with professional analysis.
Features:
- Professional running analysis (Heart Rate Zones, TRIMP, Jack Daniels VDOT)
- Personalized sleep advice
- Fun step suggestions
- Long-term trend analysis (7 days)

Version: 2.0 - Standalone (uses garth library)
"""

import json
import sys
from datetime import date, datetime, timedelta
import os

# ============================================================================
# CONFIGURATION - Update these values for your setup
# ============================================================================

# Health history file for trend analysis
# This file stores daily health data for 7-day trend analysis
HISTORY_FILE = os.path.expanduser("~/.garmin_health_report/history.json")

# User profile (optional, for more accurate HR zone calculations)
# Set to None to use automatic detection from Garmin data
USER_RESTING_HR = None  # e.g., 53
USER_AGE = None        # e.g., 25

# ============================================================================

# Import our custom Garmin client
try:
    from garmin_client import GarminClient, GarminData, StepsData, HeartRateData, Activity
    from authenticate import GarminAuthClient, GarminAuthError
except ImportError as e:
    print(f"Error: {e}", file=sys.stderr)
    print("Ensure garmin_client.py and authenticate.py are in same directory.", file=sys.stderr)
    sys.exit(1)

# Calculate HR-related metrics if user profile is provided
MAX_HR = None
HRR = None

if USER_RESTING_HR is not None and USER_AGE is not None:
    MAX_HR = 220 - USER_AGE
    HRR = MAX_HR - USER_RESTING_HR


def format_pace(pace_min_per_km):
    """Convert pace from decimal minutes to MM'SS format."""
    minutes = int(pace_min_per_km)
    seconds = int((pace_min_per_km - minutes) * 60)
    return f"{minutes}'{seconds:02d}"


def get_client() -> GarminClient:
    """Get authenticated Garmin client."""
    try:
        return GarminClient.from_saved_tokens()
    except GarminAuthError as e:
        print(f"Error: Not authenticated. {e}", file=sys.stderr)
        print("Run 'python3 authenticate.py' first.", file=sys.stderr)
        sys.exit(1)


def get_user_profile_values(client, user_resting_hr, user_age):
    """
    Get user profile values if not provided in configuration.

    Returns: (resting_hr, age)
    """
    if user_resting_hr is not None and user_age is not None:
        return user_resting_hr, user_age

    # Try to get from user profile
    try:
        profile = client.get_user_profile()
        if profile:
            # Use estimated age from profile if available
            age = profile.get('age', None)
            if age:
                return user_resting_hr, age
    except Exception as e:
        print(f"Warning: Could not fetch user profile: {e}", file=sys.stderr)

    # Use defaults if not available
    default_age = 30
    default_resting_hr = 60
    print(f"Warning: Using default values (Age: {default_age}, Resting HR: {default_resting_hr})", file=sys.stderr)
    print("Update USER_RESTING_HR and USER_AGE in script for more accurate analysis.", file=sys.stderr)
    return default_resting_hr, default_age


def format_qualifier(qualifier):
    """Format qualifier key to readable text."""
    qual_map = {
        'EXCELLENT': '优秀',
        'GOOD': '良好',
        'FAIR': '一般',
        'POOR': '需改善'
    }
    return qual_map.get(qualifier.upper(), qualifier)


def estimate_hr_zones(avg_hr, resting_hr, hrr):
    """Estimate HR zone distribution based on average HR."""
    if avg_hr is None or hrr is None:
        return None

    # Calculate percentage of HRR
    avg_hr_percent = ((avg_hr - resting_hr) / hrr) * 100 if hrr > 0 else 0

    # Estimate distribution (simplified normal distribution)
    if avg_hr_percent < 50:
        return {
            'avg_hr_percent': avg_hr_percent,
            'zone1_pct': 90, 'zone2_pct': 10, 'zone3_pct': 0,
            'zone4_pct': 0, 'zone5_pct': 0,
            'training_type': '恢复性训练',
            'training_purpose': '促进身体恢复，不累积疲劳'
        }
    elif avg_hr_percent < 60:
        return {
            'avg_hr_percent': avg_hr_percent,
            'zone1_pct': 70, 'zone2_pct': 30, 'zone3_pct': 0,
            'zone4_pct': 0, 'zone5_pct': 0,
            'training_type': '有氧基础训练',
            'training_purpose': '建立心肺基础，增加肌肉毛细血管密度'
        }
    elif avg_hr_percent < 70:
        return {
            'avg_hr_percent': avg_hr_percent,
            'zone1_pct': 30, 'zone2_pct': 50, 'zone3_pct': 20,
            'zone4_pct': 0, 'zone5_pct': 0,
            'training_type': '有氧耐力训练',
            'training_purpose': '提升耐力水平，增强长时间运动能力'
        }
    elif avg_hr_percent < 80:
        return {
            'avg_hr_percent': avg_hr_percent,
            'zone1_pct': 10, 'zone2_pct': 30, 'zone3_pct': 50,
            'zone4_pct': 10, 'zone5_pct': 0,
            'training_type': '乳酸阈值训练',
            'training_purpose': '提升清除乳酸能力，接近耐力天花板'
        }
    else:
        return {
            'avg_hr_percent': avg_hr_percent,
            'zone1_pct': 5, 'zone2_pct': 15, 'zone3_pct': 30,
            'zone4_pct': 40, 'zone5_pct': 10,
            'training_type': '高强度间歇训练',
            'training_purpose': '刺激最大摄氧量，提升无氧能力'
        }


def calculate_trimp(duration_seconds, avg_hr, resting_hr, hrr):
    """Calculate Training Load (TRIMP)."""
    if avg_hr is None or hrr is None:
        return None

    duration_min = duration_seconds / 60

    # Heart rate ratio
    hr_ratio = (avg_hr - resting_hr) / hrr if hrr > 0 else 0

    # Banister TRIMP formula
    trimp = duration_min * hr_ratio * (0.64 ** (1.92 * hr_ratio))

    # Load level
    if trimp < 100:
        load_level = "小负荷"
        load_desc = "适合恢复日训练"
    elif trimp < 200:
        load_level = "中等负荷"
        load_desc = "适合日常训练"
    elif trimp < 300:
        load_level = "较大负荷"
        load_desc = "需要充分恢复"
    else:
        load_level = "高强度负荷"
        load_desc = "强烈建议安排休息日"

    return {
        'trimp_value': round(trimp, 1),
        'load_level': load_level,
        'load_desc': load_desc,
        'hr_ratio': round(hr_ratio * 100, 1)
    }


def estimate_vdot(pace_min_per_km):
    """Estimate VDOT based on pace (more accurate)."""
    # Convert to seconds per km
    pace_sec = pace_min_per_km * 60

    # More precise VDOT-pace lookup table (based on Jack Daniels)
    # Format: (pace_sec_per_km, vdot)
    vdot_table = [
        (240, 80),
        (270, 72),
        (300, 65),
        (330, 58),
        (360, 52),  # 6:00/km
        (378, 50),  # 6:18/km
        (400, 47),  # 6:40/km
        (420, 45),  # 7:00/km
        (450, 42),  # 7:30/km
        (480, 40),  # 8:00/km
        (510, 38),  # 8:30/km
        (540, 36),  # 9:00/km
    ]

    # Find closest VDOT (find minimum absolute difference)
    best_vdot = 30
    min_diff = float('inf')
    for sec_per_km, vdot_val in vdot_table:
        diff = abs(pace_sec - sec_per_km)
        if diff < min_diff:
            min_diff = diff
            best_vdot = vdot_val

    return best_vdot


def get_daniels_training_paces(vdot):
    """Get Jack Daniels training paces based on VDOT."""
    if vdot >= 70:
        return {
            'e_pace': 4.7, 'm_pace': 5.0, 't_pace': 4.6,
            'i_pace': 4.2, 'r_pace': 4.0
        }
    elif vdot >= 65:
        return {
            'e_pace': 5.0, 'm_pace': 5.3, 't_pace': 4.9,
            'i_pace': 4.5, 'r_pace': 4.3
        }
    elif vdot >= 62:
        return {
            'e_pace': 5.3, 'm_pace': 5.6, 't_pace': 5.2,
            'i_pace': 4.8, 'r_pace': 4.6
        }
    elif vdot >= 58:
        return {
            'e_pace': 5.6, 'm_pace': 5.9, 't_pace': 5.5,
            'i_pace': 5.1, 'r_pace': 4.8
        }
    elif vdot >= 55:
        return {
            'e_pace': 5.9, 'm_pace': 6.2, 't_pace': 5.8,
            'i_pace': 5.4, 'r_pace': 5.1
        }
    elif vdot >= 52:
        return {
            'e_pace': 6.2, 'm_pace': 6.5, 't_pace': 6.1,
            'i_pace': 5.7, 'r_pace': 5.4
        }
    elif vdot >= 50:
        return {
            'e_pace': 6.4, 'm_pace': 6.7, 't_pace': 6.3,
            'i_pace': 5.9, 'r_pace': 5.6
        }
    elif vdot >= 47:
        return {
            'e_pace': 6.8, 'm_pace': 7.1, 't_pace': 6.7,
            'i_pace': 6.3, 'r_pace': 6.0
        }
    elif vdot >= 45:
        return {
            'e_pace': 7.1, 'm_pace': 7.5, 't_pace': 7.0,
            'i_pace': 6.6, 'r_pace': 6.3
        }
    elif vdot >= 42:
        return {
            'e_pace': 7.5, 'm_pace': 8.0, 't_pace': 7.4,
            'i_pace': 6.9, 'r_pace': 6.6
        }
    elif vdot >= 40:
        return {
            'e_pace': 8.0, 'm_pace': 8.4, 't_pace': 7.8,
            'i_pace': 7.3, 'r_pace': 7.0
        }
    elif vdot >= 38:
        return {
            'e_pace': 8.4, 'm_pace': 8.8, 't_pace': 8.2,
            'i_pace': 7.7, 'r_pace': 7.4
        }
    elif vdot >= 35:
        return {
            'e_pace': 9.0, 'm_pace': 9.4, 't_pace': 8.8,
            'i_pace': 8.3, 'r_pace': 7.9
        }
    else:  # vdot < 35
        return {
            'e_pace': 9.8, 'm_pace': 10.2, 't_pace': 9.6,
            'i_pace': 9.0, 'r_pace': 8.6
        }


def analyze_pace_zone(current_pace, training_paces):
    """Analyze which Daniels zone is current pace belongs to."""
    e_pace = training_paces['e_pace']
    m_pace = training_paces['m_pace']
    t_pace = training_paces['t_pace']
    i_pace = training_paces['i_pace']
    r_pace = training_paces['r_pace']

    if current_pace <= e_pace:
        return {
            'zone': 'E区（轻松跑）',
            'zone_desc': '可以边跑边完整说话的轻松配速',
            'zone_purpose': '建立心肺基础，增加肌肉毛细血管密度',
            'zone_comment': '非常适合恢复性训练或日常轻松跑'
        }
    elif current_pace <= m_pace:
        return {
            'zone': 'E区~M区之间',
            'zone_desc': '介于轻松跑和马拉松配速之间',
            'zone_purpose': '维持有氧基础，为强度训练做准备',
            'zone_comment': '这是有氧耐力的甜点区间'
        }
    elif current_pace <= t_pace:
        return {
            'zone': 'M区~T区之间',
            'zone_desc': '马拉松配速到乳酸阈值之间',
            'zone_purpose': '提升耐力水平，适应比赛强度',
            'zone_comment': '可以尝试逐渐接近T区，提升阈值'
        }
    elif current_pace <= i_pace:
        return {
            'zone': 'T区（乳酸阈值跑）',
            'zone_desc': '节奏跑强度，能维持20-60分钟',
            'zone_purpose': '提升清除乳酸能力，提升耐力天花板',
            'zone_comment': '这是提升耐力的关键训练强度'
        }
    elif current_pace <= r_pace:
        return {
            'zone': 'I区（间歇跑）',
            'zone_desc': '间歇跑强度，维持3-5分钟',
            'zone_purpose': '刺激提升最大摄氧量（VO₂Max）',
            'zone_comment': '建议每次3-5分钟，间歇1-2分钟'
        }
    else:
        return {
            'zone': 'R区（重复跑）',
            'zone_desc': '全力冲刺，维持30秒-2分钟',
            'zone_purpose': '提升跑步经济性，锻炼肌肉神经爆发力',
            'zone_comment': '适合短距离冲刺训练'
        }


def assess_recovery_status(hrv, sleep_hours, sleep_score):
    """Assess overall recovery status based on HRV and sleep."""
    # HRV assessment
    if hrv is None:
        hrv_status = "未知"
        hrv_desc = "暂无HRV数据"
        recovery_advice = "无法评估"
    elif hrv < 30:
        hrv_status = "压力过大"
        hrv_desc = "HRV偏低，可能处于疲劳状态"
        recovery_advice = "建议减少训练强度或安排休息日"
    elif hrv < 40:
        hrv_status = "轻度疲劳"
        hrv_desc = "HRV略低，身体可能有轻度疲劳"
        recovery_advice = "建议进行轻松训练或适度训练"
    elif hrv < 60:
        hrv_status = "状态良好"
        hrv_desc = "HRV处于正常范围，身体恢复良好"
        recovery_advice = "可以进行正常训练"
    else:
        hrv_status = "状态优秀"
        hrv_desc = "HRV较高，身体恢复状态很好"
        recovery_advice = "可以安排较高强度训练"

    # Sleep assessment
    if sleep_hours is None:
        sleep_status = "未知"
        sleep_desc = "暂无睡眠时长数据"
    elif sleep_hours < 6:
        sleep_status = "不足"
        sleep_desc = "睡眠时长偏少，恢复时间不足"
    elif sleep_hours < 7:
        sleep_status = "略显不足"
        sleep_desc = "睡眠时长略少，勉强够用"
    elif sleep_hours < 8:
        sleep_status = "良好"
        sleep_desc = "睡眠时长适中，恢复充分"
    else:
        sleep_status = "充足"
        sleep_desc = "睡眠时长充足，恢复很好"

    # Overall assessment
    if hrv_status in ["压力过大", "轻度疲劳"] or sleep_status in ["不足", "略显不足"]:
        overall_status = "需要恢复"
        overall_desc = "身体疲劳或睡眠不足，建议降低训练强度"
        overall_advice = "建议安排轻松训练或休息，优先恢复"
    elif hrv_status == "状态良好" and sleep_status == "良好":
        overall_status = "状态良好"
        overall_desc = "身体恢复状态良好，适合正常训练"
        overall_advice = "可以按计划进行正常训练"
    elif hrv_status == "状态优秀" or sleep_status == "充足":
        overall_status = "状态优秀"
        overall_desc = "身体恢复状态优秀，可以挑战高强度"
        overall_advice = "可以安排间歇训练或长距离训练"
    else:
        overall_status = "状态一般"
        overall_desc = "身体恢复状态一般，需要平衡训练强度"
        overall_advice = "建议进行中等强度训练"

    return {
        'hrv_status': hrv_status,
        'hrv_desc': hrv_desc,
        'hrv_value': hrv,
        'sleep_status': sleep_status,
        'sleep_desc': sleep_desc,
        'sleep_hours': sleep_hours,
        'sleep_score': sleep_score,
        'overall_status': overall_status,
        'overall_desc': overall_desc,
        'overall_advice': overall_advice
    }


def generate_sleep_advice(sleep_dto):
    """Generate personalized sleep advice."""
    if not sleep_dto or not sleep_dto.raw_data:
        return []

    advice_list = []

    total_seconds = sleep_dto.sleep_time_seconds
    if total_seconds <= 0:
        return ["暂无睡眠数据，无法给出建议"]

    deep_seconds = sleep_dto.deep_sleep_seconds
    light_seconds = sleep_dto.light_sleep_seconds
    rem_seconds = sleep_dto.rem_sleep_seconds

    deep_pct = (deep_seconds / total_seconds * 100) if total_seconds > 0 else 0
    light_pct = (light_seconds / total_seconds * 100) if total_seconds > 0 else 0
    rem_pct = (rem_seconds / total_seconds * 100) if total_seconds > 0 else 0

    # Deep sleep percentage
    if deep_pct < 15:
        advice_list.append({
            'issue': '深睡比例偏低',
            'suggestion': '建议睡前1小时远离电子屏幕，保持卧室完全黑暗。白天适度运动有助于提升深睡比例。'
        })

    # Light sleep percentage
    if light_pct > 65:
        advice_list.append({
            'issue': '浅睡比例偏高',
            'suggestion': '检查睡眠环境是否有噪音干扰，考虑使用白噪音机。确保床铺舒适度，温度保持在18-22°C。'
        })

    # REM percentage
    if rem_pct < 20:
        advice_list.append({
            'issue': 'REM睡眠偏少',
            'suggestion': 'REM偏少可能与压力或酒精摄入有关。建议睡前进行放松练习，如冥想或深呼吸。'
        })

    # Sleep duration
    sleep_hours = total_seconds / 3600
    if sleep_hours < 6:
        advice_list.append({
            'issue': '睡眠时长不足',
            'suggestion': '建议将睡眠时间逐步延长到7-8小时。建立固定的睡前仪式，避免周末过度补睡。'
        })

    # HRV
    hrv = sleep_dto.avg_overnight_hrv
    if hrv and hrv > 80:
        advice_list.append({
            'issue': 'HRV偏高',
            'suggestion': 'HRV偏高可能表示身体处于兴奋状态。建议减少睡前刺激，进行放松练习。'
        })
    elif hrv and hrv < 30:
        advice_list.append({
            'issue': 'HRV偏低',
            'suggestion': 'HRV偏低可能表示身体疲劳或压力过大。建议适当休息，减少高强度训练。'
        })

    return advice_list


def generate_steps_advice(steps, goal):
    """Generate fun and personalized step advice."""
    steps_pct = (steps / goal * 100) if goal > 0 else 0

    # Fun comment
    if steps < 3000:
        fun_comment = "今天是不是沙发封印了？明天起来走动走动吧~"
        emoji = "🛋️"
    elif steps < 5000:
        fun_comment = "轻度活动，适合轻松的一天。"
        emoji = "🚶"
    elif steps < 8000:
        fun_comment = "中规中矩，继续保持。"
        emoji = "😊"
    elif steps < 10000:
        fun_comment = f"不错！再坚持{goal - steps}步就达标了！"
        emoji = "💪"
    elif steps < 15000:
        fun_comment = "完美达标！身体感谢你的努力。"
        emoji = "🎉"
    else:
        fun_comment = "太厉害了！你今天是不是霸屏了？"
        emoji = "🏆"

    # Scenario-based advice
    advice = []
    if steps < 5000:
        advice.append("建议明天主动走楼梯代替电梯，午休后散步10分钟。")
    elif steps > 15000:
        advice.append("明天注意休息，避免过度疲劳。膝盖可能需要放松。")
    elif steps < 10000:
        advice.append(f"还差{goal - steps}步就达标了，走一圈就到了！")

    return {
        'fun_comment': fun_comment,
        'emoji': emoji,
        'advice': advice,
        'steps_pct': steps_pct
    }


def load_history(days=7):
    """Load health history from file."""
    if not os.path.exists(HISTORY_FILE):
        return []

    try:
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            history = json.load(f)

        # Filter last N days
        cutoff_date = date.today() - timedelta(days=days)
        filtered = [d for d in history if datetime.fromisoformat(d['date']).date() >= cutoff_date]

        return filtered
    except Exception as e:
        print(f"Error loading history: {e}", file=sys.stderr)
        return []


def save_history(date_str, data):
    """Save health history to file."""
    history = load_history(days=30)

    # Check if date already exists
    existing_index = next((i for i, d in enumerate(history) if d['date'] == date_str), None)

    if existing_index is not None:
        history[existing_index] = data
    else:
        history.append(data)

    # Save to file
    try:
        os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error saving history: {e}", file=sys.stderr)


def analyze_long_term_trends(history):
    """Analyze long-term trends from history."""
    if not history or len(history) < 3:
        return None

    trend_advice = []

    # Running consistency
    running_days = [d for d in history if d.get('has_running', False)]
    running_days_count = len(running_days)

    # Check consecutive running days
    consecutive_running = 0
    max_consecutive_running = 0
    for d in reversed(history):
        if d.get('has_running', False):
            consecutive_running += 1
            max_consecutive_running = max(max_consecutive_running, consecutive_running)
        else:
            break

    if max_consecutive_running >= 3:
        trend_advice.append(f"你已连续{max_consecutive_running}天跑步，建议注意运动疲劳，适当安排休息日")
    elif max_consecutive_running >= 7:
        trend_advice.append(f"你已连续{max_consecutive_running}天跑步，强烈建议安排休息日，让身体充分恢复")

    # Check consecutive no-running days
    consecutive_no_running = 0
    max_consecutive_no_running = 0
    for d in reversed(history):
        if not d.get('has_running', False):
            consecutive_no_running += 1
            max_consecutive_no_running = max(max_consecutive_no_running, consecutive_no_running)
        else:
            break

    if max_consecutive_no_running >= 3:
        trend_advice.append(f"你已连续{max_consecutive_no_running}天没跑步了，建议适当增加运动量")

    # Steps trend
    high_steps_days = len([d for d in history if d.get('steps', 0) > 12000])
    low_steps_days = len([d for d in history if d.get('steps', 0) < 5000])

    if high_steps_days >= 3:
        trend_advice.append(f"近期有{high_steps_days}天步数较高，建议注意休息，避免过度疲劳")
    if low_steps_days >= 3:
        trend_advice.append(f"近期有{low_steps_days}天步数偏低，建议增加日常活动")

    return trend_advice if trend_advice else None


def get_weekday(dt):
    """Get Chinese weekday name."""
    weekdays = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
    return weekdays[dt.weekday()]


def extract_location(activity_name):
    """Extract location from activity name."""
    # Simple extraction - looks for common patterns
    if '浦东新区' in activity_name:
        return '浦东新区'
    elif '源深路' in activity_name:
        return '源深路'
    elif '跑步机' in activity_name:
        return '跑步机'
    elif '家' in activity_name:
        return '家附近'
    else:
        return activity_name[:20]  # Return first 20 chars if no known location


def infer_training_type(activity):
    """Infer training type based on training effect label."""
    label = activity.training_effect_label

    if not label:
        return '训练'

    label_map = {
        'RECOVERY': '恢复性训练',
        'AEROBIC_BASE': '有氧耐力跑',
        'TEMPO': '节奏跑',
        'THRESHOLD': '乳酸阈值跑',
        'INTERVAL': '间歇跑',
        'SPEED': '速度训练'
    }

    return label_map.get(label, '训练')


def describe_activity(activity, sleep_data=None):
    """Generate scenario-based activity description."""
    # Time
    hour = activity.start_time.hour if activity.start_time else 0
    if 6 <= hour < 9:
        time_desc = "清晨"
    elif 9 <= hour < 12:
        time_desc = "上午"
    elif 12 <= hour < 17:
        time_desc = "下午"
    elif 17 <= hour < 20:
        time_desc = "傍晚"
    else:
        time_desc = "晚上"

    # Location
    location = extract_location(activity.activity_name)

    # Training type
    training_type = infer_training_type(activity)

    # Generate description
    description = f"{get_weekday(activity.start_time)}{time_desc}{location}的{training_type}"

    # Add background
    if sleep_data:
        total_seconds = sleep_data.sleep_time_seconds
        if total_seconds > 0:
            sleep_hours = total_seconds / 3600
            description += f"。今天你的睡眠时间达到{sleep_hours:.1f}小时"

    return description


def generate_health_report(target_date=None):
    """
    Generate comprehensive daily health report for specified date.
    """
    if target_date is None:
        target_date = date.today()
    elif isinstance(target_date, str):
        target_date = datetime.strptime(target_date, "%Y-%m-%d").date()

    client = get_client()

    # Get user profile values if not set
    resting_hr, age = get_user_profile_values(client, USER_RESTING_HR, USER_AGE)
    max_hr = 220 - age
    hrr = max_hr - resting_hr

    # Start building report
    report = f"""📅 {target_date.strftime('%Y-%m-%d')} 健康日报
{'=' * 60}"""

    # === Sleep Data ===
    sleep_data_raw = client.get_sleep(target_date)

    # Sleep analysis
    sleep_hours = None
    sleep_score = None
    hrv_value = None

    if sleep_data_raw and sleep_data_raw.raw_data:
        total_seconds = sleep_data_raw.sleep_time_seconds
        sleep_hours = total_seconds / 3600 if total_seconds else 0

        deep_seconds = sleep_data_raw.deep_sleep_seconds
        light_seconds = sleep_data_raw.light_sleep_seconds
        rem_seconds = sleep_data_raw.rem_sleep_seconds

        deep_hours = deep_seconds / 3600 if deep_seconds else 0
        light_hours = light_seconds / 3600 if light_seconds else 0
        rem_hours = rem_seconds / 3600 if rem_seconds else 0

        deep_pct = (deep_seconds / total_seconds * 100) if total_seconds > 0 else 0
        light_pct = (light_seconds / total_seconds * 100) if total_seconds > 0 else 0
        rem_pct = (rem_seconds / total_seconds * 100) if total_seconds > 0 else 0

        # Sleep scores
        overall_value = sleep_data_raw.overall_sleep_score
        overall_qualifier = sleep_data_raw.sleep_qualifier

        sleep_score = overall_value
        overall_text = format_qualifier(overall_qualifier) if overall_qualifier else "N/A"

        # HRV
        hrv_value = sleep_data_raw.avg_overnight_hrv

        report += f"""

😴 睡眠质量
总睡眠：{sleep_hours:.1f} 小时
└─ 深睡：{deep_hours:.1f}h ({deep_pct:.0f}%) | 浅睡：{light_hours:.1f}h ({light_pct:.0f}%) | REM：{rem_hours:.1f}h ({rem_pct:.0f}%)

睡眠评分：{overall_value if overall_value else 'N/A'} ({overall_text})"""

        # Recovery status
        if hrv_value is not None and overall_value is not None:
            recovery = assess_recovery_status(hrv_value, sleep_hours, overall_value)

            report += f"""

• HRV状态：{recovery['hrv_status']}（{recovery['hrv_value']}ms）
  {recovery['hrv_desc']}
• 睡眠状态：{recovery['sleep_status']}（{recovery['sleep_hours']:.1f}小时）
  {recovery['sleep_desc']}
• 综合评估：{recovery['overall_status']}
  {recovery['overall_desc']}
• 建议：{recovery['overall_advice']}"""

        # Sleep advice
        advice_list = generate_sleep_advice(sleep_data_raw)
        if advice_list and len(advice_list) > 0:
            report += f"""

💡 睡眠建议"""
            for i, advice_item in enumerate(advice_list, 1):
                if isinstance(advice_item, dict):
                    report += f"""
• {advice_item['issue']}：{advice_item['suggestion']}"""
                else:
                    report += f"""
• {advice_item}"""
    else:
        report += f"""

😴 睡眠质量
暂无睡眠数据"""

    # === Heart Rate Data ===
    hr_data = client.get_heart_rate(target_date)
    resting_hr_data = hr_data.resting_heart_rate if hr_data else resting_hr

    report += f"""

💓 心率监测
静息心率：{resting_hr_data} bpm 💙"""

    # === Steps Data ===
    steps_data = client.get_steps(target_date)
    steps = steps_data.total_steps if steps_data else 0
    step_goal = steps_data.step_goal if steps_data else 10000

    if steps > 0:
        steps_advice = generate_steps_advice(steps, step_goal)

        report += f"""

👟 活动量
今日步数：{steps} 步
步数目标：{step_goal} 步
完成度：{steps_advice['steps_pct']:.1f}%
距离：{steps_data.total_distance_meters/1000 if steps_data.total_distance_meters else 0:.2f} km
爬升：{steps_data.floors_ascended if steps_data.floors_ascended else 0:.2f} 层

{steps_advice['emoji']} {steps_advice['fun_comment']}"""

        if steps_advice['advice']:
            report += f"""
💡 活动建议"""
            for advice in steps_advice['advice']:
                report += f"""
• {advice}"""
    else:
        report += f"""

👟 活动量
今日步数：无记录"""

    # === Activities Data ===
    activities = client.get_activities(start_date=target_date, end_date=target_date, limit=50)
    has_running = any('running' in a.activity_type for a in activities)

    if activities:
        # Sort by time
        activities_sorted = sorted(activities, key=lambda a: a.start_time if a.start_time else datetime.min)

        # Get main activity (usually first one)
        main_activity = activities_sorted[0]

        # Generate description
        activity_desc = describe_activity(main_activity, sleep_data_raw)

        report += f"""

🏃‍♂️ 运动表现
{activity_desc}。"""

        if main_activity.distance_meters > 0:
            distance_km = main_activity.distance_meters / 1000
            duration_min = main_activity.duration_seconds / 60
            pace = duration_min / distance_km if distance_km > 0 else 0

            report += f"""用时{int(duration_min)}分{int(duration_min * 60 % 60)}秒，平均配速{int(pace)}'{int(pace * 60 % 60):02d}'。"""

        if sleep_hours and hrv_value:
            report += f"""HRV为{int(hrv_value) if hrv_value else 'N/A'}ms，身体状态保持得不错。"""

        # Professional analysis
        report += f"""

💪 运动数据分析（专业版）"""

        # 1. HR zones analysis
        if main_activity.avg_heart_rate and hrr is not None:
            hr_zones = estimate_hr_zones(main_activity.avg_heart_rate, resting_hr, hrr)

            if hr_zones:
                report += f"""

1. 五区间心率分析
   • 数据表现：平均心率{main_activity.avg_heart_rate}次/分，占储备心率的{hr_zones['avg_hr_percent']:.0f}%
   • 区间分布估算：Zone 2（有氧基础）约{hr_zones['zone2_pct']}%，Zone 3（有氧耐力）约{hr_zones['zone3_pct']}%，Zone 4（乳酸阈值）约{hr_zones['zone4_pct']}%
   • 训练类型：{hr_zones['training_type']}
   • 训练目的：{hr_zones['training_purpose']}
   • 客观评价：{hr_zones['training_type']}，平均心率在{hr_zones['avg_hr_percent']:.0f}%心率时间处于有氧耐力区间，这是稳态有氧训练的绝佳表现"""

        # 2. Training load (TRIMP)
        if hrr is not None:
            trimp = calculate_trimp(main_activity.duration_seconds, main_activity.avg_heart_rate, resting_hr, hrr)

            if trimp:
                report += f"""

2. 训练负荷评估
   • TRIMP值：{trimp['trimp_value']}
   • 负荷等级：{trimp['load_level']}
   • 训练价值：{trimp['load_desc']}
   • 心率储备利用率：{trimp['hr_ratio']}%
   • 客观评价：本次训练属于{trimp['load_level']}，不会造成过度疲劳
   • 建议：适合作为恢复性训练或日常训练，每周可安排3-4次"""

        # 3. VDOT analysis
        if main_activity.distance_meters > 0 and main_activity.duration_seconds > 0:
            distance_km = main_activity.distance_meters / 1000
            duration_min = main_activity.duration_seconds / 60
            pace = duration_min / distance_km
            vdot = estimate_vdot(pace)
            training_paces = get_daniels_training_paces(vdot)
            pace_zone = analyze_pace_zone(pace, training_paces)

            report += f"""

3. 杰克·丹尼尔斯训练法（VDOT分析）
   • 跑步距离：{distance_km:.2f} 公里
   • 运动时长：{int(duration_min)} 分钟
   • 估算VDOT：{vdot}
   • 当前配速：{format_pace(pace)}/公里
   • 所属区间：{pace_zone['zone']}
   • {pace_zone['zone_desc']}
   • 训练目的：{pace_zone['zone_purpose']}
   • {pace_zone['zone_comment']}
   • VDOT对应训练区间：
     - E区（轻松跑）：{format_pace(training_paces['e_pace'])}/公里
     - M区（马拉松）：{format_pace(training_paces['m_pace'])}/公里
     - T区（阈值）：{format_pace(training_paces['t_pace'])}/公里
     - I区（间歇）：{format_pace(training_paces['i_pace'])}/公里
     - R区（重复）：{format_pace(training_paces['r_pace'])}/公里
   • 客观评价：你的配速介于E区和M区之间，是有氧耐力训练的黄金区间
   • 建议：可以尝试在长距离训练中保持这个配速，逐步提升VDOT"""

        # JARVIS summary
        report += f"""

💡 J.A.R.V.I.S.有话说"""

        # Combine insights from all analyses
        insights = []

        if main_activity.avg_heart_rate and hr_zones:
            insights.append(f"• 五区间心率分析：本次训练{hr_zones['avg_hr_percent']:.0f}%时间处于有氧耐力区间，是一次绝佳的稳态有氧训练")

        if trimp:
            insights.append(f"• 训练负荷评估：TRIMP值{trimp['trimp_value']}属于{trimp['load_level']}，适合作为日常训练，不会造成过度疲劳")

        if main_activity.distance_meters > 0 and vdot:
            insights.append(f"• VDOT分析：你的配速{format_pace(pace)}/公里对应VDOT~{vdot}，介于E区和M区之间，是有氧耐力训练的黄金区间")

        if len(insights) > 0:
            for insight in insights:
                report += f"""
{insight}"""

        if main_activity.distance_meters > 0 and vdot:
            report += f"""
• 综合建议：基于专业分析，这是一次质量很高的有氧耐力训练。建议在周训练中保持这个强度，适当增加距离以进一步提升VDOT。"""
    else:
        report += f"""

🏃‍♂️ 运动表现
今天没有运动记录"""

    # === Long-term trends ===
    # Save today's data to history
    date_str = target_date.strftime('%Y-%m-%d')
    today_data = {
        'date': date_str,
        'steps': steps if steps else 0,
        'has_running': has_running,
        'sleep_hours': sleep_hours if sleep_hours else 0,
        'hrv': hrv_value
    }
    save_history(date_str, today_data)

    # Analyze trends
    history = load_history(days=7)
    trend_advice = analyze_long_term_trends(history)

    if trend_advice:
        report += f"""

📈 长期趋势（过去7天）"""
        for advice in trend_advice:
            report += f"""
• {advice}"""

    # === Summary ===
    report += f"""

{'=' * 60}"""

    # Overall summary
    if activities:
        total_distance = sum(a.distance_meters for a in activities) / 1000
        total_duration = sum(a.duration_seconds for a in activities) / 3600

        if total_distance > 5:
            report += f"\n💪 今天运动量很充足！继续保持！"
        elif total_distance > 2:
            report += f"\n👍 今天运动量不错，保持节奏！"
        else:
            report += f"\n💤 今天运动量较少，明天加把劲！"
    else:
        if steps < 5000:
            report += f"\n💤 今天活动量较少，适当运动对身体有好处哦~"

    report += f"\n\n✨ 明天加油！💪"

    return report


def main():
    """Main function to generate and print health report."""
    date_arg = None
    if len(sys.argv) > 1:
        date_arg = sys.argv[1]

    # Generate report
    report = generate_health_report(date_arg)
    print(report)


if __name__ == "__main__":
    main()
