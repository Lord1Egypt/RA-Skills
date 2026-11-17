#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
voice_channel.py — 多渠道语音消息抽象层

功能：
1. 抽象 VoiceChannel 接口，统一企业微信/钉钉/飞书消息格式
2. 工厂模式创建渠道实例
3. 消息标准化输出（统一格式，屏蔽渠道差异）
4. 零外部依赖：纯 Python 标准库

依赖：纯 Python 标准库（零外部依赖）
联系信息：njskills@agent.qq.com

版本：v1.0 (2026-08-17)
"""

import re
import json
import logging
import hashlib
import time
from abc import ABC, abstractmethod
from typing import Optional, Dict, List, Any
from enum import Enum

logger = logging.getLogger(__name__)


# ==========================================
# 渠道类型枚举
# ==========================================

class ChannelType(Enum):
    """支持的渠道类型"""
    WECHAT = "wechat"       # 企业微信
    DINGTALK = "dingtalk"   # 钉钉
    FEISHU = "feishu"       # 飞书
    UNKNOWN = "unknown"


# ==========================================
# 标准化消息格式
# ==========================================

class StandardMessage:
    """标准化消息格式（屏蔽渠道差异）"""
    
    def __init__(self, channel: ChannelType, msgid: str, userid: str,
                 msgtype: str, content: str, audio_url: str = "",
                 audio_duration: float = 0.0, raw_data: Dict = None):
        self.channel = channel
        self.msgid = msgid
        self.userid = userid
        self.msgtype = msgtype  # voice/text/image/file/video
        self.content = content  # 文本内容或 ASR 转写
        self.audio_url = audio_url  # 音频文件下载 URL
        self.audio_duration = audio_duration  # 音频时长（秒）
        self.raw_data = raw_data or {}  # 原始渠道数据
        self.timestamp = time.time()
    
    def is_voice(self) -> bool:
        return self.msgtype == "voice"
    
    def is_text(self) -> bool:
        return self.msgtype == "text"
    
    def __str__(self):
        return (f"StandardMessage(channel={self.channel.value}, "
                f"msgid={self.msgid[:12]}, userid={self.userid}, "
                f"type={self.msgtype}, content={self.content[:50]})")


# ==========================================
# 抽象渠道接口
# ==========================================

class VoiceChannel(ABC):
    """语音消息渠道抽象接口"""
    
    @abstractmethod
    def parse_callback(self, callback_data: Dict) -> Optional[StandardMessage]:
        """解析渠道回调数据为标准化消息"""
        pass
    
    @abstractmethod
    def send_text(self, userid: str, content: str) -> bool:
        """发送文本消息"""
        pass
    
    @abstractmethod
    def send_voice(self, userid: str, audio_data: bytes) -> bool:
        """发送语音消息"""
        pass
    
    @abstractmethod
    def download_audio(self, audio_url: str) -> Optional[bytes]:
        """下载音频文件"""
        pass
    
    @abstractmethod
    def get_channel_type(self) -> ChannelType:
        """获取渠道类型"""
        pass


# ==========================================
# 企业微信渠道
# ==========================================

class WeChatChannel(VoiceChannel):
    """企业微信渠道实现"""
    
    def __init__(self, api_base: str = "https://qyapi.weixin.qq.com/cgi-bin"):
        self.api_base = api_base
    
    def parse_callback(self, callback_data: Dict) -> Optional[StandardMessage]:
        """解析企业微信回调"""
        try:
            msgid = callback_data.get("msgid", "")
            msgtype = callback_data.get("msgtype", "")
            userid = callback_data.get("from", {}).get("userid", "")
            
            content = ""
            audio_url = ""
            audio_duration = 0.0
            
            if msgtype == "voice":
                voice_data = callback_data.get("voice", {})
                content = voice_data.get("content", "")  # ASR 转写
                audio_url = voice_data.get("media_id", "")
                audio_duration = voice_data.get("duration", 0.0)
            elif msgtype == "text":
                content = callback_data.get("text", {}).get("content", "")
            
            return StandardMessage(
                channel=ChannelType.WECHAT,
                msgid=msgid,
                userid=userid,
                msgtype=msgtype,
                content=content,
                audio_url=audio_url,
                audio_duration=audio_duration,
                raw_data=callback_data,
            )
        except Exception as e:
            logger.error(f"企业微信回调解析失败: {e}")
            return None
    
    def send_text(self, userid: str, content: str) -> bool:
        """发送企业微信文本消息"""
        # 预留接口，实际需调用企微 API
        logger.info(f"企业微信发送文本: userid={userid}, content={content[:30]}")
        return True
    
    def send_voice(self, userid: str, audio_data: bytes) -> bool:
        """发送企业微信语音消息"""
        logger.info(f"企业微信发送语音: userid={userid}, size={len(audio_data)} bytes")
        return True
    
    def download_audio(self, audio_url: str) -> Optional[bytes]:
        """下载企业微信音频文件"""
        logger.info(f"企业微信下载音频: {audio_url[:50]}")
        # 实际需调用企微 media/get API
        return b""
    
    def get_channel_type(self) -> ChannelType:
        return ChannelType.WECHAT


# ==========================================
# 钉钉渠道
# ==========================================

class DingTalkChannel(VoiceChannel):
    """钉钉渠道实现"""
    
    def __init__(self, api_base: str = "https://api.dingtalk.com/v1.0"):
        self.api_base = api_base
    
    def parse_callback(self, callback_data: Dict) -> Optional[StandardMessage]:
        """解析钉钉回调"""
        try:
            msgid = callback_data.get("msgId", "")
            msgtype = callback_data.get("msgtype", "")
            userid = callback_data.get("senderStaffId", "")
            
            content = ""
            audio_url = ""
            audio_duration = 0.0
            
            if msgtype == "voice":
                voice_data = callback_data.get("voiceContent", {})
                content = voice_data.get("content", "")
                audio_url = voice_data.get("mediaId", "")
                audio_duration = voice_data.get("duration", 0.0)
            elif msgtype == "text":
                content = callback_data.get("text", {}).get("content", "")
            
            return StandardMessage(
                channel=ChannelType.DINGTALK,
                msgid=msgid,
                userid=userid,
                msgtype=msgtype,
                content=content,
                audio_url=audio_url,
                audio_duration=audio_duration,
                raw_data=callback_data,
            )
        except Exception as e:
            logger.error(f"钉钉回调解析失败: {e}")
            return None
    
    def send_text(self, userid: str, content: str) -> bool:
        """发送钉钉文本消息"""
        logger.info(f"钉钉发送文本: userid={userid}, content={content[:30]}")
        return True
    
    def send_voice(self, userid: str, audio_data: bytes) -> bool:
        """发送钉钉语音消息"""
        logger.info(f"钉钉发送语音: userid={userid}, size={len(audio_data)} bytes")
        return True
    
    def download_audio(self, audio_url: str) -> Optional[bytes]:
        """下载钉钉音频文件"""
        logger.info(f"钉钉下载音频: {audio_url[:50]}")
        return b""
    
    def get_channel_type(self) -> ChannelType:
        return ChannelType.DINGTALK


# ==========================================
# 飞书渠道
# ==========================================

class FeishuChannel(VoiceChannel):
    """飞书渠道实现"""
    
    def __init__(self, api_base: str = "https://open.feishu.cn/open-apis/im/v1"):
        self.api_base = api_base
    
    def parse_callback(self, callback_data: Dict) -> Optional[StandardMessage]:
        """解析飞书回调"""
        try:
            msgid = callback_data.get("message_id", "")
            msgtype = callback_data.get("message_type", "")
            userid = callback_data.get("sender", {}).get("sender_id", {}).get("open_id", "")
            
            content = ""
            audio_url = ""
            audio_duration = 0.0
            
            if msgtype == "voice":
                voice_data = callback_data.get("voice", {})
                content = voice_data.get("text", "")
                audio_url = voice_data.get("file_key", "")
                audio_duration = voice_data.get("duration", 0.0)
            elif msgtype == "text":
                content = callback_data.get("text", {}).get("text", "")
            
            return StandardMessage(
                channel=ChannelType.FEISHU,
                msgid=msgid,
                userid=userid,
                msgtype=msgtype,
                content=content,
                audio_url=audio_url,
                audio_duration=audio_duration,
                raw_data=callback_data,
            )
        except Exception as e:
            logger.error(f"飞书回调解析失败: {e}")
            return None
    
    def send_text(self, userid: str, content: str) -> bool:
        """发送飞书文本消息"""
        logger.info(f"飞书发送文本: userid={userid}, content={content[:30]}")
        return True
    
    def send_voice(self, userid: str, audio_data: bytes) -> bool:
        """发送飞书语音消息"""
        logger.info(f"飞书发送语音: userid={userid}, size={len(audio_data)} bytes")
        return True
    
    def download_audio(self, audio_url: str) -> Optional[bytes]:
        """下载飞书音频文件"""
        logger.info(f"飞书下载音频: {audio_url[:50]}")
        return b""
    
    def get_channel_type(self) -> ChannelType:
        return ChannelType.FEISHU


# ==========================================
# 渠道工厂
# ==========================================

class VoiceChannelFactory:
    """渠道工厂"""
    
    _channels: Dict[ChannelType, VoiceChannel] = {}
    
    @classmethod
    def create(cls, channel_type: ChannelType) -> VoiceChannel:
        """创建渠道实例"""
        if channel_type not in cls._channels:
            if channel_type == ChannelType.WECHAT:
                cls._channels[channel_type] = WeChatChannel()
            elif channel_type == ChannelType.DINGTALK:
                cls._channels[channel_type] = DingTalkChannel()
            elif channel_type == ChannelType.FEISHU:
                cls._channels[channel_type] = FeishuChannel()
            else:
                raise ValueError(f"不支持的渠道类型: {channel_type}")
        return cls._channels[channel_type]
    
    @classmethod
    def create_from_string(cls, channel_str: str) -> VoiceChannel:
        """从字符串创建渠道实例"""
        channel_map = {
            "wechat": ChannelType.WECHAT,
            "weixin": ChannelType.WECHAT,
            "dingtalk": ChannelType.DINGTALK,
            "dingding": ChannelType.DINGTALK,
            "feishu": ChannelType.FEISHU,
            "lark": ChannelType.FEISHU,
        }
        channel_type = channel_map.get(channel_str.lower(), ChannelType.WECHAT)
        return cls.create(channel_type)
    
    @classmethod
    def register(cls, channel_type: ChannelType, channel: VoiceChannel):
        """注册自定义渠道实例"""
        cls._channels[channel_type] = channel


# ==========================================
# 便捷函数
# ==========================================

def parse_message(channel_str: str, callback_data: Dict) -> Optional[StandardMessage]:
    """便捷函数：解析消息"""
    channel = VoiceChannelFactory.create_from_string(channel_str)
    return channel.parse_callback(callback_data)


def get_supported_channels() -> List[str]:
    """便捷函数：获取支持的渠道列表"""
    return [ct.value for ct in ChannelType if ct != ChannelType.UNKNOWN]


# ==========================================
# 自测
# ==========================================

def run_self_test():
    """自测"""
    print("=" * 60)
    print("多渠道抽象层 — 自测模式")
    print("=" * 60)
    
    # 测试 1: 企业微信回调解析
    print("\n[测试 1] 企业微信回调解析")
    wechat_callback = {
        "msgid": "msg_001",
        "msgtype": "voice",
        "from": {"userid": "user_123"},
        "voice": {
            "content": "你好，我想查天气",
            "media_id": "media_001",
            "duration": 3.5,
        }
    }
    msg = parse_message("wechat", wechat_callback)
    assert msg is not None
    assert msg.channel == ChannelType.WECHAT
    assert msg.userid == "user_123"
    assert msg.content == "你好，我想查天气"
    print(f"  解析: {msg}")
    print("✅ 企业微信回调解析通过")
    
    # 测试 2: 钉钉回调解析
    print("\n[测试 2] 钉钉回调解析")
    dingtalk_callback = {
        "msgId": "msg_dt_001",
        "msgtype": "voice",
        "senderStaffId": "user_dt_001",
        "voiceContent": {
            "content": "帮我查一下天气",
            "mediaId": "media_dt_001",
            "duration": 2.0,
        }
    }
    msg = parse_message("dingtalk", dingtalk_callback)
    assert msg is not None
    assert msg.channel == ChannelType.DINGTALK
    assert "天气" in msg.content
    print(f"  解析: {msg}")
    print("✅ 钉钉回调解析通过")
    
    # 测试 3: 飞书回调解析
    print("\n[测试 3] 飞书回调解析")
    feishu_callback = {
        "message_id": "msg_fs_001",
        "message_type": "voice",
        "sender": {"sender_id": {"open_id": "user_fs_001"}},
        "voice": {
            "text": "明天天气怎么样",
            "file_key": "file_fs_001",
            "duration": 4.0,
        }
    }
    msg = parse_message("feishu", feishu_callback)
    assert msg is not None
    assert msg.channel == ChannelType.FEISHU
    assert "天气" in msg.content
    print(f"  解析: {msg}")
    print("✅ 飞书回调解析通过")
    
    # 测试 4: 文本消息解析
    print("\n[测试 4] 文本消息解析")
    text_callback = {
        "msgid": "msg_002",
        "msgtype": "text",
        "from": {"userid": "user_456"},
        "text": {"content": "你好"}
    }
    msg = parse_message("wechat", text_callback)
    assert msg is not None
    assert msg.is_text()
    assert msg.content == "你好"
    print("✅ 文本消息解析通过")
    
    # 测试 5: 工厂模式
    print("\n[测试 5] 工厂模式")
    channel = VoiceChannelFactory.create_from_string("wechat")
    assert isinstance(channel, WeChatChannel)
    channel = VoiceChannelFactory.create_from_string("dingtalk")
    assert isinstance(channel, DingTalkChannel)
    channel = VoiceChannelFactory.create_from_string("feishu")
    assert isinstance(channel, FeishuChannel)
    print("✅ 工厂模式通过")
    
    # 测试 6: 获取支持渠道
    print("\n[测试 6] 获取支持渠道")
    channels = get_supported_channels()
    print(f"  支持渠道: {channels}")
    assert "wechat" in channels
    assert "dingtalk" in channels
    assert "feishu" in channels
    print("✅ 获取支持渠道通过")
    
    # 测试 7: 渠道类型枚举
    print("\n[测试 7] 渠道类型枚举")
    assert ChannelType.WECHAT.value == "wechat"
    assert ChannelType.DINGTALK.value == "dingtalk"
    assert ChannelType.FEISHU.value == "feishu"
    print("✅ 枚举值正确")
    
    print(f"\n{'='*60}")
    print("所有自测通过 ✓")
    print("=" * 60)


if __name__ == "__main__":
    run_self_test()
