#!/usr/bin/env python3
"""
Telegram语音消息配置类模板
版本: 1.0.0
创建: 2026-03-09
作者: 银月 (Silvermoon)
"""

import os
import json
import logging
from dataclasses import dataclass, field
from typing import Optional, Dict, List, Any
from pathlib import Path


@dataclass
class TelegramConfig:
    """Telegram配置"""
    bot_token: str = ""
    chat_id: str = ""
    api_endpoint: str = "https://api.telegram.org"
    timeout_seconds: int = 30
    max_retries: int = 3
    retry_delay_seconds: int = 2
    
    def validate(self) -> List[str]:
        """验证配置"""
        errors = []
        
        if not self.bot_token:
            errors.append("Telegram Bot Token未设置")
        
        if not self.chat_id:
            errors.append("Telegram Chat ID未设置")
        
        if self.timeout_seconds <= 0:
            errors.append("超时时间必须大于0")
        
        if self.max_retries < 0:
            errors.append("最大重试次数不能为负数")
        
        return errors


@dataclass
class TTSConfig:
    """TTS服务配置"""
    enabled: bool = True
    api_key: str = ""
    endpoint: str = ""
    model: str = ""
    voice: str = ""
    language: str = ""
    timeout_seconds: int = 30
    
    def validate(self) -> List[str]:
        """验证配置"""
        errors = []
        
        if self.enabled and not self.api_key:
            errors.append("TTS API Key未设置")
        
        if self.timeout_seconds <= 0:
            errors.append("TTS超时时间必须大于0")
        
        return errors


@dataclass
class AudioConfig:
    """音频配置"""
    format: Dict[str, Any] = field(default_factory=lambda: {
        "container": "ogg",
        "codec": "libopus",
        "bitrate": "64k",
        "sample_rate": 48000,
        "channels": 1,
        "application": "voip"
    })
    
    quality: Dict[str, Any] = field(default_factory=lambda: {
        "preset": "balanced",
        "compression_level": 5,
        "vbr": True
    })
    
    limits: Dict[str, Any] = field(default_factory=lambda: {
        "max_file_size_mb": 50,
        "max_duration_seconds": 300,
        "min_duration_seconds": 0.5
    })
    
    def get_ffmpeg_args(self) -> List[str]:
        """获取ffmpeg参数"""
        args = [
            "-acodec", self.format["codec"],
            "-b:a", self.format["bitrate"],
            "-ar", str(self.format["sample_rate"]),
            "-ac", str(self.format["channels"])
        ]
        
        if self.format.get("application"):
            args.extend(["-application", self.format["application"]])
        
        return args


@dataclass
class ProcessingConfig:
    """处理配置"""
    temp_directory: str = "/tmp/telegram_voice"
    
    cleanup: Dict[str, Any] = field(default_factory=lambda: {
        "enabled": True,
        "interval_minutes": 60,
        "max_age_minutes": 120
    })
    
    caching: Dict[str, Any] = field(default_factory=lambda: {
        "enabled": True,
        "directory": "/tmp/telegram_voice_cache",
        "max_size_mb": 500,
        "expire_hours": 24
    })
    
    parallel: Dict[str, Any] = field(default_factory=lambda: {
        "max_concurrent": 1,
        "batch_size": 10
    })


@dataclass
class LoggingConfig:
    """日志配置"""
    level: str = "INFO"
    file: str = "/tmp/telegram_voice.log"
    max_size_mb: int = 10
    max_files: int = 5
    format: str = "json"
    enable_console: bool = True
    
    def setup_logging(self):
        """设置日志"""
        level = getattr(logging, self.level.upper(), logging.INFO)
        
        # 配置根日志
        logging.basicConfig(
            level=level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # 文件处理器
        if self.file:
            from logging.handlers import RotatingFileHandler
            file_handler = RotatingFileHandler(
                self.file,
                maxBytes=self.max_size_mb * 1024 * 1024,
                backupCount=self.max_files
            )
            
            if self.format == "json":
                import json_log_formatter
                formatter = json_log_formatter.JSONFormatter()
                file_handler.setFormatter(formatter)
            
            logging.getLogger().addHandler(file_handler)


@dataclass
class SecurityConfig:
    """安全配置"""
    encryption: Dict[str, Any] = field(default_factory=lambda: {
        "enabled": False,
        "algorithm": "aes-256-gcm"
    })
    
    sanitization: Dict[str, Any] = field(default_factory=lambda: {
        "enabled": True,
        "remove_sensitive_data": True
    })
    
    rate_limiting: Dict[str, Any] = field(default_factory=lambda: {
        "enabled": True,
        "requests_per_minute": 30
    })


@dataclass
class VoiceMessageConfig:
    """Telegram语音消息完整配置"""
    
    # 配置版本
    version: str = "1.0.0"
    
    # 配置说明
    description: str = "Telegram语音消息配置"
    
    # 各模块配置
    telegram: TelegramConfig = field(default_factory=TelegramConfig)
    tts_services: Dict[str, TTSConfig] = field(default_factory=lambda: {
        "aliyun": TTSConfig(
            enabled=True,
            endpoint="https://dashscope.aliyuncs.com/api/v1/services/aigc/multisodal-generation/generation",
            model="qwen3-tts-flash",
            voice="Maia",
            language="Chinese"
        ),
        "openai": TTSConfig(
            enabled=False,
            endpoint="https://api.openai.com/v1/audio/speech",
            model="tts-1",
            voice="alloy"
        )
    })
    audio: AudioConfig = field(default_factory=AudioConfig)
    processing: ProcessingConfig = field(default_factory=ProcessingConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    security: SecurityConfig = field(default_factory=SecurityConfig)
    
    # 默认TTS服务
    default_tts_service: str = "aliyun"
    
    @classmethod
    def from_file(cls, config_file: str) -> "VoiceMessageConfig":
        """从配置文件加载"""
        if not os.path.exists(config_file):
            raise FileNotFoundError(f"配置文件不存在: {config_file}")
        
        with open(config_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return cls.from_dict(data)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "VoiceMessageConfig":
        """从字典加载"""
        # 创建配置实例
        config = cls()
        
        # 更新Telegram配置
        if "telegram" in data:
            telegram_data = data["telegram"]
            config.telegram = TelegramConfig(
                bot_token=telegram_data.get("bot_token", ""),
                chat_id=telegram_data.get("chat_id", ""),
                api_endpoint=telegram_data.get("api_endpoint", "https://api.telegram.org"),
                timeout_seconds=telegram_data.get("timeout_seconds", 30),
                max_retries=telegram_data.get("max_retries", 3),
                retry_delay_seconds=telegram_data.get("retry_delay_seconds", 2)
            )
        
        # 更新TTS服务配置
        if "tts_services" in data:
            tts_data = data["tts_services"]
            for service_name, service_data in tts_data.items():
                if service_name in config.tts_services:
                    config.tts_services[service_name] = TTSConfig(
                        enabled=service_data.get("enabled", True),
                        api_key=service_data.get("api_key", ""),
                        endpoint=service_data.get("endpoint", ""),
                        model=service_data.get("model", ""),
                        voice=service_data.get("voice", ""),
                        language=service_data.get("language", ""),
                        timeout_seconds=service_data.get("timeout_seconds", 30)
                    )
        
        # 更新音频配置
        if "audio" in data:
            audio_data = data["audio"]
            config.audio = AudioConfig(
                format=audio_data.get("format", config.audio.format),
                quality=audio_data.get("quality", config.audio.quality),
                limits=audio_data.get("limits", config.audio.limits)
            )
        
        # 更新处理配置
        if "processing" in data:
            processing_data = data["processing"]
            config.processing = ProcessingConfig(
                temp_directory=processing_data.get("temp_directory", "/tmp/telegram_voice"),
                cleanup=processing_data.get("cleanup", config.processing.cleanup),
                caching=processing_data.get("caching", config.processing.caching),
                parallel=processing_data.get("parallel", config.processing.parallel)
            )
        
        # 更新日志配置
        if "logging" in data:
            logging_data = data["logging"]
            config.logging = LoggingConfig(
                level=logging_data.get("level", "INFO"),
                file=logging_data.get("file", "/tmp/telegram_voice.log"),
                max_size_mb=logging_data.get("max_size_mb", 10),
                max_files=logging_data.get("max_files", 5),
                format=logging_data.get("format", "json"),
                enable_console=logging_data.get("enable_console", True)
            )
        
        # 更新安全配置
        if "security" in data:
            security_data = data["security"]
            config.security = SecurityConfig(
                encryption=security_data.get("encryption", config.security.encryption),
                sanitization=security_data.get("sanitization", config.security.sanitization),
                rate_limiting=security_data.get("rate_limiting", config.security.rate_limiting)
            )
        
        # 更新默认TTS服务
        if "default_tts_service" in data:
            config.default_tts_service = data["default_tts_service"]
        
        return config
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "version": self.version,
            "description": self.description,
            "telegram": {
                "bot_token": self.telegram.bot_token,
                "chat_id": self.telegram.chat_id,
                "api_endpoint": self.telegram.api_endpoint,
                "timeout_seconds": self.telegram.timeout_seconds,
                "max_retries": self.telegram.max_retries,
                "retry_delay_seconds": self.telegram.retry_delay_seconds
            },
            "tts_services": {
                name: {
                    "enabled": service.enabled,
                    "api_key": service.api_key,
                    "endpoint": service.endpoint,
                    "model": service.model,
                    "voice": service.voice,
                    "language": service.language,
                    "timeout_seconds": service.timeout_seconds
                }
                for name, service in self.tts_services.items()
            },
            "audio": {
                "format": self.audio.format,
                "quality": self.audio.quality,
                "limits": self.audio.limits
            },
            "processing": {
                "temp_directory": self.processing.temp_directory,
                "cleanup": self.processing.cleanup,
                "caching": self.processing.caching,
                "parallel": self.processing.parallel
            },
            "logging": {
                "level": self.logging.level,
                "file": self.logging.file,
                "max_size_mb": self.logging.max_size_mb,
                "max_files": self.logging.max_files,
                "format": self.logging.format,
                "enable_console": self.logging.enable_console
            },
            "security": {
                "encryption": self.security.encryption,
                "sanitization": self.security.sanitization,
                "rate_limiting": self.security.rate_limiting
            },
            "default_tts_service": self.default_tts_service
        }
    
    def save_to_file(self, config_file: str):
        """保存到配置文件"""
        data = self.to_dict()
        
        # 确保目录存在
        os.makedirs(os.path.dirname(os.path.abspath(config_file)), exist_ok=True)
        
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def validate(self) -> List[str]:
        """验证所有配置"""
        errors = []
        
        # 验证Telegram配置
        errors.extend(self.telegram.validate())
        
        # 验证启用的TTS服务
        for name, service in self.tts_services.items():
            if service.enabled:
                service_errors = service.validate()
                if service_errors:
                    errors.extend([f"TTS服务 '{name}': {err}" for err in service_errors])
        
        # 验证音频配置
        if not self.audio.format.get("container") == "ogg":
            errors.append("音频容器格式必须是ogg")
        
        if not self.audio.format.get("codec") == "libopus":
            errors.append("音频编码器必须是libopus")
        
        # 验证默认TTS服务
        if self.default_tts_service not in self.tts_services:
            errors.append(f"默认TTS服务 '{self.default_tts_service}' 未定义")
        elif not self.tts_services[self.default_tts_service].enabled:
            errors.append(f"默认TTS服务 '{self.default_tts_service}' 未启用")
        
        return errors
    
    def get_env_vars(self) -> Dict[str, str]:
        """获取环境变量映射"""
        return {
            "TELEGRAM_BOT_TOKEN": self.telegram.bot_token,
            "TELEGRAM_CHAT_ID": self.telegram.chat_id,
            "ALIYUN_TTS_API_KEY": self.tts_services.get("aliyun", TTSConfig()).api_key,
            "OPENAI_API_KEY": self.tts_services.get("openai", TTSConfig()).api_key
        }
    
    def apply_env_vars(self):
        """应用环境变量"""
        env_vars = self.get_env_vars()
        for key, value in env_vars.items():
            if value:
                os.environ[key] = value


# 配置管理器
class ConfigManager:
    """配置管理器"""
    
    def __init__(self, config_file: Optional[str] = None):
        self.config_file = config_file
        self.config: Optional[VoiceMessageConfig] = None
        
        if config_file:
            self.load_config(config_file)
    
    def load_config(self, config_file: str):
        """加载配置"""
        self.config = VoiceMessageConfig.from_file(config_file)
        self.config_file = config_file
        return self.config
    
    def save_config(self, config_file: Optional[str] = None):
        """保存配置"""
        if not self.config:
            raise ValueError("没有配置可保存")
        
        save_file = config_file or self.config_file
        if not save_file:
            raise ValueError("未指定配置文件路径")
        
        self.config.save_to_file(save_file)
    
    def validate_config(self) -> bool:
        """验证配置"""
        if not self.config:
            return False
        
        errors = self.config.validate()
        if errors:
            print("配置验证失败:")
            for error in errors:
                print(f"  ❌ {error}")
            return False
        
        print("✅ 配置验证通过")
        return True
    
    def apply_to_environment(self):
        """应用到环境变量"""
        if self.config:
            self.config.apply_env_vars()
            print("✅ 配置已应用到环境变量")
    
    def get_config_summary(self) -> Dict[str, Any]:
        """获取配置摘要（不含敏感信息）"""
        if not self.config:
            return {}
        
        data = self.config.to_dict()
        
        # 隐藏敏感信息
        if "telegram" in data:
            if "bot_token" in data["telegram"]:
                token = data["telegram"]["bot_token"]
                if token:
                    data["telegram"]["bot_token"] = f"{token[:10]}...{token[-5:]}"
        
        if "tts_services" in data:
            for service_name, service_data in data["tts_services"].items():
                if "api_key" in service_data:
                    api_key = service_data["api_key"]
                    if api_key:
                        service_data["api_key"] = f"{api_key[:10]}...{api_key[-5:]}"
        
        return data


# 使用示例
if __name__ == "__main__":
    print("Telegram语音消息配置类示例")
    print("=" * 50)
    
    # 创建默认配置
    config = VoiceMessageConfig()
    
    # 验证配置
    errors = config.validate()
    if errors:
        print("配置错误:")
        for error in errors:
            print(f"  ❌ {error}")
    else:
        print("✅ 默认配置验证通过")
    
    # 转换为字典
    config_dict = config.to_dict()
    print(f"配置字典大小: {len(json.dumps(config_dict))} 字符")
    
    # 保存到文件
    config.save_to_file("config.example.json")
    print("✅ 配置已保存到 config.example.json")
    
    # 使用配置管理器
    print("\n配置管理器示例:")
    manager = ConfigManager()
    
    # 从文件加载
    try:
        loaded_config = manager.load_config("config.example.json")
        print("✅ 配置加载成功")
        
        # 验证
        if manager.validate_config():
            print("✅ 配置验证成功")
            
            # 应用到环境
            manager.apply_to_environment()
            
            # 获取摘要
            summary = manager.get_config_summary()
            print(f"配置摘要: {json.dumps(summary, indent=2)}")
    
    except FileNotFoundError as e:
        print(f"❌ 文件未找到: {e}")
    except json.JSONDecodeError as e:
        print(f"❌ JSON解析错误: {e}")
    
    print("\n✅ 配置类示例完成")