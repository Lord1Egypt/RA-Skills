#!/usr/bin/env python3
"""
WhatsApp 客户端 - 集成 OpenClaw WhatsApp 渠道
通过 OpenClaw 的 WhatsApp 渠道 API 获取消息
"""

import json
import logging
import asyncio
import aiohttp
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta


class WhatsAppClient:
    """WhatsApp 客户端"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
        # OpenClaw Gateway 配置
        openclaw_config = config.get("openclaw", {})
        host = openclaw_config.get("host", "localhost")
        port = openclaw_config.get("port", 18789)
        self.base_url = f"http://{host}:{port}"
        
        self.api_key = None
        self.session = None
        
        # 监控配置
        self.monitoring_config = config.get("monitoring", {})
        self.targets = config.get("targets", [])
        
        # 状态跟踪
        self.last_check_time = None
        self.message_cache = {}  # 缓存已处理的消息ID
        
        self.logger = logging.getLogger(__name__)
    
    async def initialize(self) -> bool:
        """初始化 WhatsApp 客户端"""
        try:
            # 检查 OpenClaw Gateway 是否运行
            if not await self._check_gateway_health():
                self.logger.error("OpenClaw Gateway 未运行或无法访问")
                return False
            
            # 获取 WhatsApp 渠道状态
            whatsapp_status = await self._get_whatsapp_status()
            if not whatsapp_status:
                self.logger.error("无法获取 WhatsApp 渠道状态")
                return False
            
            # 检查是否有已配对的设备
            paired_devices = whatsapp_status.get("paired_devices", [])
            if not paired_devices:
                self.logger.warning("没有已配对的 WhatsApp 设备，请先配对")
                # 显示配对说明
                self._show_pairing_instructions()
                return False
            
            self.logger.info(f"找到 {len(paired_devices)} 个已配对的 WhatsApp 设备")
            
            # 初始化消息缓存
            self.message_cache = {}
            
            self.logger.info("WhatsApp 客户端初始化成功")
            return True
            
        except Exception as e:
            self.logger.error(f"WhatsApp 客户端初始化失败: {str(e)}", exc_info=True)
            return False
    
    async def _check_gateway_health(self) -> bool:
        """检查 OpenClaw Gateway 健康状态"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/health", timeout=5) as response:
                    return response.status == 200
        except Exception as e:
            self.logger.debug(f"Gateway 健康检查失败: {str(e)}")
            return False
    
    async def _get_whatsapp_status(self) -> Optional[Dict[str, Any]]:
        """获取 WhatsApp 渠道状态"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/api/v1/channels/whatsapp/status",
                    timeout=10
                ) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        self.logger.error(f"获取 WhatsApp 状态失败: {response.status}")
                        return None
        except Exception as e:
            self.logger.error(f"获取 WhatsApp 状态时出错: {str(e)}")
            return None
    
    def _show_pairing_instructions(self):
        """显示 WhatsApp 配对说明"""
        instructions = """
        ⚠️ WhatsApp 设备未配对
        
        要使用 WhatsApp 监控功能，请先配对您的设备：
        
        1. 确保您的手机安装了 WhatsApp
        2. 在浏览器中打开 WhatsApp Web (web.whatsapp.com)
        3. 扫描二维码配对
        
        或者，如果您使用 WhatsApp Business API：
        
        1. 获取您的 Business API 凭证
        2. 在 OpenClaw 配置中添加 WhatsApp Business 渠道
        3. 配置 API 密钥和 Webhook
        
        配对完成后，重新启动监控服务。
        """
        self.logger.warning(instructions)
    
    async def fetch_messages(self) -> List[Dict[str, Any]]:
        """获取新消息"""
        try:
            # 获取启用的目标
            enabled_targets = [t for t in self.targets if t.get("enabled", False)]
            if not enabled_targets:
                self.logger.warning("没有启用的监控目标")
                return []
            
            all_messages = []
            
            # 为每个目标获取消息
            for target in enabled_targets:
                target_messages = await self._fetch_messages_for_target(target)
                all_messages.extend(target_messages)
            
            # 过滤已处理的消息
            new_messages = self._filter_new_messages(all_messages)
            
            # 更新最后检查时间
            self.last_check_time = datetime.now()
            
            self.logger.debug(f"获取到 {len(new_messages)} 条新消息")
            return new_messages
            
        except Exception as e:
            self.logger.error(f"获取消息时出错: {str(e)}", exc_info=True)
            return []
    
    async def _fetch_messages_for_target(self, target: Dict[str, Any]) -> List[Dict[str, Any]]:
        """为特定目标获取消息"""
        try:
            target_id = target.get("identifier")
            target_type = target.get("type", "contact")
            target_name = target.get("name", "未知目标")
            
            # 构建请求参数
            params = {
                "target": target_id,
                "limit": 50,  # 每次获取最多50条消息
                "since": self._get_since_timestamp()
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/api/v1/channels/whatsapp/messages",
                    params=params,
                    timeout=30
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        messages = data.get("messages", [])
                        
                        # 添加目标信息到每条消息
                        for msg in messages:
                            msg["target_name"] = target_name
                            msg["target_config"] = target
                            msg["priority"] = target.get("priority", "medium")
                        
                        self.logger.debug(f"从 {target_name} 获取到 {len(messages)} 条消息")
                        return messages
                    else:
                        self.logger.error(f"获取 {target_name} 消息失败: {response.status}")
                        return []
                        
        except Exception as e:
            self.logger.error(f"获取 {target.get('name', '未知')} 消息时出错: {str(e)}")
            return []
    
    def _get_since_timestamp(self) -> Optional[str]:
        """获取自上次检查以来的时间戳"""
        if not self.last_check_time:
            # 如果是第一次检查，获取最近1小时的消息
            one_hour_ago = datetime.now() - timedelta(hours=1)
            return one_hour_ago.isoformat()
        
        return self.last_check_time.isoformat()
    
    def _filter_new_messages(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """过滤新消息（基于消息ID）"""
        new_messages = []
        
        for msg in messages:
            msg_id = msg.get("id") or msg.get("message_id")
            if not msg_id:
                continue
            
            # 检查是否已处理过
            if msg_id in self.message_cache:
                continue
            
            # 添加到新消息列表
            new_messages.append(msg)
            
            # 更新缓存
            self.message_cache[msg_id] = datetime.now()
            
            # 限制缓存大小
            if len(self.message_cache) > 1000:
                self._cleanup_message_cache()
        
        return new_messages
    
    def _cleanup_message_cache(self):
        """清理消息缓存（保留最近1小时的消息）"""
        one_hour_ago = datetime.now() - timedelta(hours=1)
        
        # 移除超过1小时的消息ID
        to_remove = [
            msg_id for msg_id, timestamp 
            in self.message_cache.items() 
            if timestamp < one_hour_ago
        ]
        
        for msg_id in to_remove:
            del self.message_cache[msg_id]
        
        self.logger.debug(f"清理消息缓存，移除了 {len(to_remove)} 条旧记录")
    
    async def send_message(self, target: str, message: str) -> bool:
        """发送 WhatsApp 消息"""
        try:
            data = {
                "to": target,
                "message": message
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/v1/channels/whatsapp/send",
                    json=data,
                    timeout=30
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        success = result.get("success", False)
                        
                        if success:
                            self.logger.info(f"成功发送消息到 {target}")
                        else:
                            self.logger.error(f"发送消息失败: {result.get('error', '未知错误')}")
                        
                        return success
                    else:
                        self.logger.error(f"发送消息 HTTP 错误: {response.status}")
                        return False
                        
        except Exception as e:
            self.logger.error(f"发送消息时出错: {str(e)}", exc_info=True)
            return False
    
    async def get_chat_list(self) -> List[Dict[str, Any]]:
        """获取聊天列表"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/api/v1/channels/whatsapp/chats",
                    timeout=30
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("chats", [])
                    else:
                        self.logger.error(f"获取聊天列表失败: {response.status}")
                        return []
                        
        except Exception as e:
            self.logger.error(f"获取聊天列表时出错: {str(e)}")
            return []
    
    async def get_contact_list(self) -> List[Dict[str, Any]]:
        """获取联系人列表"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/api/v1/channels/whatsapp/contacts",
                    timeout=30
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("contacts", [])
                    else:
                        self.logger.error(f"获取联系人列表失败: {response.status}")
                        return []
                        
        except Exception as e:
            self.logger.error(f"获取联系人列表时出错: {str(e)}")
            return []
    
    async def test_connection(self) -> bool:
        """测试连接"""
        try:
            # 测试 Gateway 连接
            if not await self._check_gateway_health():
                self.logger.error("Gateway 连接测试失败")
                return False
            
            # 测试 WhatsApp 渠道
            status = await self._get_whatsapp_status()
            if not status:
                self.logger.error("WhatsApp 渠道测试失败")
                return False
            
            # 检查设备配对状态
            paired_devices = status.get("paired_devices", [])
            if not paired_devices:
                self.logger.warning("测试通过，但未配对设备")
                return True  # 仍返回 True，因为连接正常
            
            self.logger.info("WhatsApp 连接测试成功")
            return True
            
        except Exception as e:
            self.logger.error(f"连接测试失败: {str(e)}")
            return False
    
    async def cleanup(self):
        """清理资源"""
        if self.session:
            await self.session.close()
            self.session = None
        
        self.logger.info("WhatsApp 客户端清理完成")
    
    def get_target_status(self) -> Dict[str, Any]:
        """获取目标状态"""
        enabled_targets = [t for t in self.targets if t.get("enabled", False)]
        disabled_targets = [t for t in self.targets if not t.get("enabled", False)]
        
        return {
            "total_targets": len(self.targets),
            "enabled_targets": len(enabled_targets),
            "disabled_targets": len(disabled_targets),
            "last_check_time": self.last_check_time.isoformat() if self.last_check_time else None,
            "cached_messages": len(self.message_cache)
        }