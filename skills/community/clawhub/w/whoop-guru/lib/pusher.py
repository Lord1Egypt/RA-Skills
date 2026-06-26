"""
主动推送模块
负责教练推送的时间调度和消息生成

三个推送各有侧重：
- 09:00: 今日训练建议 + 个性化教练洞察 + 目标进度
- 18:00: 明日训练计划 + 教练反馈 + 打卡统计
- 20:00: 打卡激励 + 训练记录

整合所有模块：
- health_score: 综合健康评分
- ml_predictor: ML预测
- comprehensive_analysis: 综合分析
- health_advisor: 健康顾问洞察
- dynamic_planner: 动态训练规划
- goals: 目标追踪
- tracker: 进度追踪
- data_cleaner: WHOOP数据
"""

import os
import sys
from datetime import datetime, time
from lib.tz import now as bj_now
from typing import List, Optional

# 设置路径
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, SKILL_DIR)

from lib.data_cleaner import get_whoop_data, get_today_data

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
        return {"prediction": 50, "confidence": "low", "reason": ""}

def _get_comprehensive():
    try:
        from lib.comprehensive_analysis import generate_comprehensive
        return generate_comprehensive()
    except:
        return {"heart_zones": {}, "sleep_stages": {}, "body_battery": {}, "hrv_trend": {}}

def _get_health_advisor():
    try:
        from lib.health_advisor import generate_health_report
        return generate_health_report()
    except:
        return {"overall_score": 0, "insights": [], "training_recommendation": {"message": ""}}

def _get_dynamic_planner():
    try:
        from lib.dynamic_planner import DynamicPlanner
        return DynamicPlanner()
    except:
        return None

def _get_goals(user_id: str = "dongyi"):
    try:
        from lib.goals import GoalsManager
        return GoalsManager(user_id)
    except:
        return None

def _get_tracker():
    try:
        from lib.tracker import ProgressTracker
        return ProgressTracker()
    except:
        return None


class CoachPushMessage:
    """教练推送消息生成"""
    
    @staticmethod
    def morning() -> str:
        """
        09:00 早安推送 - AI教练视角 + 目标进度
        """
        today = get_today_data()
        summary = get_whoop_data(7)
        health_score = _get_health_score()
        ml_pred = _get_ml_prediction()
        comprehensive = _get_comprehensive()
        advisor = _get_health_advisor()
        planner = _get_dynamic_planner()
        
        recovery = today.get('recovery', 0)
        hrv = today.get('hrv', 0)
        rhr = today.get('rhr', 0)
        sleep_hours = today.get('sleep_hours', 0)
        avg_recovery = summary.get('avg_recovery', 0)
        training_days = summary.get('training_days', 0)
        sleep_debt = summary.get('sleep_debt', 0)
        
        hs_score = health_score.get('score', 0)
        ml_p = ml_pred.get('prediction', 50)
        
        # ========== LLM分析 ==========
        user_data = {
            "recovery": recovery,
            "hrv": hrv,
            "rhr": rhr,
            "sleep_hours": sleep_hours,
            "strain": today.get('strain', 0),
            "sleep_debt": sleep_debt,
            "training_days": training_days,
            "avg_recovery": avg_recovery,
            "avg_hrv": summary.get('avg_hrv', 0),
            "health_score": hs_score,
            "ml_prediction": ml_p,
        }
        llm_analysis = _get_llm_analysis(user_data, "morning")
        
        # ========== AI教练状态评估 ==========
        if recovery >= 80:
            coach_mood, coach_vibe = "🎉 太棒了！", "今天你的身体状态处于最佳区间，作为你的教练，我为你感到骄傲！"
        elif recovery >= 60:
            coach_mood, coach_vibe = "💪 状态不错！", "今天你的身体状态良好，神经系统运作正常。这是适合训练的日子。"
        elif recovery >= 40:
            coach_mood, coach_vibe = "🤔 恢复一般", "作为你的教练，我认为今天需要注意一下。建议降低强度，以身体感受为主。"
        else:
            coach_mood, coach_vibe = "🛋️ 建议休息", "亲爱的，我必须诚实告诉你：今天的身体状态不适合训练。休息不是软弱。"
        
        # ========== 训练建议 ==========
        if recovery >= 80:
            plan_type, plan_desc, plan_strain = "全力以赴日", "今天适合高强度训练", "12-15"
            exercises = ["力量训练（胸/背/腿）", "间歇跑", "HIIT"]
            coach_tip = "这是你展现训练成果的日子！全力以赴。"
        elif recovery >= 60:
            plan_type, plan_desc, plan_strain = "稳定进步日", "今天适合中等强度训练", "8-12"
            exercises = ["跑步（中等配速）", "力量训练", "游泳"]
            coach_tip = "稳扎稳打是进步的关键。"
        elif recovery >= 40:
            plan_type, plan_desc, plan_strain = "轻量活动日", "今天建议以轻度活动为主", "5-8"
            exercises = ["瑜伽/拉伸", "散步", "轻松骑行"]
            coach_tip = "倾听身体的声音。今天的活动重点是激活肌肉。"
        else:
            plan_type, plan_desc, plan_strain = "完全休息日", "今天身体需要休息", "0-3"
            exercises = ["充分睡眠", "轻度拉伸", "冥想放松"]
            coach_tip = "休息也是训练的一部分。今天就让自己完全恢复吧。"
        
        # ========== HRV解读 ==========
        if hrv >= 60:
            hrv_coach = "你的HRV非常出色（{}ms），说明神经系统非常健康。".format(int(hrv))
        elif hrv >= 40:
            hrv_coach = "HRV处于正常范围（{}ms），身体状态稳定。".format(int(hrv))
        elif hrv >= 25:
            hrv_coach = "HRV偏低（{}ms），可能近期有一些疲劳累积。".format(int(hrv))
        else:
            hrv_coach = "HRV较低（{}ms），强烈建议休息！".format(int(hrv))
        
        # ========== 本周回顾 ==========
        if training_days >= 6:
            week_review = "本周你已经训练了{}天，训练量较大。建议适当休息1-2天。".format(training_days)
        elif training_days >= 4:
            week_review = "本周你训练了{}天，节奏不错。继续坚持！".format(training_days)
        else:
            week_review = "本周你只训练了{}天，如果状态好可以适当加练。".format(training_days)
        
        # ========== 动态规划 ==========
        dynamic_rec = ""
        if planner:
            dp_rec = planner.get_recommended_intensity()
            dp_status = planner.get_current_status()
            dynamic_rec = "动态规划建议：{} - {}".format(
                dp_rec.get('intensity', 'N/A'),
                dp_rec.get('description', '')
            )
        
        # ========== 目标进度 ==========
        goals_section = ""
        goals_manager = _get_goals()
        if goals_manager:
            active_goals = goals_manager.get_active_goals()
            if active_goals:
                goals_section = "\n🎯 **当前目标进度**\n\n"
                for goal in active_goals[:3]:  # 最多显示3个
                    progress = (goal.current / goal.target * 100) if goal.target > 0 else 0
                    goals_section += "• {}：{:.0f}{} / {:.0f}{} ({:.0f}%)\n".format(
                        goal.goal_type, goal.current, goal.unit, goal.target, goal.unit, progress
                    )
        
        # ========== ML预测 ==========
        ml_emoji = "🟢" if ml_p >= 70 else "🟡" if ml_p >= 50 else "🔴"
        
        # ========== 健康评分 ==========
        hs_emoji = "🟢" if hs_score >= 70 else "🟡" if hs_score >= 50 else "🟠"
        
        # ========== 综合分析 ==========
        comp = comprehensive
        hz = comp.get('heart_zones', {})
        hz_aerobic = hz.get('aerobic', 0)
        hz_anaerobic = hz.get('anaerobic', 0)
        
        # ========== 构建消息 ==========
        msg = "☀️ **早安！我是你的AI健身教练**\n\n"
        msg += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        
        # LLM生成的深度分析（如果已配置LLM）
        if llm_analysis:
            msg += "🤖 **AI教练深度分析**\n\n"
            msg += llm_analysis + "\n\n"
            msg += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        
        msg += "🤖 **教练视角今日评估**\n\n"
        msg += "{}\n{}\n\n".format(coach_mood, coach_vibe)
        msg += "💡 **解读**：恢复评分是判断今天能否训练的核心依据。\n\n"
        msg += "📈 **HRV专项分析**\n\n"
        msg += "{:.1f}ms — {}\n\n".format(hrv, hrv_coach)
        msg += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        
        # 添加马拉松训练部分
        marathon_section = ""
        if marathon_section:
            msg += marathon_section
        
        msg += "🎯 **今日训练计划**\n\n"
        msg += "**计划类型**：{}\n".format(plan_type)
        msg += "**计划描述**：{}\n".format(plan_desc)
        msg += "**目标strain：{}\n\n".format(plan_strain)
        msg += "**推荐训练**：\n"
        for ex in exercises:
            msg += "• {}\n".format(ex)
        msg += "\n💡 **教练建议**：{}\n\n".format(coach_tip)
        
        if dynamic_rec:
            msg += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            msg += "⚡ **动态规划参考**\n\n"
            msg += "{}\n\n".format(dynamic_rec)
        
        msg += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        msg += "📋 **本周训练概况**\n\n"
        msg += "• 训练天数：{}天\n".format(training_days)
        msg += "• 平均恢复：{:.0f}%\n".format(avg_recovery)
        msg += "{}\n\n".format(week_review)
        
        if sleep_debt > 2:
            msg += "⚠️ 睡眠债务：{:.1f}小时，注意多睡\n\n".format(sleep_debt)
        
        msg += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        msg += "🔮 **ML预测参考**\n\n"
        msg += "{} 明日预测恢复：{:.0f}%\n\n".format(ml_emoji, ml_p)
        
        msg += "📊 **综合数据**\n\n"
        msg += "• 心率区间：有氧{:.1f}% / 无氧{:.1f}%\n".format(hz_aerobic, hz_anaerobic)
        msg += "• 健康评分：{} {:.0f}/100\n\n".format(hs_emoji, hs_score)
        
        if goals_section:
            msg += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            msg += goals_section
        
        msg += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        msg += "💬 **教练寄语**\n\n"
        if recovery >= 60:
            msg += "准备好了吗？让我们开始今天的训练吧！💪\n"
        elif recovery >= 40:
            msg += "听从身体的反馈，我们慢慢来。一步一个脚印！🌱\n"
        else:
            msg += "今天的任务就是：好好休息。这是变强的必经之路。🌙\n"
        
        msg += "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        msg += "📌 **如何使用今日计划**\n\n"
        msg += "• 训练前：先做5-10分钟热身\n"
        msg += "• 训练中：保持专注，感受身体反馈\n"
        msg += "• 训练后：记得来20:00打卡记录！\n\n"
        msg += "⏰ 下次推送：今天18:00 晚间追踪\n"
        msg += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        
        return msg
    
    @staticmethod
    def evening() -> str:
        """
        18:00 晚间推送 - 教练反馈 + 打卡统计 + 明日计划
        """
        today = get_today_data()
        summary = get_whoop_data(7)
        health_score = _get_health_score()
        ml_pred = _get_ml_prediction()
        comprehensive = _get_comprehensive()
        
        recovery = today.get('recovery', 0)
        strain = today.get('strain', 0)
        has_training = today.get('has_training', False)
        
        training_days = summary.get('training_days', 0)
        avg_recovery = summary.get('avg_recovery', 0)
        sleep_debt = summary.get('sleep_debt', 0)
        
        hs_score = health_score.get('score', 0)
        ml_p = ml_pred.get('prediction', 50)
        
        # ========== LLM分析 ==========
        user_data = {
            "recovery": recovery,
            "hrv": today.get('hrv', 0),
            "rhr": today.get('rhr', 0),
            "strain": strain,
            "has_training": has_training,
            "sleep_debt": sleep_debt,
            "training_days": training_days,
            "avg_recovery": avg_recovery,
            "health_score": hs_score,
            "ml_prediction": ml_p,
        }
        llm_analysis = _get_llm_analysis(user_data, "evening")
        
        # ========== 今日训练总结 ==========
        if has_training and strain > 0:
            if strain >= 12:
                training_eval, training_review = "💪 出色完成！", "今天你的strain达到了{:.1f}，非常高强度训练！你付出了100%的努力！".format(strain)
                training_effect = "有效提升力量和耐力"
            elif strain >= 8:
                training_eval, training_review = "🏃 不错的训练！", "今天strain为{:.1f}，中等强度训练，训练量适中。".format(strain)
                training_effect = "维持体能，保持节奏"
            else:
                training_eval, training_review = "🚶 轻度活动", "今天活动量较小，strain为{:.1f}。".format(strain)
                training_effect = "保持活跃状态"
        else:
            training_eval, training_review = "😌 今日休息", "今天你选择了休息，这对身体恢复非常重要。"
            training_effect = "充分恢复，为明天做准备"
        
        # ========== 教练点评 ==========
        if recovery >= 70:
            coach_comment = "你的身体恢复得非常好！"
        elif recovery >= 50:
            coach_comment = "恢复状态处于中等水平，注意不要连续高强度训练。"
        else:
            coach_comment = "恢复状态不太理想，建议增加休息日。"
        
        # ========== 明日预测 ==========
        ml_emoji = "🟢" if ml_p >= 70 else "🟡" if ml_p >= 50 else "🔴"
        
        if ml_p >= 70:
            tomorrow_plan = "根据预测，明天状态应该不错！"
            tomorrow_type = "可以进行高质量训练"
            tomorrow_exercises = ["力量训练", "节奏跑", "综合训练"]
        elif ml_p >= 50:
            tomorrow_plan = "明天的状态可能一般，建议中等强度。"
            tomorrow_type = "中等强度训练或休息"
            tomorrow_exercises = ["轻松跑", "瑜伽", "拉伸放松"]
        else:
            tomorrow_plan = "预测显示疲劳还在累积，建议继续休息。"
            tomorrow_type = "以休息恢复为主"
            tomorrow_exercises = ["充足睡眠", "轻度拉伸", "冥想放松"]
        
        # ========== 打卡统计 ==========
        tracker_section = ""
        tracker = _get_tracker()
        if tracker:
            streak = tracker.get_streak("dongyi")
            weekly = tracker.get_weekly_summary("dongyi")
            
            tracker_section = "\n📊 **打卡统计**\n\n"
            tracker_section += "• 连续打卡：{}天\n".format(streak)
            tracker_section += "• 本周打卡：{}/7天\n".format(weekly.get('total_checkins', 0))
            if weekly.get('completion_rate', 0) > 0:
                tracker_section += "• 完成率：{:.0f}%\n".format(weekly.get('completion_rate', 0))
        
        # ========== 目标进度 ==========
        goals_section = ""
        goals_manager = _get_goals()
        if goals_manager:
            active_goals = goals_manager.get_active_goals()
            if active_goals:
                goals_section = "\n🎯 **目标进度**\n\n"
                for goal in active_goals[:2]:
                    progress = (goal.current / goal.target * 100) if goal.target > 0 else 0
                    goals_section += "• {}：{:.0f}{} / {:.0f}{} ({:.0f}%)\n".format(
                        goal.goal_type, goal.current, goal.unit, goal.target, goal.unit, progress
                    )
        
        # ========== 本周总结 ==========
        if training_days >= 6:
            week_summary = "本周训练较密集（{}天），注意轮休。".format(training_days)
        elif training_days >= 4:
            week_summary = "本周训练量适中（{}天），继续保持！".format(training_days)
        else:
            week_summary = "本周训练偏少（{}天），可根据状态适当增加。".format(training_days)
        
        # ========== 睡眠提醒 ==========
        sleep_reminder = ""
        if sleep_debt > 5:
            sleep_reminder = "\n⚠️ 睡眠债务（{:.1f}小时），优先补觉！".format(sleep_debt)
        
        # ========== 教练关怀 ==========
        if recovery < 50:
            care_msg = "我注意到你的恢复状态不太理想。建议今晚早点睡觉，睡眠是最好的恢复方式。🌙"
        elif has_training and strain >= 10:
            care_msg = "今天训练强度很大！记得补充营养，训练后30分钟内摄入蛋白质很重要。💪"
        else:
            care_msg = "保持现在的节奏，你做得很好！有任何问题随时问我。🌟"
        
        # ========== 综合分析 ==========
        comp = comprehensive
        hz = comp.get('heart_zones', {})
        hz_aerobic = hz.get('aerobic', 0)
        hz_anaerobic = hz.get('anaerobic', 0)
        
        # ========== 构建消息 ==========
        msg = "🌙 **晚间教练追踪**\n\n"
        msg += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        
        # LLM生成的深度分析（如果已配置LLM）
        if llm_analysis:
            msg += "🤖 **AI教练晚间总结**\n\n"
            msg += llm_analysis + "\n\n"
            msg += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        
        msg += "🤖 **教练今日总结**\n\n"
        msg += "{}\n{}\n\n".format(training_eval, training_review)
        msg += "💡 **解读**：无论训练还是休息，都是训练计划的一部分。\n\n"
        msg += "📊 **训练效果**：{}\n\n".format(training_effect)
        msg += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        msg += "🔮 **教练点评**\n\n"
        msg += "{}\n\n".format(coach_comment)
        msg += "💡 **恢复参考**：今日恢复 {:.0f}%，健康评分 {:.0f}/100\n\n".format(recovery, hs_score)
        msg += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        msg += "📅 **明日训练预告**\n\n"
        msg += "{}\n\n".format(tomorrow_plan)
        msg += "**计划类型**：{}\n".format(tomorrow_type)
        msg += "**推荐活动**：\n"
        for ex in tomorrow_exercises:
            msg += "• {}\n".format(ex)
        msg += "\n{} 预测恢复：{:.0f}%\n\n".format(ml_emoji, ml_p)
        msg += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        msg += "📋 **本周训练总览**\n\n"
        msg += "• 训练天数：{}天\n".format(training_days)
        msg += "• 平均恢复：{:.0f}%\n".format(avg_recovery)
        msg += "{}\n".format(week_summary)
        
        if sleep_reminder:
            msg += "{}\n".format(sleep_reminder)
        
        if tracker_section:
            msg += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            msg += tracker_section
        
        if goals_section:
            msg += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            msg += goals_section
        
        msg += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        msg += "📊 **综合数据**\n\n"
        msg += "• 心率区间：有氧{:.1f}% / 无氧{:.1f}%\n\n".format(hz_aerobic, hz_anaerobic)
        msg += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        msg += "💬 **教练寄语**\n\n"
        msg += "{}\n\n".format(care_msg)
        msg += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        msg += "📌 **晚间提醒**\n\n"
        msg += "记得20:00来这里打卡记录今天的训练和身体感受！\n\n"
        msg += "⏰ 打卡提醒：今天22:00前来打卡！\n"
        msg += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        
        return msg
    
    @staticmethod
    @staticmethod
    @staticmethod
    def checkin_reminder() -> str:
        """
        20:00 打卡提醒推送 - WHOOP数据自动检测 + 确认流程
        """
        # === 获取数据 ===
        from lib.checkin_auto import auto_checkin_data

        today = get_today_data()
        health_score = _get_health_score()
        ml_pred = _get_ml_prediction()

        recovery = today.get('recovery', 0)
        hrv = today.get('hrv', 0)
        rhr = today.get('rhr', 0)

        hs_score = health_score.get('score', 0)
        ml_p = ml_pred.get('prediction', 50)

        auto = auto_checkin_data()
        has_workout = auto['has_workout']
        workout = auto.get('workout')
        strain = auto.get('strain', 0)

        # === 基础信息 ===
        hs_emoji = "🟢" if hs_score >= 70 else "🟡" if hs_score >= 50 else "🔴"
        rec_emoji = "🟢" if recovery >= 70 else "🟡" if recovery >= 50 else "🔴"

        # === 打卡统计 ===
        tracker = _get_tracker()
        streak = tracker.get_streak("dongyi") if tracker else 0
        weekly = tracker.get_weekly_summary("dongyi") if tracker else {}

        # === 目标进度 ===
        goals_manager = _get_goals()
        active_goals = goals_manager.get_active_goals() if goals_manager else []

        # === 构建消息 ===
        msg = "📊 **20:00 训练打卡提醒**\n\n"
        msg += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"

        # ---- 今日概况 ----
        msg += "📋 **今日概况**\n\n"
        msg += f"• 今日恢复：{rec_emoji} {recovery:.0f}%\n"
        msg += f"• HRV：{hrv:.1f}ms\n"
        msg += f"• 静息心率：{rhr:.0f}bpm\n"
        msg += f"• 健康评分：{hs_emoji} {hs_score:.0f}/100\n"
        if has_workout:
            msg += f"• WHOOP记录：✅ 检测到训练（strain {strain:.1f}）\n"
        else:
            msg += "• WHOOP记录：📝 今日无训练记录\n"
        msg += "\n"

        # ---- WHOOP 自动打卡预览 ----
        if has_workout and workout:
            sport = workout['sport']
            dist = workout.get('distance_km')
            pace = workout.get('pace', 'N/A')
            avg_hr = workout.get('avg_hr', 0)
            max_hr = workout.get('max_hr', 0)
            duration = workout.get('duration_min', 0)
            zones_formatted = workout.get('zones_formatted', '')

            msg += "✅ **WHOOP 检测到今日训练**\n\n"
            msg += "📋 **初步打卡内容**（来自WHOOP自动同步）\n\n"
            msg += "━━━━━━ auto ━━━━━━\n\n"
            msg += f"**类型**：{sport}\n"
            if dist:
                msg += f"**距离**：{dist}km\n"
            if pace and pace != 'N/A':
                msg += f"**配速**：{pace}/km\n"
            if duration:
                msg += f"**时长**：{duration}min\n"
            if avg_hr:
                msg += f"**平均心率**：{avg_hr}bpm\n"
            if max_hr:
                msg += f"**最大心率**：{max_hr}bpm\n"
            if zones_formatted:
                msg += f"**心率区间**：{zones_formatted}\n"
            msg += f"**Strain**：{strain:.1f}\n"
            msg += "\n⏰ *数据来源：WHOOP 自动同步*\n"
            msg += "*请告诉我感受如何：*\n\n"
            msg += "💬 **回复示例**：\n"
            msg += "• `✅` — 确认这个打卡内容，完成记录\n"
            msg += "• `感觉很好` — 确认打卡并记录感受\n"
            msg += "• `配速不对，应该是5:30` — 修改后确认\n"
            msg += "• `不是今天跑的` — 忽略此记录\n\n"

        else:
            msg += "📝 **今日为休息日**\n\n"
            msg += "━━━━━━ auto ━━━━━━\n\n"
            msg += "**类型**：休息/恢复\n\n"
            msg += "💬 直接回复「✅」即完成今日打卡，或告诉我你今天做了什么其他活动\n\n"

        msg += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"

        # ---- 打卡统计 ----
        msg += "📊 **打卡统计**\n\n"
        if streak > 0:
            msg += f"• 连续打卡：{streak}天 🔥\n"
        else:
            msg += "• 连续打卡：0天\n"
        if weekly:
            msg += f"• 本周打卡：{weekly.get('total_checkins', 0)}次\n"
            cr = weekly.get('completion_rate', 0)
            if cr > 0:
                msg += f"• 本周完成率：{cr:.0f}%\n"
        msg += "\n"

        # ---- 目标进度 ----
        if active_goals:
            msg += "🎯 **当前目标**\n\n"
            for goal in active_goals[:3]:
                pct = (goal.current / goal.target * 100) if goal.target > 0 else 0
                msg += f"• {goal.goal_type}：{goal.current}/{goal.target} {goal.unit}（{pct:.0f}%）\n"
            msg += "\n"

        # ---- 明日预测 ----
        msg += "🔮 **明日预测**\n\n"
        ml_emoji = "🟢" if ml_p >= 70 else "🟡" if ml_p >= 50 else "🔴"
        msg += f"• 预测恢复：{ml_emoji} {ml_p:.0f}%\n"
        if ml_p < 50:
            msg += "• 建议：明天可能需要多休息\n"
        elif ml_p < 70:
            msg += "• 建议：明天可以中等强度训练\n"
        else:
            msg += "• 建议：明天状态不错，可以正常训练\n"

        msg += "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"

        # ---- 睡眠反馈征集 ----
        sleep_data = auto.get('sleep')
        if sleep_data:
            sleep_eff = sleep_data.get('sleep_efficiency', 0)
            deep_sleep = sleep_data.get('deep_sleep_min', 0)
            msg += "😴 **睡眠反馈**（可选）\n\n"
            msg += f"WHOOP记录：效率{sleep_eff:.0f}% | 深睡眠{deep_sleep:.0f}min\n"
            msg += "你觉得今晚睡眠质量如何？\n"
            msg += "回复示例：`睡眠不错` / `半夜醒来` / `睡得很沉`\n\n"
            msg += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"

        # ---- 结束语 ----
        if has_workout:
            msg += "💪 *完成训练就是进步！记录下来，我会帮你追踪成长。*\n"
        else:
            msg += "🌙 *休息也是训练的一部分。明天继续加油！*\n"

        msg += "*我是你的AI教练，随时在这里等你！🏋️*\n"
        msg += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"

        return msg


        return msg


class CoachScheduler:
    """推送调度器"""
    
    PUSH_TIMES = {
        "morning": {"hour": 9, "minute": 0},
        "evening": {"hour": 18, "minute": 0},
        "checkin": {"hour": 20, "minute": 0},
    }
    
    @staticmethod
    def should_push(push_type: str) -> bool:
        now = bj_now()
        push_time = CoachScheduler.PUSH_TIMES.get(push_type)
        if not push_time:
            return False
        return now.hour == push_time["hour"] and now.minute == push_time["minute"]

# LLM增强报告（延迟导入避免循环依赖）
def _get_llm_analysis(user_data: dict, analysis_type: str) -> str:
    """获取LLM生成的详细分析，如果没有配置LLM则返回空"""
    try:
        from lib.enhanced_reports import EnhancedReports
        result = EnhancedReports._generate_llm_analysis(user_data, analysis_type)
        return result if result else ""
    except:
        return ""
