#!/usr/bin/env python3
"""
智能提示构建器 - Smart Prompt Builder

根据语料库检索结果生成优化的写作提示，支持多种场景和上下文注入。
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


class PromptBuilder:
    """智能提示构建器核心类"""

    SCENE_TEMPLATES = {
        "description": {
            "system": "你是一名专业的环境描写大师，擅长通过细腻的笔触营造氛围。",
            "user_prefix": "请根据以下描述需求生成一段富有画面感的环境描写：",
            "constraints": [
                "使用五感描写法（视觉、听觉、嗅觉、味觉、触觉）",
                "包含至少3个具体的细节描写",
                "使用比喻或拟人手法增强表现力",
                "保持描写节奏的层次感",
            ],
        },
        "dialogue": {
            "system": "你是一位擅长人物对话的作家，能通过对话展现角色性格。",
            "user_prefix": "请根据以下对话需求生成自然流畅的人物对话：",
            "constraints": [
                "对话需符合角色身份和性格特征",
                "每段对话不超过3轮",
                "包含非语言动作描述（动作、表情）",
                "使用口语化表达，避免书面腔",
            ],
        },
        "action": {
            "system": "你擅长描写动作场景，能通过动态描写展现紧张感。",
            "user_prefix": "请根据以下动作需求生成富有张力的动作描写：",
            "constraints": [
                "使用短句增强节奏感",
                "动作描写需连贯有序",
                "包含细节（手部动作、表情变化等）",
                "适当使用动词强化表现力",
            ],
        },
        "emotion": {
            "system": "你善于刻画人物内心世界，能将抽象情感具象化。",
            "user_prefix": "请根据以下情感需求生成细腻的心理描写：",
            "constraints": [
                "将抽象情感转化为具体意象",
                "描写身体反应（心跳、温度、手势等）",
                "避免直接陈述情感词语",
                "展现情感的层次变化",
            ],
        },
    }

    def __init__(self, style_file: Optional[str] = None):
        """初始化提示构建器

        Args:
            style_file: Voice Profile配置文件路径
        """
        self.style_config: Dict[str, Any] = {}
        if style_file:
            self._load_style_config(style_file)

    def _load_style_config(self, file_path: str) -> None:
        """加载Voice Profile配置

        Args:
            file_path: YAML配置文件路径

        Raises:
            FileNotFoundError: 当配置文件不存在时
            yaml.YAMLError: 当YAML格式错误时
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"配置文件不存在: {file_path}")

        try:
            with open(path, "r", encoding="utf-8") as f:
                self.style_config = yaml.safe_load(f) or {}
            console.print(f"[green]✓ 已加载Voice Profile: {file_path}[/green]")
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"YAML格式错误: {e}")

    def _inject_style(self, prompt: str) -> str:
        """注入Voice Profile风格配置

        Args:
            prompt: 原始提示词

        Returns:
            注入风格后的提示词
        """
        if not self.style_config:
            return prompt

        style_parts = []

        # 注入风格标签
        if "voice_tags" in self.style_config:
            tags = ", ".join(self.style_config["voice_tags"])
            style_parts.append(f"风格标签: {tags}")

        # 注入语速
        if "speed" in self.style_config:
            style_parts.append(f"语速: {self.style_config['speed']}")

        # 注入语气
        if "tone" in self.style_config:
            style_parts.append(f"语气: {self.style_config['tone']}")

        # 注入情感倾向
        if "emotional_predisposition" in self.style_config:
            style_parts.append(
                f"情感倾向: {self.style_config['emotional_predisposition']}"
            )

        if style_parts:
            instruction = "\n[Voice Profile]\n" + "\n".join(style_parts)
            return f"{prompt}\n\n{instruction}"

        return prompt

    def _build_context_section(self, context: Dict[str, Any]) -> str:
        """构建上下文注入部分

        Args:
            context: 上下文字典，包含前文摘要、角色状态、当前场景等

        Returns:
            格式化后的上下文字符串
        """
        sections = []

        if "summary" in context:
            sections.append(f"[前文摘要]\n{context['summary']}")

        if "characters" in context:
            char_info = "\n".join(
                f"- {name}: {status}" for name, status in context["characters"].items()
            )
            sections.append(f"[角色状态]\n{char_info}")

        if "scene" in context:
            sections.append(f"[当前场景]\n{context['scene']}")

        if "previous_output" in context:
            sections.append(f"[前文输出]\n{context['previous_output']}")

        return "\n\n".join(sections) if sections else "无上下文信息"

    def _format_corpus_results(self, results: List[Dict[str, Any]]) -> str:
        """格式化语料库检索结果

        Args:
            results: 语料库检索结果列表

        Returns:
            格式化后的语料文本
        """
        if not results:
            return "无检索结果"

        formatted = []
        for i, result in enumerate(results, 1):
            _ = result.get("title", f"结果{i}")
            content = result.get("content", "")
            score = result.get("relevance_score", 0)

            entry = f"【结果{i}】（相关度: {score:.2f}）\n{content}"
            formatted.append(entry)

        return "\n\n".join(formatted)

    def build_prompt(
        self,
        scene_type: str,
        context: Optional[Dict[str, Any]] = None,
        corpus_results: Optional[List[Dict[str, Any]]] = None,
        custom_constraints: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """构建完整提示词

        Args:
            scene_type: 场景类型（description/dialogue/action/emotion）
            context: 上下文信息字典
            corpus_results: 语料库检索结果
            custom_constraints: 自定义约束条件

        Returns:
            包含系统提示、用户提示和约束条件的字典
        """
        # 验证场景类型
        if scene_type not in self.SCENE_TEMPLATES:
            available = ", ".join(self.SCENE_TEMPLATES.keys())
            raise ValueError(f"不支持的场景类型: {scene_type}。可用类型: {available}")

        # 获取基础模板
        template = self.SCENE_TEMPLATES[scene_type]
        system_prompt = template["system"]

        # 构建用户提示
        user_base = template["user_prefix"]

        # 添加上下文注入
        if context:
            context_section = self._build_context_section(context)
            user_base = f"{user_base}\n\n{context_section}"

        # 添加语料库结果
        if corpus_results:
            corpus_section = self._format_corpus_results(corpus_results)
            user_base = f"{user_base}\n\n[语料库参考]\n{corpus_section}"

        # 构建约束条件
        constraints = list(template["constraints"])
        if custom_constraints:
            constraints.extend(custom_constraints)

        # 组合最终用户提示
        user_prompt = self._inject_style(user_base)

        return {
            "system": system_prompt,
            "user": user_prompt,
            "constraints": constraints,
            "metadata": {
                "scene_type": scene_type,
                "has_context": bool(context),
                "corpus_results_count": len(corpus_results or []),
            },
        }

    def format_output(self, prompt_data: Dict[str, Any]) -> str:
        """格式化输出为富文本

        Args:
            prompt_data: 提示词数据字典

        Returns:
            格式化后的字符串
        """
        panels = []

        # 系统提示
        system_panel = Panel(
            prompt_data["system"], title="[bold blue]系统提示", border_style="blue"
        )
        panels.append(system_panel)

        # 用户提示
        user_panel = Panel(
            prompt_data["user"], title="[bold green]用户提示", border_style="green"
        )
        panels.append(user_panel)

        # 约束条件
        constraints_text = "\n".join(
            f"[bold]\\[✓][/bold] {c}" for c in prompt_data["constraints"]
        )
        constraints_panel = Panel(
            constraints_text, title="[bold yellow]约束条件", border_style="yellow"
        )
        panels.append(constraints_panel)

        # 元数据表格
        meta_table = Table(show_header=False, box=None)
        meta_table.add_row("场景类型", prompt_data["metadata"]["scene_type"])
        meta_table.add_row(
            "语料结果数", str(prompt_data["metadata"]["corpus_results_count"])
        )
        meta_table.add_row(
            "包含上下文", "是" if prompt_data["metadata"]["has_context"] else "否"
        )

        panels.append(meta_table)

        return self._render_panels(panels)

    def _render_panels(self, panels: list) -> str:
        """使用临时控制台渲染面板

        Args:
            panels: 面板列表

        Returns:
            渲染后的字符串
        """
        from io import StringIO

        output_buffer = StringIO()
        temp_console = Console(file=output_buffer, force_terminal=True)

        for panel in panels:
            temp_console.print(panel)

        return output_buffer.getvalue()

    def format_output_plain(self, prompt_data: Dict[str, Any]) -> str:
        """格式化输出为纯文本（无ANSI代码）

        Args:
            prompt_data: 提示词数据字典

        Returns:
            格式化后的纯文本字符串
        """
        lines = []
        separator = "=" * 60

        # 系统提示
        lines.append(f"{separator}")
        lines.append("【系统提示】")
        lines.append(f"{separator}")
        lines.append(prompt_data["system"])
        lines.append("")

        # 用户提示
        lines.append(f"{separator}")
        lines.append("【用户提示】")
        lines.append(f"{separator}")
        lines.append(prompt_data["user"])
        lines.append("")

        # 约束条件
        lines.append(f"{separator}")
        lines.append("【约束条件】")
        lines.append(f"{separator}")
        for c in prompt_data["constraints"]:
            lines.append(f"• {c}")
        lines.append("")

        # 元数据
        lines.append(f"{separator}")
        lines.append("【元数据】")
        lines.append(f"{separator}")
        lines.append(f"场景类型: {prompt_data['metadata']['scene_type']}")
        lines.append(f"语料结果数: {prompt_data['metadata']['corpus_results_count']}")
        lines.append(
            f"包含上下文: {'是' if prompt_data['metadata']['has_context'] else '否'}"
        )

        return "\n".join(lines)


def parse_yaml_style(file_path: str) -> Dict[str, Any]:
    """解析YAML风格配置文件

    Args:
        file_path: YAML文件路径

    Returns:
        配置字典
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except FileNotFoundError:
        console.print(f"[red]错误: 配置文件不存在 '{file_path}'[/red]")
        sys.exit(1)
    except yaml.YAMLError as e:
        console.print(f"[red]错误: YAML格式无效 - {e}[/red]")
        sys.exit(1)


def parse_corpus_results(results_str: Optional[str]) -> List[Dict[str, Any]]:
    """解析语料库结果（JSON格式字符串）

    Args:
        results_str: JSON格式的检索结果字符串

    Returns:
        检索结果列表
    """
    import json

    if not results_str:
        return []

    try:
        return json.loads(results_str)
    except json.JSONDecodeError as e:
        console.print(f"[red]错误: 无效的JSON格式 - {e}[/red]")
        sys.exit(1)


def main():
    """主入口函数"""
    parser = argparse.ArgumentParser(
        description="智能提示构建器 - 根据语料库检索结果生成优化的写作提示",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 基本用法
  python build_prompt.py --scene-type description --context '{"scene": "森林"}'
  
  # 使用Voice Profile和语料库结果
  python build_prompt.py --scene-type dialogue \\
    --style-file style.yml \\
    --corpus-results '[{"title": "对话范例", "content": "...", "relevance_score": 0.95}]'
  
  # 输出到文件
  python build_prompt.py --scene-type action --output prompt.txt
        """,
    )

    parser.add_argument(
        "--scene-type",
        required=True,
        choices=["description", "dialogue", "action", "emotion"],
        help="场景类型: description, dialogue, action, emotion",
    )

    parser.add_argument(
        "--context", help="上下文信息（JSON格式）", type=str, default="{}"
    )

    parser.add_argument(
        "--style-file",
        help="Voice Profile配置文件路径（YAML格式）",
        type=str,
        default=None,
    )

    parser.add_argument(
        "--corpus-results", help="语料库检索结果（JSON格式）", type=str, default=None
    )

    parser.add_argument("--output", help="输出文件路径", type=str, default=None)

    args = parser.parse_args()

    try:
        # 初始化构建器
        builder = PromptBuilder(style_file=args.style_file)

        # 解析上下文
        context = json.loads(args.context) or {}

        # 解析语料库结果
        corpus_results = parse_corpus_results(args.corpus_results)

        # 构建提示
        prompt_data = builder.build_prompt(
            scene_type=args.scene_type, context=context, corpus_results=corpus_results
        )

        # 格式化输出
        output = builder.format_output(prompt_data)

        # 输出到文件或终端
        if args.output:
            markup_safe = builder.format_output_plain(prompt_data)
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(markup_safe)
            console.print(f"[green]✓ 提示词已保存至: {args.output}[/green]")
        else:
            console.print("\n")
            console.print(output)
            console.print("\n")

        sys.exit(0)

    except ValueError as e:
        console.print(f"[red]错误: {e}[/red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]未预期的错误: {e}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main()
