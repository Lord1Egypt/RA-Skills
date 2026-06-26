"""
配置文件管理器
管理 ~/.xinling-bushou/config.json
"""
import json
import os
from pathlib import Path
from typing import Dict, Optional, Any
from dataclasses import dataclass, asdict, field
from datetime import datetime


@dataclass
class XinlingConfig:
    """心灵补手配置"""
    enabled: bool = True
    persona: str = "taijian"  # taijian, xiaoyahuan, zaomiao, siji
    level: int = 5  # 1-10
    gender: str = "male"  # male, female
    mode: str = "normal"  # normal, couple (couple需要确认解锁)
    
    # 会话状态
    session_trigger_count: int = 0
    session_start_time: Optional[str] = None
    last_trigger_round: Dict[str, int] = field(default_factory=dict)  # scenario -> round
    
    # 历史话术（用于去重）
    recent_phrases: list = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "XinlingConfig":
        # 过滤掉未知字段
        known_fields = {f.name for f in cls.__dataclass_fields__.values()}
        filtered = {k: v for k, v in data.items() if k in known_fields}
        return cls(**filtered)


class ConfigManager:
    """配置文件管理器"""
    
    CONFIG_DIR = Path.home() / ".xinling-bushou"
    CONFIG_FILE = CONFIG_DIR / "config.json"
    
    def __init__(self):
        self._config: Optional[XinlingConfig] = None
        self._ensure_config_dir()
    
    def _ensure_config_dir(self) -> None:
        """确保配置目录存在"""
        self.CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    
    def _get_default_config(self) -> XinlingConfig:
        """获取默认配置"""
        return XinlingConfig(
            enabled=True,
            persona="taijian",
            level=5,
            gender="male",
            mode="normal",
            session_start_time=datetime.now().isoformat()
        )
    
    def load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        if self._config is not None:
            return self._config.to_dict()
        
        if not self.CONFIG_FILE.exists():
            self._config = self._get_default_config()
            self.save_config(self._config.to_dict())
            return self._config.to_dict()
        
        try:
            with open(self.CONFIG_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self._config = XinlingConfig.from_dict(data)
            
            # 重置会话状态
            self._config.session_trigger_count = 0
            self._config.session_start_time = datetime.now().isoformat()
            self._config.last_trigger_round = {}
            # recent_phrases 保留以保持去重功能
            
            return self._config.to_dict()
        except (json.JSONDecodeError, TypeError) as e:
            print(f"配置读取失败: {e}, 使用默认配置")
            self._config = self._get_default_config()
            return self._config.to_dict()
    
    def save_config(self, config: Dict[str, Any]) -> bool:
        """保存配置文件"""
        try:
            with open(self.CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            self._config = XinlingConfig.from_dict(config)
            return True
        except Exception as e:
            print(f"配置保存失败: {e}")
            return False
    
    def get_config(self) -> Dict[str, Any]:
        """获取当前配置"""
        if self._config is None:
            self.load_config()
        return self._config.to_dict()
    
    def update_config(self, changes: Dict[str, Any]) -> bool:
        """更新配置"""
        if self._config is None:
            self.load_config()
        
        current = self._config.to_dict()
        current.update(changes)
        
        # 验证字段
        valid_personas = ["taijian", "xiaoyahuan", "zaomiao", "siji"]
        valid_modes = ["normal", "couple"]
        
        if "persona" in changes and changes["persona"] not in valid_personas:
            print(f"无效的persona: {changes['persona']}, 必须是 {valid_personas}")
            return False
        
        if "mode" in changes and changes["mode"] not in valid_modes:
            print(f"无效的mode: {changes['mode']}, 必须是 {valid_modes}")
            return False
        
        if "level" in changes:
            level = changes["level"]
            if isinstance(level, int) and (level < 1 or level > 10):
                print(f"无效的level: {level}, 必须在1-10之间")
                return False
        
        return self.save_config(current)
    
    def reset_config(self) -> bool:
        """重置配置"""
        self._config = self._get_default_config()
        return self.save_config(self._config.to_dict())
    
    def increment_trigger_count(self) -> int:
        """增加触发计数"""
        if self._config is None:
            self.load_config()
        self._config.session_trigger_count += 1
        self.save_config(self._config.to_dict())
        return self._config.session_trigger_count
    
    def update_last_trigger_round(self, scenario: str, round_num: int) -> None:
        """更新最后触发轮次"""
        if self._config is None:
            self.load_config()
        self._config.last_trigger_round[scenario] = round_num
        self.save_config(self._config.to_dict())
    
    def add_recent_phrase(self, phrase: str) -> None:
        """添加最近使用的话术"""
        if self._config is None:
            self.load_config()
        self._config.recent_phrases.append(phrase)
        # 只保留最近10条
        if len(self._config.recent_phrases) > 10:
            self._config.recent_phrases = self._config.recent_phrases[-10:]
        self.save_config(self._config.to_dict())
    
    def get_recent_phrases(self) -> list:
        """获取最近使用的话术"""
        if self._config is None:
            self.load_config()
        return self._config.recent_phrases.copy()


# 全局单例
_config_manager: Optional[ConfigManager] = None


def get_config_manager() -> ConfigManager:
    """获取配置管理器单例"""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager


def load_config() -> Dict[str, Any]:
    """快捷函数：加载配置"""
    return get_config_manager().load_config()


def save_config(config: Dict[str, Any]) -> bool:
    """快捷函数：保存配置"""
    return get_config_manager().save_config(config)


def update_config(changes: Dict[str, Any]) -> bool:
    """快捷函数：更新配置"""
    return get_config_manager().update_config(changes)


def get_config() -> Dict[str, Any]:
    """快捷函数：获取配置"""
    return get_config_manager().get_config()


def reset_config() -> bool:
    """快捷函数：重置配置"""
    return get_config_manager().reset_config()
