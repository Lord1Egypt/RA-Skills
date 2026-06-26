#!/usr/bin/env python3
"""
文本风格分析器 (LLM 版本) - 通过 DashScope API 分析写作风格特征并生成 Voice Profile 配置文件

Usage:
    python3 analyze_style_llm.py --input text.txt --output style.yml
    python3 analyze_style_llm.py --input text.txt --output style.yml --model qwen3.6-plus
"""

import argparse
import json
import os
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import requests
import yaml
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.text import Text

console = Console()


@dataclass
class VoiceProfile:
    """语音配置文件"""

    labels: list[str]
    pace: str
    tone: str
    sentiment: float


@dataclass
class StyleAnalysisResult:
    """风格分析结果"""

    voice_profile: VoiceProfile
    analysis_notes: str


class StyleAnalyzerLLM:
    """通过 LLM 分析文本风格"""

    def __init__(self, model: str = "qwen3.6-plus"):
        self.model = model
        self.api_key = os.getenv("DASHSCOPE_API_KEY")
        if not self.api_key:
            raise ValueError("环境变量 DASHSCOPE_API_KEY 未设置")

    def analyze(self, text: str) -> StyleAnalysisResult:
        """通过 LLM 分析文本风格"""
        prompt = self._build_prompt(text)

        try:
            response = self._call_dashscope_api(prompt)
            return self._parse_response(response)
        except requests.exceptions.RequestException as e:
            console.print(f"[red]❌ API 调用失败：{e}[/red]")
            raise
        except json.JSONDecodeError as e:
            console.print(f"[red]❌ 响应解析失败：{e}[/red]")
            raise

    def _build_prompt(self, text: str) -> str:
        """构建 API 调用提示词"""
        return f"""请分析以下文本的写作风格特征，并以 JSON 格式返回分析结果。

文本内容：
{text[:8000]}

请分析以下维度：
1. 风格标签：提取 5-8 个关键风格特征词（如：简洁、华丽、正式、幽默、感性等）
2. 语速：根据平均句长判断（缓慢/适中/快速）
3. 语气：根据用词风格判断（正式/中性/随意）
4. 情感倾向：-1（负面）到 1（正面）之间的数值

返回格式要求：
{{"voice_profile": {{"labels": ["标签1", "标签2"], "pace": "apidity", "tone": "tone", "sentiment": 0.0}}}}

附加分析说明：
请用中文简要说明分析依据（2-3 句话）"""

    def _call_dashscope_api(self, prompt: str) -> dict[str, Any]:
        """调用 DashScope API"""
        url = "https://coding.dashscope.aliyuncs.com/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3,
            "response_format": {"type": "json_object"},
        }

        with Progress(
            SpinnerColumn(),
            TextColumn("[bold cyan]正在调用 LLM 分析风格...[/bold cyan]"),
            console=console,
            transient=True,
        ) as progress:
            progress.add_task("analyzing", total=None)
            response = requests.post(url, headers=headers, json=payload, timeout=60)

        response.raise_for_status()
        return response.json()

    def _parse_response(self, response: dict[str, Any]) -> StyleAnalysisResult:
        """解析 API 响应"""
        try:
            output = response["choices"][0]["message"]["content"]
        except (KeyError, TypeError) as e:
            console.print(f"[red]❌ 响应格式错误：{e}[/red]")
            console.print(
                f"响应内容：{json.dumps(response, indent=2, ensure_ascii=False)}"
            )
            raise

        try:
            json_start = output.find("{")
            json_end = output.rfind("}") + 1

            if json_start == -1 or json_end == 0:
                raise ValueError("未找到有效的 JSON 对象")

            json_str = output[json_start:json_end]
            data = json.loads(json_str)

            voice_profile_data = data.get("voice_profile", {})
            analysis_notes = data.get("analysis_notes", "")

            voice_profile = VoiceProfile(
                labels=voice_profile_data.get("labels", []),
                pace=voice_profile_data.get("pace", "适中"),
                tone=voice_profile_data.get("tone", "中性"),
                sentiment=float(voice_profile_data.get("sentiment", 0.0)),
            )

            return StyleAnalysisResult(
                voice_profile=voice_profile,
                analysis_notes=analysis_notes,
            )
        except json.JSONDecodeError as e:
            console.print(f"[yellow]⚠️  JSON 解析失败，尝试原始响应：{e}[/yellow]")
            return StyleAnalysisResult(
                voice_profile=VoiceProfile(
                    labels=["未知"],
                    pace="适中",
                    tone="中性",
                    sentiment=0.0,
                ),
                analysis_notes=f"原始响应：{output}",
            )


def load_text(filepath: str) -> str:
    """加载文本文件"""
    path = Path(filepath)

    if not path.exists():
        raise FileNotFoundError(f"文件不存在：{filepath}")

    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        with open(path, "r", encoding="gbk") as f:
            return f.read()


def save_yaml(result: StyleAnalysisResult, filepath: str) -> None:
    """保存为 YAML 配置文件"""
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)

    data = {
        "voice_profile": asdict(result.voice_profile),
        "analysis_notes": result.analysis_notes,
    }

    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False)


def print_result(result: StyleAnalysisResult) -> None:
    """美化输出结果"""
    console.print("\n")
    console.print(
        Panel.fit(
            "[bold cyan]LLM 风格分析完成！[/bold cyan]",
            border_style="cyan",
            padding=(1, 2),
        )
    )

    table = Table(title="风格分析报告", show_header=True, header_style="bold magenta")
    table.add_column("特征", style="cyan")
    table.add_column("详情", style="green")

    vp = result.voice_profile
    voice_info = Text()
    voice_info.append(f"风格标签：{', '.join(vp.labels)}\n")
    voice_info.append(f"语速：{vp.pace}\n")
    voice_info.append(f"语气：{vp.tone}\n")
    voice_info.append(f"情感倾向：{vp.sentiment:+.3f}")

    table.add_row("Voice Profile", voice_info)

    if result.analysis_notes:
        table.add_row("分析说明", Text(result.analysis_notes, style="italic"))

    console.print(table)


def create_parser() -> argparse.ArgumentParser:
    """创建命令行参数解析器"""
    parser = argparse.ArgumentParser(
        prog="analyze_style_llm",
        description="通过 LLM 分析文本的写作风格特征，生成 Voice Profile 配置文件",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s --input story.txt --output style.yml
  %(prog)s --input story.txt --output output/style.yml --model qwen3.6-plus
        """,
    )

    parser.add_argument(
        "--input",
        "-i",
        type=str,
        required=True,
        help="输入文本文件路径",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        required=True,
        help="输出 YAML 配置文件路径",
    )
    parser.add_argument(
        "--model",
        "-m",
        type=str,
        default="qwen3.6-plus",
        help="使用的 DashScope 模型（默认：qwen3.6-plus）",
    )

    return parser


def main() -> int:
    """主函数"""
    parser = create_parser()
    args = parser.parse_args()

    console.print("[bold cyan]文本风格分析器 (LLM 版本)[/bold cyan]")
    console.print(f"输入文件：[yellow]{args.input}[/yellow]")
    console.print(f"输出文件：[yellow]{args.output}[/yellow]")
    console.print(f"使用的模型：[yellow]{args.model}[/yellow]")
    console.print()

    text = load_text(args.input)
    console.print(f"文本长度：[yellow]{len(text)}[/yellow] 字符")
    console.print()

    try:
        analyzer = StyleAnalyzerLLM(model=args.model)
        result = analyzer.analyze(text)

        save_yaml(result, args.output)
        console.print(f"\n[green]✓ 配置文件已保存至：{args.output}[/green]")

        print_result(result)

        return 0
    except FileNotFoundError as e:
        console.print(f"[red]❌ {e}[/red]")
        return 1
    except ValueError as e:
        console.print(f"[red]❌ {e}[/red]")
        return 1
    except Exception as e:
        console.print(f"[red]❌ 未预期的错误：{e}[/red]")
        return 1


if __name__ == "__main__":
    sys.exit(main())
