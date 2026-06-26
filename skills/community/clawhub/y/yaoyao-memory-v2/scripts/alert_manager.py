#!/usr/bin/env python3
"""
alert_manager.py - 监控告警系统

功能：
- 多级别告警：CRITICAL / WARNING / INFO
- 多种渠道：负一屏 / MeoW / 邮件 / Webhook
- 告警抑制（避免重复告警）
- 自动恢复通知

配置：
- ALERT_THRESHOLDS: 告警阈值
- ALERT_CHANNELS: 告警渠道
- ALERT_COOLDOWN: 抑制时间（秒）
"""

import json
import logging
import os
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

# ============================================================================
# 常量
# ============================================================================

ALERT_STATE_FILE = Path.home() / ".openclaw" / "workspace" / "memory" / ".alert_state.json"

# 告警级别
class AlertLevel(Enum):
    CRITICAL = "critical"  # 紧急，需立即处理
    WARNING = "warning"     # 警告，需关注
    INFO = "info"          # 信息，记录

# 告警渠道
ALERT_CHANNELS = {
    "feishu": True,      # 飞书（通过 today-task）
    "meow": True,        # MeoW App
    "webhook": False,     # Webhook
    "email": False,      # 邮件（待实现）
}

# 默认阈值
DEFAULT_THRESHOLDS = {
    "health_score": 90,       # 健康度低于此值告警
    "error_count": 10,         # 错误日志超过此值告警
    "memory_usage_mb": 500,     # 内存使用超过此值告警
    "disk_usage_percent": 90,   # 磁盘使用率超过此值告警
    "response_time_ms": 1000,   # 响应时间超过此值告警
    "cache_hit_rate": 0.6,     # 缓存命中率低于此值告警
}

# 抑制时间（秒）
DEFAULT_COOLDOWN = 3600  # 1小时

# ============================================================================
# 数据结构
# ============================================================================

@dataclass
class Alert:
    """告警对象"""
    level: AlertLevel
    title: str
    message: str
    source: str = "yaoyao-memory"
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    data: Dict[str, Any] = field(default_factory=dict)
    resolved: bool = False
    resolved_at: Optional[str] = None


@dataclass
class AlertConfig:
    """告警配置"""
    enabled: bool = True
    thresholds: Dict[str, Any] = field(default_factory=lambda: DEFAULT_THRESHOLDS)
    channels: Dict[str, bool] = field(default_factory=lambda: ALERT_CHANNELS.copy())
    cooldown: int = DEFAULT_COOLDOWN
    auto_resolve: bool = True
    auto_resolve_after: int = 300  # 5分钟后自动恢复


# ============================================================================
# 告警状态管理
# ============================================================================

class AlertState:
    """告警状态管理器"""
    
    def __init__(self, state_file: Path = ALERT_STATE_FILE):
        self.state_file = state_file
        self.alerts: List[Alert] = []
        self.last_alert_time: Dict[str, float] = {}  # key -> timestamp
        self.load()
    
    def load(self):
        """加载状态"""
        if self.state_file.exists():
            try:
                with open(self.state_file) as f:
                    data = json.load(f)
                    self.alerts = [Alert(**a) for a in data.get("alerts", [])]
                    self.last_alert_time = data.get("last_alert_time", {})
            except Exception as e:
                logger.warning(f"Failed to load alert state: {e}")
    
    def save(self):
        """保存状态"""
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.state_file, "w") as f:
            json.dump({
                "alerts": [
                    {
                        **vars(a),
                        "level": a.level.value,
                    } for a in self.alerts
                ],
                "last_alert_time": self.last_alert_time,
            }, f, indent=2, ensure_ascii=False)
    
    def add_alert(self, alert: Alert) -> bool:
        """
        添加告警（如果不在冷却期）
        
        Returns:
            True if alert was added, False if suppressed
        """
        alert_key = f"{alert.level.value}:{alert.source}:{alert.title}"
        
        # 检查冷却期
        if alert_key in self.last_alert_time:
            elapsed = time.time() - self.last_alert_time[alert_key]
            if elapsed < DEFAULT_COOLDOWN:
                logger.debug(f"Alert suppressed (cooldown): {alert_key}")
                return False
        
        self.alerts.append(alert)
        self.last_alert_time[alert_key] = time.time()
        self.save()
        return True
    
    def resolve_alert(self, alert_key: str) -> bool:
        """标记告警为已解决"""
        for alert in self.alerts:
            key = f"{alert.level.value}:{alert.source}:{alert.title}"
            if key == alert_key:
                alert.resolved = True
                alert.resolved_at = datetime.now().isoformat()
                self.save()
                return True
        return False
    
    def get_active_alerts(self) -> List[Alert]:
        """获取活跃告警"""
        return [a for a in self.alerts if not a.resolved]
    
    def clear_resolved(self, before_hours: int = 24):
        """清理已解决的旧告警"""
        cutoff = datetime.now() - timedelta(hours=before_hours)
        self.alerts = [
            a for a in self.alerts
            if not a.resolved or (
                a.resolved_at and 
                datetime.fromisoformat(a.resolved_at) > cutoff
            )
        ]
        self.save()


# ============================================================================
# 告警渠道
# ============================================================================

class AlertChannel:
    """告警渠道基类"""
    
    def send(self, alert: Alert) -> bool:
        raise NotImplementedError


class FeishuChannel(AlertChannel):
    """飞书/负一屏渠道"""
    
    def send(self, alert: Alert) -> bool:
        try:
            sys.path.insert(0, str(Path.home() / ".openclaw" / "workspace" / "skills" / "today-task" / "scripts"))
            from quick_push import push
            
            emoji = {
                AlertLevel.CRITICAL: "🔴",
                AlertLevel.WARNING: "🟡",
                AlertLevel.INFO: "🔵",
            }.get(alert.level, "ℹ️")
            
            title = f"{emoji} {alert.title}"
            result = push(title, alert.message, alert.level.value)
            
            if result and result.get("success"):
                logger.info(f"Feishu alert sent: {alert.title}")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to send Feishu alert: {e}")
            return False


class MeoWChannel(AlertChannel):
    """MeoW App渠道"""
    
    def send(self, alert: Alert) -> bool:
        try:
            sys.path.insert(0, str(Path.home() / ".openclaw" / "workspace" / "skills" / "today-task" / "scripts"))
            from meow_pusher import push
            
            emoji = {
                AlertLevel.CRITICAL: "🚨",
                AlertLevel.WARNING: "⚠️",
                AlertLevel.INFO: "ℹ️",
            }.get(alert.level, "ℹ️")
            
            result = push(
                f"{emoji} {alert.title}",
                alert.message,
                alert.level.value
            )
            
            if result and result.get("success"):
                logger.info(f"MeoW alert sent: {alert.title}")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to send MeoW alert: {e}")
            return False


class WebhookChannel(AlertChannel):
    """Webhook渠道"""
    
    def __init__(self, url: str = None):
        self.url = url or os.environ.get("ALERT_WEBHOOK_URL")
    
    def send(self, alert: Alert) -> bool:
        if not self.url:
            return False
        
        try:
            import urllib.request
            
            payload = {
                "alert": {
                    "level": alert.level.value,
                    "title": alert.title,
                    "message": alert.message,
                    "source": alert.source,
                    "timestamp": alert.timestamp,
                }
            }
            
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                self.url,
                data=data,
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            
            with urllib.request.urlopen(req, timeout=10) as resp:
                return resp.status == 200
        except Exception as e:
            logger.error(f"Failed to send webhook alert: {e}")
            return False


# ============================================================================
# 告警管理器
# ============================================================================

class AlertManager:
    """告警管理器"""
    
    def __init__(self, config: Optional[AlertConfig] = None):
        self.config = config or AlertConfig()
        self.state = AlertState()
        self.channels: Dict[str, AlertChannel] = {
            "feishu": FeishuChannel(),
            "meow": MeoWChannel(),
            "webhook": WebhookChannel(),
        }
    
    def check_and_alert(
        self,
        level: AlertLevel,
        title: str,
        message: str,
        source: str = "yaoyao-memory",
        data: Dict[str, Any] = None,
        force: bool = False
    ) -> bool:
        """
        检查条件并发送告警
        
        Args:
            level: 告警级别
            title: 告警标题
            message: 告警消息
            source: 告警来源
            data: 附加数据
            force: 强制发送（忽略冷却期）
        
        Returns:
            True if alert was sent
        """
        if not self.config.enabled:
            return False
        
        alert = Alert(
            level=level,
            title=title,
            message=message,
            source=source,
            data=data or {},
        )
        
        # 检查是否在冷却期
        if not force:
            if not self.state.add_alert(alert):
                return False
        
        # 发送到所有启用的渠道
        sent = False
        for channel_name, channel in self.channels.items():
            if self.config.channels.get(channel_name, False):
                if channel.send(alert):
                    sent = True
        
        return sent
    
    def alert_critical(self, title: str, message: str, **kwargs) -> bool:
        """发送紧急告警"""
        return self.check_and_alert(AlertLevel.CRITICAL, title, message, **kwargs)
    
    def alert_warning(self, title: str, message: str, **kwargs) -> bool:
        """发送警告告警"""
        return self.check_and_alert(AlertLevel.WARNING, title, message, **kwargs)
    
    def alert_info(self, title: str, message: str, **kwargs) -> bool:
        """发送信息告警"""
        return self.check_and_alert(AlertLevel.INFO, title, message, **kwargs)
    
    def check_health_score(self, score: float) -> bool:
        """检查健康度"""
        threshold = self.config.thresholds.get("health_score", 90)
        if score < threshold:
            self.alert_critical(
                "健康度异常",
                f"系统健康度仅 {score}分，低于阈值 {threshold}分",
                source="health_check"
            )
            return False
        return True
    
    def check_error_count(self, count: int) -> bool:
        """检查错误数量"""
        threshold = self.config.thresholds.get("error_count", 10)
        if count > threshold:
            self.alert_warning(
                "错误日志过多",
                f"错误日志 {count}条，超过阈值 {threshold}条",
                source="health_check"
            )
            return False
        return True
    
    def check_cache_hit_rate(self, rate: float) -> bool:
        """检查缓存命中率"""
        threshold = self.config.thresholds.get("cache_hit_rate", 0.6)
        if rate < threshold:
            self.alert_warning(
                "缓存命中率低",
                f"缓存命中率 {rate:.1%}，低于阈值 {threshold:.1%}",
                source="health_check"
            )
            return False
        return True
    
    def check_disk_usage(self, percent: float) -> bool:
        """检查磁盘使用率"""
        threshold = self.config.thresholds.get("disk_usage_percent", 90)
        if percent > threshold:
            self.alert_critical(
                "磁盘空间不足",
                f"磁盘使用率 {percent:.1f}%，超过阈值 {threshold}%",
                source="system_check"
            )
            return False
        return True
    
    def resolve_and_notify(self, title: str):
        """解决告警并发送恢复通知"""
        alert_key = f"warning:yaoyao-memory:{title}"
        if self.state.resolve_alert(alert_key):
            self.alert_info(
                f"✅ {title} 已恢复",
                "告警已自动解决",
                source="alert_manager"
            )
    
    def get_status(self) -> Dict[str, Any]:
        """获取告警状态"""
        active = self.state.get_active_alerts()
        return {
            "enabled": self.config.enabled,
            "active_count": len(active),
            "active_alerts": [
                {"level": a.level.value, "title": a.title, "message": a.message}
                for a in active
            ],
            "channels": list(self.config.channels.keys()),
        }


# ============================================================================
# 主函数
# ============================================================================

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="告警管理器")
    parser.add_argument("--test", "-t", action="store_true", help="发送测试告警")
    parser.add_argument("--status", "-s", action="store_true", help="查看告警状态")
    parser.add_argument("--resolve", "-r", help="解决告警")
    parser.add_argument("--clear", action="store_true", help="清理旧告警")
    parser.add_argument("--config", help="配置文件路径")
    
    args = parser.parse_args()
    
    # 加载配置
    config = AlertConfig()
    if args.config:
        with open(args.config) as f:
            data = json.load(f)
            config = AlertConfig(**data)
    
    manager = AlertManager(config)
    
    if args.test:
        print("发送测试告警...")
        manager.alert_critical("测试告警", "这是一条CRITICAL测试告警")
        manager.alert_warning("测试告警", "这是一条WARNING测试告警")
        manager.alert_info("测试告警", "这是一条INFO测试告警")
        print("测试告警已发送")
    
    elif args.status:
        status = manager.get_status()
        print(json.dumps(status, indent=2, ensure_ascii=False))
    
    elif args.resolve:
        manager.state.resolve_alert(args.resolve)
        print(f"告警已解决: {args.resolve}")
    
    elif args.clear:
        manager.state.clear_resolved()
        print("已清理旧告警")
    
    else:
        # 默认：显示状态
        status = manager.get_status()
        print(json.dumps(status, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
