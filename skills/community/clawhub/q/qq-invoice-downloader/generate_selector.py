#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动 Selector 生成工具
使用 MiniMax LLM 根据 HTML 结构推断最佳 CSS selector
"""

import os
import json
import sys
from typing import List, Optional, Dict

# MiniMax API 配置
MINIMAX_API_KEY = os.environ.get("MINIMAX_API_KEY", "")
MINIMAX_BASE_URL = "https://api.minimax.io/v1/text/chatcompletion_pro"


def generate_selectors_with_llm(
    platform_name: str,
    html_content: str = "",
    page_description: str = "",
    invoice_type: str = "tax_platform"
) -> List[Dict[str, str]]:
    """
    使用 LLM 生成推荐的 CSS selector

    Args:
        platform_name: 平台名称
        html_content: 页面 HTML 片段（可选）
        page_description: 页面描述（当没有 HTML 时使用）
        invoice_type: 发票类型

    Returns:
        推荐的选择器列表，每项包含 selector 和 reason
    """
    if not MINIMAX_API_KEY:
        print("警告: MINIMAX_API_KEY 环境变量未设置", file=sys.stderr)
        return _fallback_selectors(platform_name, invoice_type)

    prompt = _build_prompt(platform_name, html_content, page_description, invoice_type)

    try:
        import requests
        headers = {
            "Authorization": f"Bearer {MINIMAX_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "MiniMax-Text-01",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,
            "max_tokens": 1024
        }
        response = requests.post(
            MINIMAX_BASE_URL,
            headers=headers,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        result = response.json()
        content = result.get("choices", [{}])[0].get("message", {}).get("content", "")

        return _parse_llm_response(content)

    except Exception as e:
        print(f"LLM 调用失败: {e}", file=sys.stderr)
        return _fallback_selectors(platform_name, invoice_type)


def _build_prompt(
    platform_name: str,
    html_content: str,
    page_description: str,
    invoice_type: str
) -> str:
    """构建 LLM prompt"""
    prompt_parts = [
        f"你是一个 Playwright 自动化专家。请为以下平台生成发票下载按钮的 CSS selector。",
        f"",
        f"平台名称: {platform_name}",
        f"发票类型: {invoice_type}",
        f"",
    ]

    if html_content:
        prompt_parts.extend([
            "页面 HTML 片段:",
            "```html",
            html_content[:3000],  # 限制长度
            "```",
            "",
        ])

    if page_description:
        prompt_parts.extend([
            "页面描述:",
            page_description,
            "",
        ])

    prompt_parts.extend([
        "请生成 3-5 个 Playwright 兼容的 CSS selector，按优先级排序。",
        "必须使用 Playwright 支持的 selector 语法，包括:",
        "  - button:has-text('文本') - 包含特定文本的按钮",
        "  - a:has-text('文本') - 包含特定文本的链接",
        "  - [class*='关键字'] - class 包含关键字的元素",
        "  - [id*='关键字'] - id 包含关键字的元素",
        "  - [data-action='值'] - data 属性选择器",
        "",
        "请以 JSON 数组格式输出，每项包含:",
        "  - selector: CSS selector 字符串",
        "  - reason: 选择该 selector 的原因",
        "  - priority: 优先级 (1=最高)",
        "",
        '输出格式: [{"selector": "...", "reason": "...", "priority": 1}, ...]',
    ])

    return "\n".join(prompt_parts)


def _parse_llm_response(content: str) -> List[Dict[str, str]]:
    """解析 LLM 响应，提取 selector 列表"""
    try:
        # 尝试提取 JSON 数组
        content = content.strip()
        # 去掉可能的前缀（如 ```json ... ```）
        if "```" in content:
            lines = content.split("\n")
            json_lines = []
            in_json = False
            for line in lines:
                if line.strip().startswith("```"):
                    in_json = not in_json
                    continue
                if in_json:
                    json_lines.append(line)
            content = "\n".join(json_lines)

        selectors = json.loads(content)
        if isinstance(selectors, list):
            return selectors
        return []
    except json.JSONDecodeError:
        print("警告: LLM 响应 JSON 解析失败", file=sys.stderr)
        return []


def _fallback_selectors(platform_name: str, invoice_type: str) -> List[Dict[str, str]]:
    """当 LLM 不可用时的备选选择器"""
    base_selectors = [
        {"selector": f'a:has-text("电子发票")', "reason": "最常见的电子发票链接文字", "priority": 1},
        {"selector": f'button:has-text("下载")', "reason": "通用下载按钮", "priority": 2},
        {"selector": f'a:has-text("下载")', "reason": "通用下载链接", "priority": 3},
        {"selector": '[class*="invoice"]', "reason": "class 包含 invoice 关键字", "priority": 4},
        {"selector": '[id*="download"]', "reason": "id 包含 download 关键字", "priority": 5},
    ]
    return base_selectors


def interactive_generate():
    """交互式生成 selector"""
    print("=== 自动 Selector 生成工具 ===")
    print("按 Ctrl+C 退出\n")

    platform_name = input("请输入平台名称: ").strip()
    if not platform_name:
        print("平台名称不能为空")
        return

    invoice_type = input("发票类型 [tax_platform]: ").strip() or "tax_platform"
    page_desc = input("页面描述（可选，直接回车跳过）: ").strip()

    has_html = input("是否有 HTML 内容? [y/N]: ").strip().lower() == "y"
    html_content = ""
    if has_html:
        print("请输入 HTML 内容（输入 EOF 或空行结束）:")
        lines = []
        while True:
            try:
                line = input()
                if not line:
                    break
                lines.append(line)
            except EOFError:
                break
        html_content = "\n".join(lines)

    print("\n正在调用 MiniMax LLM 生成 selector...\n")

    results = generate_selectors_with_llm(
        platform_name=platform_name,
        html_content=html_content,
        page_description=page_desc,
        invoice_type=invoice_type
    )

    if results:
        print(f"为 {platform_name} 生成了 {len(results)} 个 selector:\n")
        for i, item in enumerate(results, 1):
            print(f"{i}. {item.get('selector', 'N/A')}")
            print(f"   原因: {item.get('reason', 'N/A')}")
            print(f"   优先级: {item.get('priority', 'N/A')}")
            print()
    else:
        print("未能生成 selector，请检查 MINIMAX_API_KEY 环境变量")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # 命令行模式: python generate_selector.py "平台名称" ["HTML内容"]
        platform = sys.argv[1]
        html = sys.argv[2] if len(sys.argv) > 2 else ""
        results = generate_selectors_with_llm(platform, html_content=html)
        for item in results:
            print(f"{item.get('selector', '')}")
    else:
        interactive_generate()
