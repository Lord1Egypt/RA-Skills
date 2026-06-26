#!/usr/bin/env python3
"""
Telegram Bot 主程序
基于 smart-agent-template 的多渠道 Agent 通信实现
"""

import logging
import sys
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from config import config
from ai_adapter import create_ai_adapter
from handlers import MessageHandlers

# 配置日志
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


def main():
    """启动 Bot"""
    
    print("=" * 60)
    print("🚀 Smart Agent Telegram Bot")
    print("=" * 60)
    
    # 验证配置
    try:
        config.validate()
        print(f"✅ 配置验证通过")
        print(f"📱 Bot Token: {config.telegram.bot_token[:20]}...")
        print(f"👤 Admin Chat ID: {config.telegram.admin_chat_id}")
        print(f"🤖 AI Engine: {config.ai.engine}")
        print(f"📦 Model: {config.ai.model}")
    except ValueError as e:
        print(f"❌ 配置错误: {e}")
        print("\n请检查环境变量配置:")
        print("  - TELEGRAM_BOT_TOKEN")
        print("  - TELEGRAM_ADMIN_CHAT_ID")
        print("  - AI_ENGINE (openai/claude/deepseek/ollama)")
        print("  - <ENGINE>_API_KEY (如果需要)")
        sys.exit(1)
    
    # 创建 AI 适配器
    try:
        ai_adapter = create_ai_adapter(
            engine=config.ai.engine,
            api_key=config.ai.api_key,
            model=config.ai.model,
            base_url=config.ai.base_url
        )
        print(f"✅ AI 适配器创建成功")
    except Exception as e:
        print(f"❌ AI 适配器创建失败: {e}")
        sys.exit(1)
    
    # 创建消息处理器（传入存储目录）
    handlers = MessageHandlers(ai_adapter, storage_dir="./data/memory")
    
    # 创建应用
    application = Application.builder().token(config.telegram.bot_token).build()
    
    # 注册命令处理器
    application.add_handler(CommandHandler("start", handlers.start_command))
    application.add_handler(CommandHandler("help", handlers.help_command))
    application.add_handler(CommandHandler("status", handlers.status_command))
    application.add_handler(CommandHandler("memory", handlers.memory_command))  # 新增
    application.add_handler(CommandHandler("tasks", handlers.tasks_command))    # 新增
    
    # 注册消息处理器
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.handle_text_message)
    )
    application.add_handler(MessageHandler(filters.PHOTO, handlers.handle_photo))
    application.add_handler(MessageHandler(filters.Document.ALL, handlers.handle_document))
    
    # 注册错误处理器
    application.add_error_handler(handlers.error_handler)
    
    # 启动 Bot
    print("=" * 60)
    print("✅ Bot 已启动，正在监听消息...")
    print("💬 发送消息给 Bot，体验智能回复！")
    print("按 Ctrl+C 停止")
    print("=" * 60)
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
