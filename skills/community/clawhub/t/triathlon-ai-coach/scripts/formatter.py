# coding: utf-8
# formatter.py - 格式化输出模块
# ⚠️ 本模块为 trainer.py 拆分，原函数已迁移至此

# 导入依赖模块
import json, os, subprocess
from pathlib import Path

# ── 从 plan_engine 导入 ──
from pathlib import Path
import json as _json

# ── 反馈模块 ──
try:
    from feedback_manager import get_preferences
except:
    get_preferences = None

try:
    from plan_engine import get_training_zones, load_config
except ImportError:
    # 向后兼容
    def load_config(): pass
    def get_training_zones(cfg): return {}

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
        ctl = fitness.get('ctl', '-')
        tsb = fitness.get('tsb', '-')
        status = "疲劳积累" if fitness.get('tsb', 0) < -10 else "状态良好"
        content += f"""
📊 **体能状态：** CTL {ctl} | TSB {tsb} | {status}
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
        emoji = "😴" if isinstance(readiness, str) and int(readiness or 0) < 40 else ("😐" if isinstance(readiness, str) and int(readiness or 0) < 60 else "💪")
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

    # ── 教练建议 ──
    try:
        from plan_engine import get_coach_tip_for_plan
        tips = get_coach_tip_for_plan(plan)
        if tips:
            for t in tips:
                content += f"\n🎯 教练建议：{t}"
            content += "\n"
    except Exception:
        pass

# ── 加反馈提示 ──
    try:
        if get_preferences:
            prefs = get_preferences()
            sat = prefs.get("satisfaction_rate", 0)
            if sat > 0:
                content += f"\n📝 **近期满意度: {sat}%**\n"
    except:
        pass
    
    content += "\n━━━━━━━━━━━━━━━━\n"
    content += "\n📌 **今日计划满意吗？**\n"
    content += "回复「👍满意」或「👎不满意」帮我优化\n"
    content += "\n"
    
    return content


