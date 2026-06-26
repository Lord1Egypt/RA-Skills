"""
平台集成抽象基类
支持多通信平台：飞书、微信、QQ、钉钉、Slack等
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass
from enum import Enum
import os


class PlatformType(Enum):
    """支持的通信平台类型"""
    FEISHU = "feishu"
    WECHAT = "wechat"
    QQ = "qq"
    DINGTALK = "dingtalk"
    SLACK = "slack"
    TELEGRAM = "telegram"
    DISCORD = "discord"
    EMAIL = "email"
    WEBHOOK = "webhook"


@dataclass
class UploadResult:
    """文件上传结果"""
    success: bool
    file_url: Optional[str] = None
    file_id: Optional[str] = None
    file_token: Optional[str] = None
    error_message: Optional[str] = None
    platform_specific_data: Optional[Dict[str, Any]] = None


@dataclass
class MessageResult:
    """消息发送结果"""
    success: bool
    message_id: Optional[str] = None
    error_message: Optional[str] = None
    platform_specific_data: Optional[Dict[str, Any]] = None


@dataclass
class PlatformConfig:
    """平台配置"""
    platform_type: PlatformType
    api_key: Optional[str] = None
    api_secret: Optional[str] = None
    access_token: Optional[str] = None
    webhook_url: Optional[str] = None
    bot_token: Optional[str] = None
    channel_id: Optional[str] = None
    user_id: Optional[str] = None
    group_id: Optional[str] = None
    timeout: int = 30
    max_retries: int = 3
    retry_delay: float = 2.0


class BasePlatform(ABC):
    """平台集成抽象基类"""
    
    def __init__(self, config: PlatformConfig):
        """
        初始化平台
        
        Args:
            config: 平台配置
        """
        self.config = config
        self.platform_type = config.platform_type
        
    @abstractmethod
    def upload_file(self, file_path: str, file_name: Optional[str] = None,
                   folder_id: Optional[str] = None) -> UploadResult:
        """
        上传文件到平台
        
        Args:
            file_path: 本地文件路径
            file_name: 上传后的文件名
            folder_id: 目标文件夹ID
            
        Returns:
            上传结果
        """
        pass
    
    @abstractmethod
    def send_message(self, message: str, attachments: Optional[List[str]] = None,
                    target: Optional[str] = None) -> MessageResult:
        """
        发送消息到平台
        
        Args:
            message: 消息内容
            attachments: 附件文件路径列表
            target: 目标（用户/群组/频道）
            
        Returns:
            消息发送结果
        """
        pass
    
    @abstractmethod
    def get_file_url(self, file_id: str) -> str:
        """
        根据文件ID获取访问URL
        
        Args:
            file_id: 文件ID
            
        Returns:
            文件访问URL
        """
        pass
    
    def upload_and_share(self, file_path: str, file_name: Optional[str] = None,
                        folder_id: Optional[str] = None) -> Dict[str, Any]:
        """
        上传文件并生成分享信息
        
        Args:
            file_path: 本地文件路径
            file_name: 上传后的文件名
            folder_id: 目标文件夹ID
            
        Returns:
            包含上传和分享信息的字典
        """
        # 上传文件
        upload_result = self.upload_file(file_path, file_name, folder_id)
        
        if not upload_result.success:
            return {
                "success": False,
                "error": upload_result.error_message,
                "step": "upload"
            }
        
        # 生成分享信息
        share_info = self._generate_share_info(upload_result)
        
        return {
            "success": True,
            "upload_result": upload_result,
            "share_info": share_info,
            "file_url": upload_result.file_url,
            "file_id": upload_result.file_id
        }
    
    def _generate_share_info(self, upload_result: UploadResult) -> Dict[str, Any]:
        """
        生成分享信息
        
        Args:
            upload_result: 上传结果
            
        Returns:
            分享信息字典
        """
        return {
            "file_url": upload_result.file_url,
            "file_id": upload_result.file_id,
            "platform": self.platform_type.value,
            "share_message": self._create_share_message(upload_result)
        }
    
    def _create_share_message(self, upload_result: UploadResult) -> str:
        """
        创建分享消息
        
        Args:
            upload_result: 上传结果
            
        Returns:
            分享消息文本
        """
        if upload_result.file_url:
            return f"文件已上传到{self.platform_type.value}，访问链接：{upload_result.file_url}"
        else:
            return f"文件已上传到{self.platform_type.value}，文件ID：{upload_result.file_id}"
    
    def validate_config(self) -> bool:
        """
        验证平台配置是否有效
        
        Returns:
            配置是否有效
        """
        required_fields = self._get_required_config_fields()
        
        for field in required_fields:
            if not getattr(self.config, field, None):
                return False
        
        return True
    
    @abstractmethod
    def _get_required_config_fields(self) -> List[str]:
        """
        获取必需的配置字段
        
        Returns:
            必需字段列表
        """
        pass
    
    def test_connection(self) -> bool:
        """
        测试平台连接
        
        Returns:
            连接是否成功
        """
        try:
            return self._perform_connection_test()
        except Exception as e:
            print(f"平台连接测试失败: {e}")
            return False
    
    @abstractmethod
    def _perform_connection_test(self) -> bool:
        """
        执行具体的连接测试
        
        Returns:
            连接是否成功
        """
        pass


class PlatformFactory:
    """平台集成工厂，支持多种通信平台"""
    
    @staticmethod
    def create_platform(platform_type: PlatformType, config: PlatformConfig):
        """
        创建平台集成实例
        
        Args:
            platform_type: 平台类型
            config: 平台配置
            
        Returns:
            BasePlatform实例
            
        Raises:
            ValueError: 如果平台类型不支持
        """
        if platform_type == PlatformType.FEISHU:
            from .feishu.feishu_platform import FeishuPlatform
            return FeishuPlatform(config)
        
        elif platform_type == PlatformType.WECHAT:
            from .wechat.wechat_platform import WechatPlatform
            return WechatPlatform(config)
        
        elif platform_type == PlatformType.QQ:
            from .qq.qq_platform import QQPlatform
            return QQPlatform(config)
        
        elif platform_type == PlatformType.DINGTALK:
            from .dingtalk.dingtalk_platform import DingtalkPlatform
            return DingtalkPlatform(config)
        
        elif platform_type == PlatformType.SLACK:
            from .slack.slack_platform import SlackPlatform
            return SlackPlatform(config)
        
        elif platform_type == PlatformType.TELEGRAM:
            from .telegram.telegram_platform import TelegramPlatform
            return TelegramPlatform(config)
        
        elif platform_type == PlatformType.DISCORD:
            from .discord.discord_platform import DiscordPlatform
            return DiscordPlatform(config)
        
        elif platform_type == PlatformType.EMAIL:
            from .email.email_platform import EmailPlatform
            return EmailPlatform(config)
        
        elif platform_type == PlatformType.WEBHOOK:
            from .webhook.webhook_platform import WebhookPlatform
            return WebhookPlatform(config)
        
        else:
            raise ValueError(f"不支持的平台类型: {platform_type}")