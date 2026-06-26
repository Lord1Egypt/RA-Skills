"""
Check-in Auto-Detection Module
从 WHOOP 数据自动检测今日训练，生成初步打卡内容
"""

import os
import sys
import json
import subprocess
from datetime import datetime, timedelta, date
from typing import Dict, List, Optional, Tuple

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, SKILL_DIR)

from lib.tz import now, today, today_str, datetime_to_bj, is_bj_today, format_bj, BEIJING_OFFSET_HOURS


# ============================================================
# WHOOP Workout 查询
# ============================================================

def _call_whoop_api(endpoint: str, params: List[str] = None) -> Dict:
    """调用 WHOOP API"""
    try:
        cmd = ['python3', 'scripts/whoop_data.py'] + endpoint.split()
        if params:
            if '--days' in endpoint:
                # Handle --days parameter in endpoint
                pass
        result = subprocess.run(
            cmd,
            capture_output=True, text=True,
            cwd=SKILL_DIR
        )
        if result.returncode != 0:
            return {}
        return json.loads(result.stdout)
    except Exception:
        return {}


def get_today_workouts(days: int = 2) -> List[Dict]:
    """
    获取今日训练记录。
    默认为 days=2，因为北京凌晨跑步（如 08:48 北京时间）
    对应 UTC 00:48，会跨越 UTC 日期边界。
    """
    try:
        result = subprocess.run(
            ['python3', 'scripts/whoop_data.py', 'workouts', '--days', str(days)],
            capture_output=True, text=True,
            cwd=SKILL_DIR
        )
        if result.returncode != 0:
            return []
        data = json.loads(result.stdout)
        return data.get('records', [])
    except Exception:
        return []


def get_recovery_data() -> Dict:
    """获取今日恢复数据"""
    try:
        result = subprocess.run(
            ['python3', 'scripts/whoop_data.py', 'recovery', '--days', '1'],
            capture_output=True, text=True,
            cwd=SKILL_DIR
        )
        if result.returncode != 0:
            return {}
        data = json.loads(result.stdout)
        records = data.get('records', [])
        if records:
            return records[0].get('score', {})
        return {}
    except Exception:
        return {}


# ============================================================
# 训练类型识别
# ============================================================

SPORT_LABELS = {
    'running': '跑步',
    'strength_training': '力量训练',
    'cycling': '骑行',
    'swimming': '游泳',
    'yoga': '瑜伽',
    'hiit': 'HIIT',
    'walking': '散步',
    '登山': '登山',
    'cross_training': '综合训练',
    'recovery': '恢复',
}


def _parse_duration_minutes(start: str, end: str) -> int:
    """计算训练时长（分钟）"""
    try:
        # WHOOP timestamps are ISO format
        s = datetime.fromisoformat(start.replace('Z', '+00:00'))
        e = datetime.fromisoformat(end.replace('Z', '+00:00'))
        return int((e - s).total_seconds() / 60)
    except Exception:
        return 0


def _calc_pace(distance_m: float, duration_min: int) -> str:
    """计算配速 (min/km)"""
    if distance_m <= 0 or duration_min <= 0:
        return 'N/A'
    km = distance_m / 1000
    pace = duration_min / km
    m = int(pace)
    s = int((pace - m) * 60)
    return f"{m}:{s:02d}"


def _estimate_distance_from_kj(kj: float, sport: str) -> Optional[float]:
    """从千焦估算距离（跑步）"""
    if sport == 'running' and kj > 0:
        # 粗略估算：跑步约 4kJ/km
        return round(kj / 4, 1)
    return None


def _zone_label(zone_key: str) -> str:
    """心率区间名称"""
    labels = {
        'zone_zero': 'Z0（恢复）',
        'zone_one': 'Z1（轻松）',
        'zone_two': 'Z2（有氧）',
        'zone_three': 'Z3（阈值）',
        'zone_four': 'Z4（无氧）',
        'zone_five': 'Z5（最大）',
    }
    return labels.get(zone_key, zone_key)


# ============================================================
# 今日训练分析
# ============================================================

def analyze_today_workout(workout: Dict) -> Dict:
    """
    分析单条训练记录，生成结构化摘要

    Returns:
        {
            'sport': '跑步',
            'distance_km': 10.3,
            'duration_min': 60,
            'pace': '5:48',
            'strain': 16.0,
            'avg_hr': 146,
            'max_hr': 169,
            'calories_kj': 3141,
            'zones': {'Z2': 6.4, 'Z3': 24.0, 'Z4': 21.7, 'Z5': 0.7},
            'summary': '跑步 10.3km | 配速 5:48/km | 平均心率 146bpm',
            'heart_rate_zones_formatted': '...',
        }
    """
    score = workout.get('score', {})
    sport_key = workout.get('sport_name', 'unknown')
    sport = SPORT_LABELS.get(sport_key, sport_key)

    distance_m = score.get('distance_meter', 0)
    kj = score.get('kilojoule', 0)
    strain = score.get('strain', 0)
    avg_hr = score.get('average_heart_rate', 0)
    max_hr = score.get('max_heart_rate', 0)

    start = workout.get('start', '')
    end = workout.get('end', '')
    duration_min = _parse_duration_minutes(start, end)

    distance_km = round(distance_m / 1000, 1) if distance_m > 0 else None

    # 配速计算
    pace = None
    if distance_km and duration_min > 0 and sport_key == 'running':
        pace = _calc_pace(distance_m, duration_min)
    elif distance_km is None and kj > 0:
        est_dist = _estimate_distance_from_kj(kj, sport_key)
        if est_dist and duration_min > 0 and sport_key == 'running':
            pace = _calc_pace(est_dist * 1000, duration_min)

    # 心率区间
    zd = score.get('zone_durations', {})
    zones_min = {k.replace('_milli', ''): round(v / 60000, 1) for k, v in zd.items()}
    zones_formatted = []
    for k, v in zones_min.items():
        if v >= 1:
            zones_formatted.append(f"{_zone_label(k.replace('_milli',''))} {v:.0f}min")
    zones_str = ' | '.join(zones_formatted) if zones_formatted else '无区间数据'

    # 摘要文字
    summary_parts = [sport]
    if distance_km:
        summary_parts.append(f"{distance_km}km")
    if pace and pace != 'N/A':
        summary_parts.append(f"配速{pace}/km")
    if avg_hr:
        summary_parts.append(f"均心{avg_hr}bpm")
    if duration_min:
        summary_parts.append(f"{duration_min}min")
    summary = ' | '.join(summary_parts)

    return {
        'sport': sport,
        'sport_key': sport_key,
        'distance_km': distance_km,
        'duration_min': duration_min,
        'pace': pace,
        'strain': round(strain, 1),
        'avg_hr': avg_hr,
        'max_hr': max_hr,
        'calories_kj': round(kj),
        'zones': zones_min,
        'zones_formatted': zones_str,
        'summary': summary,
        'start_local': _to_local_time(start),
        'end_local': _to_local_time(end),
    }


def _to_local_time(iso_str: str) -> str:
    """将 UTC ISO 时间转北京时间（HH:MM 格式）"""
    return format_bj(iso_str, '%H:%M')


def get_today_workout_analysis() -> Optional[Dict]:
    """
    获取今日训练分析（仅返回今天北京时间的数据）

    北京时间今日 = UTC [今天08:00 ~ 明天07:59]
    （WHOOP 跑步数据在北京凌晨 00:00-08:00 同步，对应 UTC 前一天16:00-00:00）
    """
    workouts = get_today_workouts(days=2)
    today_workouts = [
        w for w in workouts
        if is_bj_today(w.get('start', ''))
    ]

    if not today_workouts:
        return None

    # 如果有多条，取 strain 最高的一条
    best = max(today_workouts, key=lambda w: w.get('score', {}).get('strain', 0))
    return analyze_today_workout(best)


# ============================================================
# 自动打卡预览生成
# ============================================================

def generate_checkin_preview(workout_analysis: Dict) -> str:
    """
    根据训练分析生成打卡预览消息
    用户确认后即可完成打卡
    """
    sport = workout_analysis['sport']
    dist = workout_analysis['distance_km']
    pace = workout_analysis['pace']
    avg_hr = workout_analysis['avg_hr']
    max_hr = workout_analysis['max_hr']
    strain = workout_analysis['strain']
    duration = workout_analysis['duration_min']
    zones = workout_analysis['zones_formatted']
    summary = workout_analysis['summary']

    # 心率区间标签
    zd = workout_analysis['zones']
    zone_parts = []
    for z in ['zone_two', 'zone_three', 'zone_four', 'zone_five']:
        mins = zd.get(z, 0)
        if mins >= 1:
            label = _zone_label(z)
            zone_parts.append(f"{label} {mins:.0f}min")

    lines = [
        f"📋 **初步打卡内容预览**\n",
        f"━━━━━━ auto-generated ━━━━━━\n",
        f"**类型**：{sport}\n",
    ]

    if dist:
        lines.append(f"**距离**：{dist}km\n")
    if pace and pace != 'N/A':
        lines.append(f"**配速**：{pace}/km\n")
    if duration:
        lines.append(f"**时长**：{duration}min\n")
    if avg_hr:
        lines.append(f"**平均心率**：{avg_hr}bpm\n")
    if max_hr:
        lines.append(f"**最大心率**：{max_hr}bpm\n")
    if zone_parts:
        lines.append(f"**心率区间**：{' / '.join(zone_parts)}\n")
    if strain:
        lines.append(f"**Strain**：{strain}\n")

    lines.extend([
        f"\n⏰ *数据来源：WHOOP 自动同步*\n",
        f"💬 *请告诉我感受如何，或直接回复「✅确认打卡」完成记录*\n",
    ])

    return ''.join(lines)


# ============================================================
# 无训练日打卡模板
# ============================================================

def generate_restday_preview() -> str:
    """生成休息日的打卡预览"""
    return (
        "📋 **今日打卡预览**\n\n"
        "━━━━━━ auto-generated ━━━━━━\n"
        "**类型**：休息/恢复\n\n"
        "💬 *今天是休息日，直接回复「✅确认打卡」即可*\n"
    )


# ============================================================
# WHOOP 睡眠数据查询（用于反馈学习）
# ============================================================

def get_today_sleep_data() -> Optional[Dict]:
    """获取今日睡眠数据（用于与用户反馈对比）"""
    try:
        result = subprocess.run(
            ['python3', 'scripts/whoop_data.py', 'sleep', '--days', '1'],
            capture_output=True, text=True,
            cwd=SKILL_DIR
        )
        if result.returncode != 0:
            return None
        data = json.loads(result.stdout)
        records = data.get('records', [])

        today_bj = today_str()
        for r in records:
            if today_bj in r.get('start', ''):
                score = r.get('score', {})
                stage = score.get('stage_summary', {})
                return {
                    'sleep_performance': score.get('sleep_performance_percentage', 0),
                    'sleep_efficiency': score.get('sleep_efficiency_percentage', 0),
                    'total_in_bed_hours': round(stage.get('total_in_bed_time_milli', 0) / 3600000, 1),
                    'total_awake_minutes': round(stage.get('total_awake_time_milli', 0) / 60000, 1),
                    'light_sleep_min': round(stage.get('total_light_sleep_time_milli', 0) / 60000, 0),
                    'deep_sleep_min': round(stage.get('total_slow_wave_sleep_time_milli', 0) / 60000, 0),
                    'rem_sleep_min': round(stage.get('total_rem_sleep_time_milli', 0) / 60000, 0),
                    'disturbance_count': stage.get('disturbance_count', 0),
                    'respiratory_rate': score.get('respiratory_rate', 0),
                    'sleep_consistency': score.get('sleep_consistency_percentage', 0),
                }
        return None
    except Exception:
        return None


# ============================================================
# 便捷函数
# ============================================================

def auto_checkin_data(user_id: str = "dongyi") -> Dict:
    """
    汇总自动打卡所需数据
    返回给 pusher 使用
    """
    workout = get_today_workout_analysis()
    sleep = get_today_sleep_data()

    has_workout = workout is not None
    strain = workout.get('strain', 0) if workout else 0

    return {
        'has_workout': has_workout,
        'workout': workout,
        'sleep': sleep,
        'strain': strain,
        'preview': generate_checkin_preview(workout) if has_workout else generate_restday_preview(),
        'workout_summary': workout.get('summary', '') if workout else '',
    }
