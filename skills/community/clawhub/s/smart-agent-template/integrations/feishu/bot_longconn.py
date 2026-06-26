#!/usr/bin/env python3
"""
飞书 Bot 主程序（长链接模式）
不需要公网 URL，通过 SDK 长连接接收事件
"""

import os
# 禁用 SSL 证书验证（解决本地代理证书问题）
os.environ['PYTHONHTTPSVERIFY'] = '0'
os.environ['CURL_CA_BUNDLE'] = ''
os.environ['REQUESTS_CA_BUNDLE'] = ''

import logging
import sys
import json
import asyncio
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import config

# 导入 Telegram 的 AI 适配器（复用）
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'telegram'))
from ai_adapter import create_ai_adapter

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from memory_manager import MemoryManager
from task_parser import TaskParser
from task_tracker import TaskTracker

# 配置日志
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# 全局变量
_ai_adapter = None
_memory = None
_task_parser = None
_tracker = None


async def handle_message_async(event_data):
    """处理消息事件（异步）"""
    try:
        # 提取消息内容
        message = event_data.event.message
        sender = event_data.event.sender
        
        # 解析消息内容
        content = json.loads(message.content)
        text = content.get('text', '').strip()
        
        if not text:
            return
        
        # 获取用户信息
        user_id = sender.sender_id.open_id
        chat_id = message.chat_id
        
        logger.info(f"收到消息：{text[:50]}... (from {user_id})")
        
        # 加载用户记忆
        user_memory = _memory.load_memory(user_id)
        
        # 解析任务
        task_info = _task_parser.parse(text)
        
        # 构建上下文
        context = {
            'user_id': user_id,
            'memory': user_memory,
            'task_info': task_info
        }
        
        # 获取 AI 回复
        response = await _ai_adapter.get_response(text, context)
        
        # 保存对话到记忆
        _memory.add_message(user_id, "user", text)
        _memory.add_message(user_id, "assistant", response)
        
        # 发送回复
        await send_feishu_message_async(chat_id, response)
        
        logger.info(f"已回复：{response[:50]}...")
        
    except Exception as e:
        logger.error(f"处理消息失败: {e}", exc_info=True)


async def send_feishu_message_async(chat_id: str, text: str):
    """发送飞书消息（异步）"""
    try:
        import urllib.request as _urllib
        
        # 获取 access token
        token_data = json.dumps({
            "app_id": config.feishu.app_id,
            "app_secret": config.feishu.app_secret
        }).encode('utf-8')
        token_req = _urllib.Request(
            "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
            data=token_data,
            headers={'Content-Type': 'application/json; charset=utf-8'}
        )
        with _urllib.urlopen(token_req) as resp:
            access_token = json.loads(resp.read()).get('tenant_access_token', '')
        
        if not access_token:
            logger.error("获取 access token 失败")
            return
        
        # 发送消息
        msg_data = json.dumps({
            "receive_id": chat_id,
            "content": json.dumps({"text": text}),
            "msg_type": "text"
        }).encode('utf-8')
        msg_req = _urllib.Request(
            "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id",
            data=msg_data,
            headers={
                'Content-Type': 'application/json; charset=utf-8',
                'Authorization': f'Bearer {access_token}'
            }
        )
        with _urllib.urlopen(msg_req) as resp:
            result = json.loads(resp.read())
        
        if result.get('code') != 0:
            logger.error(f"发送消息失败: {result}")
        
    except Exception as e:
        logger.error(f"发送消息异常: {e}", exc_info=True)


def main():
    global _ai_adapter, _memory, _task_parser, _tracker
    
    print("=" * 60)
    print("🚀 Smart Agent 飞书 Bot（长链接模式）")
    print("=" * 60)
    
    # 验证配置
    try:
        config.validate()
        print(f"✅ 配置验证通过")
        print(f"🔑 App ID: {config.feishu.app_id}")
        print(f"🤖 AI Engine: {config.ai.engine}")
        print(f"📦 Model: {config.ai.model}")
    except ValueError as e:
        print(f"❌ 配置错误: {e}")
        sys.exit(1)
    
    # 创建 AI 适配器
    try:
        _ai_adapter = create_ai_adapter(
            engine=config.ai.engine,
            api_key=config.ai.api_key,
            model=config.ai.model,
            base_url=config.ai.base_url
        )
        print(f"✅ AI 适配器创建成功")
    except Exception as e:
        print(f"❌ AI 适配器创建失败: {e}")
        sys.exit(1)
    
    # 初始化记忆管理
    _memory = MemoryManager(
        storage_dir="./data/memory",
        ai_client=_ai_adapter,
        ai_model=_ai_adapter.model
    )
    _task_parser = TaskParser()
    _tracker = TaskTracker(storage_dir="./data/tasks")
    
    # 导入飞书 SDK
    try:
        from lark_oapi.ws import Client as WSClient
        from lark_oapi.event.dispatcher_handler import EventDispatcherHandler
        from lark_oapi.api.im.v1 import P2ImMessageReceiveV1
    except ImportError:
        print("❌ 缺少飞书 SDK，请安装：pip install lark-oapi")
        sys.exit(1)
    
    # 创建事件处理器（encrypt_key 和 verification_token 可留空，长链接模式 SDK 自行验证）
    event_handler = EventDispatcherHandler.builder(
        config.feishu.encrypt_key or "",
        config.feishu.verification_token or ""
    ) \
        .register_p2_im_message_receive_v1(
            lambda event: asyncio.create_task(handle_message_async(event))
        ) \
        .build()
    
    # 创建长链接客户端
    ws_client = WSClient(
        app_id=config.feishu.app_id,
        app_secret=config.feishu.app_secret,
        event_handler=event_handler
    )
    
    print("=" * 60)
    print("✅ 飞书 Bot 已启动（长链接模式）")
    print("💬 无需公网 URL，通过 SDK 长连接接收消息")
    print("按 Ctrl+C 停止")
    print("=" * 60)
    
    # 启动长连接
    try:
        ws_client.start()
    except KeyboardInterrupt:
        print("\n⏹️  Bot 已停止")


if __name__ == '__main__':
    main()
