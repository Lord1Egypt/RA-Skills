"""generate mode 质检 — 硬错 + 软错。

设计原则（spec §10）：
- **硬错**（hard）：确定性问题，agent 应自动重跑相应步骤
  例：desc 含禁忌词 / tags 数 < 5 / 文件为空 / 图片生成失败
- **软错**（soft）：判断性问题，agent 不应自动重跑（避免无限循环），
  改为写 quality_report.md 让用户决定
  例：desc 长度异常 / 风格关键词命中率低 / 钩子未在 graph 中

每个 issue 含：severity / file / message / suggestion
"""

from __future__ import annotations
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal


@dataclass
class Issue:
    severity: Literal["hard", "soft"]
    file: str             # 哪个产出文件出问题（"desc.txt" / "tags.txt" / ...）
    message: str          # 一句话描述
    suggestion: str = ""  # 修复建议


@dataclass
class ValidationReport:
    hard: list[Issue] = field(default_factory=list)
    soft: list[Issue] = field(default_factory=list)
    files_checked: list[str] = field(default_factory=list)

    @property
    def has_hard_errors(self) -> bool:
        return len(self.hard) > 0

    @property
    def has_any_issues(self) -> bool:
        return self.has_hard_errors or len(self.soft) > 0

    def summary_line(self) -> str:
        """1 行摘要，用于 generate.py 的 step log。"""
        if not self.has_any_issues:
            return f"✅ All {len(self.files_checked)} files passed validation"
        parts = []
        if self.hard:
            parts.append(f"❌ {len(self.hard)} hard error(s)")
        if self.soft:
            parts.append(f"⚠️ {len(self.soft)} soft warning(s)")
        return f"{', '.join(parts)} across {len(self.files_checked)} files"

    def to_markdown(self) -> str:
        """生成 quality_report.md 内容。"""
        lines = ["# Quality Report\n"]
        lines.append(f"**Files checked**: {len(self.files_checked)}\n")
        lines.append(f"**Hard errors**: {len(self.hard)}  ｜  **Soft warnings**: {len(self.soft)}\n")

        if self.hard:
            lines.append("\n## ❌ Hard errors（自动重跑触发条件）\n")
            for i, issue in enumerate(self.hard, 1):
                lines.append(f"### {i}. {issue.file}")
                lines.append(f"**问题**：{issue.message}")
                if issue.suggestion:
                    lines.append(f"**建议**：{issue.suggestion}")
                lines.append("")

        if self.soft:
            lines.append("\n## ⚠️ Soft warnings（人工 review）\n")
            for i, issue in enumerate(self.soft, 1):
                lines.append(f"### {i}. {issue.file}")
                lines.append(f"**问题**：{issue.message}")
                if issue.suggestion:
                    lines.append(f"**建议**：{issue.suggestion}")
                lines.append("")

        if not self.has_any_issues:
            lines.append("\n✅ **全部产出通过质检。** 可直接发布。")

        return "\n".join(lines)


# ─── 默认禁忌词（可被 graph/engine/taboo 覆盖）───

DEFAULT_BANNED_WORDS = (
    # 极限词（XHS 高敏感）
    "最", "第一", "唯一", "顶级", "极致", "国家级", "世界级",
    "100%", "绝对", "永久", "终身",
    # 营销过度词
    "神器", "王炸", "救命", "必入", "快冲", "求求了",
)

# 默认期望的 tags 数量
MIN_TAGS = 5
MAX_TAGS = 20

# 默认期望的 desc 长度
MIN_DESC_LEN = 80
MAX_DESC_LEN = 800

# script.md 最少字数
MIN_SCRIPT_LEN = 200


# ─── 各文件的 validator ───

def validate_text_file(
    path: Path,
    file_label: str,
    min_len: int = 1,
    banned_words: tuple[str, ...] = DEFAULT_BANNED_WORDS,
) -> list[Issue]:
    """通用文本文件检查：存在 / 非空 / 无禁忌词。"""
    out: list[Issue] = []
    if not path.exists():
        out.append(Issue("hard", file_label, "文件不存在", "重跑生成"))
        return out
    try:
        text = path.read_text(encoding="utf-8").strip()
    except (OSError, UnicodeDecodeError) as e:
        out.append(Issue("hard", file_label, f"读取失败：{e}", "检查权限/编码"))
        return out
    if not text:
        out.append(Issue("hard", file_label, "文件为空", "重跑生成"))
        return out
    if len(text) < min_len:
        out.append(Issue("hard", file_label, f"内容太短（{len(text)} < {min_len}）", "重跑生成"))
    # 禁忌词检查
    hits = [w for w in banned_words if w in text]
    if hits:
        out.append(Issue(
            "hard", file_label,
            f"含禁忌词：{', '.join(hits[:5])}",
            "重跑生成；prompt 强调禁忌词列表",
        ))
    return out


def validate_desc(
    path: Path,
    banned_words: tuple[str, ...] = DEFAULT_BANNED_WORDS,
) -> list[Issue]:
    """desc.txt 专项：长度 + 禁忌词 + emoji 数量克制 + 段落空行。"""
    out = validate_text_file(path, "desc.txt", min_len=10, banned_words=banned_words)
    if not path.exists():
        return out
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return out

    # 长度（软错）
    n = len(text)
    if n < MIN_DESC_LEN:
        out.append(Issue(
            "soft", "desc.txt",
            f"长度偏短（{n} < {MIN_DESC_LEN} 字）",
            "考虑加 1-2 句具体材质/工艺描述",
        ))
    elif n > MAX_DESC_LEN:
        out.append(Issue(
            "soft", "desc.txt",
            f"长度偏长（{n} > {MAX_DESC_LEN} 字）",
            "可精简，保留最强钩子句",
        ))

    # emoji 数量（软错：>3 视为堆砌）
    emoji_pattern = re.compile(
        "["
        "\U0001F300-\U0001F9FF"  # 各种 emoji
        "✀-➿"          # dingbats
        "☀-⛿"          # 杂项符号
        "\U0001FA70-\U0001FAFF"  # 扩展
        "]"
    )
    emoji_count = len(emoji_pattern.findall(text))
    if emoji_count > 3:
        out.append(Issue(
            "soft", "desc.txt",
            f"emoji 过多（{emoji_count} 个）",
            "XHS 调性建议 1-2 个克制使用",
        ))

    return out


def validate_tags(path: Path) -> list[Issue]:
    """tags.txt 专项：数量 + 格式 + 全部带 #。"""
    out: list[Issue] = []
    if not path.exists():
        out.append(Issue("hard", "tags.txt", "文件不存在", "重跑生成"))
        return out
    try:
        text = path.read_text(encoding="utf-8").strip()
    except (OSError, UnicodeDecodeError) as e:
        out.append(Issue("hard", "tags.txt", f"读取失败：{e}", ""))
        return out
    if not text:
        out.append(Issue("hard", "tags.txt", "文件为空", "重跑生成"))
        return out

    # 提取所有 #开头的 token
    tags = re.findall(r"#\S+", text)
    n = len(tags)

    if n < MIN_TAGS:
        out.append(Issue(
            "hard", "tags.txt",
            f"标签太少（{n} < {MIN_TAGS}）",
            "重跑 + prompt 强调最少 10 个",
        ))
    elif n > MAX_TAGS:
        out.append(Issue(
            "soft", "tags.txt",
            f"标签偏多（{n} > {MAX_TAGS}）",
            "考虑精简到 10-15 个最相关",
        ))

    # 检查是否所有非空 token 都带 #
    non_hash_tokens = re.findall(r"(?<!#)\b[一-龥\w]{2,}\b", text)
    # 这是粗糙检测，主要看是否大量裸词
    if non_hash_tokens and len(non_hash_tokens) > n:
        out.append(Issue(
            "soft", "tags.txt",
            "可能有未加 # 的标签",
            "确认所有标签都带 # 前缀",
        ))

    return out


def validate_script(
    path: Path,
    banned_words: tuple[str, ...] = DEFAULT_BANNED_WORDS,
) -> list[Issue]:
    """script.md 专项：存在 + 不太短 + 无禁忌词。"""
    return validate_text_file(path, "script.md", min_len=MIN_SCRIPT_LEN, banned_words=banned_words)


def validate_cover_text(
    path: Path,
    banned_words: tuple[str, ...] = DEFAULT_BANNED_WORDS,
) -> list[Issue]:
    """cover.txt 专项：1 行字 ≤ 20 字。"""
    out = validate_text_file(path, "cover.txt", min_len=2, banned_words=banned_words)
    if not path.exists():
        return out
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return out
    # 行数（多行警告）
    lines = [ln for ln in text.splitlines() if ln.strip()]
    if len(lines) > 2:
        out.append(Issue(
            "soft", "cover.txt",
            f"封面文案 {len(lines)} 行（建议 1 行）",
            "封面适合一行字 + 1 个 emoji",
        ))
    # 长度
    if len(text) > 30:
        out.append(Issue(
            "soft", "cover.txt",
            f"封面文案偏长（{len(text)} 字）",
            "封面建议 ≤ 15 字",
        ))
    return out


def validate_image(path: Path, file_label: str) -> list[Issue]:
    """图片：存在 + 大小合理（不太小不太大）。"""
    out: list[Issue] = []
    if not path.exists():
        out.append(Issue("hard", file_label, "图片不存在（生成失败？）", "重跑生成"))
        return out
    size = path.stat().st_size
    if size < 50_000:  # < 50KB 几乎肯定是错误
        out.append(Issue(
            "hard", file_label,
            f"图片过小（{size} bytes，疑似生成失败）",
            "重跑图片生成",
        ))
    elif size > 30_000_000:  # > 30MB 异常大
        out.append(Issue(
            "soft", file_label,
            f"图片偏大（{size // (1024*1024)} MB）",
            "可考虑压缩",
        ))
    return out


# ─── 入口：批量检查整个 gen_dir ───

def validate_workspace(
    gen_dir: Path,
    output_type: str,  # video / image / script
    extra_banned_words: tuple[str, ...] = (),
) -> ValidationReport:
    """检查 gen_dir 下所有产出文件。

    Args:
        gen_dir: GEN-xxx 目录
        output_type: 决定哪些文件该存在（video 必须有 caption + seedance）
        extra_banned_words: 额外的禁忌词（来自 graph/engine/taboo）

    Returns:
        ValidationReport
    """
    report = ValidationReport()
    banned = DEFAULT_BANNED_WORDS + tuple(extra_banned_words)

    # 通用必有
    files = ["script.md", "cover.txt", "desc.txt", "tags.txt"]

    # 视频额外
    if output_type == "video":
        files += ["caption.txt", "seedance-prompt.md"]

    for fname in files:
        path = gen_dir / fname
        report.files_checked.append(fname)

        if fname == "script.md":
            issues = validate_script(path, banned_words=banned)
        elif fname == "desc.txt":
            issues = validate_desc(path, banned_words=banned)
        elif fname == "tags.txt":
            issues = validate_tags(path)
        elif fname == "cover.txt":
            issues = validate_cover_text(path, banned_words=banned)
        elif fname == "caption.txt":
            issues = validate_text_file(path, fname, min_len=5, banned_words=banned)
        elif fname == "seedance-prompt.md":
            issues = validate_text_file(path, fname, min_len=100, banned_words=banned)
        else:
            issues = validate_text_file(path, fname, banned_words=banned)

        for issue in issues:
            (report.hard if issue.severity == "hard" else report.soft).append(issue)

    # 图片：image 类型 frames/ + cover.png；video 类型 1 张关键帧 + cover.png
    if output_type in ("video", "image"):
        cover_path = gen_dir / "cover.png"
        report.files_checked.append("cover.png")
        for issue in validate_image(cover_path, "cover.png"):
            (report.hard if issue.severity == "hard" else report.soft).append(issue)

        frames_dir = gen_dir / "frames"
        if frames_dir.exists():
            frame_files = sorted(frames_dir.glob("frame_*.png"))
            report.files_checked.append(f"frames/ ({len(frame_files)} files)")
            for f in frame_files:
                for issue in validate_image(f, f"frames/{f.name}"):
                    (report.hard if issue.severity == "hard" else report.soft).append(issue)
        else:
            report.hard.append(Issue(
                "hard", "frames/",
                "frames/ 目录不存在",
                "图片生成步骤失败，重跑",
            ))

    return report


def extract_taboo_words_from_graph(taboo_md: str) -> list[str]:
    """从 graph/engine/taboo.md 文本提取禁忌词列表。

    简单规则：找 `- 词` / `* 词` / 词典表格行。
    """
    out: list[str] = []
    if not taboo_md:
        return out
    for line in taboo_md.splitlines():
        line = line.strip()
        # bullet item 形式
        if m := re.match(r"^[-*]\s+([^\s/—]{1,8})(?:\s|$|/|—)", line):
            word = m.group(1).strip()
            if 1 <= len(word) <= 8:
                out.append(word)
    return out
