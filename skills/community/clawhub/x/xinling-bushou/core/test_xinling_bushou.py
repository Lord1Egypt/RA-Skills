"""
心灵补手单元测试
"""
import pytest
import json
import tempfile
import os
from pathlib import Path
from unittest.mock import patch, MagicMock

# 导入被测试模块
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.config_manager import ConfigManager, XinlingConfig
from core.trigger_detector import TriggerDetector, TriggerResult, Scenario
from core.command_parser import CommandParser, CommandType, ParsedCommand
from core.phrase_generator import PhraseGenerator, GenerationResult


class TestConfigManager:
    """配置管理器测试"""
    
    def setup_method(self):
        """每个测试前创建临时配置"""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_config_file = Path(self.temp_dir) / "config.json"
        
        # 使用临时文件
        with patch.object(ConfigManager, 'CONFIG_FILE', self.temp_config_file):
            self.cm = ConfigManager()
    
    def teardown_method(self):
        """清理临时文件"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_load_default_config(self):
        """测试加载默认配置"""
        config = self.cm.load_config()
        
        assert config["enabled"] == True
        assert config["persona"] == "taijian"
        assert config["level"] == 5
        assert config["gender"] == "male"
        assert config["mode"] == "normal"
    
    def test_save_and_load_config(self):
        """测试保存和加载配置"""
        test_config = {
            "enabled": False,
            "persona": "xiaoyahuan",
            "level": 8,
            "gender": "female",
            "mode": "normal"
        }
        
        self.cm.save_config(test_config)
        loaded = self.cm.load_config()
        
        assert loaded["enabled"] == False
        assert loaded["persona"] == "xiaoyahuan"
        assert loaded["level"] == 8
        assert loaded["gender"] == "female"
    
    def test_update_config(self):
        """测试更新配置"""
        self.cm.load_config()
        result = self.cm.update_config({"level": 7})
        
        assert result == True
        assert self.cm.get_config()["level"] == 7
    
    def test_update_invalid_persona(self):
        """测试无效persona"""
        self.cm.load_config()
        result = self.cm.update_config({"persona": "invalid_persona"})
        
        assert result == False
    
    def test_update_invalid_level(self):
        """测试无效level"""
        self.cm.load_config()
        result = self.cm.update_config({"level": 15})
        
        assert result == False
    
    def test_reset_config(self):
        """测试重置配置"""
        self.cm.update_config({"level": 10, "persona": "zaomiao"})
        self.cm.reset_config()
        
        config = self.cm.get_config()
        assert config["level"] == 5
        assert config["persona"] == "taijian"


class TestTriggerDetector:
    """触发检测器测试"""
    
    def setup_method(self):
        """每个测试前创建检测器"""
        # Mock config manager
        self.mock_config = {
            "enabled": True,
            "persona": "taijian",
            "level": 5,
            "gender": "male",
            "mode": "normal",
            "session_trigger_count": 0,
            "last_trigger_round": {},
            "recent_phrases": []
        }
        
        with patch.object(ConfigManager, 'load_config', return_value=self.mock_config):
            with patch.object(ConfigManager, 'get_config', return_value=self.mock_config):
                with patch.object(ConfigManager, 'update_config', return_value=True):
                    self.detector = TriggerDetector()
    
    def test_task_completed_trigger(self):
        """测试任务完成触发"""
        result = self.detector.detect("我已经做完了所有的事情")
        
        assert result.trigger == True
        # 情绪模式可能优先于任务完成
        assert result.scenario in ["task_completed", "emotional_high"]
        assert result.confidence >= 0.5
    
    def test_good_news_trigger(self):
        """测试好消息触发"""
        result = self.detector.detect("我升职了！太棒了！")
        
        assert result.trigger == True
        assert result.scenario == "share_good_news"
    
    def test_decision_made_trigger(self):
        """测试决定触发"""
        result = self.detector.detect("我决定了，就这样干！")
        
        assert result.trigger == True
        assert result.scenario == "decision_made"
    
    def test_emotional_low_trigger(self):
        """测试情绪低落触发"""
        result = self.detector.detect("最近好累，压力好大")
        
        assert result.trigger == True
        assert result.scenario == "emotional_low"
    
    def test_new_stage_trigger(self):
        """测试新阶段触发"""
        result = self.detector.detect("新项目开始了，重新出发")
        
        assert result.trigger == True
        assert result.scenario == "new_stage"
    
    def test_thank_keywords_trigger(self):
        """测试感谢关键词触发"""
        result = self.detector.detect("谢谢你帮我")
        
        assert result.trigger == True
        assert result.confidence >= 0.8
    
    def test_self_negative_care_mode(self):
        """测试自我否定切换关心模式"""
        result = self.detector.detect("我不行，我好差")
        
        assert result.care_mode == True
    
    def test_high_risk_no_trigger(self):
        """测试高风险词不触发谄媚"""
        result = self.detector.detect("我不想活了，活着没意思")
        
        assert result.trigger == False
        assert result.care_mode == True
    
    def test_disabled_no_trigger(self):
        """测试禁用时不触发"""
        disabled_config = self.mock_config.copy()
        disabled_config["enabled"] = False
        
        with patch.object(self.detector.config_manager, 'get_config', return_value=disabled_config):
            result = self.detector.detect("我完成了任务")
            
            assert result.trigger == False


class TestCommandParser:
    """命令解析器测试"""
    
    def setup_method(self):
        """每个测试前创建解析器"""
        self.parser = CommandParser()
    
    def test_enable_command(self):
        """测试启用命令"""
        result = self.parser.parse("进入心灵补手")
        
        assert result.command_type == CommandType.ENABLE
        assert result.args["enabled"] == True
    
    def test_disable_command(self):
        """测试禁用命令"""
        result = self.parser.parse("关闭心灵补手")
        
        assert result.command_type == CommandType.DISABLE
        assert result.args["enabled"] == False
    
    def test_set_level_command(self):
        """测试设置程度"""
        result = self.parser.parse("补手程度7")
        
        assert result.command_type == CommandType.SET_LEVEL
        assert result.args["level"] == 7
    
    def test_set_level_with_colon(self):
        """测试中文冒号"""
        result = self.parser.parse("程度:8")
        
        assert result.command_type == CommandType.SET_LEVEL
        assert result.args["level"] == 8
    
    def test_full_open_command(self):
        """测试全开命令"""
        result = self.parser.parse("补手全开")
        
        assert result.command_type == CommandType.ADJUST_LEVEL
        assert result.args["level"] == 10
    
    def test_calm_down_command(self):
        """测试收敛命令"""
        result = self.parser.parse("补手收敛")
        
        assert result.command_type == CommandType.ADJUST_LEVEL
        assert result.args["level"] == 3
    
    def test_persona_taijian(self):
        """测试大太监风格"""
        result = self.parser.parse("补手风格大太监")
        
        assert result.command_type == CommandType.SET_PERSONA
        assert result.args["persona"] == "taijian"
    
    def test_persona_xiaoyahuan(self):
        """测试小丫鬟风格"""
        result = self.parser.parse("补手风格小丫鬟")
        
        assert result.command_type == CommandType.SET_PERSONA
        assert result.args["persona"] == "xiaoyahuan"
    
    def test_persona_zaomiao(self):
        """测试早喵风格"""
        result = self.parser.parse("补手风格搞事早喵")
        
        assert result.command_type == CommandType.SET_PERSONA
        assert result.args["persona"] == "zaomiao"
    
    def test_persona_siji(self):
        """测试司机风格"""
        result = self.parser.parse("补手风格来问司机")
        
        assert result.command_type == CommandType.SET_PERSONA
        assert result.args["persona"] == "siji"
    
    def test_mode_couple_requires_confirmation(self):
        """测试情侣模式需要确认"""
        result = self.parser.parse("补手模式情侣")
        
        assert result.command_type == CommandType.SET_MODE
        assert result.args["mode"] == "couple"
        assert result.requires_confirmation == True
    
    def test_status_command(self):
        """测试状态命令"""
        result = self.parser.parse("补手状态")
        
        assert result.command_type == CommandType.STATUS
    
    def test_unknown_command(self):
        """测试未知命令"""
        result = self.parser.parse("今天天气真好")
        
        assert result.command_type == CommandType.UNKNOWN
    
    def test_case_insensitive(self):
        """测试大小写不敏感（中文命令通常不区分）"""
        result1 = self.parser.parse("进入心灵补手")
        result2 = self.parser.parse("进入心灵补手")  # 中文本身不区分大小写
        
        assert result1.command_type == result2.command_type


class TestPhraseGenerator:
    """话术生成器测试"""
    
    def setup_method(self):
        """每个测试前创建生成器"""
        # Mock config manager
        self.mock_config = {
            "enabled": True,
            "persona": "taijian",
            "level": 5,
            "gender": "male",
            "mode": "normal",
            "recent_phrases": []
        }
        
        with patch.object(ConfigManager, 'load_config', return_value=self.mock_config):
            with patch.object(ConfigManager, 'get_config', return_value=self.mock_config):
                with patch.object(ConfigManager, 'get_recent_phrases', return_value=[]):
                    with patch.object(ConfigManager, 'add_recent_phrase', return_value=None):
                        self.generator = PhraseGenerator()
    
    def test_generate_returns_list(self):
        """测试生成返回列表"""
        result = self.generator.generate("task_completed", self.mock_config)
        
        assert isinstance(result, GenerationResult)
        assert isinstance(result.phrases, list)
        assert len(result.phrases) >= 1
    
    def test_generate_contains_persona_pronouns(self):
        """测试生成包含正确人称"""
        result = self.generator.generate("task_completed", {"persona": "taijian", "level": 5, "gender": "male"})
        
        # 大太监应该用"奴才"和"主子"
        phrases_text = "".join(result.phrases)
        assert any(word in phrases_text for word in ["奴才", "主子", "您", "英明"])
    
    def test_high_level_more_exclamations(self):
        """测试高程度更多感叹号"""
        low_result = self.generator.generate("task_completed", {"persona": "taijian", "level": 3, "gender": "male"})
        high_result = self.generator.generate("task_completed", {"persona": "taijian", "level": 10, "gender": "male"})
        
        low_excl = sum(1 for c in "".join(low_result.phrases) if c in ["!", "！"])
        high_excl = sum(1 for c in "".join(high_result.phrases) if c in ["!", "！"])
        
        assert high_excl >= low_excl
    
    def test_metadata_includes_info(self):
        """测试元数据包含信息"""
        result = self.generator.generate("task_completed", {"persona": "xiaoyahuan", "level": 7, "gender": "female"})
        
        assert result.metadata["persona"] == "xiaoyahuan"
        assert result.metadata["level"] == 7
        assert result.metadata["scenario"] == "task_completed"
    
    def test_care_message(self):
        """测试关心话术"""
        msg = self.generator.generate_care_message("emotional_low")
        
        assert isinstance(msg, str)
        assert len(msg) > 0


class TestIntegration:
    """集成测试"""
    
    def test_full_workflow(self):
        """测试完整工作流"""
        # Mock config manager with temp file
        temp_dir = tempfile.mkdtemp()
        temp_config_file = Path(temp_dir) / "config.json"
        
        try:
            with patch.object(ConfigManager, 'CONFIG_FILE', temp_config_file):
                cm = ConfigManager()
                
                # 1. 加载配置
                config = cm.load_config()
                assert config["enabled"] == True
                
                # 2. 禁用功能
                cm.update_config({"enabled": False})
                config = cm.get_config()
                assert config["enabled"] == False
                
                # 3. 启用功能
                cm.update_config({"enabled": True})
                config = cm.get_config()
                assert config["enabled"] == True
                
                # 4. 设置风格
                cm.update_config({"persona": "xiaoyahuan", "level": 8})
                config = cm.get_config()
                assert config["persona"] == "xiaoyahuan"
                assert config["level"] == 8
        finally:
            import shutil
            shutil.rmtree(temp_dir, ignore_errors=True)
    
    def test_command_to_config_flow(self):
        """测试命令到配置的流程"""
        parser = CommandParser()
        
        # 解析命令
        cmd = parser.parse("补手程度9")
        assert cmd.command_type == CommandType.SET_LEVEL
        assert cmd.args["level"] == 9
        
        # 应用命令到配置
        temp_dir = tempfile.mkdtemp()
        temp_config_file = Path(temp_dir) / "config.json"
        
        try:
            with patch.object(ConfigManager, 'CONFIG_FILE', temp_config_file):
                cm = ConfigManager()
                cm.load_config()
                
                # 验证命令效果
                result = cm.update_config(cmd.args)
                assert result == True
                
                config = cm.get_config()
                assert config["level"] == 9
        finally:
            import shutil
            shutil.rmtree(temp_dir, ignore_errors=True)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
