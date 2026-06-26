"""
WHOOP Guru 完整测试套件
运行: python3 -m pytest tests/ -v
或: python3 tests/test_all.py
"""

import sys
import os
import unittest
from datetime import datetime

# Setup path
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, SKILL_DIR)
sys.path.insert(0, os.path.join(SKILL_DIR, 'lib'))


class TestDataCleaner(unittest.TestCase):
    """测试数据清理模块"""
    
    def test_get_today_data(self):
        from lib.data_cleaner import get_today_data
        data = get_today_data()
        self.assertIsInstance(data, dict)
        self.assertIn('recovery', data)
        self.assertIn('hrv', data)
        self.assertIn('rhr', data)
        self.assertIn('sleep_hours', data)
        print(f"✓ get_today_data: recovery={data.get('recovery')}")
    
    def test_get_whoop_data(self):
        from lib.data_cleaner import get_whoop_data
        data = get_whoop_data(7)
        self.assertIsInstance(data, dict)
        self.assertIn('avg_recovery', data)
        self.assertIn('training_days', data)
        self.assertIn('sleep_debt', data)
        print(f"✓ get_whoop_data: training_days={data.get('training_days')}")


class TestHealthScore(unittest.TestCase):
    """测试健康评分模块"""
    
    def test_calculate_health_score(self):
        from lib.health_score import calculate_health_score
        result = calculate_health_score()
        self.assertIsInstance(result, dict)
        self.assertIn('score', result)
        self.assertIn('grade', result)
        self.assertIn('breakdown', result)
        score = result['score']
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)
        print(f"✓ Health score: {score}/100 ({result['grade']})")


class TestMLPredictor(unittest.TestCase):
    """测试ML预测模块"""
    
    def test_predict_next_day(self):
        from lib.ml_predictor import predict_next_day
        result = predict_next_day()
        self.assertIsInstance(result, dict)
        self.assertIn('prediction', result)
        self.assertIn('confidence', result)
        pred = result['prediction']
        self.assertGreaterEqual(pred, 0)
        self.assertLessEqual(pred, 100)
        print(f"✓ ML prediction: {pred}% (confidence: {result['confidence']})")


class TestComprehensiveAnalysis(unittest.TestCase):
    """测试综合分析模块"""
    
    def test_generate_comprehensive(self):
        from lib.comprehensive_analysis import generate_comprehensive
        result = generate_comprehensive()
        self.assertIsInstance(result, dict)
        self.assertIn('heart_zones', result)
        self.assertIn('sleep_stages', result)
        self.assertIn('body_battery', result)
        self.assertIn('hrv_trend', result)
        print(f"✓ Comprehensive analysis keys: {list(result.keys())}")


class TestHealthAdvisor(unittest.TestCase):
    """测试健康顾问模块"""
    
    def test_generate_health_report(self):
        from lib.health_advisor import generate_health_report
        result = generate_health_report()
        self.assertIsInstance(result, dict)
        self.assertIn('overall_score', result)
        self.assertIn('state', result)
        self.assertIn('training_recommendation', result)
        print(f"✓ Health advisor: state={result['state']}")


class TestDynamicPlanner(unittest.TestCase):
    """测试动态规划模块"""
    
    def setUp(self):
        from lib.dynamic_planner import DynamicPlanner
        self.planner = DynamicPlanner()
    
    def test_get_current_status(self):
        status = self.planner.get_current_status()
        self.assertIsInstance(status, dict)
        self.assertIn('recovery', status)
        self.assertIn('hrv', status)
        print(f"✓ Dynamic planner status: recovery={status['recovery']}")
    
    def test_get_recommended_intensity(self):
        rec = self.planner.get_recommended_intensity()
        self.assertIsInstance(rec, dict)
        self.assertIn('intensity', rec)
        self.assertIn('description', rec)
        print(f"✓ Recommended intensity: {rec['intensity']} - {rec['description']}")


class TestGoals(unittest.TestCase):
    """测试目标管理模块"""
    
    def setUp(self):
        from lib.goals import GoalsManager
        self.manager = GoalsManager("test_user_" + str(datetime.now().timestamp()))
    
    def test_get_active_goals(self):
        goals = self.manager.get_active_goals()
        self.assertIsInstance(goals, list)
        print(f"✓ Active goals: {len(goals)}")
    
    def test_create_and_delete_goal(self):
        # Create
        goal = self.manager.create_goal("增肌", 80, 60, "kg", "2026-06-01")
        self.assertIsNotNone(goal)
        goals = self.manager.get_active_goals()
        self.assertEqual(len(goals), 1)
        # Delete
        self.manager.delete_goal(goal.goal_id)
        goals = self.manager.get_active_goals()
        self.assertEqual(len(goals), 0)
        print(f"✓ Create/delete goal: OK")
    
    def test_mark_completed(self):
        goal = self.manager.create_goal("减脂", 15, 20, "%", "2026-07-01")
        self.manager.mark_completed(goal.goal_id)
        completed = self.manager.get_completed_goals()
        self.assertEqual(len(completed), 1)
        print(f"✓ Mark completed: {completed[0].goal_type}")


class TestMarathonGoals(unittest.TestCase):
    """测试马拉松目标管理"""
    
    def setUp(self):
        from lib.goals import GoalsManager
        self.manager = GoalsManager("test_user_" + str(datetime.now().timestamp()))
    
    def test_create_marathon_goal(self):
        goal = self.manager.create_marathon_goal(
            race_name="北京半马",
            race_date="2026-04-12",
            goal_time="02:00:00",
            race_type="半程马拉松"
        )
        self.assertIsNotNone(goal)
        self.assertEqual(goal.goal_name, "北京半马")
        self.assertEqual(goal.race_type, "半程马拉松")
        self.assertEqual(goal.target_pace, "5:41")  # 2h / 21.0975km ≈ 5:41/km
        print(f"✓ Create marathon goal: {goal.goal_name} ({goal.target_pace}/km)")
    
    def test_get_marathon_goals(self):
        goal = self.manager.create_marathon_goal(
            race_name="测试全马",
            race_date="2026-04-19",
            goal_time="04:45:00",
            race_type="全程马拉松"
        )
        goals = self.manager.get_marathon_goals()
        self.assertIsInstance(goals, list)
        self.assertGreaterEqual(len(goals), 1)
        print(f"✓ Marathon goals: {len(goals)}")
    
    def test_get_active_marathon_goal(self):
        goal = self.manager.create_marathon_goal(
            race_name="北京半马",
            race_date="2026-04-12",
            race_type="半程马拉松"
        )
        active = self.manager.get_active_marathon_goal()
        self.assertIsNotNone(active)
        self.assertEqual(active.goal_name, "北京半马")
        print(f"✓ Active marathon goal: {active.goal_name}")
    
    def test_training_phase(self):
        goal = self.manager.create_marathon_goal(
            race_name="测试半马",
            race_date="2026-04-15",
            race_type="半程马拉松"
        )
        phase = goal.training_phase
        self.assertIsInstance(phase, str)
        print(f"✓ Training phase: {phase} ({goal.days_until_race} days)")
    
    def test_delete_marathon_goal(self):
        goal = self.manager.create_marathon_goal(
            race_name="测试半马",
            race_date="2026-04-20",
            race_type="半程马拉松"
        )
        goals_before = len(self.manager.get_marathon_goals())
        self.manager.delete_marathon_goal(goal.goal_id)
        goals_after = len(self.manager.get_marathon_goals())
        self.assertEqual(goals_before - goals_after, 1)
        print(f"✓ Delete marathon goal: OK")


class TestTracker(unittest.TestCase):
    """测试进度追踪模块"""
    
    def setUp(self):
        from lib.tracker import ProgressTracker
        self.tracker = ProgressTracker()
        self.user_id = "test_user_" + str(datetime.now().timestamp())
    
    def test_add_and_get_checkin(self):
        self.tracker.add_checkin(self.user_id, "卧推", "完成", "良好")
        checkins = self.tracker.get_checkins(self.user_id)
        self.assertIsInstance(checkins, list)
        self.assertGreaterEqual(len(checkins), 1)
        print(f"✓ Checkins: {len(checkins)}")
    
    def test_get_streak(self):
        streak = self.tracker.get_streak(self.user_id)
        self.assertIsInstance(streak, int)
        self.assertGreaterEqual(streak, 0)
        print(f"✓ Streak: {streak} days")
    
    def test_weekly_summary(self):
        summary = self.tracker.get_weekly_summary(self.user_id)
        self.assertIsInstance(summary, dict)
        self.assertIn('total_checkins', summary)
        print(f"✓ Weekly summary: {summary}")
    
    def test_add_running_checkin(self):
        run_id = self.tracker.add_running_checkin(
            user_id=self.user_id,
            distance_km=10.5,
            duration_min=60,
            avg_pace="5:43",
            avg_heart_rate=145,
            max_heart_rate=168,
            feeling="良好",
            terrain="跑道"
        )
        self.assertIsNotNone(run_id)
        runs = self.tracker.get_recent_runs(self.user_id, days=7)
        self.assertGreaterEqual(len(runs), 1)
        print(f"✓ Running checkin: {runs[0]['distance_km']}km @ {runs[0]['avg_pace']}/km")
    
    def test_analyze_running_pattern(self):
        pattern = self.tracker.analyze_running_pattern(self.user_id, days=30)
        self.assertIsInstance(pattern, dict)
        self.assertIn('total_runs', pattern)
        self.assertIn('avg_pace', pattern)
        print(f"✓ Running pattern: {pattern['total_runs']} runs, avg {pattern['avg_pace']}/km")
    
    def test_suggest_next_run(self):
        suggestion = self.tracker.suggest_next_run(self.user_id)
        self.assertIsInstance(suggestion, dict)
        self.assertIn('suggested_distance', suggestion)
        self.assertIn('suggested_type', suggestion)
        print(f"✓ Next run suggestion: {suggestion['suggested_type']} {suggestion['suggested_distance']}km")
    
    def test_get_distance_summary(self):
        summary = self.tracker.get_distance_summary(self.user_id)
        self.assertIsInstance(summary, dict)
        self.assertIn('this_week_km', summary)
        print(f"✓ Distance summary: this week {summary['this_week_km']}km")


class TestLLM(unittest.TestCase):
    """测试LLM模块"""
    
    def test_llm_client_init(self):
        from lib.llm import LLMClient
        client = LLMClient("test_user")
        self.assertIsNotNone(client)
        info = client.get_info()
        self.assertIn('provider', info)
        self.assertIn('model', info)
        print(f"✓ LLM Client: provider={info['provider']}, model={info['model']}")


class TestPlanGenerator(unittest.TestCase):
    """测试计划生成模块"""
    
    def test_plan_generator_init(self):
        from lib.plan_generator import TrainingPlanGenerator
        pg = TrainingPlanGenerator()
        self.assertIsNotNone(pg)
        print(f"✓ TrainingPlanGenerator initialized")


class TestEnhancedReports(unittest.TestCase):
    """测试增强报告模块"""
    
    def test_morning_report(self):
        from lib.enhanced_reports import EnhancedReports
        report = EnhancedReports.morning_report()
        self.assertIsInstance(report, str)
        self.assertGreater(len(report), 100)
        print(f"✓ Morning report length: {len(report)}")
    
    def test_evening_report(self):
        from lib.enhanced_reports import EnhancedReports
        report = EnhancedReports.evening_report()
        self.assertIsInstance(report, str)
        self.assertGreater(len(report), 100)
        print(f"✓ Evening report length: {len(report)}")
    
    def test_full_report(self):
        from lib.enhanced_reports import EnhancedReports
        report = EnhancedReports.full_report()
        self.assertIsInstance(report, str)
        self.assertGreater(len(report), 100)
        print(f"✓ Full report length: {len(report)}")


class TestPusher(unittest.TestCase):
    """测试推送模块"""
    
    def test_morning_push(self):
        from lib.pusher import CoachPushMessage
        msg = CoachPushMessage.morning()
        self.assertIsInstance(msg, str)
        self.assertIn('早安', msg)
        self.assertIn('教练', msg)
        self.assertIn('训练', msg)
        print(f"✓ Morning push length: {len(msg)}")
    
    def test_evening_push(self):
        from lib.pusher import CoachPushMessage
        msg = CoachPushMessage.evening()
        self.assertIsInstance(msg, str)
        self.assertIn('晚间', msg)
        self.assertIn('教练', msg)
        print(f"✓ Evening push length: {len(msg)}")
    
    def test_checkin_reminder(self):
        from lib.pusher import CoachPushMessage
        msg = CoachPushMessage.checkin_reminder()
        self.assertIsInstance(msg, str)
        self.assertIn('打卡', msg)
        print(f"✓ Checkin reminder length: {len(msg)}")
    
    def test_scheduler(self):
        from lib.pusher import CoachScheduler
        times = CoachScheduler.PUSH_TIMES
        self.assertIn('morning', times)
        self.assertIn('evening', times)
        self.assertIn('checkin', times)
        print(f"✓ Scheduler times: {list(times.keys())}")


class TestCLI(unittest.TestCase):
    """测试CLI模块"""
    
    def test_cli_import(self):
        from lib import cli
        self.assertIsNotNone(cli)
        print(f"✓ CLI module imported")


class TestCheckinAuto(unittest.TestCase):
    """测试自动打卡检测模块"""

    def test_get_today_workouts(self):
        """测试获取今日训练记录"""
        from lib.checkin_auto import get_today_workouts
        result = get_today_workouts(days=1)
        self.assertIsInstance(result, list)
        print(f"✓ get_today_workouts: {len(result)} records")

    def test_analyze_today_workout(self):
        """测试训练记录分析"""
        from lib.checkin_auto import get_today_workouts, analyze_today_workout
        workouts = get_today_workouts(days=7)
        if workouts:
            analysis = analyze_today_workout(workouts[0])
            self.assertIsInstance(analysis, dict)
            self.assertIn('sport', analysis)
            self.assertIn('strain', analysis)
            self.assertIn('summary', analysis)
            self.assertIn('zones_formatted', analysis)
            print(f"✓ analyze_today_workout: {analysis['summary']}")

    def test_auto_checkin_data(self):
        """测试汇总打卡数据"""
        from lib.checkin_auto import auto_checkin_data
        result = auto_checkin_data()
        self.assertIsInstance(result, dict)
        self.assertIn('has_workout', result)
        self.assertIn('workout', result)
        self.assertIn('strain', result)
        self.assertIn('preview', result)
        self.assertIn('workout_summary', result)
        self.assertIsInstance(result['has_workout'], bool)
        print(f"✓ auto_checkin_data: has_workout={result['has_workout']}, strain={result['strain']}")

    def test_generate_checkin_preview_with_workout(self):
        """测试有训练时的打卡预览生成"""
        from lib.checkin_auto import get_today_workouts, analyze_today_workout, generate_checkin_preview
        workouts = get_today_workouts(days=7)
        if workouts:
            analysis = analyze_today_workout(workouts[0])
            preview = generate_checkin_preview(analysis)
            self.assertIsInstance(preview, str)
            self.assertIn('auto', preview)
            self.assertIn(analysis['sport'], preview)
            print(f"✓ generate_checkin_preview: {len(preview)} chars")

    def test_generate_restday_preview(self):
        """测试休息日打卡预览"""
        from lib.checkin_auto import generate_restday_preview
        preview = generate_restday_preview()
        self.assertIsInstance(preview, str)
        self.assertIn('休息', preview)
        print(f"✓ generate_restday_preview: {preview[:50]}")

    def test_get_today_sleep_data(self):
        """测试获取今日睡眠数据"""
        from lib.checkin_auto import get_today_sleep_data
        result = get_today_sleep_data()
        if result:
            self.assertIsInstance(result, dict)
            print(f"✓ get_today_sleep_data: sleep_efficiency={result.get('sleep_efficiency')}")

    def test_get_today_workout_analysis(self):
        """测试获取今日训练分析"""
        from lib.checkin_auto import get_today_workout_analysis
        result = get_today_workout_analysis()
        if result:
            self.assertIn('sport', result)
            self.assertIn('strain', result)
            print(f"✓ get_today_workout_analysis: {result.get('summary', 'N/A')}")

    def test_zone_data_types(self):
        """测试心率区间数据类型"""
        from lib.checkin_auto import get_today_workouts, analyze_today_workout
        workouts = get_today_workouts(days=7)
        if workouts:
            analysis = analyze_today_workout(workouts[0])
            zones = analysis.get('zones', {})
            for k, v in zones.items():
                self.assertIsInstance(v, (int, float))
            print(f"✓ Zone data types OK: {zones}")


class TestFeedbackLearning(unittest.TestCase):
    """测试反馈学习模块"""

    def setUp(self):
        """每个测试前清空反馈数据"""
        import json, os
        from lib.feedback_learning import FEEDBACK_FILE
        if os.path.exists(FEEDBACK_FILE):
            os.remove(FEEDBACK_FILE)

    def test_add_sleep_feedback(self):
        """测试睡眠反馈录入"""
        from lib.feedback_learning import add_feedback, get_recent_summary
        result = add_feedback(
            category="sleep",
            feedback_text="睡眠不错，很沉",
            whoop_baseline={"sleep_efficiency": 95, "deep_sleep_min": 20}
        )
        self.assertIsInstance(result, dict)
        self.assertIn('total', result)
        self.assertEqual(result['total'], 1)
        print(f"✓ add_sleep_feedback: total={result['total']}")

    def test_add_training_feedback(self):
        """测试训练反馈录入"""
        from lib.feedback_learning import add_feedback
        result = add_feedback(
            category="training",
            feedback_text="跑得很轻松",
            whoop_baseline={"strain": 10, "avg_hr": 130}
        )
        self.assertIsInstance(result, dict)
        self.assertEqual(result['total'], 1)
        print(f"✓ add_training_feedback: total={result['total']}")

    def test_add_recovery_feedback(self):
        """测试恢复反馈录入"""
        from lib.feedback_learning import add_feedback
        result = add_feedback(
            category="recovery",
            feedback_text="完全恢复了",
            whoop_baseline={"recovery_score": 80, "hrv": 50}
        )
        self.assertIsInstance(result, dict)
        self.assertEqual(result['total'], 1)
        print(f"✓ add_recovery_feedback: total={result['total']}")

    def test_feedback_text_classification(self):
        """测试反馈文字自动分类"""
        from lib.feedback_learning import _classify_sleep, _classify_training_feel

        self.assertEqual(_classify_sleep("睡眠很好"), "很好")
        self.assertEqual(_classify_sleep("睡得一般"), "一般")
        self.assertEqual(_classify_sleep("睡得很差"), "差")
        self.assertEqual(_classify_training_feel("跑得很轻松"), "轻松")
        self.assertEqual(_classify_training_feel("强度正常"), "正常")
        self.assertEqual(_classify_training_feel("跑得很吃力"), "吃力")
        print("✓ feedback text classification OK")

    def test_get_sleep_quality_baseline(self):
        """测试睡眠质量基线查询"""
        from lib.feedback_learning import add_feedback, get_sleep_quality_baseline
        add_feedback("sleep", "睡得很好", {"sleep_efficiency": 97})
        add_feedback("sleep", "睡眠不错", {"sleep_efficiency": 90})
        baseline = get_sleep_quality_baseline("很好")
        self.assertIsNotNone(baseline)
        self.assertGreater(baseline['avg_efficiency'], 0)
        print(f"✓ sleep baseline: avg_efficiency={baseline['avg_efficiency']}")

    def test_get_training_feel_baseline(self):
        """测试训练感受基线查询"""
        from lib.feedback_learning import add_feedback, get_training_feel_baseline
        add_feedback("training", "跑得很轻松", {"strain": 8})
        baseline = get_training_feel_baseline("轻松")
        self.assertIsNotNone(baseline)
        self.assertGreater(baseline['avg_strain'], 0)
        print(f"✓ training baseline: avg_strain={baseline['avg_strain']}")

    def test_should_adjust_recommendation(self):
        """测试建议调整判断"""
        from lib.feedback_learning import add_feedback, should_adjust_recommendation
        for _ in range(3):
            add_feedback("sleep", "睡得很好", {"sleep_efficiency": 95})
        should, reason = should_adjust_recommendation(
            "sleep", "差", {"sleep_efficiency": 95}
        )
        self.assertIsInstance(should, bool)
        self.assertIsInstance(reason, str)
        print(f"✓ should_adjust: {should}, reason: {reason[:30]}")

    def test_multiple_feedback_accumulates(self):
        """测试多次反馈累积"""
        from lib.feedback_learning import add_feedback, get_recent_summary
        for i in range(5):
            add_feedback("general", f"反馈{i}", notes=f"note{i}")
        summary = get_recent_summary()
        self.assertEqual(summary['total'], 5)
        print(f"✓ multiple feedback: total={summary['total']}")


class TestCheckinReminderEnhanced(unittest.TestCase):
    """增强测试：checkin_reminder 完整逻辑"""

    def test_checkin_reminder_structure(self):
        """测试消息结构完整性"""
        from lib.pusher import CoachPushMessage
        msg = CoachPushMessage.checkin_reminder()
        self.assertIsInstance(msg, str)
        self.assertIn('打卡', msg)
        self.assertIn('恢复', msg)
        self.assertIn('健康评分', msg)
        print(f"✓ checkin_reminder length: {len(msg)} chars")

    def test_checkin_reminder_has_workout_detection(self):
        """测试WHOOP训练自动检测"""
        from lib.pusher import CoachPushMessage
        from lib.checkin_auto import get_today_workout_analysis
        msg = CoachPushMessage.checkin_reminder()
        workout = get_today_workout_analysis()
        if workout:
            self.assertIn('WHOOP', msg)
            self.assertIn('auto', msg)
            print(f"✓ workout detection: strain={workout.get('strain')}")
        else:
            self.assertIn('休息', msg)
            print("✓ rest day message shown")

    def test_checkin_reminder_preview_content(self):
        """测试打卡预览内容"""
        from lib.pusher import CoachPushMessage
        from lib.checkin_auto import auto_checkin_data
        msg = CoachPushMessage.checkin_reminder()
        auto = auto_checkin_data()
        if auto['has_workout'] and auto['workout']:
            self.assertIn(auto['workout']['sport'], msg)
            print(f"✓ workout preview: {auto['workout']['summary']}")
        else:
            print("✓ rest day preview")

    def test_checkin_reminder_reply_guide(self):
        """测试回复指引"""
        from lib.pusher import CoachPushMessage
        msg = CoachPushMessage.checkin_reminder()
        self.assertIn('回复', msg)
        self.assertTrue('✅' in msg or '确认' in msg)
        print("✓ reply guide present")

    def test_checkin_reminder_no_training_day(self):
        """测试无训练日的消息内容"""
        from lib.pusher import CoachPushMessage
        from lib.checkin_auto import get_today_workout_analysis
        workout = get_today_workout_analysis()
        if not workout:
            msg = CoachPushMessage.checkin_reminder()
            self.assertIn('休息', msg)
            self.assertIn('恢复', msg)


class TestTrackerQuickCheckin(unittest.TestCase):
    """测试快速打卡接口"""

    def test_quick_checkin(self):
        """测试quick_checkin基本功能"""
        import time
        from lib.tracker import quick_checkin, ProgressTracker

        user_id = f"test_quick_{int(time.time())}"
        checkin_id = quick_checkin(user_id, "跑步", notes="10公里测试")
        self.assertIsInstance(checkin_id, str)

        tracker = ProgressTracker(user_id)
        checkins = tracker.get_checkins(user_id, limit=1)
        self.assertGreater(len(checkins), 0)
        latest = checkins[0]
        self.assertEqual(latest['type'], "跑步")
        self.assertEqual(latest['notes'], "10公里测试")
        self.assertEqual(latest['feedback'], "良好")

        data = tracker._load_checkins()
        data['checkins'] = [c for c in data['checkins'] if c.get('user_id') != user_id]
        tracker._save_checkins(data)
        print(f"✓ quick_checkin: {checkin_id}")

    def test_quick_checkin_rest_day(self):
        """测试休息日快速打卡"""
        import time
        from lib.tracker import quick_checkin, ProgressTracker

        user_id = f"test_rest_{int(time.time())}"
        checkin_id = quick_checkin(user_id, "休息", notes="今天完全休息")
        self.assertIsInstance(checkin_id, str)

        tracker = ProgressTracker(user_id)
        checkins = tracker.get_checkins(user_id, limit=1)
        self.assertEqual(checkins[0]['type'], "休息")

        data = tracker._load_checkins()
        data['checkins'] = [c for c in data['checkins'] if c.get('user_id') != user_id]
        tracker._save_checkins(data)

    def test_quick_checkin_default_feedback(self):
        """测试快速打卡默认反馈"""
        import time
        from lib.tracker import quick_checkin, ProgressTracker

        user_id = f"test_df_{int(time.time())}"
        checkin_id = quick_checkin(user_id, "力量训练")
        self.assertIsInstance(checkin_id, str)

        tracker = ProgressTracker(user_id)
        checkins = tracker.get_checkins(user_id, limit=1)
        self.assertEqual(checkins[0]['feedback'], "良好")
        self.assertEqual(checkins[0]['completed'], "力量训练")

        data = tracker._load_checkins()
        data['checkins'] = [c for c in data['checkins'] if c.get('user_id') != user_id]
        tracker._save_checkins(data)
def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("WHOOP GURU - 完整测试套件")
    print("=" * 60)
    print()
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestDataCleaner,
        TestHealthScore,
        TestMLPredictor,
        TestComprehensiveAnalysis,
        TestHealthAdvisor,
        TestDynamicPlanner,
        TestGoals,
        TestTracker,
        TestLLM,
        TestPlanGenerator,
        TestEnhancedReports,
        TestPusher,
        TestCLI,
        TestCheckinAuto,
        TestFeedbackLearning,
        TestCheckinReminderEnhanced,
        TestTrackerQuickCheckin,
    ]
    
    for tc in test_classes:
        suite.addTests(loader.loadTestsFromTestCase(tc))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print()
    print("=" * 60)
    print("测试结果摘要")
    print("=" * 60)
    print(f"测试数: {result.testsRun}")
    print(f"成功: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"失败: {len(result.failures)}")
    print(f"错误: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\n✅ 所有测试通过!")
        return 0
    else:
        print("\n❌ 有测试失败")
        return 1


if __name__ == '__main__':
    sys.exit(run_all_tests())


class TestMarathonAnalyzer(unittest.TestCase):
    """测试马拉松分析器"""
    
    def setUp(self):
        from lib.marathon_analyzer import MarathonAnalyzer
        from lib.goals import GoalsManager
        self.user_id = "test_user_" + str(datetime.now().timestamp())
        self.analyzer = MarathonAnalyzer(self.user_id)
        self.goals_manager = GoalsManager(self.user_id)
    
    def test_phase_from_days(self):
        from lib.marathon_analyzer import MarathonAnalyzer
        analyzer = MarathonAnalyzer("test")
        
        self.assertEqual(analyzer.get_phase_from_days(35), "基础期")
        self.assertEqual(analyzer.get_phase_from_days(21), "巅峰期")
        self.assertEqual(analyzer.get_phase_from_days(10), "减量期")
        self.assertEqual(analyzer.get_phase_from_days(5), "比赛周")
        self.assertEqual(analyzer.get_phase_from_days(0), "比赛日")
        print("✓ Phase from days: OK")
    
    def test_get_training_advice(self):
        advice = self.analyzer.get_training_advice(
            self.user_id,
            whoop_data={"recovery": 70, "hrv": 45}
        )
        self.assertIsInstance(advice, dict)
        self.assertIn("has_marathon_plan", advice)
        print(f"✓ Training advice: has_plan={advice['has_marathon_plan']}")
    
    def test_should_adjust_plan(self):
        should, reason, adjustment = self.analyzer.should_adjust_plan(self.user_id, 35)
        self.assertIsInstance(should, bool)
        self.assertIsInstance(reason, str)
        print(f"✓ Should adjust plan: {should} - {reason[:30] if reason else 'N/A'}")
    
    def test_get_phase_summary(self):
        goal = self.goals_manager.create_marathon_goal(
            race_name="测试半马",
            race_date="2026-04-15",
            race_type="半程马拉松"
        )
        summary = self.analyzer.get_phase_summary(goal)
        self.assertIsInstance(summary, dict)
        self.assertIn("phase", summary)
        self.assertIn("phase_tips", summary)
        print(f"✓ Phase summary: {summary['phase']} - {len(summary['phase_tips'])} tips")
        
        # Cleanup
        self.goals_manager.delete_marathon_goal(goal.goal_id)


class TestMarathonCommands(unittest.TestCase):
    """测试马拉松指令处理"""
    
    def setUp(self):
        from lib.marathon_commands import MarathonCommands
        self.user_id = "test_user_" + str(datetime.now().timestamp())
        self.cmd = MarathonCommands(self.user_id)
    
    def test_parse_race_info(self):
        parsed = self.cmd.parse_race_info("4月12号半马目标是破2")
        self.assertTrue(parsed["success"])
        self.assertEqual(parsed["race_type"], "半程马拉松")
        self.assertEqual(parsed["goal_time"], "02:00:00")
        print(f"✓ Parse race info: {parsed['race_name']} {parsed['race_date']}")
    
    def test_set_marathon_goal(self):
        result = self.cmd.set_marathon_goal(
            race_name="北京半马",
            race_date="2026-04-12",
            goal_time="02:00:00",
            race_type="半程马拉松"
        )
        self.assertTrue(result["success"])
        print(f"✓ Set marathon goal: {result['goal'].goal_name}")
        
        # Cleanup
        self.cmd.goals_manager.delete_marathon_goal(result["goal"].goal_id)
    
    def test_get_marathon_status(self):
        status = self.cmd.get_marathon_status()
        self.assertIsInstance(status, str)
        print(f"✓ Marathon status: {len(status)} chars")
    
    def test_adjust_plan(self):
        result = self.cmd.adjust_plan("明天", "休息")
        self.assertTrue(result["success"])
        print(f"✓ Adjust plan: {result['message'][:50]}")
