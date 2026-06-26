#!/usr/bin/env python3
"""
文本风格分析器 - 分析写作风格特征并生成 Voice Profile 配置文件

Usage:
    python3 analyze_style.py --input text.txt --output style.yml
"""

import argparse
import re
import sys
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path

import yaml
from rich.console import Console
from rich.panel import Panel
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
class SentenceFeatures:
    """句式特征"""

    average_length: float
    long_sentence_ratio: float
    short_sentence_ratio: float
    rhetorical_devices: dict[str, int]


@dataclass
class VocabularyFeatures:
    """词汇特征"""

    adj_ratio: float
    verb_ratio: float
    noun_ratio: float
    most_frequent_words: list[tuple[str, int]]
    unique_words_ratio: float


@dataclass
class RhythmFeatures:
    """节奏特征"""

    average_paragraph_length: int
    punctuation_distribution: dict[str, int]
    dialogue_ratio: float


@dataclass
class StyleAnalysisResult:
    """风格分析结果"""

    voice_profile: VoiceProfile
    sentence_features: SentenceFeatures
    vocabulary_features: VocabularyFeatures
    rhythm_features: RhythmFeatures


class StyleAnalyzer:
    """文本风格分析器"""

    rhetorical_markers = {
        "metaphor": ["如同", "好像", "仿佛", "似", "像一样", "是", "成了"],
        "simile": ["如同", "好像", "仿佛", "似的", "一般"],
        "hyperbole": ["无比", "极了", "天地", "世界", "全部", "永远"],
        "parallelism": ["不仅而且", "既又", "不是而是", "一方面另一方面"],
    }

    def __init__(self, sample_size: int = 1000):
        self.sample_size = sample_size

    def analyze(self, text: str) -> StyleAnalysisResult:
        """分析文本风格"""
        voice_profile = self._analyze_voice_profile(text)
        sentence_features = self._analyze_sentence_features(text)
        vocabulary_features = self._analyze_vocabulary_features(text)
        rhythm_features = self._analyze_rhythm_features(text)

        return StyleAnalysisResult(
            voice_profile=voice_profile,
            sentence_features=sentence_features,
            vocabulary_features=vocabulary_features,
            rhythm_features=rhythm_features,
        )

    def _analyze_voice_profile(self, text: str) -> VoiceProfile:
        """分析声音配置文件"""
        sentences = self._split_sentences(text)
        sentiment_score = self._calculate_sentiment(text)
        avg_sentence_length = sum(len(s) for s in sentences) / max(len(sentences), 1)
        labels = self._extract_labels(text)
        pace = self._determine_pace(avg_sentence_length)
        tone = self._determine_tone(text)

        return VoiceProfile(
            labels=labels[:5],
            pace=pace,
            tone=tone,
            sentiment=sentiment_score,
        )

    def _analyze_sentence_features(self, text: str) -> SentenceFeatures:
        """分析句式特征"""
        sentences = self._split_sentences(text)

        if not sentences:
            return SentenceFeatures(
                average_length=0.0,
                long_sentence_ratio=0.0,
                short_sentence_ratio=0.0,
                rhetorical_devices={},
            )

        lengths = [len(s) for s in sentences]
        avg_length = sum(lengths) / len(lengths)

        short_count = sum(1 for length in lengths if length < 20)
        long_count = sum(1 for length in lengths if length > 50)

        short_ratio = short_count / len(sentences)
        long_ratio = long_count / len(sentences)

        rhetorical_devices = self._detect_rhetorical_devices(text)

        return SentenceFeatures(
            average_length=round(avg_length, 2),
            long_sentence_ratio=round(long_ratio, 2),
            short_sentence_ratio=round(short_ratio, 2),
            rhetorical_devices=rhetorical_devices,
        )

    def _analyze_vocabulary_features(self, text: str) -> VocabularyFeatures:
        """分析词汇特征"""
        words = self._tokenize_words(text)

        total_words = len(words)
        if total_words == 0:
            return VocabularyFeatures(
                adj_ratio=0.0,
                verb_ratio=0.0,
                noun_ratio=0.0,
                most_frequent_words=[],
                unique_words_ratio=0.0,
            )

        adj_count = self._count_adjectives(words)
        verb_count = self._count_verbs(words)
        noun_count = self._count_nouns(words)

        word_freq = Counter(words)
        most_frequent = word_freq.most_common(10)

        unique_words = len(set(words))
        unique_ratio = unique_words / total_words

        return VocabularyFeatures(
            adj_ratio=round(adj_count / total_words, 3),
            verb_ratio=round(verb_count / total_words, 3),
            noun_ratio=round(noun_count / total_words, 3),
            most_frequent_words=most_frequent,
            unique_words_ratio=round(unique_ratio, 3),
        )

    def _analyze_rhythm_features(self, text: str) -> RhythmFeatures:
        """分析节奏特征"""
        paragraphs = self._split_paragraphs(text)

        avg_paragraph_length = sum(len(p) for p in paragraphs) / max(len(paragraphs), 1)

        punctuation = self._analyze_punctuation(text)

        dialogue_ratio = self._calculate_dialogue_ratio(text)

        return RhythmFeatures(
            average_paragraph_length=int(avg_paragraph_length),
            punctuation_distribution=punctuation,
            dialogue_ratio=round(dialogue_ratio, 3),
        )

    def _split_sentences(self, text: str) -> list[str]:
        """分割句子"""
        sentences = re.split(r"[。！？!?]", text)
        return [s.strip() for s in sentences if s.strip()]

    def _split_paragraphs(self, text: str) -> list[str]:
        """分割段落"""
        paragraphs = text.split("\n\n")
        return [p.strip() for p in paragraphs if p.strip()]

    def _tokenize_words(self, text: str) -> list[str]:
        """分词（简化版）"""
        words = re.findall(r"[\u4e00-\u9fa5]+|[a-zA-Z]+|\d+", text)
        return [w for w in words if len(w) > 1]

    def _detect_rhetorical_devices(self, text: str) -> dict[str, int]:
        """检测修辞手法"""
        device_counts = {}

        for device, markers in self.rhetorical_markers.items():
            count = sum(1 for marker in markers if marker in text)
            if count > 0:
                device_counts[device] = count

        return device_counts

    def _calculate_sentiment(self, text: str) -> float:
        """计算情感倾向（-1 到 1）"""
        positive_words = [
            "好",
            "美",
            "喜欢",
            "爱",
            "快乐",
            "幸福",
            "温暖",
            "明亮",
            "希望",
            "梦想",
        ]
        negative_words = [
            "坏",
            "丑",
            "讨厌",
            "恨",
            "悲伤",
            "痛苦",
            "寒冷",
            "黑暗",
            "绝望",
            "失败",
        ]

        positive_count = sum(text.count(word) for word in positive_words)
        negative_count = sum(text.count(word) for word in negative_words)

        total = positive_count + negative_count
        if total == 0:
            return 0.0

        sentiment = (positive_count - negative_count) / total
        return round(sentiment, 3)

    def _extract_labels(self, text: str) -> list[str]:
        """提取风格标签"""
        labels = []

        sentences = self._split_sentences(text)
        avg_length = sum(len(s) for s in sentences) / max(len(sentences), 1)

        if avg_length > 40:
            labels.append("复杂")
        else:
            labels.append("简洁")

        punct_count = len(re.findall(r"[。！？]", text))
        if punct_count > 0:
            avg_sentence_by_punctuation = len(text) / punct_count
            if avg_sentence_by_punctuation < 30:
                labels.append("快速")
                labels.append("紧凑")
            else:
                labels.append("舒缓")
                labels.append("娓娓道来")

        if re.search(r"[？!]", text):
            labels.append("互动性")

        if re.search(r'["].*?["]', text) or re.search(r"'.*?'", text):
            labels.append("对话性强")

        if re.search(r"[，、；]", text):
            labels.append("节奏感强")

        return labels if labels else ["中性"]

    def _determine_pace(self, avg_length: float) -> str:
        """确定语速"""
        if avg_length > 50:
            return "缓慢"
        elif avg_length > 30:
            return "适中"
        else:
            return "快速"

    def _determine_tone(self, text: str) -> str:
        """确定语气"""
        formal_markers = ["因此", "然而", "综上所述", "基于此", "由此可见"]
        casual_markers = ["我觉得", "我想", "你知道", "其实", "就是说"]

        formal_count = sum(text.count(marker) for marker in formal_markers)
        casual_count = sum(text.count(marker) for marker in casual_markers)

        if formal_count > casual_count * 2:
            return "正式"
        elif casual_count > formal_count * 2:
            return "随意"
        else:
            return "中性"

    def _count_adjectives(self, words: list[str]) -> int:
        """计算形容词数量（简化）"""
        adjective_suffixes = ["的", "好", "坏", "美", "丑", "大", "小", "老", "新"]
        return sum(1 for w in words if any(w.endswith(s) for s in adjective_suffixes))

    def _count_verbs(self, words: list[str]) -> int:
        """计算动词数量（简化）"""
        verb_patterns = ["是", "有", "在", "做", "看", "听", "说", "想", "需要", "应该"]
        return sum(1 for w in words if any(w.startswith(v) or w.endswith(v) for v in verb_patterns))

    def _count_nouns(self, words: list[str]) -> int:
        """计算名词数量（简化）"""
        noun_markers = ["人", "事", "物", "书", "文", "国", "家", "天", "地"]
        return sum(1 for w in words if any(w.endswith(n) for n in noun_markers))

    def _analyze_punctuation(self, text: str) -> dict[str, int]:
        """分析标点使用"""
        punctuation = {
            "period": len(re.findall(r"。", text)),
            "question": len(re.findall(r"[？?]", text)),
            "exclamation": len(re.findall(r"[！!]", text)),
            "comma": len(re.findall(r"[，、]", text)),
            "semicolon": len(re.findall(r"[；;]", text)),
            "colon": len(re.findall(r"[：:]", text)),
        }
        return punctuation

    def _calculate_dialogue_ratio(self, text: str) -> float:
        """计算对话比例"""
        dialogue_patterns = [
            r'["].*?["]',
            r"'.*?'",
            r"[说问答答]道",
            r"[说问答答]曰",
        ]

        total_chars = len(text)
        if total_chars == 0:
            return 0.0

        dialogue_chars = 0
        for pattern in dialogue_patterns:
            matches = re.findall(pattern, text)
            dialogue_chars += sum(len(m) for m in matches)

        return dialogue_chars / total_chars


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
        "sentence_features": asdict(result.sentence_features),
        "vocabulary_features": asdict(result.vocabulary_features),
        "rhythm_features": asdict(result.rhythm_features),
    }

    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False)


def print_result(result: StyleAnalysisResult) -> None:
    """美化输出结果"""
    console.print("\n")
    console.print(
        Panel.fit(
            "[bold cyan]分析完成！[/bold cyan]",
            border_style="cyan",
            padding=(1, 2),
        )
    )

    table = Table(title="风格分析报告", show_header=True, header_style="bold magenta")
    table.add_column("特征", style="cyan")
    table.add_column("详情", style="green")

    # Voice Profile
    vp = result.voice_profile
    voice_info = Text()
    voice_info.append(f"风格标签：{', '.join(vp.labels)}\n")
    voice_info.append(f"语速：{vp.pace}\n")
    voice_info.append(f"语气：{vp.tone}\n")
    voice_info.append(f"情感倾向：{vp.sentiment:+.3f}")
    table.add_row("Voice Profile", voice_info)

    # Sentence Features
    sf = result.sentence_features
    sentence_info = Text()
    sentence_info.append(f"平均句长：{sf.average_length:.2f} 字符\n")
    sentence_info.append(
        f"长句比例：{sf.long_sentence_ratio:.2%} | 短句比例：{sf.short_sentence_ratio:.2%}\n"
    )
    if sf.rhetorical_devices:
        devices = ", ".join(f"{k}: {v}" for k, v in sf.rhetorical_devices.items())
        sentence_info.append(f"修辞手法：{devices}")
    table.add_row("句式特征", sentence_info)

    # Vocabulary Features
    vf = result.vocabulary_features
    vocab_info = Text()
    vocab_info.append(
        f"形容词占比：{vf.adj_ratio:.3f} | 动词占比：{vf.verb_ratio:.3f} | 名词占比：{vf.noun_ratio:.3f}\n"
    )
    vocab_info.append(f"词汇丰富度：{vf.unique_words_ratio:.3f}\n")
    vocab_info.append(
        "高频词：" + ", ".join(f"{w}({c})" for w, c in vf.most_frequent_words[:5])
    )
    table.add_row("词汇特征", vocab_info)

    # Rhythm Features
    rf = result.rhythm_features
    rhythm_info = Text()
    rhythm_info.append(f"平均段落长度：{rf.average_paragraph_length} 字符\n")
    rhythm_info.append(
        f"对话比例：{rf.dialogue_ratio:.2%}\n"
    )
    punct = rf.punctuation_distribution
    rhythm_info.append(
        f"标点：句号{punct.get('period', 0)}, 逗号{punct.get('comma', 0)}, 问号{punct.get('question', 0)}"
    )
    table.add_row("节奏特征", rhythm_info)

    console.print(table)


def create_parser() -> argparse.ArgumentParser:
    """创建命令行参数解析器"""
    parser = argparse.ArgumentParser(
        prog="analyze_style",
        description="分析文本的写作风格特征，生成 Voice Profile 配置文件",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s --input story.txt --output style.yml
  %(prog)s --input story.txt --output output/style.yml --sample-size 500
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
        "--sample-size",
        "-s",
        type=int,
        default=1000,
        help="分析样本大小（字符数）",
    )

    return parser


def main() -> int:
    """主函数"""
    parser = create_parser()
    args = parser.parse_args()

    console.print("[bold cyan]文本风格分析器[/bold cyan]")
    console.print(f"输入文件：[yellow]{args.input}[/yellow]")
    console.print(f"输出文件：[yellow]{args.output}[/yellow]")
    console.print(f"样本大小：[yellow]{args.sample_size}[/yellow]")
    console.print()

    text = load_text(args.input)

    if len(text) > args.sample_size:
        text = text[: args.sample_size]
        console.print(f"[yellow]⚠️  限制样本大小至 {args.sample_size} 字符[/yellow]")

    analyzer = StyleAnalyzer(sample_size=args.sample_size)
    result = analyzer.analyze(text)

    save_yaml(result, args.output)
    console.print(f"\n[green]✓ 配置文件已保存至：{args.output}[/green]")

    print_result(result)

    return 0


if __name__ == "__main__":
    sys.exit(main())
