"""
全局设置和配置管理
"""

import os
import json
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum


class LogLevel(Enum):
    """日志级别"""
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class GlobalSettings:
    """全局设置"""
    # 日志设置
    log_level: LogLevel = LogLevel.INFO
    log_file: Optional[str] = None
    enable_console_log: bool = True
    
    # 性能设置
    max_workers: int = 4
    timeout_seconds: int = 30
    max_retries: int = 3
    retry_delay_seconds: float = 2.0
    
    # 文件设置
    default_output_dir: str = "~/Desktop"
    temp_dir: str = "/tmp/ppt_maker"
    max_file_size_mb: int = 100  # 最大文件大小限制
    
    # 安全设置
    enable_ssl_verification: bool = True
    allow_insecure_connections: bool = False
    
    # 功能开关
    enable_advanced_features: bool = False
    enable_ai_assistance: bool = False
    enable_template_cache: bool = True
    
    # 用户界面
    default_language: str = "zh-CN"
    show_progress_bar: bool = True
    enable_notifications: bool = True


@dataclass
class PlatformSettings:
    """平台特定设置"""
    # 飞书设置
    feishu_app_id: Optional[str] = None
    feishu_app_secret: Optional[str] = None
    feishu_default_folder: Optional[str] = None
    
    # 微信设置
    wechat_app_id: Optional[str] = None
    wechat_app_secret: Optional[str] = None
    
    # 钉钉设置
    dingtalk_app_key: Optional[str] = None
    dingtalk_app_secret: Optional[str] = None
    
    # Slack设置
    slack_bot_token: Optional[str] = None
    slack_default_channel: Optional[str] = None
    
    # 通用设置
    default_platform: str = "feishu"
    enable_auto_upload: bool = True
    enable_auto_cleanup: bool = False


@dataclass
class GeneratorSettings:
    """生成器设置"""
    # 默认生成器
    default_generator: str = "powerpoint"  # powerpoint, wps, google_slides
    
    # PowerPoint设置
    powerpoint_template: str = "business"
    powerpoint_quality: str = "high"  # low, medium, high
    
    # WPS设置
    wps_template: str = "business"
    wps_use_online: bool = False
    
    # 内容设置
    default_title: str = "演示文稿"
    default_author: str = "OpenClaw PPT Maker"
    enable_auto_date: bool = True
    enable_page_numbers: bool = True
    
    # 样式设置
    default_font_family: str = "微软雅黑"
    default_font_size: int = 18
    enable_custom_colors: bool = True
    enable_animations: bool = False
    
    # 模板设置
    template_cache_size: int = 10
    enable_template_download: bool = True


class ConfigManager:
    """配置管理器"""
    
    def __init__(self, config_file: Optional[str] = None):
        """
        初始化配置管理器
        
        Args:
            config_file: 配置文件路径
        """
        self.config_file = config_file or self._get_default_config_path()
        self.global_settings = GlobalSettings()
        self.platform_settings = PlatformSettings()
        self.generator_settings = GeneratorSettings()
        
        # 加载配置
        self.load_config()
    
    def _get_default_config_path(self) -> str:
        """
        获取默认配置文件路径
        
        Returns:
            配置文件路径
        """
        config_dir = os.path.expanduser("~/.openclaw/ppt_maker")
        os.makedirs(config_dir, exist_ok=True)
        return os.path.join(config_dir, "config.json")
    
    def load_config(self) -> None:
        """
        从配置文件加载配置
        """
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                
                # 加载全局设置
                if 'global' in config_data:
                    self._load_settings_from_dict(self.global_settings, config_data['global'])
                
                # 加载平台设置
                if 'platform' in config_data:
                    self._load_settings_from_dict(self.platform_settings, config_data['platform'])
                
                # 加载生成器设置
                if 'generator' in config_data:
                    self._load_settings_from_dict(self.generator_settings, config_data['generator'])
                
                print(f"✅ 配置已从文件加载: {self.config_file}")
                
            except Exception as e:
                print(f"❌ 加载配置文件失败: {e}")
                print("使用默认配置")
        else:
            print(f"⚠️ 配置文件不存在: {self.config_file}")
            print("使用默认配置")
    
    def _load_settings_from_dict(self, settings_obj, data_dict: Dict[str, Any]) -> None:
        """
        从字典加载设置到数据类
        
        Args:
            settings_obj: 设置对象
            data_dict: 数据字典
        """
        for key, value in data_dict.items():
            if hasattr(settings_obj, key):
                # 特殊处理枚举类型
                if isinstance(getattr(settings_obj, key), Enum):
                    try:
                        enum_type = type(getattr(settings_obj, key))
                        setattr(settings_obj, key, enum_type(value))
                    except ValueError:
                        print(f"⚠️ 无法将 {value} 转换为 {type(getattr(settings_obj, key))}")
                else:
                    setattr(settings_obj, key, value)
    
    def save_config(self) -> None:
        """
        保存配置到文件
        """
        config_data = {
            'global': asdict(self.global_settings),
            'platform': asdict(self.platform_settings),
            'generator': asdict(self.generator_settings)
        }
        
        # 转换枚举值为字符串
        for section in config_data.values():
            for key, value in section.items():
                if isinstance(value, Enum):
                    section[key] = value.value
        
        try:
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ 配置已保存到文件: {self.config_file}")
            
        except Exception as e:
            print(f"❌ 保存配置文件失败: {e}")
    
    def update_platform_config(self, platform: str, config: Dict[str, Any]) -> None:
        """
        更新平台配置
        
        Args:
            platform: 平台名称
            config: 配置字典
        """
        if platform == "feishu":
            for key, value in config.items():
                if hasattr(self.platform_settings, f"feishu_{key}"):
                    setattr(self.platform_settings, f"feishu_{key}", value)
                elif hasattr(self.platform_settings, key):
                    setattr(self.platform_settings, key, value)
        
        elif platform == "wechat":
            for key, value in config.items():
                if hasattr(self.platform_settings, f"wechat_{key}"):
                    setattr(self.platform_settings, f"wechat_{key}", value)
                elif hasattr(self.platform_settings, key):
                    setattr(self.platform_settings, key, value)
        
        # 其他平台类似...
        
        self.save_config()
    
    def get_platform_config(self, platform: str) -> Dict[str, Any]:
        """
        获取平台配置
        
        Args:
            platform: 平台名称
            
        Returns:
            平台配置字典
        """
        config = {}
        
        if platform == "feishu":
            config = {
                'app_id': self.platform_settings.feishu_app_id,
                'app_secret': self.platform_settings.feishu_app_secret,
                'default_folder': self.platform_settings.feishu_default_folder
            }
        
        elif platform == "wechat":
            config = {
                'app_id': self.platform_settings.wechat_app_id,
                'app_secret': self.platform_settings.wechat_app_secret
            }
        
        elif platform == "dingtalk":
            config = {
                'app_key': self.platform_settings.dingtalk_app_key,
                'app_secret': self.platform_settings.dingtalk_app_secret
            }
        
        elif platform == "slack":
            config = {
                'bot_token': self.platform_settings.slack_bot_token,
                'default_channel': self.platform_settings.slack_default_channel
            }
        
        return {k: v for k, v in config.items() if v is not None}
    
    def validate_config(self) -> bool:
        """
        验证配置是否有效
        
        Returns:
            配置是否有效
        """
        errors = []
        
        # 验证全局设置
        if self.global_settings.max_file_size_mb <= 0:
            errors.append("最大文件大小必须大于0")
        
        if self.global_settings.timeout_seconds <= 0:
            errors.append("超时时间必须大于0")
        
        # 验证平台设置
        if self.platform_settings.default_platform == "feishu":
            if not self.platform_settings.feishu_app_id:
                errors.append("飞书应用ID未配置")
            if not self.platform_settings.feishu_app_secret:
                errors.append("飞书应用密钥未配置")
        
        # 验证生成器设置
        if self.generator_settings.default_generator not in ["powerpoint", "wps", "google_slides"]:
            errors.append(f"不支持的生成器类型: {self.generator_settings.default_generator}")
        
        if errors:
            print("❌ 配置验证失败:")
            for error in errors:
                print(f"   - {error}")
            return False
        
        print("✅ 配置验证通过")
        return True


# 全局配置实例
_config_manager = None

def get_config_manager(config_file: Optional[str] = None) -> ConfigManager:
    """
    获取全局配置管理器实例
    
    Args:
        config_file: 配置文件路径
        
    Returns:
        ConfigManager实例
    """
    global _config_manager
    
    if _config_manager is None:
        _config_manager = ConfigManager(config_file)
    
    return _config_manager


if __name__ == "__main__":
    # 测试配置管理
    print("🔧 配置管理器测试")
    print("=" * 50)
    
    config_manager = get_config_manager()
    
    print("📋 当前配置:")
    print(f"  默认生成器: {config_manager.generator_settings.default_generator}")
    print(f"  默认平台: {config_manager.platform_settings.default_platform}")
    print(f"  日志级别: {config_manager.global_settings.log_level.value}")
    
    # 验证配置
    is_valid = config_manager.validate_config()
    print(f"\n🔍 配置验证: {'✅ 有效' if is_valid else '❌ 无效'}")
    
    # 保存测试配置
    config_manager.save_config()