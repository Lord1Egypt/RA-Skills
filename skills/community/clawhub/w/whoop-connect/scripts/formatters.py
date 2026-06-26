#!/usr/bin/env python3
"""Output formatters for WHOOP data. Respects user config for language and detail level."""

import json
import os

CONFIG_PATH = os.path.expanduser("~/.whoop/config.json")


def _load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH) as f:
            return json.load(f)
    return {"language": "en", "detail_level": "compact", "units": "metric",
            "trend_comparison": True, "training_advice": True}


def _ms_to_hm(ms):
    """Convert milliseconds to 'Xh Ym' string."""
    if ms is None:
        return "N/A"
    minutes = int(ms / 60000)
    h, m = divmod(minutes, 60)
    if h > 0:
        return f"{h}h {m}m"
    return f"{m}m"


def _recovery_emoji(score):
    if score is None:
        return ""
    if score >= 67:
        return "🟢"
    if score >= 34:
        return "🟡"
    return "🔴"


def _strain_level(strain):
    if strain is None:
        return ""
    if strain >= 18:
        return "Overreaching" if _lang() == "en" else "过度"
    if strain >= 14:
        return "High" if _lang() == "en" else "高"
    if strain >= 10:
        return "Medium" if _lang() == "en" else "中"
    return "Light" if _lang() == "en" else "轻"


_config_cache = None

def _cfg():
    global _config_cache
    if _config_cache is None:
        _config_cache = _load_config()
    return _config_cache


def _lang():
    return _cfg().get("language", "en")


def _detailed():
    return _cfg().get("detail_level", "compact") == "detailed"


def _t(en, zh):
    return zh if _lang() == "zh" else en


# --- Recovery ---

def format_recovery(data, compact_override=None):
    score = data.get("score") or {}
    state = data.get("score_state", "")
    is_compact = compact_override if compact_override is not None else not _detailed()

    if state != "SCORED":
        return _t(f"Recovery: {state}", f"恢复: {state}")

    rs = score.get("recovery_score")
    hrv = score.get("hrv_rmssd_milli")
    rhr = score.get("resting_heart_rate")
    spo2 = score.get("spo2_percentage")
    temp = score.get("skin_temp_celsius")
    cal = score.get("user_calibrating")

    emoji = _recovery_emoji(rs)

    if is_compact:
        parts = [f"{emoji} Recovery: {rs:.0f}%"]
        if hrv is not None:
            parts.append(f"HRV: {hrv:.0f}ms")
        if rhr is not None:
            parts.append(f"RHR: {rhr:.0f}bpm")
        if spo2 is not None:
            parts.append(f"SpO2: {spo2:.0f}%")
        return " | ".join(parts)

    lines = [
        f"{emoji} {_t('Recovery Report', '恢复报告')}",
        f"  {_t('Recovery Score', '恢复分数')}: {rs:.0f}%",
        f"  {_t('HRV (RMSSD)', 'HRV (RMSSD)')}: {hrv:.1f} ms" if hrv else None,
        f"  {_t('Resting HR', '静息心率')}: {rhr:.0f} bpm" if rhr else None,
        f"  {_t('SpO2', '血氧')}: {spo2:.0f}%" if spo2 else None,
        f"  {_t('Skin Temp', '皮肤温度')}: {temp:.1f}°C" if temp else None,
        f"  {_t('Calibrating', '校准中')}: {_t('Yes', '是')}" if cal else None,
    ]
    return "\n".join(l for l in lines if l is not None)


# --- Sleep ---

def format_sleep(data, compact_override=None):
    score = data.get("score") or {}
    state = data.get("score_state", "")
    is_nap = data.get("nap", False)
    is_compact = compact_override if compact_override is not None else not _detailed()

    label = _t("Nap", "午睡") if is_nap else _t("Sleep", "睡眠")

    if state != "SCORED":
        return f"{label}: {state}"

    stage = score.get("stage_summary") or {}
    needed = score.get("sleep_needed") or {}

    total = stage.get("total_in_bed_time_milli")
    deep = stage.get("total_slow_wave_sleep_time_milli")
    rem = stage.get("total_rem_sleep_time_milli")
    light = stage.get("total_light_sleep_time_milli")
    awake = stage.get("total_awake_time_milli")
    perf = score.get("sleep_performance_percentage")
    eff = score.get("sleep_efficiency_percentage")
    cons = score.get("sleep_consistency_percentage")
    rr = score.get("respiratory_rate")
    dist = stage.get("disturbance_count")
    cycles = stage.get("sleep_cycle_count")

    if is_compact:
        parts = [f"😴 {label}: {_ms_to_hm(total)}"]
        if perf is not None:
            parts.append(f"Perf: {perf:.0f}%")
        if deep is not None:
            parts.append(f"Deep: {_ms_to_hm(deep)}")
        if rem is not None:
            parts.append(f"REM: {_ms_to_hm(rem)}")
        return " | ".join(parts)

    baseline = needed.get("baseline_milli")
    debt = needed.get("need_from_sleep_debt_milli")
    strain_need = needed.get("need_from_recent_strain_milli")
    nap_adj = needed.get("need_from_recent_nap_milli")

    lines = [
        f"😴 {_t('Sleep Report', '睡眠报告')}" + (f" ({_t('Nap', '午睡')})" if is_nap else ""),
        f"  {_t('Total', '总时长')}: {_ms_to_hm(total)}",
        f"  {_t('Deep', '深睡')}: {_ms_to_hm(deep)}",
        f"  {_t('REM', 'REM')}: {_ms_to_hm(rem)}",
        f"  {_t('Light', '浅睡')}: {_ms_to_hm(light)}",
        f"  {_t('Awake', '清醒')}: {_ms_to_hm(awake)}",
        f"  {_t('Cycles', '周期数')}: {cycles}" if cycles is not None else None,
        f"  {_t('Disruptions', '中断次数')}: {dist}" if dist is not None else None,
        f"  {_t('Performance', '表现')}: {perf:.0f}%" if perf is not None else None,
        f"  {_t('Efficiency', '效率')}: {eff:.0f}%" if eff is not None else None,
        f"  {_t('Consistency', '一致性')}: {cons:.0f}%" if cons is not None else None,
        f"  {_t('Respiratory Rate', '呼吸频率')}: {rr:.1f}/min" if rr is not None else None,
        "",
        f"  {_t('Sleep Need', '睡眠需求')}:" if baseline else None,
        f"    {_t('Baseline', '基线')}: {_ms_to_hm(baseline)}" if baseline else None,
        f"    {_t('Sleep Debt', '睡眠债')}: +{_ms_to_hm(debt)}" if debt else None,
        f"    {_t('Strain Load', '训练负荷')}: +{_ms_to_hm(strain_need)}" if strain_need else None,
        f"    {_t('Nap Adj', '午睡调整')}: {_ms_to_hm(nap_adj)}" if nap_adj else None,
    ]
    return "\n".join(l for l in lines if l is not None)


# --- Workout ---

def format_workout(data, compact_override=None):
    score = data.get("score") or {}
    state = data.get("score_state", "")
    sport = data.get("sport_name", "Unknown")
    is_compact = compact_override if compact_override is not None else not _detailed()

    if state != "SCORED":
        return f"🏋️ {sport}: {state}"

    strain = score.get("strain")
    avg_hr = score.get("average_heart_rate")
    max_hr = score.get("max_heart_rate")
    kj = score.get("kilojoule")
    dist = score.get("distance_meter")
    alt = score.get("altitude_gain_meter")
    pct = score.get("percent_recorded")

    kcal = kj * 0.239006 if kj else None

    if is_compact:
        parts = [f"🏋️ {sport}"]
        if strain is not None:
            parts.append(f"Strain: {strain:.1f} ({_strain_level(strain)})")
        if kcal is not None:
            parts.append(f"{kcal:.0f} kcal")
        if avg_hr is not None:
            parts.append(f"HR: {avg_hr}/{max_hr or '?'}")
        if dist is not None and dist > 0:
            parts.append(f"{dist/1000:.1f} km")
        return " | ".join(parts)

    zones = score.get("zone_durations") or {}
    zone_names = [
        ("zone_zero_milli", _t("Rest", "休息")),
        ("zone_one_milli", _t("Very Light", "极轻")),
        ("zone_two_milli", _t("Light", "轻度")),
        ("zone_three_milli", _t("Moderate", "中度")),
        ("zone_four_milli", _t("Hard", "高强度")),
        ("zone_five_milli", _t("Max", "极限")),
    ]

    lines = [
        f"🏋️ {_t('Workout Report', '运动报告')}: {sport}",
        f"  {_t('Strain', 'Strain')}: {strain:.1f} ({_strain_level(strain)})" if strain is not None else None,
        f"  {_t('Avg HR', '平均心率')}: {avg_hr} bpm" if avg_hr else None,
        f"  {_t('Max HR', '最大心率')}: {max_hr} bpm" if max_hr else None,
        f"  {_t('Energy', '能量')}: {kcal:.0f} kcal ({kj:.0f} kJ)" if kcal else None,
        f"  {_t('Distance', '距离')}: {dist/1000:.2f} km" if dist and dist > 0 else None,
        f"  {_t('Elevation Gain', '累计爬升')}: {alt:.0f} m" if alt and alt > 0 else None,
        f"  {_t('Data Coverage', '数据完整度')}: {pct:.0f}%" if pct is not None else None,
        "",
        f"  {_t('HR Zones', '心率区间')}:",
    ]
    for key, name in zone_names:
        ms = zones.get(key)
        if ms and ms > 0:
            lines.append(f"    {name}: {_ms_to_hm(ms)}")

    return "\n".join(l for l in lines if l is not None)


# --- Cycle ---

def format_cycle(data, compact_override=None):
    score = data.get("score") or {}
    state = data.get("score_state", "")
    is_compact = compact_override if compact_override is not None else not _detailed()

    if state != "SCORED":
        date = data.get("start", "")[:10]
        return f"📊 Cycle {date}: {state}"

    strain = score.get("strain")
    kj = score.get("kilojoule")
    avg_hr = score.get("average_heart_rate")
    max_hr = score.get("max_heart_rate")
    date = data.get("start", "")[:10]
    kcal = kj * 0.239006 if kj else None

    if is_compact:
        parts = [f"📊 {date}"]
        if strain is not None:
            parts.append(f"Strain: {strain:.1f}")
        if kcal is not None:
            parts.append(f"{kcal:.0f} kcal")
        if avg_hr is not None:
            parts.append(f"HR: {avg_hr}/{max_hr or '?'}")
        return " | ".join(parts)

    lines = [
        f"📊 {_t('Daily Cycle', '日周期')}: {date}",
        f"  {_t('Strain', 'Strain')}: {strain:.1f} ({_strain_level(strain)})" if strain is not None else None,
        f"  {_t('Energy', '能量')}: {kcal:.0f} kcal" if kcal else None,
        f"  {_t('Avg HR', '平均心率')}: {avg_hr} bpm" if avg_hr else None,
        f"  {_t('Max HR', '最大心率')}: {max_hr} bpm" if max_hr else None,
    ]
    return "\n".join(l for l in lines if l is not None)


# --- Profile ---

def format_profile(data):
    lines = [
        f"👤 {data.get('first_name', '')} {data.get('last_name', '')}",
        f"  Email: {data.get('email', 'N/A')}",
        f"  User ID: {data.get('user_id', 'N/A')}",
    ]
    return "\n".join(lines)


# --- Trends ---

def format_trends(results, days):
    lines = [_t(f"Trends ({days} days)", f"趋势 ({days} 天)"), ""]
    units = {
        "recovery_score": "%", "hrv": "ms", "resting_hr": "bpm",
        "spo2": "%", "skin_temp": "°C", "strain": "",
        "sleep_duration": "ms", "sleep_efficiency": "%",
    }
    names_en = {
        "recovery_score": "Recovery", "hrv": "HRV", "resting_hr": "Resting HR",
        "spo2": "SpO2", "skin_temp": "Skin Temp", "strain": "Strain",
        "sleep_duration": "Sleep Duration", "sleep_efficiency": "Sleep Efficiency",
    }
    names_zh = {
        "recovery_score": "恢复", "hrv": "HRV", "resting_hr": "静息心率",
        "spo2": "血氧", "skin_temp": "皮肤温度", "strain": "Strain",
        "sleep_duration": "睡眠时长", "sleep_efficiency": "睡眠效率",
    }
    names = names_zh if _lang() == "zh" else names_en

    trend_labels = {
        "improving": _t("↑ improving", "↑ 上升"),
        "declining": _t("↓ declining", "↓ 下降"),
        "stable": _t("→ stable", "→ 稳定"),
        "insufficient_data": _t("? insufficient data", "? 数据不足"),
    }

    for metric, data in results.items():
        if data.get("count", 0) == 0:
            continue
        name = names.get(metric, metric)
        unit = units.get(metric, "")
        mean = data["mean"]
        trend = trend_labels.get(data.get("trend", ""), "")

        if metric == "sleep_duration":
            mean_str = _ms_to_hm(mean)
        else:
            mean_str = f"{mean:.1f}{unit}"

        lines.append(f"  {name}: {mean_str} {trend} (n={data['count']})")

    return "\n".join(lines)
