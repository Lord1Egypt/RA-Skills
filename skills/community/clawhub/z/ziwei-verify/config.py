"""
config.py - 配置管理
"""

import os
import logging
from dataclasses import dataclass, field
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class ZiweiVerifyConfig:
    """ziwei_verify 技能配置"""
    
    # 生时校正范围（时辰）
    max_shifts: int = 2
    
    # 超时设置（秒）
    timeout_per_candidate: float = 5.0
    total_timeout: float = 30.0
    
    # 缓存设置
    cache_enabled: bool = True
    cache_ttl_seconds: int = 3600  # 1小时
    
    # 交互模式
    interactive_by_default: bool = False
    
    # 置信度阈值
    confidence_threshold_auto: float = 0.7
    confidence_threshold_low: float = 0.4
    
    # 日志级别
    log_level: str = "INFO"
    
    # 模拟模式（开发用）
    simulation_mode: bool = False
    
    # 扩展配置（自由字段）
    extra: dict = field(default_factory=dict)
    
    @classmethod
    def from_env(cls) -> "ZiweiVerifyConfig":
        """
        从环境变量加载配置
        
        环境变量前缀：ZIWEI_VERIFY_
        示例：ZIWEI_VERIFY_MAX_SHIFTS=2
        """
        config = cls()
        
        # 读取环境变量
        for field_name, field_info in cls.__dataclass_fields__.items():
            env_key = f"ZIWEI_VERIFY_{field_name.upper()}"
            env_val = os.environ.get(env_key)
            
            if env_val is not None:
                try:
                    # 类型转换
                    field_type = field_info.type
                    if field_type == int:
                        setattr(config, field_name, int(env_val))
                    elif field_type == float:
                        setattr(config, field_name, float(env_val))
                    elif field_type == bool:
                        setattr(config, field_name, env_val.lower() in ("true", "1", "yes"))
                    elif field_type == str:
                        setattr(config, field_name, env_val)
                    elif field_type == dict:
                        import json
                        setattr(config, field_name, json.loads(env_val))
                    else:
                        logger.warning(f"未知配置类型: {field_name} = {field_type}")
                except Exception as e:
                    logger.error(f"配置解析失败 {env_key}={env_val}: {e}")
        
        return config
    
    def validate(self) -> tuple[bool, list[str]]:
        """
        验证配置合法性
        
        返回：(is_valid, error_messages)
        """
        errors = []
        
        if self.max_shifts not in (1, 2):
            errors.append(f"max_shifts 必须为 1 或 2，当前: {self.max_shifts}")
        
        if not (0 < self.timeout_per_candidate <= 60):
            errors.append(f"timeout_per_candidate 必须在 (0, 60] 范围内，当前: {self.timeout_per_candidate}")
        
        if self.total_timeout < self.timeout_per_candidate * 5:  # 至少能跑完5个候选
            errors.append(f"total_timeout 过小，至少应为 {self.timeout_per_candidate * 5}s")
        
        if not (0 <= self.confidence_threshold_auto <= 1):
            errors.append(f"confidence_threshold_auto 必须在 [0, 1]，当前: {self.confidence_threshold_auto}")
        
        if not (0 <= self.confidence_threshold_low <= 1):
            errors.append(f"confidence_threshold_low 必须在 [0, 1]，当前: {self.confidence_threshold_low}")
        
        if self.cache_ttl_seconds < 60:
            errors.append(f"cache_ttl_seconds 不应小于 60 秒")
        
        return len(errors) == 0, errors


# 全局配置实例
_config: Optional[ZiweiVerifyConfig] = None


def get_config() -> ZiweiVerifyConfig:
    """获取全局配置实例（单例）"""
    global _config
    if _config is None:
        _config = ZiweiVerifyConfig.from_env()
        valid, errors = _config.validate()
        if not valid:
            logger.error(f"配置验证失败: {errors}")
            # 不抛出异常，允许降级运行
        logger.info(f"ziwei_verify 配置加载完成: max_shifts={_config.max_shifts}, simulation_mode={_config.simulation_mode}")
    return _config


def set_config(new_config: ZiweiVerifyConfig):
    """设置全局配置（用于测试或热更新）"""
    global _config
    _config = new_config
