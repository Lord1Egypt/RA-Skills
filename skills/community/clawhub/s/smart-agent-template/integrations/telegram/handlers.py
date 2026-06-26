"""
Telegram Bot 消息处理器（优化版 v2.2）
新增：任务解析增强、回复验证（防止乱回答）
"""

import logging
import os
import sys
from telegram import Update
from telegram.ext import ContextTypes

# 添加父目录到路径，以便导入 memory_manager 和 task_parser
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from memory_manager import MemoryManager
from task_parser import TaskParser, ResponseValidator
from conversation_health import ConversationHealth
from task_tracker import TaskTracker

from .ai_adapter import AIAdapter

logger = logging.getLogger(__name__)


class MessageHandlers:
    """消息处理器集合（优化版 v2.2）"""
    
    def __init__(self, ai_adapter: AIAdapter, storage_dir: str = "./data/memory"):
        self.ai_adapter = ai_adapter
        # 初始化记忆管理器
        self.memory = MemoryManager(
            storage_dir=storage_dir,
            ai_client=ai_adapter,  # 复用 AI 客户端
            ai_model=ai_adapter.model
        )
        # 初始化任务解析器
        self.task_parser = TaskParser()
        self.response_validator = ResponseValidator()
        # 初始化健康评分
        self.health = ConversationHealth(self.memory)
        # 初始化任务追踪器
        self.tracker = TaskTracker(storage_dir=storage_dir.replace("memory", "tasks"))
        logger.info(f"Memory manager initialized: {storage_dir}")
        logger.info(f"Task parser initialized")
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """处理 /start 命令"""
        user = update.effective_user
        user_id = str(user.id)
        
        # 加载用户记忆
        memory_text = self.memory.load_memory(user_id)
        memory_hint = ""
        if memory_text:
            memory_hint = "\n\n💡 我记得你，让我们继续之前的对话吧！"
        
        welcome_message = f"""
👋 你好 {user.first_name}！

我是 Smart Agent Bot，一个智能助手。

可用命令：
/start - 开始使用
/help - 查看帮助
/status - 查看状态
/memory - 查看我对你的记忆

💬 直接发送消息，我会智能回复你！{memory_hint}
"""
        await update.message.reply_text(welcome_message)
        logger.info(f"User {user_id} started the bot")
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """处理 /help 命令"""
        help_text = """
📖 帮助信息

我是一个智能助手，可以：
• 回答各种问题
• 提供技术建议
• 帮助解决问题
• 进行自然对话
• 记住我们的对话历史
• 从你的纠正中学习

💡 使用方法：
直接发送消息给我，我会智能回复。

🧠 记忆能力：
• 短期记忆：最近 5 轮对话
• 长期记忆：自动压缩保存
• 自我学习：记住你的纠正

🤖 基于 smart-agent-template 构建
"""
        await update.message.reply_text(help_text)
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """处理 /status 命令"""
        user_id = str(update.effective_user.id)
        
        # 获取记忆统计
        history = self.memory.load_history(user_id)
        memory_text = self.memory._load_memory_file(user_id)
        
        # 健康评分
        health_result = self.health.calculate_score(user_id)
        
        # 检测 OpenClaw
        openclaw_status = "✅ 已启用（语义搜索）" if self.memory.use_openclaw else "❌ 未安装"
        
        status_text = f"""
✅ 系统状态

• Bot 状态: 运行中
• AI 引擎: 已连接
• 版本: v2.5.0
• OpenClaw: {openclaw_status}

🧠 你的记忆状态：
• 短期记忆：{len(history)} 条消息
• 长期记忆：{len(memory_text)} 字符
• 总对话轮数：{self.memory._get_total_rounds(user_id)}

💊 对话健康评分：
• 评分：{health_result['score']}/100 ({health_result['level']})
• 策略：{health_result['strategy']}
• 满意度：{health_result['breakdown']['satisfaction']}/30
• 质量：{health_result['breakdown']['quality']}/30
• 完成率：{health_result['breakdown']['completion']}/20

一切正常！
"""
        await update.message.reply_text(status_text)
    
    async def memory_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """处理 /memory 命令 - 查看记忆"""
        user_id = str(update.effective_user.id)
        memory_text = self.memory.load_memory(user_id)
        
        if not memory_text:
            await update.message.reply_text("🧠 我还没有关于你的长期记忆。让我们多聊聊吧！")
            return
        
        # 限制输出长度
        if len(memory_text) > 1000:
            memory_text = memory_text[:1000] + "\n\n... (更多内容已省略)"
        
        await update.message.reply_text(f"🧠 我对你的记忆：\n\n{memory_text}")
    
    async def handle_text_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """处理普通文本消息（v2.2：任务解析 + 回复验证）"""
        user = update.effective_user
        user_id = str(user.id)
        user_message = update.message.text
        
        logger.info(f"User {user_id} ({user.first_name}): {user_message}")
        
        # 发送"正在输入"状态
        await update.message.chat.send_action("typing")
        
        try:
            # 1. 任务解析（新增）
            parsed = self.task_parser.parse(user_message)
            logger.info(f"Task parsed: intent={parsed['intent']}, complexity={parsed['complexity']}")
            
            # 2. 健康评分 + 自适应策略
            health_result = self.health.calculate_score(user_id)
            strategy = health_result['strategy']
            logger.info(f"Health score: {health_result['score']} ({health_result['level']}), strategy: {strategy}")
            
            # 3. 动态构建 Context
            message_context = self._build_dynamic_context(
                user_id=user_id,
                user_message=user_message,
                parsed=parsed,
                user=user,
                chat_id=update.message.chat_id
            )
            
            # 4. 应用自适应策略
            message_context = self.health.apply_strategy(strategy, message_context)
            
            # 5. 任务编号处理
            task_ref = self.tracker.detect_task_reference(user_message)
            task_info = ""
            
            if task_ref:
                # 用户引用了任务编号 → 注入任务信息到 context
                task = self.tracker.get_task(user_id, task_ref)
                if task:
                    task_info = f"\n\n【任务 {task_ref}】{self.tracker.format_task(task)}"
                    message_context["system_prompt"] += f"\n\n当前讨论任务：{task_ref} - {task['title']}（状态：{task['status']}）"
            
            elif self.tracker.detect_new_task(user_message, parsed['intent']):
                # 检测到新任务 → 自动创建并分配编号
                task = self.tracker.create_task(user_id, user_message[:50])
                task_info = f"\n\n📋 已创建任务 {task['id']}"
            
            # 6. 调用 AI 获取回复（使用增强 Prompt）
            enhanced_message = parsed['enhanced_prompt']
            ai_response = await self.ai_adapter.get_response(enhanced_message, message_context)
            
            # 7. 回复验证（防止乱回答）
            validation = self.response_validator.validate(ai_response, user_message, parsed)
            if not validation['valid']:
                logger.warning(f"Response validation failed: {validation['issues']}")
                if validation['confidence'] < 0.5:
                    ai_response = f"⚠️ 以下回复仅供参考（置信度：{validation['confidence']:.0%}）：\n\n{ai_response}"
            
            # 附加任务编号信息
            if task_info:
                ai_response += task_info
            
            # 7. 保存对话到记忆
            self.memory.add_message(user_id, "user", user_message)
            self.memory.add_message(user_id, "assistant", ai_response)
            self.memory._increment_rounds(user_id)
            
            # 8. 异步压缩记忆（如果需要）
            if self.memory.should_compress(user_id):
                logger.info(f"Triggering memory compression for user {user_id}")
                self.memory.compress_async(user_id)
            
            # 9. 发送回复
            await update.message.reply_text(ai_response)
            
            logger.info(f"Bot replied to {user_id} (confidence: {validation['confidence']:.0%})")
            
        except Exception as e:
            logger.error(f"Error handling message: {e}", exc_info=True)
            await update.message.reply_text(
                "❌ 抱歉，处理消息时出错了。请稍后再试。"
            )
                self.memory.compress_async(user_id)
            
            # 7. 发送回复
            await update.message.reply_text(ai_response)
            
            logger.info(f"Bot replied to {user_id}")
            
        except Exception as e:
            logger.error(f"Error handling message: {e}", exc_info=True)
            await update.message.reply_text(
                "❌ 抱歉，处理消息时出错了。请稍后再试。"
            )
    
    def _build_dynamic_context(self, user_id: str, user_message: str, parsed: dict, user, chat_id: int) -> dict:
        """
        动态构建 Context（双重优化：连续性 + 复杂度，节省 60%+ token）
        
        优先级1：判断连续性
        - 新任务 → 不传历史（节省 token）
        - 连续任务 → 传历史（理解上下文）
        
        优先级2：判断复杂度
        - 简单 → 最小 Context
        - 中等 → 部分 Context
        - 复杂 → 完整 Context
        """
        from task_parser import TaskComplexity
        
        complexity = parsed['complexity']
        needs_context = parsed['needs_context']  # 是否需要上下文
        
        base = {
            "user_id": user_id,
            "username": user.username,
            "first_name": user.first_name,
            "chat_id": chat_id,
            "parsed": parsed
        }
        
        # 新任务 + 简单 → 最小 Context（进一步优化）
        if not needs_context and complexity == TaskComplexity.SIMPLE:
            return {
                **base,
                "history": [],
                "memory": "",
                "system_prompt": "你是 Smart Agent Bot，一个智能助手。简洁回答用户问题，不知道就说不知道。"
            }
        
        # 新任务 + 中等 → 不传历史，只传规范
        elif not needs_context and complexity == TaskComplexity.MEDIUM:
            return {
                **base,
                "history": [],
                "memory": "",
                "system_prompt": """你是 Smart Agent Bot，一个智能助手。
- 简洁、专业、友好
- 不知道就说不知道"""
            }
        
        # 连续任务 + 简单/中等 → 传部分历史
        elif needs_context and complexity in [TaskComplexity.SIMPLE, TaskComplexity.MEDIUM]:
            history = self.memory.load_history(user_id)
            return {
                **base,
                "history": history[-4:],  # 最近 2 轮
                "memory": "",
                "system_prompt": """你是 Smart Agent Bot，一个智能助手。
- 简洁、专业、友好
- 利用对话历史理解上下文"""
            }
        
        # 复杂任务 → 完整 Context
        else:
            history = self.memory.load_history(user_id)
            memory_text = self.memory.load_memory(
                user_id,
                query=user_message if self.memory.use_openclaw else None
            )
            return {
                **base,
                "history": history[-10:],  # 最近 5 轮
                "memory": memory_text[:500],
                "system_prompt": self._build_system_prompt()  # 完整规范
            }

    async def tasks_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """处理 /tasks 命令 - 查看任务列表"""
        user_id = str(update.effective_user.id)
        tasks = self.tracker.list_tasks(user_id)
        
        if not tasks:
            await update.message.reply_text("📋 暂无任务。发送命令类消息会自动创建任务。")
            return
        
        pending = self.tracker.list_tasks(user_id, "pending")
        in_progress = self.tracker.list_tasks(user_id, "in_progress")
        done = self.tracker.list_tasks(user_id, "done")
        
        text = "📋 任务列表\n\n"
        if in_progress:
            text += "🔄 进行中：\n" + self.tracker.format_task_list(in_progress) + "\n\n"
        if pending:
            text += "⏳ 待处理：\n" + self.tracker.format_task_list(pending) + "\n\n"
        if done:
            text += "✅ 已完成：\n" + self.tracker.format_task_list(done[-3:]) + "\n"  # 只显示最近3个
        
        await update.message.reply_text(text)

    def _detect_correction(self, message: str) -> bool:
        """检测用户纠正"""
        correction_keywords = [
            "不对", "不是", "错了", "应该是", "其实是",
            "不对，", "不是，", "错了，", "应该是", "其实是",
            "no,", "wrong", "actually", "should be", "it's"
        ]
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in correction_keywords)
    
    def _build_system_prompt(self) -> str:
        """构建 System Prompt（融入工作规范）"""
        return """你是 Smart Agent Bot，一个智能助手。

【核心原则】
1. 3高原则：高质量 + 高效率 + 高节省
2. 第一性原理：从本质出发，找最简解法
3. 主动执行，不反复询问

【工作规范】
- 理解上下文：利用对话历史和长期记忆
- 自我学习：记住用户的纠正，下次不再犯错
- 简洁回复：直接给答案，不废话
- 承认不足：不知道就说不知道，不要编造

【记忆能力】
- 你有短期记忆（最近5轮对话）
- 你有长期记忆（自动压缩保存）
- 你会从用户纠正中学习

【回复风格】
- 友好、专业、简洁
- 用 emoji 增加亲和力
- 避免冗长的解释
"""
    
    async def handle_photo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """处理图片消息"""
        await update.message.reply_text(
            "📷 我看到你发了一张图片！目前我还不能分析图片内容，但未来会支持的。"
        )
    
    async def handle_document(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """处理文件消息"""
        file_name = update.message.document.file_name
        await update.message.reply_text(
            f"📄 收到文件: {file_name}\n目前我还不能处理文件，但未来会支持的。"
        )
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """处理错误"""
        logger.error(f"Update {update} caused error {context.error}")
        
        if update and update.effective_message:
            await update.effective_message.reply_text(
                "❌ 抱歉，处理消息时出错了。请稍后再试。"
            )
