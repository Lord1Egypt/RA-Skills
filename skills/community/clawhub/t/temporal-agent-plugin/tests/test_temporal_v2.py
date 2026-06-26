import pytest
import time
from datetime import datetime, timedelta
from src.core.smart_timeout_predictor import SmartTimeoutPredictor
from src.core.cron_task_context import CronTaskContext, TaskState
from src.core.distributed_clock_sync import DistributedClockSync, AgentClockInfo
from src.core.time_anchor import TimeAnchorInjector, SessionTimeContext
from src.core.bayesian_predictor import BayesianTimeoutPredictor, BayesianPrior, BayesianTimeoutManager


class TestSmartTimeoutPredictor:
    """测试智能超时预测器"""

    def test_record_and_predict(self):
        """测试记录和预测"""
        predictor = SmartTimeoutPredictor(use_ml=False)

        predictor.record_duration("api_call", 1.0)
        predictor.record_duration("api_call", 1.2)
        predictor.record_duration("api_call", 0.9)

        timeout = predictor.predict_timeout("api_call")
        assert timeout > 0

    def test_statistics(self):
        """测试统计信息"""
        predictor = SmartTimeoutPredictor(use_ml=False)

        for duration in [1.0, 1.5, 2.0, 1.3, 1.7]:
            predictor.record_duration("compute_task", duration)

        stats = predictor.get_task_statistics("compute_task")
        assert stats['count'] == 5
        assert stats['mean'] > 0
        assert stats['predicted_timeout'] > 0

    def test_confidence(self):
        """测试置信度"""
        predictor = SmartTimeoutPredictor(use_ml=False, min_samples_for_ml=3)

        predictor.record_duration("file_op", 0.5)
        confidence = predictor.get_prediction_confidence("file_op")
        assert confidence == 0.0

        predictor.record_duration("file_op", 0.6)
        predictor.record_duration("file_op", 0.7)
        confidence = predictor.get_prediction_confidence("file_op")
        assert confidence > 0

    def test_realtime_adjustment(self):
        """测试实时调整"""
        predictor = SmartTimeoutPredictor(use_ml=False)

        for duration in [1.0, 1.1, 0.9, 1.2]:
            predictor.record_duration("network", duration)

        predicted = predictor.predict_timeout("network")
        adjusted = predictor.adjust_timeout_realtime("network", elapsed=5.0, predicted_total=predicted)
        assert adjusted > 0


class TestCronTaskContext:
    """测试定时任务上下文"""

    def test_initialization(self):
        """测试初始化"""
        scheduled = datetime.now() + timedelta(minutes=5)
        context = CronTaskContext(
            task_id="cron_001",
            scheduled_time=scheduled,
            deadline=datetime.now() + timedelta(hours=1)
        )

        assert context.task_id == "cron_001"
        assert context.state == TaskState.PENDING
        assert context.checkpoint_count == 0

    def test_start_task(self):
        """测试任务开始"""
        scheduled = datetime.now() - timedelta(minutes=1)
        context = CronTaskContext(task_id="cron_002", scheduled_time=scheduled)

        context.start()

        assert context.state == TaskState.RUNNING
        assert context.started_at is not None

    def test_should_checkpoint(self):
        """测试检查点判断"""
        scheduled = datetime.now() - timedelta(hours=1)
        context = CronTaskContext(
            task_id="cron_003",
            scheduled_time=scheduled,
            checkpoint_interval=60.0
        )

        context.start()
        time.sleep(0.1)

        assert not context.should_checkpoint()

    def test_should_recheck(self):
        """测试是否需要回来看结果"""
        scheduled = datetime.now() - timedelta(minutes=1)
        context = CronTaskContext(
            task_id="cron_004",
            scheduled_time=scheduled,
            min_expected_duration=5.0,
            max_expected_duration=300.0
        )

        context.start()
        time.sleep(0.1)

        assert not context.should_recheck()

    def test_suspend_and_resume(self):
        """测试暂停和恢复功能"""
        scheduled = datetime.now() - timedelta(minutes=1)
        context = CronTaskContext(
            task_id="cron_005",
            scheduled_time=scheduled,
            max_expected_duration=60.0
        )

        context.start()
        time.sleep(0.2)

        # 暂停任务
        context.suspend(reason="waiting_user_confirm")
        assert context.state == TaskState.SUSPENDED
        assert context.suspended_count == 1
        assert context.last_suspend_time is not None

        # 暂停期间等待
        time.sleep(0.5)

        # 恢复任务
        context.resume()
        assert context.state == TaskState.RUNNING
        assert context.suspended_time > 0
        assert context.last_suspend_time is None

    def test_suspend_time_not_counted_in_timeout(self):
        """测试暂停时间不计入超时"""
        scheduled = datetime.now() - timedelta(minutes=1)
        context = CronTaskContext(
            task_id="cron_006",
            scheduled_time=scheduled,
            max_expected_duration=1.0  # 1秒超时
        )

        context.start()
        time.sleep(0.3)

        # 暂停任务（暂停0.8秒）
        context.suspend()
        time.sleep(0.8)
        context.resume()

        # 实际执行时间只有0.3秒，不应该超时
        assert not context.should_timeout()

        # 再执行0.8秒，总执行时间达到1.1秒，应该超时
        time.sleep(0.8)
        assert context.should_timeout()

    def test_multiple_suspend_resume(self):
        """测试多次暂停和恢复"""
        scheduled = datetime.now() - timedelta(minutes=1)
        context = CronTaskContext(
            task_id="cron_007",
            scheduled_time=scheduled,
            max_expected_duration=100.0
        )

        context.start()

        # 第一次暂停/恢复
        context.suspend()
        time.sleep(0.2)
        context.resume()

        # 第二次暂停/恢复
        context.suspend()
        time.sleep(0.2)
        context.resume()

        assert context.suspended_count == 2
        assert context.suspended_time > 0

    def test_get_context_with_suspend(self):
        """测试获取包含暂停信息的上下文"""
        scheduled = datetime.now() - timedelta(minutes=1)
        context = CronTaskContext(
            task_id="cron_008",
            scheduled_time=scheduled,
            max_expected_duration=100.0
        )

        context.start()
        context.suspend()
        time.sleep(0.2)
        context.resume()

        ctx = context.get_context()

        assert 'total_elapsed' in ctx
        assert 'active_elapsed' in ctx
        assert 'suspended_time' in ctx
        assert 'suspended_count' in ctx
        assert ctx['suspended_count'] == 1
        assert ctx['active_elapsed'] < ctx['total_elapsed']


class TestDistributedClockSync:
    """测试分布式时钟同步"""

    def test_initialization(self):
        """测试初始化"""
        sync = DistributedClockSync(agent_id="test_agent")
        assert sync.local_agent_id == "test_agent"

    def test_add_agent(self):
        """测试添加Agent"""
        sync = DistributedClockSync(agent_id="test_agent")
        sync.add_agent("agent1")
        sync.add_agent("agent2")
        assert len(sync.agent_clocks) == 2

    def test_remove_agent(self):
        """测试移除Agent"""
        sync = DistributedClockSync(agent_id="test_agent")
        sync.add_agent("agent1")
        sync.remove_agent("agent1")
        assert len(sync.agent_clocks) == 0


class TestTimeAnchorInjector:
    """测试时间锚点注入器"""

    def test_create_session(self):
        """测试创建会话"""
        injector = TimeAnchorInjector()
        session = injector.create_session("test_session")
        assert session.session_id == "test_session"
        assert session.timezone == 'Asia/Shanghai'

    def test_get_session_context(self):
        """测试获取会话上下文"""
        injector = TimeAnchorInjector()
        injector.create_session("test_session")
        context = injector.get_session_context("test_session")
        assert context is not None
        assert context.session_id == "test_session"

    def test_remove_session(self):
        """测试移除会话"""
        injector = TimeAnchorInjector()
        injector.create_session("test_session")
        injector.remove_session("test_session")
        context = injector.get_session_context("test_session")
        assert context is None

    def test_get_current_timestamp(self):
        """测试获取当前时间戳"""
        injector = TimeAnchorInjector()
        timestamp1 = injector.get_current_timestamp()
        time.sleep(0.1)
        timestamp2 = injector.get_current_timestamp()
        assert timestamp2 > timestamp1

    def test_get_current_timestamp_with_session(self):
        """测试获取会话级时间戳"""
        injector = TimeAnchorInjector()
        injector.create_session("test_session")
        timestamp1 = injector.get_current_timestamp("test_session")
        time.sleep(0.1)
        timestamp2 = injector.get_current_timestamp("test_session")
        assert timestamp2 > timestamp1

    def test_get_time_context(self):
        """测试获取时间上下文"""
        injector = TimeAnchorInjector()
        context = injector.get_time_context()
        assert 'current_time' in context
        assert 'current_date' in context
        assert 'day_of_week' in context
        assert 'timezone' in context

    def test_get_time_context_with_session(self):
        """测试获取会话级时间上下文"""
        injector = TimeAnchorInjector()
        injector.create_session("test_session")
        context = injector.get_time_context(session_id="test_session")
        assert 'current_time' in context
        assert 'current_date' in context

    def test_inject_time_anchor(self):
        """测试注入时间锚点"""
        injector = TimeAnchorInjector()
        prompt = "Hello, what time is it?"
        injected = injector.inject_time_anchor(prompt)
        assert "[时间锚点]" in injected
        assert "当前时间：" in injected

    def test_inject_time_anchor_with_session(self):
        """测试会话级时间锚点注入"""
        injector = TimeAnchorInjector()
        injector.create_session("test_session")
        prompt = "Hello, what time is it?"
        injected = injector.inject_time_anchor(prompt, session_id="test_session")
        assert "[时间锚点]" in injected

    def test_sync_time(self):
        """测试时间同步"""
        injector = TimeAnchorInjector()
        injector.create_session("test_session")
        reference_time = time.time() + 10.0  # 模拟时间偏移
        injector.sync_time("test_session", reference_time)
        synced_time = injector.get_current_timestamp("test_session")
        assert abs(synced_time - reference_time) < 0.1

    def test_get_time_drift(self):
        """测试获取时间漂移"""
        injector = TimeAnchorInjector()
        injector.create_session("test_session")
        reference_time = time.time() + 5.0
        injector.sync_time("test_session", reference_time)
        drift = injector.get_time_drift("test_session")
        assert drift > 0

    def test_is_time_drift_excessive(self):
        """测试时间漂移是否过大"""
        injector = TimeAnchorInjector()
        injector.create_session("test_session")
        # 小漂移
        injector.sync_time("test_session", time.time() + 0.1)
        assert not injector.is_time_drift_excessive("test_session")
        # 大漂移
        injector.sync_time("test_session", time.time() + 10.0)
        assert injector.is_time_drift_excessive("test_session")

    def test_get_all_sessions(self):
        """测试获取所有会话"""
        injector = TimeAnchorInjector()
        injector.create_session("session1")
        injector.create_session("session2")
        sessions = injector.get_all_sessions()
        assert len(sessions) == 2

    def test_clear_all_sessions(self):
        """测试清除所有会话"""
        injector = TimeAnchorInjector()
        injector.create_session("session1")
        injector.create_session("session2")
        injector.clear_all_sessions()
        sessions = injector.get_all_sessions()
        assert len(sessions) == 0


class TestBayesianTimeoutPredictor:
    """测试贝叶斯超时预测器"""

    def test_initialization(self):
        """测试初始化"""
        predictor = BayesianTimeoutPredictor(task_type="api_call")
        assert predictor.task_type == "api_call"
        assert predictor.observation_count == 0
        assert predictor.predict_timeout() > 0

    def test_conservative_prior(self):
        """测试保守先验（冷启动时高估超时）"""
        predictor = BayesianTimeoutPredictor(
            task_type="test",
            prior=BayesianPrior(alpha=2.0, beta=0.05)
        )

        # 冷启动时预测值应等于先验均值 * 安全系数
        expected = (2.0 / 0.05) * 2.0  # 40 * 2 = 80
        assert abs(predictor.predict_timeout() - expected) < 0.01

    def test_bayesian_update(self):
        """测试贝叶斯更新"""
        predictor = BayesianTimeoutPredictor(
            task_type="test",
            prior=BayesianPrior(alpha=2.0, beta=0.1)
        )

        # 初始预测
        initial_timeout = predictor.predict_timeout()

        # 记录观测数据（实际执行时间约10秒）
        for duration in [9.5, 10.2, 10.8, 9.8, 10.5]:
            predictor.update(duration)

        # 更新后预测值应接近观测均值 * 安全系数
        updated_timeout = predictor.predict_timeout()
        assert updated_timeout < initial_timeout  # 收敛到更小的值

    def test_confidence_increases(self):
        """测试置信度随观测数据增加而提高"""
        predictor = BayesianTimeoutPredictor(task_type="test")

        confidence_0 = predictor.get_confidence()
        assert confidence_0 == 0.0

        predictor.update(10.0)
        confidence_1 = predictor.get_confidence()
        assert confidence_1 > confidence_0

        for i in range(9):
            predictor.update(10.0)
        confidence_10 = predictor.get_confidence()
        assert confidence_10 > confidence_1
        assert confidence_10 > 0.5

    def test_posterior_stats(self):
        """测试后验分布统计"""
        predictor = BayesianTimeoutPredictor(task_type="test")

        for duration in [10.0, 12.0, 11.0, 9.0, 13.0]:
            predictor.update(duration)

        stats = predictor.get_posterior_stats()
        assert stats['observation_count'] == 5
        assert stats['posterior_mean'] > 0
        assert stats['predicted_timeout'] > 0
        assert stats['confidence'] > 0

    def test_reset(self):
        """测试重置预测器"""
        predictor = BayesianTimeoutPredictor(task_type="test")

        for duration in [10.0, 12.0, 11.0]:
            predictor.update(duration)

        assert predictor.observation_count == 3

        predictor.reset()
        assert predictor.observation_count == 0
        assert len(predictor.observations) == 0

    def test_calibration_data(self):
        """测试校准数据"""
        predictor = BayesianTimeoutPredictor(task_type="test")

        # 数据不足时
        calibration = predictor.get_calibration_data()
        assert not calibration['calibrated']

        # 数据充足时
        for duration in [10.0, 10.5, 9.8, 10.2, 10.1, 9.9]:
            predictor.update(duration)

        calibration = predictor.get_calibration_data()
        assert calibration['calibrated']
        assert calibration['observation_count'] == 6

    def test_min_max_timeout(self):
        """测试最小/最大超时限制"""
        predictor = BayesianTimeoutPredictor(
            task_type="test",
            min_timeout=5.0,
            max_timeout=100.0,
            safety_multiplier=1.0
        )

        # 极小先验
        predictor.reset(BayesianPrior(alpha=1.0, beta=100.0))  # 均值 0.01
        assert predictor.predict_timeout() >= 5.0  # 不低于最小值

        # 极大先验
        predictor.reset(BayesianPrior(alpha=1000.0, beta=0.01))  # 均值 100000
        assert predictor.predict_timeout() <= 100.0  # 不超过最大值


class TestBayesianTimeoutManager:
    """测试贝叶斯超时预测管理器"""

    def test_get_predictor(self):
        """测试获取预测器"""
        manager = BayesianTimeoutManager()
        predictor1 = manager.get_predictor("api_call")
        predictor2 = manager.get_predictor("api_call")
        assert predictor1 is predictor2  # 同一个实例

    def test_record_and_predict(self):
        """测试记录和预测"""
        manager = BayesianTimeoutManager()

        manager.record_duration("api_call", 10.0)
        manager.record_duration("api_call", 12.0)
        manager.record_duration("api_call", 11.0)

        timeout = manager.predict_timeout("api_call")
        assert timeout > 0

    def test_multiple_task_types(self):
        """测试多任务类型管理"""
        manager = BayesianTimeoutManager()

        manager.record_duration("api_call", 10.0)
        manager.record_duration("file_op", 30.0)
        manager.record_duration("network", 20.0)

        stats = manager.get_all_stats()
        assert len(stats) == 3
        assert 'api_call' in stats
        assert 'file_op' in stats
        assert 'network' in stats

    def test_calibration_report(self):
        """测试校准报告"""
        manager = BayesianTimeoutManager()

        # 添加足够数据
        for _ in range(6):
            manager.record_duration("api_call", 10.0)

        report = manager.get_calibration_report()
        assert 'api_call' in report
        assert report['api_call']['calibrated']


if __name__ == "__main__":
    pytest.main([__file__])