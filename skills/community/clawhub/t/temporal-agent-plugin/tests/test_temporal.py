import pytest
import time
from src.core.temporal_analyzer import TemporalAnalyzer
from src.core.progress_estimator import ProgressEstimator
from src.core.anomaly_detector import AnomalyDetector
from src.core.social_temporal import SocialTemporal
from src.core.causal_predictor import CausalPredictor
from src.core.time_anchor import TimeAnchorInjector

class TestTemporalAnalyzer:
    """测试时序分析引擎
    """
    
    def test_start_stop_timer(self):
        """测试计时功能
        """
        analyzer = TemporalAnalyzer()
        task_id = "test_task"
        
        # 开始计时
        start_time = analyzer.start_timer(task_id)
        assert start_time > 0
        
        # 等待一段时间
        time.sleep(0.1)
        
        # 停止计时
        duration = analyzer.stop_timer(task_id)
        assert duration >= 0.1
    
    def test_predict_duration(self):
        """测试预测执行时间
        """
        analyzer = TemporalAnalyzer()
        
        # 测试默认预测值
        predicted = analyzer.predict_duration("download")
        assert predicted > 0
        
        # 测试复杂度因子
        predicted_complex = analyzer.predict_duration("download", complexity=2.0)
        assert predicted_complex > predicted
    
    def test_is_taking_too_long(self):
        """测试判断任务是否执行时间过长
        """
        analyzer = TemporalAnalyzer()
        task_id = "test_task"
        
        # 开始计时
        analyzer.start_timer(task_id)
        
        # 立即检查，应该返回False
        assert not analyzer.is_taking_too_long(task_id, 1.0)
        
        # 等待一段时间
        time.sleep(0.2)
        
        # 检查，应该返回False
        assert not analyzer.is_taking_too_long(task_id, 1.0)

class TestProgressEstimator:
    """测试进度预估系统
    """
    
    def test_start_task(self):
        """测试开始任务
        """
        estimator = ProgressEstimator()
        task_id = "test_task"
        
        estimator.start_task(task_id, "download", 100)
        progress = estimator.get_progress(task_id)
        assert progress["task_type"] == "download"
        assert progress["total_steps"] == 100
    
    def test_update_progress(self):
        """测试更新进度
        """
        estimator = ProgressEstimator()
        task_id = "test_task"
        
        estimator.start_task(task_id, "download", 100)
        estimator.update_progress(task_id, 50)
        
        progress = estimator.get_progress(task_id)
        assert progress["current_step"] == 50
        assert 0.4 <= progress["progress"] <= 0.6

class TestAnomalyDetector:
    """测试异常检测模块
    """
    
    def test_detect_anomaly(self):
        """测试检测异常
        """
        detector = AnomalyDetector()
        
        # 添加正常数据
        for i in range(5):
            detector.add_duration("api_call", 0.1)
        
        # 测试正常值
        assert not detector.detect_anomaly("api_call", 0.1)
        
        # 测试异常值
        assert detector.detect_anomaly("api_call", 1.0)

class TestSocialTemporal:
    """测试社交时序理解
    """
    
    def test_record_utterance(self):
        """测试记录对话
        """
        social = SocialTemporal()
        
        social.record_utterance("user", "Hello")
        social.record_utterance("assistant", "Hi there!")
        
        assert len(social.conversation_history) == 2
    
    def test_get_pause_type(self):
        """测试获取停顿类型
        """
        social = SocialTemporal()
        
        # 测试短停顿
        assert social.get_pause_type(0.3) == "very_short"
        
        # 测试中等停顿
        assert social.get_pause_type(1.0) == "short"
        
        # 测试长停顿
        assert social.get_pause_type(3.0) == "medium"

class TestCausalPredictor:
    """测试因果预测模型
    """
    
    def test_predict_latency(self):
        """测试预测延迟
        """
        predictor = CausalPredictor()
        
        # 测试默认预测值
        latency = predictor.predict_latency("mouse_click")
        assert latency > 0
    
    def test_record_action_result(self):
        """测试记录动作和结果
        """
        predictor = CausalPredictor()
        
        # 记录动作
        predictor.record_action("mouse_click")
        
        # 等待一段时间
        time.sleep(0.1)
        
        # 记录结果
        predictor.record_result("mouse_click", "clicked")
        
        # 测试预测延迟
        latency = predictor.predict_latency("mouse_click")
        assert latency > 0

class TestTimeAnchorInjector:
    """测试时间锚点注入器
    """
    
    def test_get_current_time(self):
        """测试获取当前时间
        """
        injector = TimeAnchorInjector()
        current_time = injector.get_current_time()
        assert hasattr(current_time, 'strftime')
        assert hasattr(current_time, 'weekday')
        assert hasattr(current_time, 'month')
        assert hasattr(current_time, 'year')
    
    def test_get_time_context(self):
        """测试获取时间上下文
        """
        injector = TimeAnchorInjector()
        time_context = injector.get_time_context()
        assert isinstance(time_context, dict)
        assert "current_time" in time_context
        assert "current_date" in time_context
        assert "day_of_week" in time_context
        assert "year" in time_context
    
    def test_inject_time_anchor(self):
        """测试注入时间锚点
        """
        injector = TimeAnchorInjector()
        prompt = "今天是{{current_date}}，星期{{day_of_week_chinese}}"
        injected_prompt = injector.inject_time_anchor(prompt)
        assert isinstance(injected_prompt, str)
        assert "{{current_date}}" not in injected_prompt
        assert "{{day_of_week_chinese}}" not in injected_prompt
    
    def test_get_relative_time(self):
        """测试获取相对时间
        """
        injector = TimeAnchorInjector()
        past_timestamp = time.time() - 60  # 1分钟前
        relative_time = injector.get_relative_time(past_timestamp)
        assert isinstance(relative_time, str)
        assert "分钟前" in relative_time
    
    def test_format_time_difference(self):
        """测试格式化时间差
        """
        injector = TimeAnchorInjector()
        formatted = injector.format_time_difference(3661)  # 1小时1分钟1秒
        assert isinstance(formatted, str)
        assert "小时" in formatted
        assert "分钟" in formatted

if __name__ == "__main__":
    pytest.main([__file__])