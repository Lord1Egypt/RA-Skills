from __future__ import annotations
"""
welcome_guide.py - 首次使用引导流程

向用户介绍系统功能和使用方法
- 系统自我介绍
- 核心功能介绍
- 操作指南
- 优化建议
"""

import os
import json
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

_VERSION = "v12.0.0"

_ONBOARDING_PROGRESS_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "data", "onboarding_progress.json"
)


def seed_memories() -> List[Dict]:
    """
    返回 3 条种子记忆，用于首次运行时注入。

    Returns:
        list[dict]: 种子记忆列表
    """
    return [
        {"content": "我是一个使用 Agent Memory V12 管理知识和经验的智能体。", "metadata": {"type": "identity", "source": "onboarding"}},
        {"content": "今天是我使用 Agent Memory 的第一天，期待学习和成长。", "metadata": {"type": "milestone", "source": "onboarding"}},
        {"content": "我的目标是构建一个全面的记忆系统，帮助我更高效地工作。", "metadata": {"type": "goal", "source": "onboarding"}},
    ]


class WelcomeGuide:
    """
    欢迎引导
    
    首次使用时向用户介绍系统功能和使用方法
    """
    
    def __init__(self, memory_bridge):
        """
        初始化欢迎引导
        
        Args:
            memory_bridge: 记忆系统桥接实例
        """
        self.memory_bridge = memory_bridge
        self.is_initialized = False
        self.guide_steps = [
            self._step_introduction,
            self._step_features,
            self._step_usage,
            self._step_optimization,
            self._step_final
        ]
        self.current_step = 0
    
    def is_first_time(self) -> bool:
        """
        检查是否首次使用
        
        Returns:
            bool: 是否首次使用（onboarding 未完成）
        """
        progress = get_progress()
        if progress.get("onboarding_completed"):
            return False
        return True
    
    @staticmethod
    def mark_step_completed(step_number: int):
        """
        标记 onboarding 步骤完成
        
        Args:
            step_number: 步骤编号
        """
        progress = get_progress()
        progress["step"] = step_number
        _save_progress(progress)
    
    @staticmethod
    def mark_onboarding_completed():
        """标记 onboarding 全部完成"""
        progress = get_progress()
        progress["onboarding_completed"] = True
        _save_progress(progress)
    
    def start_guide(self) -> Dict:
        """
        开始引导流程
        
        Returns:
            dict: 引导内容
        """
        self.current_step = 0
        self.is_initialized = True
        return self._next_step()
    
    def _next_step(self) -> Dict:
        """
        进入下一步
        
        Returns:
            dict: 引导内容
        """
        if self.current_step < len(self.guide_steps):
            step_func = self.guide_steps[self.current_step]
            result = step_func()
            self.current_step += 1
            result["step"] = self.current_step
            result["total_steps"] = len(self.guide_steps)
            return result
        else:
            return {
                "type": "guide_complete",
                "message": "引导完成！现在您可以开始使用智能记忆系统了。",
                "step": self.current_step,
                "total_steps": len(self.guide_steps),
                "completed": True
            }
    
    def _step_introduction(self) -> Dict:
        """
        系统介绍
        """
        return {
            "type": "introduction",
            "title": "欢迎使用智能记忆系统！",
            "message": "您好！我是您的智能记忆助手，专为帮助您记录、整理和检索信息而设计。",
            "content": "\n我是一个基于先进记忆技术的智能系统，能够：\n\n• 智能记录和整理您的对话内容\n• 自动识别重要信息并建立关联\n• 提供快速准确的信息检索\n• 支持多种形式的知识输入\n• 随着使用不断学习和优化",
            "options": [
                {"text": "继续了解功能", "action": "next"}
            ]
        }
    
    def _step_features(self) -> Dict:
        """
        核心功能介绍
        """
        return {
            "type": "features",
            "title": "核心功能",
            "message": "我拥有以下强大功能：",
            "content": "\n**智能记忆**\n• 自动识别重要内容并记录\n• 建立记忆之间的关联关系\n• 支持情感编码和时间线追踪\n\n**投喂模式**\n• 支持导入文本、文件、链接\n• 自动整理和提取核心内容\n• 生成结构化的知识摘要\n\n**智能检索**\n• 支持关键词和语义搜索\n• 上下文感知的智能推荐\n• 多维度的信息筛选\n\n**个性化学习**\n• 分析您的兴趣和需求\n• 提供个性化的知识建议\n• 支持不同风格和角色的切换",
            "options": [
                {"text": "了解使用方法", "action": "next"}
            ]
        }
    
    def _step_usage(self) -> Dict:
        """
        使用方法指南
        """
        return {
            "type": "usage",
            "title": "使用指南",
            "message": "如何充分利用智能记忆系统：",
            "content": "\n**日常对话**\n• 开始对话时，我会询问是否记录\n• 对话过程中，重要信息会被自动识别\n• 对话结束时，我会整理并保存内容\n\n**投喂模式**\n• 输入 '开启投喂模式' 开始\n• 粘贴文本、文件路径或URL\n• 长时间无输入时，我会询问是否结束\n• 结束后，我会生成摘要并保存\n\n**信息检索**\n• 直接询问我关于之前的内容\n• 使用关键词进行精确搜索\n• 利用上下文进行关联查询\n\n**个性化设置**\n• 根据您的使用习惯自动调整\n• 支持不同风格和角色的切换\n• 提供记忆使用的分析报告",
            "options": [
                {"text": "了解优化建议", "action": "next"}
            ]
        }
    
    def _step_optimization(self) -> Dict:
        """
        优化建议
        """
        return {
            "type": "optimization",
            "title": "优化建议",
            "message": "如何优化和加强系统：",
            "content": "\n**数据质量**\n• 提供详细和准确的信息\n• 定期整理和更新记忆\n• 标记重要的内容\n\n**系统配置**\n• 根据需要调整记忆存储设置\n• 定期备份重要记忆\n• 合理设置自动记忆规则\n\n**使用习惯**\n• 养成定期投喂的习惯\n• 主动反馈记忆的准确性\n• 利用系统提供的分析报告\n\n**扩展功能**\n• 探索不同角色和风格\n• 尝试多模态内容的输入\n• 利用记忆系统的API进行集成",
            "options": [
                {"text": "完成引导", "action": "next"}
            ]
        }
    
    def _step_final(self) -> Dict:
        """
        最终步骤
        """
        return {
            "type": "final",
            "title": "开始使用",
            "message": "现在您已经了解了智能记忆系统的基本功能和使用方法。",
            "content": "\n**开始体验**\n• 尝试开启一次对话\n• 体验投喂模式的资料处理\n• 测试信息检索功能\n\n**随时帮助**\n• 输入 '帮助' 查看功能列表\n• 输入 '开启投喂模式' 开始资料导入\n• 输入 '总结对话' 整理当前内容\n\n祝您使用愉快！",
            "options": [
                {"text": "开始使用", "action": "start_using"}
            ]
        }
    
    def get_help(self) -> Dict:
        """
        获取帮助信息
        
        Returns:
            dict: 帮助内容
        """
        return {
            "type": "help",
            "title": "功能列表",
            "message": "智能记忆系统功能：",
            "content": "\n**基础功能**\n• 记录对话内容\n• 智能搜索记忆\n• 生成内容摘要\n\n**投喂模式**\n• 开启投喂模式 - 开始资料导入\n• 结束投喂 - 结束并整理资料\n\n**智能功能**\n• 总结对话 - 整理当前对话\n• 查看记忆 - 浏览已保存的记忆\n• 优化系统 - 调整系统设置\n\n**其他**\n• 帮助 - 显示此帮助信息\n• 关于 - 显示系统信息",
            "options": [
                {"text": "关闭", "action": "close_help"}
            ]
        }
    
    def get_about(self) -> Dict:
        """
        获取系统信息

        Returns:
            dict: 系统信息
        """
        return {
            "type": "about",
            "title": "关于智能记忆系统",
            "message": f"智能记忆系统 {_VERSION}",
            "content": f"\n**系统版本**：{_VERSION}\n**核心功能**：智能记忆、投喂模式、智能检索、个性化学习\n**技术特点**：6维坐标编码、RRF双路检索、情感编码、因果链检测\n**适用场景**：个人知识管理、学习辅助、工作效率提升、创意生成\n\n**开发者**：智能记忆团队\n**联系我们**：https://github.com/agent-memory-v12",
            "options": [
                {"text": "关闭", "action": "close_about"}
            ]
        }

    @staticmethod
    def get_config_guide() -> Dict:
        """
        返回分步配置指南。

        Returns:
            dict: 配置指南
        """
        return {
            "title": "配置指南",
            "steps": [
                {
                    "step": 1,
                    "title": "选择嵌入后端",
                    "description": "设置 AGENT_MEMORY_EMBEDDING_BACKEND 环境变量",
                    "options": [
                        {"value": "local", "description": "本地模型（默认，无需 API Key，首次加载约 10-15 秒）"},
                        {"value": "openai", "description": "OpenAI Embeddings（需要 OPENAI_API_KEY）"},
                        {"value": "sentence-transformers", "description": "Sentence-Transformers（本地，需 pip install sentence-transformers）"},
                    ],
                    "env_var": "AGENT_MEMORY_EMBEDDING_BACKEND",
                    "default": "local",
                },
                {
                    "step": 2,
                    "title": "配置 LLM API Key（可选）",
                    "description": "如需使用 LLM 增强功能（蒸馏摘要、叙事生成等），需配置 API Key",
                    "options": [
                        {"value": "OPENAI_API_KEY", "description": "OpenAI API Key"},
                        {"value": "ANTHROPIC_API_KEY", "description": "Anthropic API Key"},
                    ],
                    "env_var": "OPENAI_API_KEY",
                    "default": None,
                },
                {
                    "step": 3,
                    "title": "设置存储路径（可选）",
                    "description": "默认使用项目目录下的 memory.db，可通过环境变量自定义",
                    "options": [
                        {"value": "default", "description": "使用默认路径 <project>/agent_memory/memory.db"},
                        {"value": "custom", "description": "通过 AGENT_MEMORY_DB_PATH 指定自定义路径"},
                    ],
                    "env_var": "AGENT_MEMORY_DB_PATH",
                    "default": None,
                },
            ],
        }

    @staticmethod
    def is_configured() -> bool:
        """
        检查核心配置是否已设置（不仅限于首次运行检测）。

        检查项：
        - 嵌入后端是否可正常初始化
        - 数据库路径是否可写

        Returns:
            bool: 核心配置是否就绪
        """
        # 检查数据库路径是否可写
        db_path = os.environ.get("AGENT_MEMORY_DB_PATH")
        if db_path:
            try:
                parent = os.path.dirname(db_path)
                if parent and not os.path.exists(parent):
                    return False
                # 尝试写入测试
                test_file = os.path.join(parent or ".", ".agent_memory_write_test")
                with open(test_file, "w") as f:
                    f.write("test")
                os.unlink(test_file)
            except (OSError, PermissionError):
                return False

        # 检查嵌入后端配置
        backend = os.environ.get("AGENT_MEMORY_EMBEDDING_BACKEND", "local").lower()
        if backend == "openai":
            if not os.environ.get("OPENAI_API_KEY"):
                return False

        return True


def get_progress() -> Dict:
    """
    获取 onboarding 进度

    Returns:
        dict: {"step": int, "onboarding_completed": bool}
    """
    try:
        if os.path.exists(_ONBOARDING_PROGRESS_FILE):
            with open(_ONBOARDING_PROGRESS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        logger.warning("Failed to read onboarding progress: %s", e)
    return {"step": 0, "onboarding_completed": False}


def _save_progress(progress: Dict):
    """保存 onboarding 进度到 JSON 文件"""
    try:
        os.makedirs(os.path.dirname(_ONBOARDING_PROGRESS_FILE), exist_ok=True)
        with open(_ONBOARDING_PROGRESS_FILE, "w", encoding="utf-8") as f:
            json.dump(progress, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.warning("Failed to save onboarding progress: %s", e)


def create_welcome_guide(memory_bridge):
    """
    创建欢迎引导实例

    Args:
        memory_bridge: 记忆系统桥接实例

    Returns:
        WelcomeGuide: 欢迎引导实例
    """
    return WelcomeGuide(memory_bridge)


def is_first_time(memory_bridge=None) -> bool:
    """
    模块级便捷函数：检查是否首次使用。

    基于 onboarding_completed 标志判断，而非记忆数量。

    Args:
        memory_bridge: 可选的记忆系统桥接实例（保留兼容性，不再使用）

    Returns:
        bool: 是否首次使用（onboarding 未完成）
    """
    progress = get_progress()
    return not progress.get("onboarding_completed", False)
