#!/usr/bin/env python3
"""配置管理模块测试"""

import json
import os
import tempfile
import pytest
from scripts.config_manager import ConfigManager, AppConfig, LLMConfig, NotifyConfig


@pytest.fixture
def temp_config_dir():
    """创建临时配置目录"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def config_manager(temp_config_dir):
    """创建配置管理器实例"""
    config_path = os.path.join(temp_config_dir, "config.json")
    return ConfigManager(config_path)


class TestLLMConfig:
    def test_default_values(self):
        """测试LLM配置默认值"""
        config = LLMConfig()
        assert config.enabled is False
        assert config.base_url == "https://api.openai.com/v1"
        assert config.model == "gpt-4o-mini"
        assert config.timeout == 30
        assert config.retries == 2

    def test_custom_values(self):
        """测试LLM配置自定义值"""
        config = LLMConfig(
            enabled=True,
            base_url="https://custom.api.com/v1",
            model="custom-model",
            timeout=60,
            retries=3,
        )
        assert config.enabled is True
        assert config.base_url == "https://custom.api.com/v1"
        assert config.model == "custom-model"
        assert config.timeout == 60
        assert config.retries == 3


class TestNotifyConfig:
    def test_default_values(self):
        """测试通知配置默认值"""
        config = NotifyConfig()
        assert config.type == "terminal"
        assert config.webhook_url == ""

    def test_custom_values(self):
        """测试通知配置自定义值"""
        config = NotifyConfig(type="webhook", webhook_url="https://example.com/webhook")
        assert config.type == "webhook"
        assert config.webhook_url == "https://example.com/webhook"


class TestAppConfig:
    def test_default_values(self):
        """测试应用配置默认值"""
        config = AppConfig()
        assert isinstance(config.llm, LLMConfig)
        assert isinstance(config.notify, NotifyConfig)
        assert config.fetch_interval_days == 7

    def test_custom_values(self):
        """测试应用配置自定义值"""
        llm = LLMConfig(enabled=True)
        notify = NotifyConfig(type="webhook")
        config = AppConfig(llm=llm, notify=notify, fetch_interval_days=14)
        assert config.llm.enabled is True
        assert config.notify.type == "webhook"
        assert config.fetch_interval_days == 14


class TestConfigManager:
    def test_load_default_config(self, config_manager):
        """测试加载默认配置（配置文件不存在）"""
        config = config_manager.load()
        assert isinstance(config, AppConfig)
        assert config.llm.enabled is False
        assert config.notify.type == "terminal"
        assert config.fetch_interval_days == 7

    def test_load_existing_config(self, config_manager, temp_config_dir):
        """测试加载现有配置文件"""
        config_data = {
            "llm": {
                "enabled": True,
                "base_url": "https://custom.api.com/v1",
                "model": "custom-model",
                "timeout": 60,
                "retries": 3,
            },
            "notify": {
                "type": "webhook",
                "webhook_url": "https://example.com/webhook",
            },
            "fetch_interval_days": 14,
        }
        config_path = os.path.join(temp_config_dir, "config.json")
        with open(config_path, "w") as f:
            json.dump(config_data, f)
        
        config_manager.config_path = config_path
        config = config_manager.load()
        
        assert config.llm.enabled is True
        assert config.llm.base_url == "https://custom.api.com/v1"
        assert config.llm.model == "custom-model"
        assert config.llm.timeout == 60
        assert config.llm.retries == 3
        assert config.notify.type == "webhook"
        assert config.notify.webhook_url == "https://example.com/webhook"
        assert config.fetch_interval_days == 14

    def test_load_invalid_json(self, config_manager, temp_config_dir):
        """测试加载无效JSON配置文件"""
        config_path = os.path.join(temp_config_dir, "config.json")
        with open(config_path, "w") as f:
            f.write("invalid json")
        
        config_manager.config_path = config_path
        config = config_manager.load()
        
        assert isinstance(config, AppConfig)
        assert config.llm.enabled is False

    def test_save_config(self, config_manager, temp_config_dir):
        """测试保存配置"""
        config = AppConfig(
            llm=LLMConfig(enabled=True, model="test-model"),
            notify=NotifyConfig(type="webhook"),
            fetch_interval_days=21,
        )
        
        config_manager.save(config)
        
        assert os.path.exists(config_manager.config_path)
        
        with open(config_manager.config_path, "r") as f:
            saved_data = json.load(f)
        
        assert saved_data["llm"]["enabled"] is True
        assert saved_data["llm"]["model"] == "test-model"
        assert saved_data["notify"]["type"] == "webhook"
        assert saved_data["fetch_interval_days"] == 21

    def test_load_caching(self, config_manager):
        """测试配置加载缓存"""
        config1 = config_manager.load()
        config2 = config_manager.load()
        assert config1 is config2

    def test_get_llm_api_key(self, config_manager, temp_config_dir):
        """测试获取LLM API Key"""
        env_path = os.path.join(temp_config_dir, ".env")
        with open(env_path, "w") as f:
            f.write("LLM_API_KEY=test-api-key-123\n")
        
        # 更新config_manager的env路径
        original_skill_dir = __import__('scripts.config_manager', fromlist=['SKILL_DIR']).SKILL_DIR
        __import__('scripts.config_manager', fromlist=['SKILL_DIR']).SKILL_DIR = temp_config_dir
        
        api_key = config_manager.get_llm_api_key()
        assert api_key == "test-api-key-123"
        
        # 恢复原始路径
        __import__('scripts.config_manager', fromlist=['SKILL_DIR']).SKILL_DIR = original_skill_dir

    def test_get_llm_api_key_missing(self, config_manager, temp_config_dir):
        """测试获取不存在的LLM API Key"""
        # 确保没有.env文件
        env_path = os.path.join(temp_config_dir, ".env")
        if os.path.exists(env_path):
            os.remove(env_path)
        
        original_skill_dir = __import__('scripts.config_manager', fromlist=['SKILL_DIR']).SKILL_DIR
        __import__('scripts.config_manager', fromlist=['SKILL_DIR']).SKILL_DIR = temp_config_dir
        
        api_key = config_manager.get_llm_api_key()
        assert api_key is None
        
        __import__('scripts.config_manager', fromlist=['SKILL_DIR']).SKILL_DIR = original_skill_dir

    def test_get_llm_api_key_commented(self, config_manager, temp_config_dir):
        """测试获取被注释的LLM API Key"""
        env_path = os.path.join(temp_config_dir, ".env")
        with open(env_path, "w") as f:
            f.write("# LLM_API_KEY=commented-key\n")
        
        original_skill_dir = __import__('scripts.config_manager', fromlist=['SKILL_DIR']).SKILL_DIR
        __import__('scripts.config_manager', fromlist=['SKILL_DIR']).SKILL_DIR = temp_config_dir
        
        api_key = config_manager.get_llm_api_key()
        assert api_key is None
        
        __import__('scripts.config_manager', fromlist=['SKILL_DIR']).SKILL_DIR = original_skill_dir

    def test_partial_config(self, config_manager, temp_config_dir):
        """测试部分配置（使用默认值填充缺失字段）"""
        config_data = {
            "llm": {
                "enabled": True,
            },
            "fetch_interval_days": 3,
        }
        config_path = os.path.join(temp_config_dir, "config.json")
        with open(config_path, "w") as f:
            json.dump(config_data, f)
        
        config_manager.config_path = config_path
        config = config_manager.load()
        
        assert config.llm.enabled is True
        assert config.llm.base_url == "https://api.openai.com/v1"  # 默认值
        assert config.llm.model == "gpt-4o-mini"  # 默认值
        assert config.notify.type == "terminal"  # 默认值
        assert config.fetch_interval_days == 3
