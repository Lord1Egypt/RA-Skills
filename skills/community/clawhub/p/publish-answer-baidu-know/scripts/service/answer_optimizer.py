"""回答内容智能优化与审核（基于 LLM）。

职责：
  1. 从百度知道问题页提取问题上下文（标题 + 描述 + 已有回答）
  2. 调用 OpenAI 兼容 API 生成/优化回答
  3. HITL 审核：展示生成内容，等待用户确认/修改/拒绝

环境变量：
  OPENAI_API_KEY   — API 密钥（必填）
  OPENAI_BASE_URL  — API 基础 URL（默认 https://api.openai.com/v1，国内可用智谱/DeepSeek 等）
  OPENAI_MODEL     — 模型名称（默认 gpt-4o-mini）
"""

from __future__ import annotations

import asyncio
import logging
import os
import sys
from dataclasses import dataclass
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

# 默认 Prompt 模板
_SYSTEM_PROMPT = """你是一位百度知道回答专家。你的任务是根据用户的问题，撰写一条高质量的百度知道回答。

要求：
1. 回答必须直接针对问题，内容准确、有帮助
2. 语言简洁明了，避免空话套话，篇幅 100-300 字
3. 语气友好专业，符合百度知道社区风格
4. 不要包含"亲"、"你好"等客套开头
5. 如有具体方法/步骤，请分条列出
6. 仅输出回答正文，不要输出标题、编号或额外格式"""

_OPTIMIZE_PROMPT = """你是一位百度知道回答优化专家。你的任务是根据问题上下文，优化用户提供的基础回答草稿。

要求：
1. 保留原回答的核心信息，但使表达更准确、更有帮助
2. 语言简洁明了，避免空话套话，篇幅 100-300 字
3. 语气友好专业，符合百度知道社区风格
4. 不要包含"亲"、"你好"等客套开头
5. 如有具体方法/步骤，请分条列出
6. 仅输出优化后的回答正文，不要输出标题、编号或额外格式"""

_REVIEW_PROMPT = """请对以下拟提交到百度知道的回答进行审核，检查是否存在：

1. **事实性错误**：信息是否准确？
2. **违规内容**：是否包含广告、敏感词、人身攻击等？
3. **质量评估**：是否真正对提问者有帮助？
4. **重复/冗余**：是否与已有回答高度重复？

仅输出审核结论，格式如下：
- 如果通过：PASS
- 如果有问题：FAIL: <具体原因>"""


@dataclass
class QuestionContext:
    """从问题页提取的上下文。"""
    title: str
    description: str
    existing_answers: list[str]
    url: str

    def to_summary(self, max_answers: int = 3, max_len: int = 200) -> str:
        parts = [f"问题标题：{self.title}"]
        if self.description:
            parts.append(f"问题描述：{self.description[:max_len]}")
        if self.existing_answers:
            parts.append(f"已有回答（{min(len(self.existing_answers), max_answers)} 条）：")
            for i, ans in enumerate(self.existing_answers[:max_answers], 1):
                parts.append(f"  {i}. {ans[:max_len]}")
        return "\n".join(parts)


@dataclass
class OptimizedAnswer:
    """优化后的回答。"""
    content: str
    review_result: str  # "PASS" or "FAIL: <reason>"
    model: str
    tokens_used: int = 0


# ---------------------------------------------------------------------------
# 页面信息提取
# ---------------------------------------------------------------------------

async def extract_question_context(page, question_url: str) -> QuestionContext:
    """从百度知道问题页提取问题上下文。"""
    result = await page.evaluate("""() => {
        // 问题标题
        const titleEl = document.querySelector('span.ask-title, h1 span.ask-title, .ask-title');
        const title = titleEl ? titleEl.textContent.trim() : '';

        // 问题补充描述
        const descEl = document.querySelector('.supply-txt, .question-supply, .line.question-desc');
        const description = descEl ? descEl.textContent.trim() : '';

        // 已有回答
        const answers = [];
        const answerEls = document.querySelectorAll('.answer-content, .best-text, .answer-text, .reply-text');
        for (const el of answerEls) {
            const text = el.textContent.trim();
            if (text && text.length > 10) {
                answers.push(text.substring(0, 300));
            }
        }
        return {title, description, answers};
    }""")
    return QuestionContext(
        title=result.get("title", ""),
        description=result.get("description", ""),
        existing_answers=result.get("answers", []),
        url=question_url,
    )


# ---------------------------------------------------------------------------
# LLM 调用
# ---------------------------------------------------------------------------

def _get_openai_client():
    """创建 OpenAI 兼容客户端。"""
    from openai import OpenAI

    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY 未设置。请设置环境变量后重试，"
            "例如：$env:OPENAI_API_KEY='sk-xxx'"
        )

    base_url = os.getenv("OPENAI_BASE_URL", "").strip() or None
    model = os.getenv("OPENAI_MODEL", "").strip() or "gpt-4o-mini"

    client = OpenAI(api_key=api_key, base_url=base_url)
    return client, model


def _call_llm(client, model: str, system: str, user: str) -> tuple[str, int]:
    """同步调用 LLM，返回 (response_text, total_tokens)。"""
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        temperature=0.7,
        max_tokens=1024,
    )
    text = resp.choices[0].message.content or ""
    tokens = resp.usage.total_tokens if resp.usage else 0
    return text.strip(), tokens


def generate_answer(ctx: QuestionContext) -> OptimizedAnswer:
    """根据问题上下文，从头生成回答。"""
    client, model = _get_openai_client()
    user_prompt = f"请回答以下百度知道问题：\n\n{ctx.to_summary()}"
    content, tokens = _call_llm(client, model, _SYSTEM_PROMPT, user_prompt)

    # 审核生成的回答
    review_result = _review_answer(client, model, ctx, content)

    return OptimizedAnswer(
        content=content,
        review_result=review_result,
        model=model,
        tokens_used=tokens,
    )


def optimize_answer(ctx: QuestionContext, draft: str) -> OptimizedAnswer:
    """根据问题上下文，优化已有草稿回答。"""
    client, model = _get_openai_client()
    user_prompt = (
        f"问题上下文：\n{ctx.to_summary()}\n\n"
        f"基础草稿：\n{draft}\n\n"
        f"请优化上述草稿，使其成为更高质量的百度知道回答。"
    )
    content, tokens = _call_llm(client, model, _OPTIMIZE_PROMPT, user_prompt)

    # 审核优化后的回答
    review_result = _review_answer(client, model, ctx, content)

    return OptimizedAnswer(
        content=content,
        review_result=review_result,
        model=model,
        tokens_used=tokens,
    )


def _review_answer(client, model: str, ctx: QuestionContext, answer: str) -> str:
    """对回答进行内容审核。"""
    user_prompt = (
        f"问题：{ctx.title}\n\n"
        f"已有回答摘要：{'; '.join(a[:80] for a in ctx.existing_answers[:3])}\n\n"
        f"拟提交回答：\n{answer}"
    )
    result, _ = _call_llm(client, model, _REVIEW_PROMPT, user_prompt)
    return result.strip()


# ---------------------------------------------------------------------------
# HITL 审核（终端交互）
# ---------------------------------------------------------------------------

def hitl_review(answer: OptimizedAnswer) -> tuple[str, bool]:
    """人机交互审核：展示生成内容，等待用户确认/修改/拒绝。

    返回 (final_content, approved):
      - approved=True: 使用 final_content 提交
      - approved=False: 用户拒绝提交
    """
    print("\n" + "=" * 60)
    print("[AI 回答优化] 生成内容如下：")
    print("-" * 60)
    print(answer.content)
    print("-" * 60)
    print(f"[审核结果] {answer.review_result}")
    print(f"[模型] {answer.model}  [Token] {answer.tokens_used}")
    print("=" * 60)

    while True:
        print("\n请选择操作：")
        print("  1 = 确认提交（使用此回答）")
        print("  2 = 手动编辑后提交")
        print("  3 = 重新生成")
        print("  0 = 取消发布")
        choice = input(">>> 请输入选项 (1/2/3/0): ").strip()

        if choice == "1":
            return answer.content, True
        elif choice == "2":
            print("请输入修改后的回答（输入空行结束，输入 __CANCEL__ 取消）：")
            lines = []
            while True:
                line = input()
                if line == "__CANCEL__":
                    return "", False
                if line == "" and lines:
                    break
                lines.append(line)
            edited = "\n".join(lines).strip()
            if edited:
                return edited, True
            print("内容为空，请重新选择。")
        elif choice == "3":
            return answer.content, False  # 返回 False 触发重新生成
        elif choice == "0":
            print("用户取消发布。")
            return "", False
        else:
            print("无效选项，请重新输入。")


# ---------------------------------------------------------------------------
# 完整优化流程
# ---------------------------------------------------------------------------

def run_optimize_flow(
    ctx: QuestionContext,
    draft: Optional[str] = None,
    *,
    max_retries: int = 3,
    auto_approve: bool = False,
) -> tuple[str, bool]:
    """完整的优化+审核流程。

    Args:
        ctx: 问题上下文
        draft: 已有草稿（None 表示从头生成）
        max_retries: 重新生成最大次数
        auto_approve: True 时跳过 HITL 终端交互，直接采用生成内容（用于自动化测试）

    Returns:
        (final_content, approved)
    """
    for attempt in range(1, max_retries + 1):
        print(f"\n[AI 优化] 第 {attempt} 次生成{'（基于草稿优化）' if draft else '（从头生成）'}...", flush=True)

        try:
            if draft:
                answer = optimize_answer(ctx, draft)
            else:
                answer = generate_answer(ctx)
        except ValueError as exc:
            print(f"[AI 优化] 配置错误：{exc}", flush=True)
            return "", False
        except Exception as exc:
            print(f"[AI 优化] LLM 调用失败：{exc}", flush=True)
            if attempt < max_retries:
                print(f"[AI 优化] 将重试（{attempt}/{max_retries}）...", flush=True)
                continue
            return "", False

        if auto_approve:
            # 自动模式：仅打印结果不进入交互
            print("\n" + "=" * 60, flush=True)
            print("[AI 回答优化] 自动模式，跳过人工审核", flush=True)
            print("-" * 60, flush=True)
            print(answer.content, flush=True)
            print("-" * 60, flush=True)
            print(f"[审核结果] {answer.review_result}", flush=True)
            print(f"[模型] {answer.model}  [Token] {answer.tokens_used}", flush=True)
            print("=" * 60, flush=True)
            # 若审核 FAIL，自动模式仍采用但记录警告
            if not answer.review_result.startswith("PASS"):
                print(f"[警告] 自动模式采纳了未通过审核的回答：{answer.review_result}", flush=True)
            return answer.content, True

        content, approved = hitl_review(answer)
        if approved:
            return content, True
        if content == "" and not approved:
            # 用户选了取消
            return "", False
        # content 非空但 approved=False → 用户选了重新生成
        draft = None  # 重新生成时不再基于草稿

    print(f"[AI 优化] 已达最大重试次数（{max_retries}），取消发布。", flush=True)
    return "", False
