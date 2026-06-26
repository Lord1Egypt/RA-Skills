"""
LLM增强报告模块
生成真正由大模型驱动的个性化详细健康分析

使用方法:
from lib.enhanced_reports import EnhancedReports
report = EnhancedReports.morning_report()
"""

import os
import sys
from datetime import datetime
from lib.tz import now as bj_now, today_str
from typing import Dict, Optional, List

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, SKILL_DIR)


def _get_data(days: int = 7):
    """获取数据"""
    try:
        from lib.data_cleaner import get_whoop_data, get_today_data
        return get_whoop_data(days), get_today_data()
    except Exception:
        return {}, {}


def _get_llm_client():
    """获取LLM客户端"""
    try:
        from lib.llm import LLMClient
        client = LLMClient("enhanced_report")
        if client.config.api_key:
            return client
    except:
        pass
    return None


def _get_health_score():
    try:
        from lib.health_score import calculate_health_score
        return calculate_health_score()
    except:
        return {"score": 0, "grade": "N/A", "breakdown": {}}


def _get_ml_prediction():
    try:
        from lib.ml_predictor import predict_next_day
        return predict_next_day()
    except:
        return {"prediction": 50, "confidence": "low", "reason": "数据不足"}


def _get_comprehensive():
    try:
        from lib.comprehensive_analysis import generate_comprehensive
        return generate_comprehensive()
    except:
        return {}


def _get_tracker(user_id: str = "dongyi"):
    try:
        from lib.tracker import ProgressTracker
        return ProgressTracker(user_id)
    except:
        return None


def _get_goals(user_id: str = "dongyi"):
    try:
        from lib.goals import GoalsManager
        return GoalsManager(user_id)
    except:
        return None


def _get_marathon_goal(user_id: str = "dongyi"):
    try:
        from lib.goals import GoalsManager
        gm = GoalsManager(user_id)
        goals = gm.get_marathon_goals()
        for g in goals:
            if g.status == "active":
                return g
    except:
        pass
    return None


def _emoji_score(value: float, thresholds: tuple = (70, 50)) -> tuple:
    """根据阈值返回 emoji 和状态文字"""
    if value >= thresholds[0]:
        return "🟢", "良好"
    elif value >= thresholds[1]:
        return "🟡", "一般"
    else:
        return "🔴", "需关注"


def _format_trend(trend: str) -> str:
    """格式化趋势"""
    return {"up": "📈 上升", "down": "📉 下降", "stable": "➡️ 稳定"}.get(trend, "➡️ 稳定")


class EnhancedReports:

    @staticmethod
    def morning_report() -> str:
        summary, today = _get_data(7)
        health_score = _get_health_score()
        ml_pred = _get_ml_prediction()
        comprehensive = _get_comprehensive()
        tracker = _get_tracker()
        goals_mgr = _get_goals()

        recovery = today.get('recovery', 0)
        hrv = today.get('hrv', 0)
        rhr = today.get('rhr', 0)
        sleep_hours = today.get('sleep_hours', 0)
        date = today.get('date', today_str())

        avg_recovery = summary.get('avg_recovery', 0)
        avg_hrv = summary.get('avg_hrv', 0)
        avg_rhr = summary.get('avg_rhr', 0)
        avg_sleep = summary.get('avg_sleep_hours', 0)
        sleep_debt = summary.get('sleep_debt', 0)
        training_days = summary.get('training_days', 0)
        recovery_trend = summary.get('recovery_trend', 'stable')
        total_strain = summary.get('total_strain', 0)

        hs_score = health_score.get('score', 0)
        hs_breakdown = health_score.get('breakdown', {})
        hs_grade = health_score.get('grade', 'N/A')

        ml_p = ml_pred.get('prediction', 50)
        ml_conf = ml_pred.get('confidence', 'low')
        ml_reason = ml_pred.get('reason', '')

        comp = comprehensive
        body_battery = comp.get('body_battery', {})
        hz = comp.get('heart_zones', {})

        rec_emoji, rec_status = _emoji_score(recovery)
        hs_emoji, hs_status = _emoji_score(hs_score)
        ml_emoji, ml_status = _emoji_score(ml_p)

        streak = tracker.get_streak("dongyi") if tracker else 0
        weekly = tracker.get_weekly_summary("dongyi") if tracker else {}
        active_goals = goals_mgr.get_active_goals() if goals_mgr else []
        marathon_goal = _get_marathon_goal()

        llm_client = _get_llm_client()
        llm_section = ""
        if llm_client:
            try:
                prompt = EnhancedReports._build_llm_prompt(
                    summary, today, health_score, ml_pred, comprehensive,
                    tracker, goals_mgr, "morning"
                )
                result = llm_client.generate(prompt)
                if result and "error" not in result:
                    content = result.get("content", "")
                    if content:
                        llm_section = f"\n🤖 **AI教练深度分析**\n\n{content}\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            except Exception:
                pass

        msg = f"☀️ **今日健康早报** `{date}`\n\n"
        msg += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"

        if llm_section:
            msg += llm_section

        msg += "📊 **核心状态**\n\n"
        msg += f"• 恢复评分：{rec_emoji} **{recovery:.0f}%**（{rec_status}）\n"
        msg += f"• HRV：{hrv:.1f}ms\n"
        msg += f"• 静息心率：{rhr:.0f}bpm\n"
        msg += f"• 睡眠时长：{sleep_hours:.1f}h\n"
        if sleep_debt > 0:
            msg += f"• 睡眠债务：⚠️ {sleep_debt:.1f}h\n"
        msg += f"• 今日strain：{today.get('strain', 0):.1f}\n\n"

        msg += "🏆 **健康评分**\n\n"
        msg += f"• 综合评分：{hs_emoji} **{hs_score:.0f}/100**（{hs_grade}级）\n"
        if hs_breakdown:
            for k, v in hs_breakdown.items():
                label = {"recovery": "恢复", "sleep": "睡眠", "hrv": "HRV", "rhr": "心率"}.get(k, k)
                e, s = _emoji_score(v)
                msg += f"  • {label}：{e} {v:.0f}（{s}）\n"
        msg += "\n"

        msg += "🔮 **ML恢复预测**\n\n"
        msg += f"• 明日预测：{ml_emoji} **{ml_p:.0f}%**（{ml_status}）\n"
        msg += f"• 置信度：{ml_conf}\n"
        if ml_reason:
            msg += f"• 分析：{ml_reason}\n"
        msg += "\n"

        msg += "📈 **7天趋势**\n\n"
        msg += f"• 平均恢复：{avg_recovery:.1f}% {_format_trend(recovery_trend)}\n"
        msg += f"• 平均HRV：{avg_hrv:.1f}ms\n"
        msg += f"• 平均RHR：{avg_rhr:.0f}bpm\n"
        msg += f"• 平均睡眠：{avg_sleep:.1f}h\n"
        msg += f"• 7日总strain：{total_strain:.1f}\n"
        msg += f"• 训练天数：{training_days}天\n\n"

        if body_battery:
            bb = body_battery.get('level', 0)
            bb_emoji, bb_status = _emoji_score(bb, (80, 50))
            msg += "🔋 **身体电量**\n\n"
            msg += f"• 电量：{bb_emoji} **{bb:.0f}%**（{bb_status}）\n"
            msg += f"• 建议：{body_battery.get('suggestion', 'N/A')}\n\n"

        if marathon_goal:
            days_left = marathon_goal.days_until_race
            msg += "🏅 **马拉松目标**\n\n"
            msg += f"• 比赛：{marathon_goal.goal_name}\n"
            msg += f"• 目标：{marathon_goal.goal_time}（{marathon_goal.target_pace}/km）\n"
            msg += f"• 剩余：{days_left}天（{marathon_goal.training_phase}）\n\n"

        if tracker:
            msg += "📝 **打卡统计**\n\n"
            msg += f"• 连续打卡：{streak}天 🔥\n"
            if weekly:
                msg += f"• 本周打卡：{weekly.get('total_checkins', 0)}次\n"
                cr = weekly.get('completion_rate', 0)
                if cr > 0:
                    msg += f"• 完成率：{cr:.0f}%\n"
            msg += "\n"

        if active_goals:
            msg += "🎯 **当前目标**\n\n"
            for goal in active_goals[:3]:
                pct = (goal.current / goal.target * 100) if goal.target > 0 else 0
                msg += f"• {goal.goal_type}：{goal.current}/{goal.target} {goal.unit}（{pct:.0f}%）\n"
            msg += "\n"

        msg += "💡 **今日建议**\n\n"
        if recovery >= 80:
            msg += "✅ 身体状态极佳！今天适合高强度训练。\n"
        elif recovery >= 60:
            msg += "🟡 状态良好，可以进行中等强度训练。\n"
        elif recovery >= 40:
            msg += "🟠 恢复一般，建议以轻度活动为主。\n"
        else:
            msg += "🔴 恢复不足，今天建议完全休息。\n"
        msg += "\n"

        msg += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        msg += "📌 *训练后来打卡，记录训练内容和身体感受！*\n"
        msg += "⏰ *下次推送：18:00 晚间追踪*\n"

        return msg

    @staticmethod
    def evening_report() -> str:
        summary, today = _get_data(7)
        health_score = _get_health_score()
        ml_pred = _get_ml_prediction()
        comprehensive = _get_comprehensive()
        tracker = _get_tracker()
        goals_mgr = _get_goals()

        recovery = today.get('recovery', 0)
        strain = today.get('strain', 0)
        has_training = today.get('has_training', False)
        hrv = today.get('hrv', 0)
        rhr = today.get('rhr', 0)
        sleep_hours = today.get('sleep_hours', 0)
        date = today.get('date', today_str())

        avg_recovery = summary.get('avg_recovery', 0)
        sleep_debt = summary.get('sleep_debt', 0)
        training_days = summary.get('training_days', 0)
        recovery_trend = summary.get('recovery_trend', 'stable')

        hs_score = health_score.get('score', 0)
        ml_p = ml_pred.get('prediction', 50)
        ml_emoji, ml_status = _emoji_score(ml_p)

        comp = comprehensive
        hz = comp.get('heart_zones', {})
        body_battery = comp.get('body_battery', {})

        streak = tracker.get_streak("dongyi") if tracker else 0
        weekly = tracker.get_weekly_summary("dongyi") if tracker else {}
        marathon_goal = _get_marathon_goal()

        llm_client = _get_llm_client()
        llm_section = ""
        if llm_client:
            try:
                prompt = EnhancedReports._build_llm_prompt(
                    summary, today, health_score, ml_pred, comprehensive,
                    tracker, goals_mgr, "evening"
                )
                result = llm_client.generate(prompt)
                if result and "error" not in result:
                    content = result.get("content", "")
                    if content:
                        llm_section = f"\n🤖 **AI教练晚间总结**\n\n{content}\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            except Exception:
                pass

        if has_training and strain > 0:
            if strain >= 12:
                train_status = "💪 超高强度训练日"
                train_emoji = "🟢"
                train_effect = "有效提升力量和耐力"
            elif strain >= 8:
                train_status = "🏃 中高强度训练"
                train_emoji = "🟡"
                train_effect = "良好的训练刺激"
            else:
                train_status = "🚶 轻度活动"
                train_emoji = "🟠"
                train_effect = "保持身体活跃"
        else:
            train_status = "😴 今日休息"
            train_emoji = "🔴"
            train_effect = "充分休息，恢复能量"

        msg = f"🌙 **今日晚间追踪** `{date}`\n\n"
        msg += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"

        if llm_section:
            msg += llm_section

        msg += "📋 **今日训练总结**\n\n"
        msg += f"{train_emoji} {train_status}\n"
        msg += f"• strain：{strain:.1f}\n"
        msg += f"• 效果：{train_effect}\n"
        msg += f"• HRV：{hrv:.1f}ms\n"
        msg += f"• 静息心率：{rhr:.0f}bpm\n"
        msg += f"• 睡眠时长：{sleep_hours:.1f}h\n\n"

        rec_emoji, rec_status = _emoji_score(recovery)
        msg += "📊 **今日恢复**\n\n"
        msg += f"• 恢复评分：{rec_emoji} **{recovery:.0f}%**（{rec_status}）\n"
        msg += f"• 7日平均：{avg_recovery:.1f}%\n"
        msg += f"• 趋势：{_format_trend(recovery_trend)}\n"
        if sleep_debt > 2:
            msg += f"• ⚠️ 睡眠债务：{sleep_debt:.1f}h（建议今晚多睡）\n"
        msg += "\n"

        if body_battery:
            bb = body_battery.get('level', 0)
            bb_emoji, bb_status = _emoji_score(bb, (80, 50))
            msg += "🔋 **身体电量**\n\n"
            msg += f"• 电量：{bb_emoji} **{bb:.0f}%**（{bb_status}）\n"
            msg += f"• 建议：{body_battery.get('suggestion', 'N/A')}\n\n"

        if hz:
            msg += "💪 **心率区间**\n\n"
            msg += f"• 有氧区（Z2）：{hz.get('aerobic', 0):.1f}%\n"
            msg += f"• 无氧区（Z4+）：{hz.get('anaerobic', 0):.1f}%\n"
            msg += f"• 脂肪燃烧（Z1）：{hz.get('zone1', 0):.1f}%\n\n"

        if tracker:
            msg += "📝 **打卡统计**\n\n"
            msg += f"• 连续打卡：{streak}天 🔥\n"
            if weekly:
                msg += f"• 本周打卡：{weekly.get('total_checkins', 0)}次\n"
                cr = weekly.get('completion_rate', 0)
                if cr > 0:
                    msg += f"• 本周完成率：{cr:.0f}%\n"
            msg += "\n"

        if marathon_goal:
            msg += "🏅 **马拉松进度**\n\n"
            msg += f"• {marathon_goal.goal_name}：剩余{marathon_goal.days_until_race}天\n"
            msg += f"• 目标：{marathon_goal.goal_time}（{marathon_goal.target_pace}/km）\n"
            msg += f"• 阶段：{marathon_goal.training_phase}\n\n"

        msg += "🔮 **明日预测**\n\n"
        msg += f"• 预测恢复：{ml_emoji} **{ml_p:.0f}%**（{ml_status}）\n"
        if ml_p >= 70:
            msg += "✅ 明天状态不错，可以正常训练\n"
        elif ml_p >= 50:
            msg += "🟡 明天状态一般，建议中等强度\n"
        else:
            msg += "🔴 明天可能疲劳，建议休息\n"
        msg += "\n"

        msg += "😴 **睡眠建议**\n\n"
        if sleep_debt > 5:
            msg += f"⚠️ 睡眠债务{sleep_debt:.1f}h，今晚优先补觉！\n"
        elif sleep_debt > 2:
            msg += f"有{sleep_debt:.1f}h债务，建议比平时早睡30分钟。\n"
        elif recovery >= 70:
            msg += "恢复良好，保持当前睡眠节奏即可。\n"
        else:
            msg += "恢复不理想，今晚保证7-9小时睡眠。\n"
        msg += "\n"

        msg += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        msg += "📌 *记得20:00来打卡！*\n"
        msg += "⏰ *下次推送：22:00 完整日报*\n"

        return msg

    @staticmethod
    def full_report() -> str:
        summary, today = _get_data(7)
        health_score = _get_health_score()
        ml_pred = _get_ml_prediction()
        comprehensive = _get_comprehensive()
        tracker = _get_tracker()
        goals_mgr = _get_goals()

        recovery = today.get('recovery', 0)
        hrv = today.get('hrv', 0)
        rhr = today.get('rhr', 0)
        sleep_hours = today.get('sleep_hours', 0)
        strain = today.get('strain', 0)
        date = today.get('date', today_str())

        avg_recovery = summary.get('avg_recovery', 0)
        avg_hrv = summary.get('avg_hrv', 0)
        avg_rhr = summary.get('avg_rhr', 0)
        avg_sleep = summary.get('avg_sleep_hours', 0)
        sleep_debt = summary.get('sleep_debt', 0)
        training_days = summary.get('training_days', 0)
        total_strain = summary.get('total_strain', 0)
        recovery_count = summary.get('recovery_count', 0)
        recovery_trend = summary.get('recovery_trend', 'stable')

        hs_score = health_score.get('score', 0)
        hs_breakdown = health_score.get('breakdown', {})
        hs_grade = health_score.get('grade', 'N/A')
        ml_p = ml_pred.get('prediction', 50)
        ml_conf = ml_pred.get('confidence', 'low')
        ml_reason = ml_pred.get('reason', '')
        ml_emoji, ml_status = _emoji_score(ml_p)

        comp = comprehensive
        hz = comp.get('heart_zones', {})
        ss_data = comp.get('sleep_stages', {})
        bb = comp.get('body_battery', {})
        resp = comp.get('respiratory', {})
        pred_acc = comp.get('prediction_accuracy', {})

        streak = tracker.get_streak("dongyi") if tracker else 0
        weekly = tracker.get_weekly_summary("dongyi") if tracker else {}
        marathon_goal = _get_marathon_goal()
        active_goals = goals_mgr.get_active_goals() if goals_mgr else []

        llm_client = _get_llm_client()
        llm_section = ""
        if llm_client:
            try:
                prompt = EnhancedReports._build_llm_prompt(
                    summary, today, health_score, ml_pred, comprehensive,
                    tracker, goals_mgr, "full"
                )
                result = llm_client.generate(prompt)
                if result and "error" not in result:
                    content = result.get("content", "")
                    if content:
                        llm_section = f"\n🤖 **AI教练综合分析**\n\n{content}\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            except Exception:
                pass

        msg = f"🌙 **今日完整健康日报** `{date}`\n\n"
        msg += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"

        if llm_section:
            msg += llm_section

        rec_emoji, rec_status = _emoji_score(recovery)
        hs_emoji, hs_status = _emoji_score(hs_score)

        msg += "📊 **核心指标**\n\n"
        msg += f"• 恢复评分：{rec_emoji} **{recovery:.0f}%**（{rec_status}）\n"
        msg += f"• HRV：{hrv:.1f}ms\n"
        msg += f"• 静息心率：{rhr:.0f}bpm\n"
        msg += f"• 睡眠时长：{sleep_hours:.1f}h\n"
        msg += f"• 今日strain：{strain:.1f}\n"
        msg += f"• 健康评分：{hs_emoji} **{hs_score:.0f}/100**（{hs_grade}级）\n\n"

        if hs_breakdown:
            msg += "🏆 **健康评分构成**\n\n"
            for k, v in hs_breakdown.items():
                label = {"recovery": "恢复", "sleep": "睡眠", "hrv": "HRV", "rhr": "心率"}.get(k, k)
                e, s = _emoji_score(v)
                msg += f"  • {label}：{e} {v:.0f}（{s}）\n"
            msg += "\n"

        msg += "📈 **7天统计**\n\n"
        msg += f"• 平均恢复：{avg_recovery:.1f}% {_format_trend(recovery_trend)}\n"
        msg += f"• 平均HRV：{avg_hrv:.1f}ms\n"
        msg += f"• 平均RHR：{avg_rhr:.0f}bpm\n"
        msg += f"• 平均睡眠：{avg_sleep:.1f}h\n"
        msg += f"• 7日总strain：{total_strain:.1f}\n"
        msg += f"• 训练天数：{training_days}天\n"
        msg += f"• 有效数据：{recovery_count}条\n"
        if sleep_debt > 0:
            msg += f"• 睡眠债务：⚠️ {sleep_debt:.1f}h\n"
        msg += "\n"

        ss = ss_data.get('percentages', {})
        if ss:
            msg += "😴 **睡眠结构**\n\n"
            for stage, pct in ss.items():
                stage_name = {"light": "浅睡眠", "deep": "深睡眠", "rem": "REM睡眠"}.get(stage, stage)
                msg += f"• {stage_name}：{pct:.0f}%\n"
            msg += "\n"

        if resp:
            rr = resp.get('respiratory_rate', 0)
            if rr > 0:
                msg += "🫁 **呼吸**\n\n"
                msg += f"• 呼吸频率：{rr:.1f}次/分钟"
                if rr > 20:
                    msg += "（略高）\n"
                elif rr < 12:
                    msg += "（正常偏低）\n"
                else:
                    msg += "（正常）\n"
                msg += "\n"

        if hz:
            msg += "💪 **心率区间**\n\n"
            zone0_1 = hz.get('zone0', 0) + hz.get('zone1', 0)
            msg += f"• 轻松区（Z0-Z1）：{zone0_1:.1f}%\n"
            msg += f"• 有氧区（Z2-Z3）：{hz.get('aerobic', 0):.1f}%\n"
            msg += f"• 无氧区（Z4-Z5）：{hz.get('anaerobic', 0):.1f}%\n\n"

        if bb:
            bb_val = bb.get('level', 0)
            bb_emoji, bb_status = _emoji_score(bb_val, (80, 50))
            msg += "🔋 **身体电量**\n\n"
            msg += f"• 当前电量：{bb_emoji} **{bb_val:.0f}%**（{bb_status}）\n"
            msg += f"• 建议：{bb.get('suggestion', 'N/A')}\n\n"

        msg += "🔮 **ML恢复预测**\n\n"
        msg += f"• 明日预测：{ml_emoji} **{ml_p:.0f}%**（{ml_status}）\n"
        msg += f"• 置信度：{ml_conf}\n"
        if ml_reason:
            msg += f"• 判断依据：{ml_reason}\n"
        predictions = ml_pred.get('predictions', [])
        if predictions:
            msg += "• 未来趋势：\n"
            for i, p in enumerate(predictions[:7], 1):
                e = "🟢" if p >= 70 else "🟡" if p >= 50 else "🔴"
                msg += f"  第{i}天：{p:.0f}% {e}\n"
        if pred_acc:
            acc = pred_acc.get('accuracy', 0)
            if acc > 0:
                msg += f"• 模型准确率：{acc:.0f}%\n"
        msg += "\n"

        if tracker:
            msg += "📝 **打卡统计**\n\n"
            msg += f"• 连续打卡：{streak}天 🔥\n"
            if weekly:
                msg += f"• 本周打卡：{weekly.get('total_checkins', 0)}次\n"
                cr = weekly.get('completion_rate', 0)
                if cr > 0:
                    msg += f"• 本周完成率：{cr:.0f}%\n"
            msg += "\n"

        if marathon_goal:
            msg += "🏅 **马拉松目标**\n\n"
            msg += f"• {marathon_goal.goal_name} | {marathon_goal.race_type}\n"
            msg += f"• 目标：{marathon_goal.goal_time}（{marathon_goal.target_pace}/km）\n"
            msg += f"• 剩余：{marathon_goal.days_until_race}天\n"
            msg += f"• 阶段：{marathon_goal.training_phase}\n\n"

        if active_goals:
            msg += "🎯 **活跃目标**\n\n"
            for goal in active_goals:
                pct = (goal.current / goal.target * 100) if goal.target > 0 else 0
                msg += f"• {goal.goal_type}：{goal.current}/{goal.target} {goal.unit}（{pct:.0f}%）\n"
            msg += "\n"

        msg += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        msg += f"_数据来源：WHOOP | 健康糕_\n"
        msg += f"_生成时间：{bj_now().strftime('%Y-%m-%d %H:%M:%S')}_\n"

        return msg

    @staticmethod
    def _build_llm_prompt(summary, today, health_score, ml_pred, comprehensive,
                         tracker, goals_mgr, report_type: str) -> str:
        """构建 LLM 分析 prompt"""

        recovery = today.get('recovery', 0)
        hrv = today.get('hrv', 0)
        rhr = today.get('rhr', 0)
        sleep_hours = today.get('sleep_hours', 0)
        strain = today.get('strain', 0)
        sleep_debt = summary.get('sleep_debt', 0)
        training_days = summary.get('training_days', 0)
        avg_recovery = summary.get('avg_recovery', 0)
        avg_hrv = summary.get('avg_hrv', 0)
        avg_sleep = summary.get('avg_sleep_hours', 0)
        recovery_trend = summary.get('recovery_trend', 'stable')
        total_strain = summary.get('total_strain', 0)

        hs_score = health_score.get('score', 0)
        hs_grade = health_score.get('grade', 'N/A')
        ml_p = ml_pred.get('prediction', 50)
        ml_reason = ml_pred.get('reason', '')
        ml_conf = ml_pred.get('confidence', 'low')

        comp = comprehensive
        hz = comp.get('heart_zones', {})
        body_battery = comp.get('body_battery', {})
        bb = body_battery.get('level', 0) if body_battery else 0

        streak = tracker.get_streak("dongyi") if tracker else 0

        active_goals = goals_mgr.get_active_goals() if goals_mgr else []
        marathon_goal = _get_marathon_goal()

        goals_text = "\n".join([
            f"- {g.goal_type}：{g.current}/{g.target} {g.unit}"
            for g in active_goals[:3]
        ]) or "暂无"

        marathon_text = ""
        if marathon_goal:
            marathon_text = f"""
马拉松目标：
- 比赛：{marathon_goal.goal_name}（{marathon_goal.race_type}）
- 目标：{marathon_goal.goal_time}（{marathon_goal.target_pace}/km）
- 剩余：{marathon_goal.days_until_race}天
- 阶段：{marathon_goal.training_phase}"""

        base_data = f"""【用户今日数据】
- 恢复评分：{recovery:.0f}%
- HRV：{hrv:.1f}ms
- 静息心率：{rhr:.0f}bpm
- 睡眠时长：{sleep_hours:.1f}h
- 睡眠债务：{sleep_debt:.1f}h
- 今日strain：{strain:.1f}
- 本周训练天数：{training_days}天
- 7日平均恢复：{avg_recovery:.1f}%
- 7日平均HRV：{avg_hrv:.1f}ms
- 7日平均睡眠：{avg_sleep:.1f}h
- 恢复趋势：{recovery_trend}
- 健康评分：{hs_score:.0f}/100（{hs_grade}级）
- ML预测明日：{ml_p:.0f}%（置信度：{ml_conf}）
- ML判断依据：{ml_reason}
- 身体电量：{bb:.0f}%
- 连续打卡：{streak}天
- 心率区间：有氧{hz.get('aerobic', 0):.1f}% / 无氧{hz.get('anaerobic', 0):.1f}%

【当前目标】
{goals_text}
{marathon_text}"""

        if report_type == "morning":
            return f"""你是专业且温暖的AI健身教练，根据以下用户数据生成详细的早安分析报告：

{base_data}

请生成300-400字的中文分析，包括：
1. 对用户当前状态的详细解读（特别是恢复、HRV、身心状态）
2. 哪些指标需要特别关注（如果有）
3. 具体的、可执行的今日训练建议
4. 关怀和鼓励的话语

语气：专业、温暖、像了解用户的私人教练一样。直接给出分析内容，不要说"根据数据..."这类开场白。"""

        elif report_type == "evening":
            has_training = today.get('has_training', False)
            return f"""你是专业且温暖的个人健身教练，根据以下数据生成晚间总结和明日建议：

{base_data}

【今日训练】：{"有" if has_training else "无"}（strain: {strain:.1f}）

请生成300-400字的中文总结，包括：
1. 对今日训练/休息的评价
2. 恢复效果评估
3. 明日身体状态预测和具体训练建议
4. 睡眠和恢复指导

语气：专业、支持、激励。直接给出内容。"""

        else:
            return f"""你是专业且全面的AI健身教练，根据以下完整数据生成综合健康日报：

{base_data}

请生成500-600字的中文综合分析，包括：
1. 整体健康状态评估
2. 各指标详细解读（恢复、睡眠、HRV、训练负荷）
3. 发现的问题和潜在风险
4. 具体改进建议
5. 接下来的行动计划

语气：专业、详细、有洞察力。直接给出内容。"""


def get_morning_report() -> str:
    return EnhancedReports.morning_report()


def get_evening_report() -> str:
    return EnhancedReports.evening_report()


def get_full_report() -> str:
    return EnhancedReports.full_report()
