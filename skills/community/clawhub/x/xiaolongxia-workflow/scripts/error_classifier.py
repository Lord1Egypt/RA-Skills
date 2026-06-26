#!/usr/bin/env python3
"""
错误分类器 - 小龙虾工作流 v0.2.0 核心组件

功能：
1. 识别常见的API错误（400, 401, 403, 429, 500, 502, 503, 504）
2. 提供处理策略（重试、降级、拆分输入等）
3. 记录错误模式，提供改进建议
4. 集成到步骤执行器中，实现自动错误恢复
"""

import re
import json
import time
import os
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Tuple
from enum import Enum
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ErrorType(Enum):
    """错误类型枚举"""
    BAD_REQUEST = "bad_request"           # 400
    UNAUTHORIZED = "unauthorized"         # 401
    FORBIDDEN = "forbidden"               # 403
    RATE_LIMIT = "rate_limit"             # 429
    SERVER_ERROR = "server_error"         # 500
    BAD_GATEWAY = "bad_gateway"           # 502
    SERVICE_UNAVAILABLE = "service_unavailable"  # 503
    GATEWAY_TIMEOUT = "gateway_timeout"   # 504
    CONTENT_TOO_LONG = "content_too_long" # 输入/输出过长
    INVALID_FORMAT = "invalid_format"     # 格式错误
    NETWORK_ERROR = "network_error"       # 网络错误
    TIMEOUT = "timeout"                   # 超时
    UNKNOWN = "unknown"                   # 未知错误


class ErrorSeverity(Enum):
    """错误严重程度"""
    LOW = "low"          # 轻微，可自动恢复
    MEDIUM = "medium"    # 中等，可能需要人工干预
    HIGH = "high"        # 严重，需要立即关注
    CRITICAL = "critical" # 致命，任务无法继续


@dataclass
class ErrorInfo:
    """错误信息"""
    error_type: ErrorType
    severity: ErrorSeverity
    http_code: Optional[int] = None
    error_message: str = ""
    error_details: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'error_type': self.error_type.value,
            'severity': self.severity.value,
            'http_code': self.http_code,
            'error_message': self.error_message,
            'error_details': self.error_details,
            'timestamp': self.timestamp
        }


@dataclass
class RecoveryStrategy:
    """恢复策略"""
    name: str
    description: str
    actions: List[str]  # 具体操作步骤
    estimated_time_seconds: int  # 预计恢复时间
    success_probability: float   # 成功率估计（0-1）
    prerequisites: List[str] = field(default_factory=list)  # 前提条件
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'name': self.name,
            'description': self.description,
            'actions': self.actions,
            'estimated_time_seconds': self.estimated_time_seconds,
            'success_probability': self.success_probability,
            'prerequisites': self.prerequisites
        }


class ErrorClassifier:
    """错误分类器"""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        初始化错误分类器
        
        Args:
            config_path: 配置文件路径
        """
        self.config = self._load_config(config_path)
        self.error_patterns = self._load_error_patterns()
        self.recovery_strategies = self._load_recovery_strategies()
        self.error_history: List[ErrorInfo] = []
        logger.info("错误分类器初始化完成")
    
    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """加载配置文件"""
        default_config = {
            'max_error_history': 1000,           # 最大错误历史记录
            'auto_recovery_enabled': True,       # 是否启用自动恢复
            'default_retry_delay_seconds': 5,    # 默认重试延迟
            'max_retry_attempts': 3,             # 最大重试尝试次数
            'content_length_threshold': 1000000, # 内容长度阈值（1M字符）
            'output_length_threshold': 8000,     # 输出长度阈值（8K字符）
            'enable_learning': True,             # 是否启用学习模式
        }
        
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                # 深度合并
                self._merge_configs(default_config, user_config)
            except Exception as e:
                logger.warning(f"加载配置文件失败，使用默认配置: {e}")
        
        return default_config
    
    def _merge_configs(self, default: Dict[str, Any], user: Dict[str, Any]):
        """深度合并配置字典"""
        for key, value in user.items():
            if key in default and isinstance(default[key], dict) and isinstance(value, dict):
                self._merge_configs(default[key], value)
            else:
                default[key] = value
    
    def _load_error_patterns(self) -> Dict[str, Tuple[ErrorType, ErrorSeverity, re.Pattern]]:
        """加载错误模式匹配规则"""
        patterns = {
            # HTTP 错误代码
            r'400': (ErrorType.BAD_REQUEST, ErrorSeverity.MEDIUM, re.compile(r'400|bad.request|invalid.request', re.IGNORECASE)),
            r'401': (ErrorType.UNAUTHORIZED, ErrorSeverity.MEDIUM, re.compile(r'401|unauthorized|auth', re.IGNORECASE)),
            r'403': (ErrorType.FORBIDDEN, ErrorSeverity.MEDIUM, re.compile(r'403|forbidden|access.denied', re.IGNORECASE)),
            r'429': (ErrorType.RATE_LIMIT, ErrorSeverity.LOW, re.compile(r'429|rate.limit|too.many.requests', re.IGNORECASE)),
            r'500': (ErrorType.SERVER_ERROR, ErrorSeverity.HIGH, re.compile(r'500|server.error|internal.error', re.IGNORECASE)),
            r'502': (ErrorType.BAD_GATEWAY, ErrorSeverity.MEDIUM, re.compile(r'502|bad.gateway', re.IGNORECASE)),
            r'503': (ErrorType.SERVICE_UNAVAILABLE, ErrorSeverity.HIGH, re.compile(r'503|service.unavailable', re.IGNORECASE)),
            r'504': (ErrorType.GATEWAY_TIMEOUT, ErrorSeverity.MEDIUM, re.compile(r'504|gateway.timeout', re.IGNORECASE)),
            
            # 内容长度错误
            r'content_too_long': (ErrorType.CONTENT_TOO_LONG, ErrorSeverity.MEDIUM, 
                                  re.compile(r'too.long|exceeds.limit|max.length|content.length', re.IGNORECASE)),
            
            # 格式错误
            r'invalid_format': (ErrorType.INVALID_FORMAT, ErrorSeverity.MEDIUM,
                                re.compile(r'invalid.format|malformed|syntax.error|parsing.error', re.IGNORECASE)),
            
            # 网络错误
            r'network_error': (ErrorType.NETWORK_ERROR, ErrorSeverity.MEDIUM,
                               re.compile(r'network.error|connection.error|connection.refused|timeout', re.IGNORECASE)),
            
            # 超时错误
            r'timeout': (ErrorType.TIMEOUT, ErrorSeverity.MEDIUM,
                         re.compile(r'timeout|timed.out|took.too.long', re.IGNORECASE)),
        }
        return patterns
    
    def _load_recovery_strategies(self) -> Dict[ErrorType, List[RecoveryStrategy]]:
        """加载恢复策略"""
        strategies = {
            ErrorType.RATE_LIMIT: [
                RecoveryStrategy(
                    name="延迟重试",
                    description="等待一段时间后重试请求",
                    actions=["计算建议等待时间", "延迟等待", "重试请求"],
                    estimated_time_seconds=30,
                    success_probability=0.8,
                    prerequisites=["有重试次数配额"]
                ),
                RecoveryStrategy(
                    name="降低请求频率",
                    description="减少请求频率以避免限流",
                    actions=["降低并发请求数", "增加请求间隔", "使用批处理"],
                    estimated_time_seconds=60,
                    success_probability=0.9
                )
            ],
            ErrorType.CONTENT_TOO_LONG: [
                RecoveryStrategy(
                    name="拆分输入",
                    description="将过长的输入拆分为多个较小部分",
                    actions=["分析输入结构", "确定拆分点", "分批处理", "合并结果"],
                    estimated_time_seconds=120,
                    success_probability=0.7
                ),
                RecoveryStrategy(
                    name="压缩输入",
                    description="压缩或简化输入内容",
                    actions=["移除冗余信息", "使用缩写", "提取关键信息"],
                    estimated_time_seconds=90,
                    success_probability=0.6
                )
            ],
            ErrorType.SERVER_ERROR: [
                RecoveryStrategy(
                    name="重试请求",
                    description="简单重试可能解决临时服务器问题",
                    actions=["等待几秒", "重试请求"],
                    estimated_time_seconds=10,
                    success_probability=0.4
                ),
                RecoveryStrategy(
                    name="切换端点",
                    description="尝试不同的API端点或服务实例",
                    actions=["检查备用端点", "切换请求目标"],
                    estimated_time_seconds=30,
                    success_probability=0.6,
                    prerequisites=["有备用端点"]
                )
            ],
            ErrorType.TIMEOUT: [
                RecoveryStrategy(
                    name="增加超时时间",
                    description="增加请求超时时间限制",
                    actions=["调整超时配置", "重新发起请求"],
                    estimated_time_seconds=20,
                    success_probability=0.7
                ),
                RecoveryStrategy(
                    name="优化请求",
                    description="简化请求内容以加快处理速度",
                    actions=["减少请求大小", "移除非必要参数"],
                    estimated_time_seconds=60,
                    success_probability=0.5
                )
            ]
        }
        
        # 为所有错误类型添加基本重试策略
        default_strategy = RecoveryStrategy(
            name="基本重试",
            description="简单重试操作",
            actions=["延迟等待", "重试操作"],
            estimated_time_seconds=10,
            success_probability=0.5
        )
        
        for error_type in ErrorType:
            if error_type not in strategies:
                strategies[error_type] = [default_strategy]
            elif default_strategy not in strategies[error_type]:
                strategies[error_type].insert(0, default_strategy)
        
        return strategies
    
    def classify(self, error_message: str, http_code: Optional[int] = None, 
                 context: Optional[Dict[str, Any]] = None) -> ErrorInfo:
        """
        分类错误
        
        Args:
            error_message: 错误消息
            http_code: HTTP状态码
            context: 上下文信息（输入大小、输出大小等）
            
        Returns:
            ErrorInfo: 错误信息
        """
        # 默认值
        error_type = ErrorType.UNKNOWN
        severity = ErrorSeverity.MEDIUM
        
        # 检查HTTP状态码
        if http_code is not None:
            if http_code == 400:
                error_type = ErrorType.BAD_REQUEST
                severity = ErrorSeverity.MEDIUM
            elif http_code == 401:
                error_type = ErrorType.UNAUTHORIZED
                severity = ErrorSeverity.MEDIUM
            elif http_code == 403:
                error_type = ErrorType.FORBIDDEN
                severity = ErrorSeverity.MEDIUM
            elif http_code == 429:
                error_type = ErrorType.RATE_LIMIT
                severity = ErrorSeverity.LOW
            elif http_code == 500:
                error_type = ErrorType.SERVER_ERROR
                severity = ErrorSeverity.HIGH
            elif http_code == 502:
                error_type = ErrorType.BAD_GATEWAY
                severity = ErrorSeverity.MEDIUM
            elif http_code == 503:
                error_type = ErrorType.SERVICE_UNAVAILABLE
                severity = ErrorSeverity.HIGH
            elif http_code == 504:
                error_type = ErrorType.GATEWAY_TIMEOUT
                severity = ErrorSeverity.MEDIUM
        
        # 基于错误消息的模式匹配
        for pattern_name, (pattern_type, pattern_severity, pattern) in self.error_patterns.items():
            if pattern.search(error_message):
                error_type = pattern_type
                severity = pattern_severity
                break
        
        # 上下文分析
        if context:
            # 检查输入/输出长度
            input_size = context.get('input_size', 0)
            output_size = context.get('output_size', 0)
            
            if input_size > self.config['content_length_threshold']:
                error_type = ErrorType.CONTENT_TOO_LONG
                severity = ErrorSeverity.MEDIUM
            elif output_size > self.config['output_length_threshold']:
                error_type = ErrorType.CONTENT_TOO_LONG
                severity = ErrorSeverity.MEDIUM
        
        error_info = ErrorInfo(
            error_type=error_type,
            severity=severity,
            http_code=http_code,
            error_message=error_message,
            error_details={'context': context} if context else {},
            timestamp=time.time()
        )
        
        # 记录错误历史
        self.error_history.append(error_info)
        if len(self.error_history) > self.config['max_error_history']:
            self.error_history = self.error_history[-self.config['max_error_history']:]
        
        logger.info(f"错误分类: {error_type.value} (严重度: {severity.value})")
        return error_info
    
    def get_recovery_strategies(self, error_info: ErrorInfo) -> List[RecoveryStrategy]:
        """
        获取恢复策略
        
        Args:
            error_info: 错误信息
            
        Returns:
            List[RecoveryStrategy]: 恢复策略列表
        """
        strategies = self.recovery_strategies.get(error_info.error_type, [])
        
        # 按成功率排序
        strategies.sort(key=lambda s: s.success_probability, reverse=True)
        
        return strategies
    
    def recommend_strategy(self, error_info: ErrorInfo, 
                          available_prerequisites: List[str] = None) -> Optional[RecoveryStrategy]:
        """
        推荐最佳恢复策略
        
        Args:
            error_info: 错误信息
            available_prerequisites: 可用的前提条件
            
        Returns:
            Optional[RecoveryStrategy]: 推荐的策略，如果没有则返回None
        """
        strategies = self.get_recovery_strategies(error_info)
        
        if not strategies:
            return None
        
        # 过滤满足前提条件的策略
        if available_prerequisites:
            filtered_strategies = []
            for strategy in strategies:
                if not strategy.prerequisites or all(p in available_prerequisites for p in strategy.prerequisites):
                    filtered_strategies.append(strategy)
            
            if filtered_strategies:
                strategies = filtered_strategies
        
        # 选择成功率最高的策略
        if strategies:
            return strategies[0]
        
        return None
    
    def record_recovery_result(self, strategy: RecoveryStrategy, success: bool, 
                              actual_time_seconds: float, notes: str = ""):
        """记录恢复结果（用于学习）"""
        if not self.config['enable_learning']:
            return
        
        # TODO: 实现学习逻辑，调整成功率估计
        logger.info(f"记录恢复结果: {strategy.name}, 成功={success}, 耗时={actual_time_seconds}s")
    
    def get_error_stats(self) -> Dict[str, Any]:
        """获取错误统计信息"""
        if not self.error_history:
            return {'total_errors': 0}
        
        total = len(self.error_history)
        by_type = {}
        by_severity = {}
        
        for error in self.error_history:
            type_key = error.error_type.value
            severity_key = error.severity.value
            
            by_type[type_key] = by_type.get(type_key, 0) + 1
            by_severity[severity_key] = by_severity.get(severity_key, 0) + 1
        
        # 最近错误
        recent_errors = []
        for error in self.error_history[-10:]:
            recent_errors.append({
                'type': error.error_type.value,
                'severity': error.severity.value,
                'message': error.error_message[:100],
                'timestamp': error.timestamp
            })
        
        return {
            'total_errors': total,
            'by_type': by_type,
            'by_severity': by_severity,
            'recent_errors': recent_errors
        }


def test_error_classifier():
    """测试错误分类器"""
    print("🧪 测试错误分类器...")
    
    classifier = ErrorClassifier()
    
    # 测试案例
    test_cases = [
        ("Rate limit exceeded", 429),
        ("Internal server error", 500),
        ("Request timeout", None),
        ("Content too long: exceeds limit", None),
        ("Invalid JSON format", 400),
        ("Connection refused", None),
    ]
    
    for error_msg, http_code in test_cases:
        print(f"\n测试错误: {error_msg} (HTTP: {http_code})")
        error_info = classifier.classify(error_msg, http_code)
        print(f"  分类结果: {error_info.error_type.value} (严重度: {error_info.severity.value})")
        
        strategies = classifier.get_recovery_strategies(error_info)
        if strategies:
            best = classifier.recommend_strategy(error_info)
            print(f"  推荐策略: {best.name if best else '无'} (成功率: {best.success_probability if best else 0})")
        else:
            print("  无恢复策略")
    
    # 测试统计
    stats = classifier.get_error_stats()
    print(f"\n📊 错误统计: {stats['total_errors']} 个错误记录")
    
    print("\n✅ 错误分类器测试完成")
    return True


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_error_classifier()
    else:
        print("用法:")
        print("  python error_classifier.py test")
        print("\n注意: 完整使用需要与步骤执行器集成")