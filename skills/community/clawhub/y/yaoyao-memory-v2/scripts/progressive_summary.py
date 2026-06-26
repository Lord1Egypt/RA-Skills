#!/usr/bin/env python3
"""
progressive_summary.py - 迭代渐进式摘要

参考 Hermes Agent 的 ContextCompressor 迭代摘要机制：
- 保留上一轮摘要，实现跨压缩轮次的信息保持
- 头部保护（前 N 条消息）
- 尾部 Token 预算保护
- 工具输出剪枝

用途：
    - 长对话的上下文压缩
    - 多轮对话的信息保持
    - 防止重要信息在压缩中丢失
"""

import json
import logging
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

# ============================================================================
# 配置
# ============================================================================

DEFAULT_CONTEXT_LENGTH = 128_000  # GPT-4 Turbo
DEFAULT_THRESHOLD_PERCENT = 0.50  # 50% 时触发压缩
DEFAULT_SUMMARY_RATIO = 0.20  # 摘要占 20%
DEFAULT_TAIL_TOKEN_BUDGET = 20_000  # 尾部保护 20K tokens
DEFAULT_PROTECT_FIRST_N = 3  # 保护前 3 条消息

# 剪枝占位符
_PRUNED_TOOL_PLACEHOLDER = "[Old tool output cleared to save context space]"

# ============================================================================
# 数据结构
# ============================================================================

@dataclass
class CompressionConfig:
    """压缩配置"""
    context_length: int = DEFAULT_CONTEXT_LENGTH
    threshold_percent: float = DEFAULT_THRESHOLD_PERCENT
    summary_ratio: float = DEFAULT_SUMMARY_RATIO
    tail_token_budget: int = DEFAULT_TAIL_TOKEN_BUDGET
    protect_first_n: int = DEFAULT_PROTECT_FIRST_N


@dataclass
class CompressionResult:
    """压缩结果"""
    compressed_messages: List[Dict]
    summary: str
    tokens_saved: int
    compression_ratio: float
    previous_summary: Optional[str] = None


# ============================================================================
# Token 估算（简单实现）
# ============================================================================

def estimate_tokens(text: str) -> int:
    """简单估算 token 数量（中英文混合）"""
    # 粗略估算：中文约 2 tokens/字符，英文约 4 tokens/词
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    english_words = len(re.findall(r'[a-zA-Z]+', text))
    other = len(text) - chinese_chars - english_words
    return int(chinese_chars * 1.5 + english_words * 0.25 + other * 0.25)


def estimate_messages_tokens(messages: List[Dict]) -> int:
    """估算消息列表的总 token 数"""
    total = 0
    for msg in messages:
        # role
        total += estimate_tokens(msg.get("role", ""))
        # content
        content = msg.get("content", "")
        if isinstance(content, list):
            for item in content:
                if isinstance(item, dict):
                    total += estimate_tokens(str(item.get("text", "")))
                else:
                    total += estimate_tokens(str(item))
        else:
            total += estimate_tokens(str(content))
    return total


# ============================================================================
# 核心压缩逻辑
# ============================================================================

def _prune_old_tool_results(
    messages: List[Dict],
    protect_tail_tokens: int
) -> tuple[List[Dict], int]:
    """
    剪枝旧工具输出，用占位符替换。
    
    Args:
        messages: 消息列表
        protect_tail_tokens: 尾部保护的 token 数
    
    Returns:
        (pruned_messages, tokens_saved)
    """
    if not messages:
        return [], 0
    
    # 计算累积 token，找到剪枝边界
    cumulative = 0
    prune_boundary = 0
    
    for i, msg in enumerate(reversed(messages)):
        msg_tokens = estimate_tokens(str(msg.get("content", "")))
        
        if cumulative + msg_tokens <= protect_tail_tokens:
            cumulative += msg_tokens
        else:
            prune_boundary = len(messages) - i
            break
    
    # 执行剪枝
    pruned = []
    tokens_saved = 0
    
    for i, msg in enumerate(messages):
        if i < prune_boundary and msg.get("role") == "tool":
            # 检查内容是否真的是工具输出（简短或重复）
            content = str(msg.get("content", ""))
            if len(content) < 100 or content == _PRUNED_TOOL_PLACEHOLDER:
                pruned.append(msg)
                continue
            pruned_msg = msg.copy()
            pruned_msg["content"] = _PRUNED_TOOL_PLACEHOLDER
            pruned.append(pruned_msg)
            tokens_saved += estimate_tokens(content)
        else:
            pruned.append(msg)
    
    return pruned, tokens_saved


def _protect_head_messages(
    messages: List[Dict],
    protect_n: int
) -> List[Dict]:
    """
    保护头部消息（系统提示 + 初始交互）。
    """
    if not messages or protect_n <= 0:
        return messages
    
    # 找到系统消息（通常在开头）
    protected = []
    system_end = 0
    
    for i, msg in enumerate(messages):
        if msg.get("role") == "system":
            protected.append(msg)
            system_end = i + 1
    
    # 再保护前 N 条非系统消息
    protected.extend(messages[system_end:system_end + protect_n])
    
    return protected


def _extract_middle_messages(
    messages: List[Dict],
    first_n: int,
    tail_budget: int
) -> List[Dict]:
    """
    提取中间需要压缩的消息。
    """
    if not messages:
        return []
    
    # 跳过系统消息
    system_end = 0
    for i, msg in enumerate(messages):
        if msg.get("role") == "system":
            system_end = i + 1
    
    # 跳过头部保护
    head_end = system_end + first_n
    
    # 从尾部向前计算保护范围
    total_tokens = estimate_messages_tokens(messages)
    tail_tokens = 0
    tail_start = len(messages)
    
    for i in range(len(messages) - 1, head_end - 1, -1):
        msg_tokens = estimate_tokens(str(messages[i].get("content", "")))
        if tail_tokens + msg_tokens <= tail_budget:
            tail_tokens += msg_tokens
            tail_start = i
        else:
            break
    
    # 中间部分是需要压缩的
    return messages[head_end:tail_start]


def _build_compression_prompt(
    middle_messages: List[Dict],
    previous_summary: Optional[str] = None
) -> str:
    """
    构建压缩提示词。
    """
    prompt_parts = [
        "You are a context compression assistant. Your task is to summarize the following conversation history into a concise format.",
        "",
        "Guidelines:",
        "1. Preserve all important facts, decisions, and commitments",
        "2. Keep user preferences and requirements",
        "3. Note any pending tasks or follow-ups",
        "4. Use bullet points for clarity",
        "5. Maximum 500 words",
        "",
    ]
    
    if previous_summary:
        prompt_parts.extend([
            "PREVIOUS SUMMARY (for continuity):",
            previous_summary,
            "",
        ])
    
    prompt_parts.append("CONVERSATION TO SUMMARIZE:")
    prompt_parts.append("")
    
    for msg in middle_messages:
        role = msg.get("role", "unknown")
        content = msg.get("content", "")
        
        # 处理列表内容
        if isinstance(content, list):
            text_parts = []
            for item in content:
                if isinstance(item, dict):
                    text_parts.append(str(item.get("text", "")))
                else:
                    text_parts.append(str(item))
            content = "\n".join(text_parts)
        
        prompt_parts.append(f"[{role.upper()}]")
        prompt_parts.append(str(content)[:2000])  # 限制单条长度
        prompt_parts.append("")
    
    return "\n".join(prompt_parts)


def _call_llm_summary(prompt: str) -> Optional[str]:
    """
    调用 LLM 生成摘要。
    
    依赖：需要有效的 LLM API Key（当前密钥无效，401错误）
    TODO(v3.9.6): 集成 OpenClaw LLM 或使用 MiniMax API
    """
    logger.warning("LLM summary 需要有效的 API Key（当前不可用）")
    return None


# ============================================================================
# 主压缩函数
# ============================================================================

def compress_context(
    messages: List[Dict],
    config: Optional[CompressionConfig] = None,
    previous_summary: Optional[str] = None,
    llm_summarizer: Optional[callable] = None
) -> CompressionResult:
    """
    压缩对话上下文。
    
    Args:
        messages: 原始消息列表
        config: 压缩配置
        previous_summary: 上一轮摘要（用于迭代压缩）
        llm_summarizer: LLM 摘要调用函数
    
    Returns:
        CompressionResult: 压缩结果
    """
    if config is None:
        config = CompressionConfig()
    
    if not messages:
        return CompressionResult(
            compressed_messages=[],
            summary="",
            tokens_saved=0,
            compression_ratio=1.0,
            previous_summary=previous_summary,
        )
    
    original_tokens = estimate_messages_tokens(messages)
    threshold_tokens = int(config.context_length * config.threshold_percent)
    
    # 检查是否需要压缩
    if original_tokens < threshold_tokens:
        return CompressionResult(
            compressed_messages=messages,
            summary="",
            tokens_saved=0,
            compression_ratio=1.0,
            previous_summary=previous_summary,
        )
    
    logger.info(f"Compressing context: {original_tokens} tokens (threshold: {threshold_tokens})")
    
    # 1. 保护头部消息
    protected = _protect_head_messages(messages, config.protect_first_n)
    
    # 2. 提取中间消息
    middle = _extract_middle_messages(
        messages,
        config.protect_first_n,
        config.tail_token_budget
    )
    
    # 3. 剪枝旧工具输出
    protected, pruned_tokens = _prune_old_tool_results(
        protected + middle,
        config.tail_token_budget
    )
    
    # 4. LLM 摘要中间部分
    summary = ""
    if middle and llm_summarizer:
        prompt = _build_compression_prompt(middle, previous_summary)
        summary = llm_summarizer(prompt) or ""
    elif middle:
        # 无 LLM 时，简单拼接
        summary = f"[Compressed {len(middle)} messages]"
        logger.warning("No LLM summarizer, using simple compression")
    
    # 5. 构建压缩后的消息
    compressed = []
    
    # 添加头部保护
    for msg in protected[:config.protect_first_n]:
        if msg.get("role") != "tool" or msg.get("content") != _PRUNED_TOOL_PLACEHOLDER:
            compressed.append(msg)
    
    # 添加摘要消息
    if summary:
        compressed.append({
            "role": "system",
            "content": f"[COMPRESSED SUMMARY]\n{summary}"
        })
    
    # 添加尾部保护
    for msg in protected[config.protect_first_n:]:
        if msg.get("role") != "tool" or msg.get("content") != _PRUNED_TOOL_PLACEHOLDER:
            compressed.append(msg)
    
    final_tokens = estimate_messages_tokens(compressed)
    tokens_saved = original_tokens - final_tokens + pruned_tokens
    compression_ratio = final_tokens / original_tokens if original_tokens > 0 else 1.0
    
    logger.info(f"Compression complete: {final_tokens} tokens ({compression_ratio:.1%}), saved {tokens_saved}")
    
    return CompressionResult(
        compressed_messages=compressed,
        summary=summary,
        tokens_saved=tokens_saved,
        compression_ratio=compression_ratio,
        previous_summary=previous_summary,
    )


# ============================================================================
# 状态持久化
# ============================================================================

STATE_FILE = Path("~/.openclaw/workspace/memory/progressive_summary_state.json").expanduser()


def save_summary_state(summary: str, message_count: int):
    """保存摘要状态"""
    state = {
        "last_summary": summary,
        "last_message_count": message_count,
    }
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def load_summary_state() -> tuple[Optional[str], int]:
    """加载摘要状态"""
    if not STATE_FILE.exists():
        return None, 0
    
    try:
        with open(STATE_FILE) as f:
            state = json.load(f)
        return state.get("last_summary"), state.get("last_message_count", 0)
    except Exception as e:
        logger.warning(f"Failed to load summary state: {e}")
        return None, 0


# ============================================================================
# CLI 入口
# ============================================================================

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Progressive Context Compression")
    parser.add_argument("--input", "-i", help="Input messages JSON file")
    parser.add_argument("--output", "-o", help="Output compressed messages JSON file")
    parser.add_argument("--config", "-c", help="Compression config JSON file")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    
    # 加载配置
    config = CompressionConfig()
    if args.config:
        with open(args.config) as f:
            cfg = json.load(f)
            config = CompressionConfig(**cfg)
    
    # 加载消息
    if args.input:
        with open(args.input) as f:
            messages = json.load(f)
    else:
        messages = json.load(sys.stdin)
    
    # 加载上一轮摘要
    previous_summary, _ = load_summary_state()
    
    # 压缩
    result = compress_context(messages, config, previous_summary)
    
    # 保存状态
    if result.summary:
        save_summary_state(result.summary, len(messages))
    
    # 输出
    output = {
        "messages": result.compressed_messages,
        "summary": result.summary,
        "tokens_saved": result.tokens_saved,
        "compression_ratio": result.compression_ratio,
    }
    
    if args.output:
        with open(args.output, "w") as f:
            json.dump(output, f, indent=2)
        print(f"Saved to {args.output}")
    else:
        print(json.dumps(output, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
# ============================================================================
# LLM 摘要集成模块
# ============================================================================

def create_llm_summarizer(provider: str = "openai", model: str = None, api_key: str = None):
    """
    创建 LLM 摘要器
    
    Args:
        provider: 提供商 (openai/anthropic/minimax)
        model: 模型名称
        api_key: API Key (可选，从环境变量或配置读取)
    
    Returns:
        summarizer 函数
    """
    import os
    import json
    
    # 读取 API Key
    if not api_key:
        api_key = os.environ.get(f"{provider.upper()}_API_KEY") or \
                  os.environ.get("OPENAI_API_KEY") or \
                  os.environ.get("ANTHROPIC_API_KEY")
    
    def openai_summarizer(prompt: str, max_tokens: int = 500) -> str:
        """使用 OpenAI API 生成摘要"""
        import urllib.request
        import urllib.error
        
        if not model:
            model = "gpt-3.5-turbo"
        
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        data = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": 0.3,
        }
        
        req = urllib.request.Request(url, data=json.dumps(data).encode(), headers=headers, method="POST")
        
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                result = json.loads(resp.read().decode())
                return result["choices"][0]["message"]["content"]
        except Exception as e:
            logger.warning(f"OpenAI API error: {e}")
            return None
    
    def minimax_summarizer(prompt: str, max_tokens: int = 500) -> str:
        """使用 MiniMax API 生成摘要"""
        import urllib.request
        import urllib.error
        
        if not api_key:
            logger.warning("MiniMax API key not found")
            return None
        
        # MiniMax API 格式
        url = "https://api.minimax.chat/v1/text/chatcompletion_pro"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        data = {
            "model": model or "abab5.5-chat",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": 0.3,
        }
        
        req = urllib.request.Request(url, data=json.dumps(data).encode(), headers=headers, method="POST")
        
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                result = json.loads(resp.read().decode())
                return result["choices"][0]["message"]["content"]
        except Exception as e:
            logger.warning(f"MiniMax API error: {e}")
            return None
    
    # 根据 provider 返回对应的 summarizer
    if provider == "openai":
        return openai_summarizer
    elif provider == "minimax":
        return minimax_summarizer
    else:
        logger.warning(f"Unknown provider: {provider}")
        return None


def create_openclaw_summarizer():
    """
    创建 OpenClaw 集成的摘要器
    使用 OpenClaw 的 LLM 调用机制
    """
    import os
    import subprocess
    
    def openclaw_llm_summarizer(prompt: str, max_tokens: int = 500) -> str:
        """
        通过 OpenClaw CLI 调用 LLM
        
        注意：这需要 openclaw 命令可用
        """
        # 构建 prompt
        full_prompt = f"""你是一个上下文压缩助手。请将以下对话总结成一个简洁的摘要（最多{max_tokens}字）：

{prompt}

摘要："""
        
        try:
            # 尝试使用 openclaw call 或类似命令
            # 这需要 OpenClaw  支持 LLM 调用
            result = subprocess.run(
                ["openclaw", "llm", "--prompt", full_prompt],
                capture_output=True,
                text=True,
                timeout=30,
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except Exception as e:
            logger.debug(f"OpenClaw LLM call failed: {e}")
        
        return None
    
    return openclaw_llm_summarizer
