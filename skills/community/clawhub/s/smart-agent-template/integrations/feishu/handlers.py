"""
飞书 Bot 消息处理器
复用 smart-agent-template 的 AI 适配器和记忆管理
"""

import logging
import os
import sys
import json

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from memory_manager import MemoryManager
from task_parser import TaskParser, ResponseValidator
from conversation_health import ConversationHealth
from task_tracker import TaskTracker

# 导入 Telegram 的 AI 适配器（复用）
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'telegram'))
from ai_adapter import AIAdapter

logger = logging.getLogger(__name__)


class FeishuMessageHandlers:
    """飞书消息处理器"""
    
    def __init__(self, ai_adapter: AIAdapter, storage_dir: str = "./data/memory"):
        self.ai_adapter = ai_adapter
        # 初始化记忆管理器
        self.memory = MemoryManager(
            storage_dir=storage_dir,
            ai_client=ai_adapter,
            ai_model=ai_adapter.model
        )
        # 初始化任务解析器
        self.task_parser = TaskParser()
        self.response_validator = ResponseValidator()
        # 初始化健康评分
        self.health = ConversationHealth(self.memory)
        # 初始化任务追踪器
        self.tracker = TaskTracker(storage_dir=storage_dir.replace("memory", "tasks"))
        logger.info(f"Feishu handlers initialized: {storage_dir}")
    
    async def handle_message(self, event_data: dict) -> dict:
        """
        处理飞书消息事件
        
        Args:
            event_data: 飞书事件数据
            
        Returns:
            回复消息
        """
        try:
            # 提取消息内容
            message = event_data.get('event', {}).get('message', {})
            content = json.loads(message.get('content', '{}'))
            text = content.get('text', '').strip()
            
            if not text:
                return {"text": "请发送文本消息"}
            
            # 获取用户信息
            sender = event_data.get('event', {}).get('sender', {})
            user_id = sender.get('sender_id', {}).get('open_id', 'unknown')
            
            # 处理命令
            if text.startswith('/'):
                return await self._handle_command(text, user_id)
            
            # 加载用户记忆
            user_memory = self.memory.load_memory(user_id)
            
            # 解析任务（如果是任务）
            task_info = self.task_parser.parse_task(text)
            if task_info:
                # 记录任务
                self.tracker.add_task(
                    user_id=user_id,
                    task_id=task_info['task_id'],
                    description=text,
                    priority=task_info.get('priority', 'P2')
                )
            
            # 构建上下文
            context = {
                'user_id': user_id,
                'memory': user_memory,
                'task_info': task_info
            }
            
            # 获取 AI 回复
            response = await self.ai_adapter.get_response(text, context)
            
            # 验证回复质量
            if not self.response_validator.validate(response, text):
                response = "抱歉，我需要更多信息才能回答。能详细说明一下吗？"
            
            # 保存对话到记忆
            self.memory.add_message(user_id, "user", text)
            self.memory.add_message(user_id, "assistant", response)
            
            # 评估对话健康度
            health_score = self.health.evaluate(user_id)
            if health_score < 0.5:
                logger.warning(f"Low conversation health for {user_id}: {health_score}")
            
            return {"text": response}
            
        except Exception as e:
            logger.error(f"Error handling message: {e}", exc_info=True)
            return {"text": "处理消息时出错，请稍后重试"}
    
    async def _handle_command(self, command: str, user_id: str) -> dict:
        """处理命令"""
        cmd = command.split()[0].lower()
        
        if cmd == '/start':
            return {"text": "👋 你好！我是智能助手，有什么可以帮你的？"}
        
        elif cmd == '/help':
            help_text = """
📚 可用命令：
/start - 开始对话
/help - 显示帮助
/status - 查看状态
/memory - 查看记忆摘要
/tasks - 查看任务列表
"""
            return {"text": help_text}
        
        elif cmd == '/status':
            memory_count = len(self.memory.load_memory(user_id))
            health_score = self.health.evaluate(user_id)
            tasks = self.tracker.get_user_tasks(user_id)
            
            status_text = f"""
📊 状态信息：
💾 记忆条数：{memory_count}
❤️ 对话健康度：{health_score:.2f}
📋 进行中任务：{len([t for t in tasks if t['status'] == 'in_progress'])}
✅ 已完成任务：{len([t for t in tasks if t['status'] == 'completed'])}
"""
            return {"text": status_text}
        
        elif cmd == '/memory':
            memory = self.memory.load_memory(user_id)
            if not memory:
                return {"text": "暂无记忆"}
            
            summary = self.memory.get_summary(user_id)
            return {"text": f"📝 记忆摘要：\n{summary}"}
        
        elif cmd == '/tasks':
            tasks = self.tracker.get_user_tasks(user_id)
            if not tasks:
                return {"text": "暂无任务"}
            
            task_list = "\n".join([
                f"[{t['task_id']}] {t['description']} - {t['status']}"
                for t in tasks
            ])
            return {"text": f"📋 任务列表：\n{task_list}"}
        
        else:
            return {"text": f"未知命令：{cmd}"}
