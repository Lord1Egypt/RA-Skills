#!/usr/bin/env python3
"""
模型驱动的页面分析：获取页面 HTML 后调用 LLM 判断当前状态及下一步操作。
无硬编码，由模型根据页面内容动态决策。
"""
import json
import os
import re
import sys
from typing import Any

# 可选：openai 用于调用模型
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

MAX_HTML_CHARS = 60_000  # 截断过长的 HTML

# 脱敏：移除常见 token/csrf 等敏感模式
_TOKEN_PATTERNS = [
    (re.compile(r'([?&])token=[a-zA-Z0-9_-]+', re.I), r'\1token=[REDACTED]'),
    (re.compile(r'token=["\']?[a-zA-Z0-9_-]{8,}["\']?', re.I), 'token="[REDACTED]"'),
    (re.compile(r'access[_\-]?token=["\']?[a-zA-Z0-9_-]+["\']?', re.I), 'access_token="[REDACTED]"'),
    (re.compile(r'cookie=["\']?[a-zA-Z0-9_-]+["\']?', re.I), 'cookie="[REDACTED]"'),
]


def _sanitize_html(html: str) -> str:
    """脱敏：移除 script/style、常见 token 模式，压缩空白。"""
    html = re.sub(r"<script[^>]*>[\s\S]*?</script>", "", html, flags=re.IGNORECASE)
    html = re.sub(r"<style[^>]*>[\s\S]*?</style>", "", html, flags=re.IGNORECASE)
    for pat, repl in _TOKEN_PATTERNS:
        html = pat.sub(repl, html)
    html = re.sub(r"\s+", " ", html).strip()
    return html


def _get_page_summary(page) -> str:
    """获取页面内容摘要：URL + 脱敏后的简化 HTML。"""
    try:
        url = page.url
        html = page.content()
        html = _sanitize_html(html)
        if len(html) > MAX_HTML_CHARS:
            html = html[:MAX_HTML_CHARS] + "\n...[已截断]"
        return f"URL: {url}\n\nHTML(简化):\n{html}"
    except Exception as e:
        return f"获取页面失败：{e}"


# 百炼 API - OpenAI 兼容模式
BAILIAN_BASE_URL = "https://coding.dashscope.aliyuncs.com/v1"
BAILIAN_DEFAULT_MODEL = "qwen3.5-plus"


def _is_local_endpoint(url: str) -> bool:
    """判断是否为本地/自托管端点（无需 API Key）。"""
    if not url:
        return False
    lower = url.lower()
    return "localhost" in lower or "127.0.0.1" in lower


def _call_openai(prompt: str, api_key: str | None, base_url: str | None) -> str | None:
    """调用 OpenAI 兼容 API。支持百炼、Ollama（本地无需 Key）等。"""
    if not OpenAI:
        return None
    url = (
        base_url
        or os.environ.get("XHS_ANALYZER_BASE_URL")
        or os.environ.get("OPENAI_BASE_URL")
        or BAILIAN_BASE_URL
    )
    key = (
        api_key
        or os.environ.get("DASHSCOPE_API_KEY")
        or os.environ.get("OPENAI_API_KEY")
    )
    if not key and not _is_local_endpoint(url):
        return None
    client = OpenAI(api_key=key or "ollama", base_url=url)
    model_name = os.environ.get("XHS_ANALYZER_MODEL") or BAILIAN_DEFAULT_MODEL
    try:
        resp = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
        )
        return (resp.choices[0].message.content or "").strip()
    except Exception as e:
        print(f"LLM 调用失败：{e}", file=sys.stderr)
        return None


ANALYZER_PROMPT = """你正在分析小红书创作服务平台 (creator.xiaohongshu.com) 的页面。

根据下方页面内容，判断：
1. 当前页面状态
2. 下一步应执行的操作

页面内容：
---
{page_content}
---

请**仅**返回一个 JSON 对象，不要其他文字。格式如下：

{{
  "state": "login_required | logged_in_dashboard | note_editor | unknown",
  "next_action": "wait_for_scan | goto_publish | click_new_note | fill_note | upload_images | done | user_action_required",
  "reason": "简短说明判断依据",
  "selector": "可选，当 next_action 为 click_new_note 时的 Playwright 选择器",
  "url": "可选，当 next_action 为 goto_publish 时的目标 URL"
}}

规则：
- state=login_required：页面有扫码登录、重新登录、二维码等，需要用户扫码
- state=logged_in_dashboard：已登录后台，有创作管理、笔记列表等
- state=note_editor：在发布笔记编辑页，可填标题正文、上传图片
- next_action=wait_for_scan：需用户扫码，等待后重新分析
- next_action=goto_publish：跳转到发布笔记页面
- next_action=click_new_note：点击「发布笔记」或「创作」等按钮
- next_action=fill_note：进入编辑页，可填入笔记内容
- next_action=upload_images：需要上传图片
- next_action=done：流程完成
- next_action=user_action_required：需用户手动操作（如点击发布）
"""


def analyze_page(
    page,
    *,
    context: str = "",
    api_key: str | None = None,
    base_url: str | None = None,
) -> dict[str, Any]:
    """
    通过模型分析页面，返回状态与下一步操作。
    若 LLM 不可用，返回保守的 need_login 结果。
    """
    page_content = _get_page_summary(page)
    prompt = ANALYZER_PROMPT.format(page_content=page_content)
    if context:
        prompt = f"上下文：{context}\n\n{prompt}"

    raw = _call_openai(prompt, api_key, base_url)
    if not raw:
        return {
            "state": "unknown",
            "next_action": "user_action_required",
            "reason": "LLM 不可用。可选：1) 配置 DASHSCOPE_API_KEY 或 OPENAI_API_KEY；2) 本地 Ollama：XHS_ANALYZER_BASE_URL=http://localhost:11434/v1（无需 Key）；3) pip install openai",
            "selector": None,
            "url": None,
        }

    # 提取 JSON
    try:
        m = re.search(r"\{[\s\S]*\}", raw)
        if m:
            out = json.loads(m.group())
            return {
                "state": out.get("state", "unknown"),
                "next_action": out.get("next_action", "user_action_required"),
                "reason": out.get("reason", ""),
                "selector": out.get("selector"),
                "url": out.get("url"),
            }
    except json.JSONDecodeError:
        pass
    return {
        "state": "unknown",
        "next_action": "user_action_required",
        "reason": f"模型返回无法解析：{raw[:200]}",
        "selector": None,
        "url": None,
    }
