#!/usr/bin/env python3
"""
智能提示构建器 (LLM 版本) - 通过 LLM 构建高质量写作提示词

Usage:
    python3 build_prompt_llm.py --scene-type description --output prompt.json
    python3 build_prompt_llm.py --scene-type dialogue --style-file style.yml --context '{"scene": "雨夜"}' --output prompt.json
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

import requests
import yaml
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

console = Console()

# 默认模型
DEFAULT_MODEL = "qwen3.6-plus"


def load_style_file(path: str) -> dict[str, Any]:
    """加载风格配置文件"""
    style_path = Path(path)
    if not style_path.exists():
        console.print(f"[yellow]⚠️ 风格文件不存在：{path}，使用默认配置[/yellow]")
        return {}
    with open(style_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def parse_context(context_str: str) -> dict[str, Any]:
    """解析上下文 JSON"""
    if not context_str:
        return {}
    try:
        return json.loads(context_str)
    except json.JSONDecodeError as e:
        console.print(f"[red]❌ 上下文 JSON 解析失败：{e}[/red]")
        sys.exit(1)


def build_prompt(
    scene_type: str,
    style: dict[str, Any],
    context: dict[str, Any],
    model: str = DEFAULT_MODEL,
) -> dict[str, Any]:
    """通过 LLM 构建写作提示词"""
    api_key = os.environ.get("DASHSCOPE_API_KEY")
    if not api_key:
        console.print("[red]❌ 环境变量 DASHSCOPE_API_KEY 未设置[/red]")
        sys.exit(1)

    # 构建提示词
    prompt = _build_llm_prompt(scene_type, style, context)

    # 调用 API
    url = "https://coding.dashscope.aliyuncs.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "你是一名专业的提示词工程师，擅长为小说写作任务构建高质量的 LLM 提示词。必须输出标准 JSON 格式。",
            },
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.3,
        "response_format": {"type": "json_object"},
    }

    with Progress(
        SpinnerColumn(),
        TextColumn("[bold cyan]正在调用 LLM 构建提示词...[/bold cyan]"),
        console=console,
        transient=True,
    ) as progress:
        progress.add_task("building", total=None)
        response = requests.post(url, headers=headers, json=payload, timeout=60)

    response.raise_for_status()
    data = response.json()
    content = data["choices"][0]["message"]["content"]
    return json.loads(content)


def _build_llm_prompt(
    scene_type: str,
    style: dict[str, Any],
    context: dict[str, Any],
) -> str:
    """构建给 LLM 的提示词"""
    scene_desc = {
        "description": "环境描写",
        "dialogue": "人物对话",
        "action": "动作场景",
        "emotion": "心理描写",
    }
    
    style_info = json.dumps(style, ensure_ascii=False, indent=2) if style else "无"
    context_info = json.dumps(context, ensure_ascii=False, indent=2) if context else "无"

    return f"""请为以下小说写作任务构建高质量的 LLM 提示词。

## 任务信息
- 场景类型：{scene_type}（{scene_desc.get(scene_type, scene_type)}）
- 风格配置：{style_info}
- 上下文：{context_info}

## 输出要求
请输出 JSON 格式，包含以下字段：
- "system": 系统提示（定义 LLM 角色和专长，1-2 句话）
- "user": 用户提示（具体写作需求，结合风格和上下文）
- "constraints": 约束条件列表（3-5 条写作规范）

## 注意事项
- 系统提示要简洁有力，明确 LLM 的角色
- 用户提示要充分利用风格配置和上下文信息
- 约束条件要具体可操作，避免空泛要求
- 所有文本用中文输出
"""


def print_result(prompt_data: dict[str, Any]) -> None:
    """美化输出结果"""
    console.print("\n")
    console.print(
        Panel.fit(
            "[bold cyan]提示词构建完成！[/bold cyan]",
            border_style="cyan",
            padding=(1, 2),
        )
    )

    table = Table(title="提示词内容", show_header=True, header_style="bold magenta")
    table.add_column("类型", style="cyan")
    table.add_column("内容", style="green", overflow="fold")

    table.add_row("系统提示", prompt_data.get("system", "")[:200])
    table.add_row("用户提示", prompt_data.get("user", "")[:300])
    
    constraints = prompt_data.get("constraints", [])
    table.add_row("约束条件", "\n".join(f"• {c}" for c in constraints[:5]))

    console.print(table)


def main() -> int:
    """主函数"""
    parser = argparse.ArgumentParser(
        description="智能提示构建器 (LLM 版本) - 通过 LLM 构建高质量写作提示词"
    )
    parser.add_argument(
        "--scene-type",
        required=True,
        choices=["description", "dialogue", "action", "emotion"],
        help="场景类型：description/dialogue/action/emotion",
    )
    parser.add_argument(
        "--style-file",
        help="风格配置文件路径（YAML 格式）",
    )
    parser.add_argument(
        "--context",
        help="上下文信息（JSON 格式）",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"使用的模型（默认：{DEFAULT_MODEL}）",
    )
    parser.add_argument(
        "--output",
        help="输出文件路径（JSON 格式）",
    )
    args = parser.parse_args()

    console.print("[bold]🔧 智能提示构建器 (LLM 版本)[/bold]")
    console.print(f"场景类型：[yellow]{args.scene_type}[/yellow]")
    console.print(f"使用模型：[yellow]{args.model}[/yellow]")

    # 加载配置
    style = load_style_file(args.style_file) if args.style_file else {}
    context = parse_context(args.context)

    # 构建提示词
    prompt_data = build_prompt(args.scene_type, style, context, args.model)

    # 输出
    print_result(prompt_data)

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(prompt_data, f, ensure_ascii=False, indent=2)
        console.print(f"\n[green]✓ 提示词已保存至：{args.output}[/green]")

    return 0


if __name__ == "__main__":
    sys.exit(main())
