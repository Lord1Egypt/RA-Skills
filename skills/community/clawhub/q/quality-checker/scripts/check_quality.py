#!/usr/bin/env python3
"""
章节质量检测器
检测 Markdown 格式章节的写作质量并生成详细报告
"""

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

import yaml
from rich.console import Console
from rich.table import Table
from rich.text import Text


@dataclass
class QualityConfig:
    """质量检测配置"""

    target_word_count: int = 1000
    paragraph_max_length: int = 200
    paragraph_min_length: int = 30
    dialogue_min_ratio: float = 0.20
    dialogue_max_ratio: float = 0.60
    punctuation_max_consecutive: int = 1
    repeated_words_threshold: int = 5
    quality_excellent: int = 90
    quality_good: int = 70
    quality_pass: int = 50

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "QualityConfig":
        """从字典创建配置"""
        return cls(
            target_word_count=data.get("target_word_count", 1000),
            paragraph_max_length=data.get("paragraph", {}).get("max_length", 200),
            paragraph_min_length=data.get("paragraph", {}).get("min_length", 30),
            dialogue_min_ratio=data.get("dialogue", {}).get("min_ratio", 0.20),
            dialogue_max_ratio=data.get("dialogue", {}).get("max_ratio", 0.60),
            punctuation_max_consecutive=data.get("punctuation", {}).get(
                "max_consecutive", 1
            ),
            repeated_words_threshold=data.get("repeated_words", {}).get("threshold", 5),
            quality_excellent=data.get("quality", {}).get("excellent", 90),
            quality_good=data.get("quality", {}).get("good", 70),
            quality_pass=data.get("quality", {}).get("pass", 50),
        )


@dataclass
class QualityMetrics:
    """质量指标数据类"""

    total_words: int
    total_paragraphs: int
    avg_paragraph_length: float
    dialogue_ratio: float
    punctuation_issues: int
    repeated_words: dict[str, int] = field(default_factory=dict)
    quality_score: int = 0
    issues: list[str] = field(default_factory=list)


class QualityChecker:
    """章节质量检测器"""

    def __init__(self, config: Optional[QualityConfig] = None):
        self.config = config or QualityConfig()
        self.console = Console()

    def read_chapter(self, filepath: str) -> str:
        """读取章节文件"""
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"文件不存在: {filepath}")
        if path.suffix.lower() not in {".md", ".txt"}:
            self.console.print("[yellow]警告: 文件扩展名不是 .md 或 .txt[/yellow]")
        # 尝试 UTF-8，失败后尝试 GBK
        for encoding in ["utf-8", "gbk"]:
            try:
                return path.read_text(encoding=encoding)
            except UnicodeDecodeError:
                continue
        
        raise ValueError(f"无法读取文件 {filepath}: 不是有效的 UTF-8 或 GBK 文件")

    def count_words(self, text: str) -> int:
        """统计字数（中文字符 + 英文单词）"""
        chinese_chars = len(re.findall(r"[\u4e00-\u9fff]", text))
        english_words = len(re.findall(r"\b[a-zA-Z]+\b", text))
        return chinese_chars + english_words

    def analyze_paragraphs(self, text: str) -> tuple[int, float]:
        """分析段落"""
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
        paragraphs = [
            p for p in paragraphs if not p.startswith("#") and not p.startswith(">")
        ]

        if not paragraphs:
            return 0, 0.0

        lengths = [
            len(re.findall(r"[\u4e00-\u9fff]+|[a-zA-Z]+", p)) for p in paragraphs
        ]
        avg_length = sum(lengths) / len(lengths)

        return len(paragraphs), avg_length

    def calculate_dialogue_ratio(self, text: str) -> float:
        """计算对话比例"""
        dialogue_pattern = r'["\'「」"\'„"`](.*?["\'」"\'„"`])'
        dialogue_matches = re.findall(dialogue_pattern, text)
        dialogue_text = "".join(dialogue_matches)

        total_words = self.count_words(text)
        dialogue_words = self.count_words(dialogue_text)

        if total_words == 0:
            return 0.0

        return dialogue_words / total_words

    def check_punctuation(self, text: str) -> int:
        """检查标点滥用"""
        issues = 0

        consecutive_punctuation = len(re.findall(r"[，。！？、；：]{2,}", text))
        issues += consecutive_punctuation

        question_exclamation = len(re.findall(r"[？！]{2,}", text))
        issues += question_exclamation

        return issues

    def find_repeated_words(self, text: str) -> dict[str, int]:
        """查找重复用词"""
        words = re.findall(r"[\u4e00-\u9fff]{1,3}", text)
        word_counts: dict[str, int] = {}

        stop_words = {
            "的",
            "了",
            "在",
            "是",
            "就",
            "都",
            "而",
            "及",
            "与",
            "或",
            "个",
            "这",
            "那",
            "有",
            "和",
        }

        for word in words:
            if len(word) == 1 or word in stop_words:
                continue
            word_counts[word] = word_counts.get(word, 0) + 1

        threshold = self.config.repeated_words_threshold
        return {
            word: count for word, count in word_counts.items() if count >= threshold
        }

    def calculate_score(self, metrics: QualityMetrics) -> int:
        """计算质量评分 (0-100)"""
        score = 100
        cfg = self.config

        # 字数得分 (30分)
        word_score = min(30, (metrics.total_words / cfg.target_word_count) * 30)
        if metrics.total_words < cfg.target_word_count * 0.5:
            word_score *= 0.5
        score -= 30 - word_score

        # 段落长度得分 (25分)
        if metrics.avg_paragraph_length > cfg.paragraph_max_length:
            score -= 20
        elif metrics.avg_paragraph_length > cfg.paragraph_max_length * 0.75:
            score -= 10
        elif (
            metrics.avg_paragraph_length < cfg.paragraph_min_length
            and metrics.total_paragraphs > 10
        ):
            score -= 5

        # 对话比例得分 (20分)
        if metrics.dialogue_ratio > cfg.dialogue_max_ratio:
            score -= 20
        elif metrics.dialogue_ratio > cfg.dialogue_max_ratio * 0.83:
            score -= 10

        # 标点_score (15分)
        score -= min(15, metrics.punctuation_issues * 3)

        # 重复词得分 (10分)
        if metrics.repeated_words:
            max_repeats = max(metrics.repeated_words.values())
            if max_repeats > cfg.repeated_words_threshold + 2:
                score -= 10
            elif max_repeats > cfg.repeated_words_threshold:
                score -= 5

        return max(0, min(100, int(score)))

    def generate_issues(self, metrics: QualityMetrics) -> list[str]:
        """生成问题列表"""
        issues = []
        cfg = self.config

        if metrics.total_words < cfg.target_word_count * 0.8:
            issues.append(f"字数不足: {metrics.total_words}/{cfg.target_word_count}")

        if metrics.avg_paragraph_length > cfg.paragraph_max_length:
            issues.append(f"段落过长: 平均 {metrics.avg_paragraph_length:.0f} 字")

        if metrics.dialogue_ratio > cfg.dialogue_max_ratio:
            issues.append(f"对话比例过高: {metrics.dialogue_ratio:.1%}")

        if metrics.punctuation_issues > 0:
            issues.append(f"标点滥用: {metrics.punctuation_issues} 处连续标点")

        if metrics.repeated_words:
            top_repeats = sorted(
                metrics.repeated_words.items(), key=lambda x: x[1], reverse=True
            )[:3]
            repeats_str = ", ".join([f"{w} ({c}次)" for w, c in top_repeats])
            issues.append(f"重复用词: {repeats_str}")

        return issues

    def check(self, filepath: str) -> QualityMetrics:
        """执行质量检查"""
        text = self.read_chapter(filepath)

        total_words = self.count_words(text)
        total_paragraphs, avg_length = self.analyze_paragraphs(text)
        dialogue_ratio = self.calculate_dialogue_ratio(text)
        punctuation_issues = self.check_punctuation(text)
        repeated_words = self.find_repeated_words(text)

        metrics = QualityMetrics(
            total_words=total_words,
            total_paragraphs=total_paragraphs,
            avg_paragraph_length=avg_length,
            dialogue_ratio=dialogue_ratio,
            punctuation_issues=punctuation_issues,
            repeated_words=repeated_words,
            quality_score=0,
            issues=[],
        )

        metrics.quality_score = self.calculate_score(metrics)
        metrics.issues = self.generate_issues(metrics)

        return metrics

    def print_report(
        self, metrics: QualityMetrics, output_file: Optional[str] = None
    ) -> None:
        """打印质量报告"""
        cfg = self.config
        table = Table(
            title="章节质量报告", show_header=True, header_style="bold magenta"
        )
        table.add_column("指标", style="cyan")
        table.add_column("数值", style="green")
        table.add_column("状态", style="yellow")

        status_ok = "[green]✓[/green]"
        status_warn = "[yellow]⚠[/yellow]"
        status_bad = "[red]✗[/red]"

        table.add_row(
            "总字数",
            str(metrics.total_words),
            status_ok
            if metrics.total_words >= cfg.target_word_count * 0.8
            else status_warn,
        )
        table.add_row("段落数", str(metrics.total_paragraphs), status_ok)
        table.add_row(
            "平均段落长度",
            f"{metrics.avg_paragraph_length:.1f} 字",
            status_ok
            if cfg.paragraph_min_length
            <= metrics.avg_paragraph_length
            <= cfg.paragraph_max_length
            else status_warn,
        )
        table.add_row(
            "对话比例",
            f"{metrics.dialogue_ratio:.1%}",
            status_ok
            if metrics.dialogue_ratio <= cfg.dialogue_max_ratio
            else status_warn,
        )
        table.add_row(
            "标点问题",
            str(metrics.punctuation_issues),
            status_ok if metrics.punctuation_issues == 0 else status_bad,
        )

        self.console.print(table)

        score_table = Table(
            title=f"质量评分: {metrics.quality_score}/100", show_header=False
        )
        score_table.add_column(style="bold")

        if metrics.quality_score >= cfg.quality_excellent:
            color = "green"
            message = "优秀"
        elif metrics.quality_score >= cfg.quality_good:
            color = "cyan"
            message = "良好"
        elif metrics.quality_score >= cfg.quality_pass:
            color = "yellow"
            message = "及格"
        else:
            color = "red"
            message = "需改进"

        score_table.add_row(
            Text.from_markup(f"[{color} bold]等级: {message}[/{color} bold]")
        )

        if metrics.issues:
            score_table.add_row("")
            score_table.add_row(Text.from_markup("[bold red]发现问题:[/bold red]"))
            for issue in metrics.issues:
                score_table.add_row(f"  • {issue}")

        self.console.print(score_table)

        if output_file:
            self._save_report(metrics, output_file)

    def _save_report(self, metrics: QualityMetrics, filepath: str) -> None:
        """保存报告到文件"""
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)

        lines = [
            "# 章节质量报告",
            "",
            f"## 质量评分: {metrics.quality_score}/100",
            "",
            "## 指标详情",
            "",
            f"- **总字数**: {metrics.total_words}",
            f"- **段落数**: {metrics.total_paragraphs}",
            f"- **平均段落长度**: {metrics.avg_paragraph_length:.1f} 字",
            f"- **对话比例**: {metrics.dialogue_ratio:.1%}",
            f"- **标点问题**: {metrics.punctuation_issues} 处",
            "",
        ]

        if metrics.issues:
            lines.extend(["## 问题列表", ""])
            for issue in metrics.issues:
                lines.append(f"- ❌ {issue}")

        if metrics.repeated_words:
            lines.extend(["", "## 重复用词", ""])
            for word, count in sorted(
                metrics.repeated_words.items(), key=lambda x: x[1], reverse=True
            )[:10]:
                lines.append(f"- {word}: {count} 次")

        path.write_text("\n".join(lines), encoding="utf-8")
        self.console.print(f"\n[green]报告已保存到: {filepath}[/green]")


def load_config(config_path: Optional[str] = None) -> QualityConfig:
    """加载配置文件

    Args:
        config_path: 自定义配置文件路径，为 None 时使用默认路径

    Returns:
        QualityConfig 配置对象
    """
    # 确定配置文件路径
    if config_path:
        path = Path(config_path)
    else:
        path = Path("configs/quality_config.yml")

    # 如果配置文件存在，加载它
    if path.exists():
        with open(path, encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        return QualityConfig.from_dict(data)

    # 否则返回默认配置
    return QualityConfig()


def main() -> int:
    """主函数"""
    parser = argparse.ArgumentParser(
        description="章节质量检测器 - 检测 Markdown 格式章节的写作质量"
    )
    parser.add_argument(
        "--input", "-i", required=True, help="输入章节文件路径 (Markdown 格式)"
    )
    parser.add_argument(
        "--config", "-c", help="配置文件路径 (默认: configs/quality_config.yml)"
    )
    parser.add_argument(
        "--word-count", "-w", type=int, help="目标字数 (覆盖配置文件)"
    )
    parser.add_argument("--output", "-o", help="输出报告文件路径 (可选)")

    try:
        args = parser.parse_args()

        # 加载配置
        config = load_config(args.config)

        # 命令行参数覆盖配置文件
        if args.word_count is not None:
            config.target_word_count = args.word_count

        checker = QualityChecker(config)
        metrics = checker.check(args.input)
        checker.print_report(metrics, args.output)

        return 0

    except FileNotFoundError as e:
        print(f"错误: {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"错误: {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\n操作已取消", file=sys.stderr)
        return 130
    except Exception as e:
        print(f"未预期的错误: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
