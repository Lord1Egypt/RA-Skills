"""
Smart Agent 记忆管理模块
三层架构：稳定 → 持久 → 智能

- 第一层：短期记忆（最近5轮对话，防崩溃）
- 第二层：长期记忆（AI自动摘要压缩，不丢失）
- 第三层：结构化 System Prompt（准确理解上下文）

自动检测 OpenClaw：
- 如果安装了 OpenClaw → 使用 memory_search 工具（向量语义搜索）
- 如果没有安装 → 使用本地文件 + AI 压缩方案
"""

import json
import os
import shutil
import subprocess
import threading
from datetime import datetime
from typing import Optional

# 配置
SHORT_TERM_ROUNDS = 5    # 短期记忆保留轮数
COMPRESS_TRIGGER = 5     # 每N轮触发一次压缩
MEMORY_MAX_CHARS = 1000  # 长期记忆最大字符数


def _detect_openclaw() -> bool:
    """检测是否安装了 OpenClaw"""
    return shutil.which("openclaw") is not None


def _openclaw_memory_search(query: str, workspace: str = None) -> str:
    """
    使用 OpenClaw memory_search 进行语义搜索
    返回相关记忆片段
    """
    try:
        cmd = ["openclaw", "memory", "search", query]
        if workspace:
            cmd += ["--workspace", workspace]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass
    return ""


class MemoryManager:
    """记忆管理器（自动检测 OpenClaw）"""

    def __init__(self, storage_dir: str, ai_client=None, ai_model: str = None, openclaw_workspace: str = None):
        """
        storage_dir: 存储目录
        ai_client: AI 客户端（用于压缩摘要）
        ai_model: AI 模型名称
        openclaw_workspace: OpenClaw workspace 路径（可选）
        """
        self.storage_dir = storage_dir
        self.ai_client = ai_client
        self.ai_model = ai_model
        self.openclaw_workspace = openclaw_workspace
        self.use_openclaw = _detect_openclaw()
        os.makedirs(storage_dir, exist_ok=True)
        
        if self.use_openclaw:
            print("✅ 检测到 OpenClaw，使用 memory_search 语义搜索")
        else:
            print("📁 未检测到 OpenClaw，使用本地文件 + AI 压缩方案")

    # ========== 短期记忆（对话历史）==========

    def load_history(self, user_id: str) -> list:
        """加载对话历史"""
        path = os.path.join(self.storage_dir, f"{user_id}_history.json")
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def save_history(self, user_id: str, history: list):
        """保存对话历史（只保留最近 N 轮）"""
        max_msgs = SHORT_TERM_ROUNDS * 2
        if len(history) > max_msgs:
            history = history[-max_msgs:]
        path = os.path.join(self.storage_dir, f"{user_id}_history.json")
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)

    def add_message(self, user_id: str, role: str, content: str) -> list:
        """添加一条消息到历史"""
        history = self.load_history(user_id)
        history.append({"role": role, "content": content})
        self.save_history(user_id, history)
        return history

    # ========== 长期记忆（摘要压缩 + 语义搜索）==========

    def load_memory(self, user_id: str, query: str = None) -> str:
        """
        加载长期记忆
        
        Args:
            user_id: 用户ID
            query: 查询关键词（可选，用于语义搜索）
        
        Returns:
            记忆内容
        """
        # 如果有 OpenClaw 且提供了查询，使用语义搜索
        if self.use_openclaw and query:
            search_result = _openclaw_memory_search(query, self.openclaw_workspace)
            if search_result:
                return f"【语义搜索结果】\n{search_result}\n\n【完整记忆】\n{self._load_memory_file(user_id)}"
        
        # 否则返回完整记忆
        return self._load_memory_file(user_id)
    
    def _load_memory_file(self, user_id: str) -> str:
        """加载记忆文件"""
        path = os.path.join(self.storage_dir, f"{user_id}_memory.md")
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        return ""

    def save_memory(self, user_id: str, content: str):
        """保存长期记忆"""
        path = os.path.join(self.storage_dir, f"{user_id}_memory.md")
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)

    def should_compress(self, user_id: str) -> bool:
        """判断是否需要压缩（每N轮触发一次）"""
        history = self.load_history(user_id)
        total_rounds = self._get_total_rounds(user_id)
        return total_rounds > 0 and total_rounds % COMPRESS_TRIGGER == 0

    def _get_total_rounds(self, user_id: str) -> int:
        """获取总对话轮数"""
        path = os.path.join(self.storage_dir, f"{user_id}_stats.json")
        if os.path.exists(path):
            with open(path, 'r') as f:
                return json.load(f).get('total_rounds', 0)
        return 0

    def _increment_rounds(self, user_id: str):
        """增加对话轮数计数"""
        path = os.path.join(self.storage_dir, f"{user_id}_stats.json")
        stats = {}
        if os.path.exists(path):
            with open(path, 'r') as f:
                stats = json.load(f)
        stats['total_rounds'] = stats.get('total_rounds', 0) + 1
        with open(path, 'w') as f:
            json.dump(stats, f)

    def compress_async(self, user_id: str, history: list):
        """异步压缩（不阻塞用户回复）"""
        if not self.ai_client:
            return
        thread = threading.Thread(
            target=self._compress_and_save,
            args=(user_id, history),
            daemon=True
        )
        thread.start()

    def _compress_and_save(self, user_id: str, history: list):
        """执行压缩并保存（后台线程）"""
        try:
            existing_memory = self.load_memory(user_id)

            # 构建压缩提示词
            history_text = "\n".join([
                f"{m['role']}: {m['content']}" for m in history
            ])

            compress_prompt = f"""请从以下对话中提炼重要信息，更新用户记忆。

【现有记忆】
{existing_memory if existing_memory else "（空）"}

【新对话内容】
{history_text}

请输出更新后的记忆，格式如下（控制在500字以内）：

## 个人信息
（用户的基本信息、偏好）

## 项目/任务
（正在进行的项目和任务）

## 重要决策
（已做出的重要决定）

## 注意事项
（需要记住的特殊要求）

只保留真正重要的信息，过程细节不需要记录。"""

            response = self.ai_client.messages.create(
                model=self.ai_model,
                max_tokens=800,
                messages=[{"role": "user", "content": compress_prompt}]
            )

            new_memory = response.content[0].text

            # 如果超过最大字符数，再压缩一次
            if len(new_memory) > MEMORY_MAX_CHARS:
                new_memory = new_memory[:MEMORY_MAX_CHARS] + "\n...(已截断)"

            self.save_memory(user_id, new_memory)

        except Exception as e:
            pass  # 压缩失败不影响主流程

    # ========== 结构化 System Prompt ==========

    def build_system_prompt(self, user_id: str, base_prompt: str = "") -> str:
        """构建包含记忆的 System Prompt"""
        memory = self.load_memory(user_id)

        parts = [base_prompt or "你是一个智能助手，回答简洁友好。"]

        if memory:
            parts.append(f"\n【用户记忆】\n{memory}")

        parts.append("\n请根据用户记忆和对话历史，准确理解上下文并回复。")

        return "\n".join(parts)

    # ========== 完整对话流程 ==========

    def process_message(self, user_id: str, user_message: str,
                        ai_call_fn, base_prompt: str = "") -> str:
        """
        完整的消息处理流程：
        1. 加载历史
        2. 构建 System Prompt（含长期记忆）
        3. 调用 AI
        4. 保存历史
        5. 异步压缩（如需要）

        ai_call_fn: 调用 AI 的函数，签名：fn(system, messages) -> str
        """
        # 加载短期历史
        history = self.load_history(user_id)

        # 追加用户消息
        history.append({"role": "user", "content": user_message})

        # 构建 System Prompt（含长期记忆）
        system = self.build_system_prompt(user_id, base_prompt)

        # 调用 AI
        ai_response = ai_call_fn(system, history)

        # 追加 AI 回复
        history.append({"role": "assistant", "content": ai_response})

        # 保存历史
        self.save_history(user_id, history)

        # 增加轮数计数
        self._increment_rounds(user_id)

        # 异步压缩（不阻塞）
        if self.should_compress(user_id):
            self.compress_async(user_id, history)

        return ai_response

    def clear(self, user_id: str):
        """清除用户所有记忆"""
        for suffix in ['_history.json', '_memory.md', '_stats.json']:
            path = os.path.join(self.storage_dir, f"{user_id}{suffix}")
            if os.path.exists(path):
                os.remove(path)
