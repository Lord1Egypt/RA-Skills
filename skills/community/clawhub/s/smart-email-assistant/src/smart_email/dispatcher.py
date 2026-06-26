"""
消息分发模块 - 将 outbox 中的消息发送到用户指定渠道
"""
import os
import json
import subprocess
import shutil
from pathlib import Path
from typing import List, Dict
from datetime import datetime

from . import config
from .logger import get_logger

logger = get_logger(__name__)


class MessageDispatcher:
    """消息分发器 - 负责将 outbox 消息发送到用户渠道"""
    
    def __init__(self, test_mode: bool = False):
        self.test_mode = test_mode
        self.outbox_path = config.get_outbox_path(test_mode)
        self.pending_dir = self.outbox_path / "pending"
        self.sent_dir = self.outbox_path / "sent"
        self.delivery_config = config.get_delivery_config()
        
        # 确保目录存在
        self.pending_dir.mkdir(parents=True, exist_ok=True)
        self.sent_dir.mkdir(parents=True, exist_ok=True)
    
    def dispatch_all(self) -> Dict:
        """
        分发所有待发送消息
        
        Returns:
            {
                "total": 总消息数,
                "success": 成功数,
                "failed": 失败数,
                "skipped": 跳过数（测试模式）
            }
        """
        results = {
            "total": 0,
            "success": 0,
            "failed": 0,
            "skipped": 0
        }
        
        # 检查发送配置
        if not self.delivery_config["enabled"]:
            logger.warning("发送渠道未配置，跳过分发")
            logger.info("请配置 SMART_EMAIL_DELIVERY_CHANNEL 和 SMART_EMAIL_DELIVERY_TARGET")
            return results
        
        # 获取所有待发送消息
        pending_messages = self._get_pending_messages()
        results["total"] = len(pending_messages)
        
        if not pending_messages:
            logger.info("没有待发送的消息")
            return results
        
        logger.info(f"发现 {len(pending_messages)} 条待发送消息")
        
        for msg_file in pending_messages:
            try:
                result = self._dispatch_single(msg_file)
                if result == "success":
                    results["success"] += 1
                elif result == "skipped":
                    results["skipped"] += 1
                else:
                    results["failed"] += 1
            except Exception as e:
                logger.error(f"分发消息失败 {msg_file.name}: {e}")
                results["failed"] += 1
        
        return results
    
    def _get_pending_messages(self) -> List[Path]:
        """获取所有待发送消息文件"""
        if not self.pending_dir.exists():
            return []
        
        # 按创建时间排序（先创建的先发送）
        files = sorted(
            [f for f in self.pending_dir.iterdir() if f.suffix == '.json'],
            key=lambda f: f.stat().st_mtime
        )
        return files
    
    def _dispatch_single(self, msg_file: Path) -> str:
        """
        分发单条消息
        
        Returns:
            "success" - 发送成功
            "failed" - 发送失败
            "skipped" - 测试模式跳过
        """
        # 读取消息
        with open(msg_file, 'r', encoding='utf-8') as f:
            message = json.load(f)
        
        msg_id = message.get("id", msg_file.stem)
        msg_type = message.get("type", "unknown")
        content = message.get("content", {})
        
        # 构建发送内容
        title = content.get("title", "无标题")
        body = content.get("body", "")
        
        # 测试模式：仅记录，不发送
        if self.test_mode:
            logger.info(f"[测试模式] 跳过发送: {title}")
            logger.info(f"  内容预览: {body[:100]}...")
            
            # 测试模式下也移动到 sent（模拟成功）
            self._move_to_sent(msg_file, message)
            return "skipped"
        
        # 正式模式：发送到用户渠道
        channel = self.delivery_config["channel"]
        target = self.delivery_config["target"]
        
        logger.info(f"正在发送消息: {title}")
        logger.info(f"  渠道: {channel}")
        logger.info(f"  目标: {target}")
        
        # 使用 OpenClaw message 工具发送
        success = self._send_via_openclaw(channel, target, title, body, self.test_mode)
        
        if success:
            logger.info(f"发送成功: {msg_id}")
            # 移动到已发送目录
            self._move_to_sent(msg_file, message)
            return "success"
        else:
            logger.error(f"发送失败: {msg_id}")
            return "failed"
    
    def _send_via_openclaw(self, channel: str, target: str, title: str, body: str, test_mode: bool = False) -> bool:
        """
        使用 OpenClaw message 工具发送消息
        
        Args:
            channel: 渠道类型 (telegram, dingtalk, wecom, etc.)
            target: 目标用户/群组 ID
            title: 消息标题
            body: 消息内容
            test_mode: 是否测试模式
        
        Returns:
            bool: 是否发送成功
        """
        try:
            # 查找 openclaw 命令
            openclaw_cmd = shutil.which("openclaw")
            if not openclaw_cmd:
                logger.error("未找到 openclaw 命令")
                return False
            
            # 直接使用 outbox 生成的完整内容，不额外包装
            full_content = f"{title}\n\n{body}"
            
            # 构建命令
            cmd = [
                openclaw_cmd, "message", "send",
                "--channel", channel,
                "--target", target,
                "--message", full_content
            ]
            
            logger.debug(f"执行命令: {' '.join(cmd)}")
            
            # 执行发送
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return True
            else:
                logger.error(f"发送失败: {result.stderr or result.stdout}")
                return False
                
        except subprocess.TimeoutExpired:
            logger.error("发送超时")
            return False
        except Exception as e:
            logger.error(f"发送异常: {e}")
            return False
    
    def _move_to_sent(self, msg_file: Path, message: Dict):
        """将消息移动到已发送目录（使用原子操作）"""
        # 创建日期子目录
        today = datetime.now().strftime("%Y-%m-%d")
        sent_today_dir = self.sent_dir / today
        sent_today_dir.mkdir(parents=True, exist_ok=True)
        
        # 使用原子操作移动文件（os.rename 在 POSIX 上是原子的）
        dest_file = sent_today_dir / msg_file.name
        try:
            # 优先使用 os.rename（原子操作）
            os.rename(msg_file, dest_file)
        except OSError:
            # 跨文件系统时回退到 shutil.move
            shutil.move(str(msg_file), str(dest_file))
        
        logger.debug(f"消息已归档: {dest_file}")
    
    def get_pending_count(self) -> int:
        """获取待发送消息数量"""
        return len(self._get_pending_messages())
    
    def get_stats(self) -> Dict:
        """获取分发统计信息"""
        pending = self._get_pending_messages()
        
        # 统计已发送（按日期）
        sent_stats = {}
        if self.sent_dir.exists():
            for date_dir in self.sent_dir.iterdir():
                if date_dir.is_dir():
                    count = len(list(date_dir.glob("*.json")))
                    sent_stats[date_dir.name] = count
        
        return {
            "pending_count": len(pending),
            "pending_files": [f.name for f in pending],
            "sent_by_date": sent_stats,
            "delivery_config": {
                "channel": self.delivery_config["channel"] if self.delivery_config["enabled"] else None,
                "target": self.delivery_config["target"] if self.delivery_config["enabled"] else None,
                "enabled": self.delivery_config["enabled"]
            }
        }
