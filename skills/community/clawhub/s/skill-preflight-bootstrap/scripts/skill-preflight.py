#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import shlex
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Sequence, Tuple

ANSI_ESCAPE_RE = re.compile(r"\x1B\[[0-?]*[ -/]*[@-~]")
ASCII_TOKEN_RE = re.compile(r"[a-z0-9][a-z0-9_+.-]{1,}")
CJK_TOKEN_RE = re.compile(r"[\u4e00-\u9fff]{2,}")
HEADING_RE = re.compile(r"^#\s+(.+)$", re.MULTILINE)
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
STOPWORDS = {
    "the", "and", "for", "with", "that", "this", "from", "into", "your", "task",
    "need", "help", "make", "build", "create", "using", "use", "run", "add", "fix",
    "how", "what", "when", "where", "which", "why", "are", "is", "to", "of", "in",
}


@dataclass(frozen=True)
class SkillMatch:
    name: str
    description: str
    title: str
    path: Path
    source: str
    score: int
    reasons: Tuple[str, ...]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="任务开始前的技能预检：先匹配本地技能，不足时再调用 find-skills 远程搜索。"
    )
    parser.add_argument("query", nargs="+", help="任务描述，例如：优化 React 性能")
    parser.add_argument("--limit", type=int, default=8, help="本地结果展示数量上限，默认 8")
    parser.add_argument(
        "--min-score",
        type=int,
        default=12,
        help="本地技能命中最低分数，默认 12",
    )
    parser.add_argument(
        "--remote",
        action="store_true",
        help="即使本地已命中，也继续调用 `npx -y skills find` 搜索远程技能",
    )
    parser.add_argument(
        "--skills-dir",
        action="append",
        default=[],
        help="附加技能目录，可重复传入",
    )
    return parser.parse_args()


def candidate_skill_dirs(extra_dirs: Sequence[str]) -> List[Path]:
    home = Path.home()
    dirs = [
        Path.cwd() / "skills",
        home / ".codex" / "skills",
        home / ".agents" / "skills",
        home / ".claude" / "skills",
    ]
    dirs.extend(Path(item).expanduser() for item in extra_dirs)
    seen = set()
    result: List[Path] = []
    for item in dirs:
        key = item.resolve() if item.exists() else item.expanduser()
        if str(key) in seen:
            continue
        seen.add(str(key))
        result.append(item)
    return result


def list_skill_files(skill_dirs: Iterable[Path]) -> List[Path]:
    skill_files: List[Path] = []
    for skill_dir in skill_dirs:
        if not skill_dir.exists():
            continue
        skill_files.extend(sorted(skill_dir.glob("*/SKILL.md")))
    return skill_files


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def tokenize(query: str) -> List[str]:
    normalized = normalize(query)
    tokens = {normalized} if normalized else set()
    tokens.update(
        token
        for token in ASCII_TOKEN_RE.findall(normalized)
        if token not in STOPWORDS
    )
    tokens.update(CJK_TOKEN_RE.findall(query))
    return [token for token in tokens if token]


def extract_frontmatter_value(frontmatter: str, key: str) -> str:
    for line in frontmatter.splitlines():
        if not line.startswith(f"{key}:"):
            continue
        value = line.split(":", 1)[1].strip()
        return value.strip('"').strip("'")
    return ""


def infer_source(path: Path) -> str:
    posix_path = path.as_posix()
    if "/.codex/skills/" in posix_path:
        return "codex"
    if "/.agents/skills/" in posix_path:
        return "agents"
    if "/.claude/skills/" in posix_path:
        return "claude"
    return "project"


def parse_skill_file(path: Path) -> Tuple[str, str, str, str]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    frontmatter_match = FRONTMATTER_RE.search(text)
    frontmatter = frontmatter_match.group(1) if frontmatter_match else ""
    name = extract_frontmatter_value(frontmatter, "name") or path.parent.name
    description = extract_frontmatter_value(frontmatter, "description")
    title_match = HEADING_RE.search(text)
    title = title_match.group(1).strip() if title_match else name
    return name, description, title, text[:1200]


def score_skill(query: str, query_tokens: Sequence[str], path: Path) -> SkillMatch | None:
    name, description, title, excerpt = parse_skill_file(path)
    fields = {
        "name": normalize(name),
        "description": normalize(description),
        "title": normalize(title),
        "path": normalize(path.parent.name),
        "excerpt": normalize(excerpt),
    }
    normalized_query = normalize(query)
    score = 0
    reasons: List[str] = []
    matched_query_tokens = set()
    phrase_hit = False

    weighted_fields = (
        ("name", 56, 14),
        ("title", 30, 8),
        ("description", 24, 6),
        ("path", 16, 4),
        ("excerpt", 12, 3),
    )

    for field_name, full_score, token_score in weighted_fields:
        content = fields[field_name]
        if normalized_query and normalized_query in content:
            score += full_score
            phrase_hit = True
            reasons.append(f"{field_name}:phrase")
        for token in query_tokens:
            if len(token) < 2 or token == normalized_query:
                continue
            if token in content:
                score += token_score
                matched_query_tokens.add(token)
                reasons.append(f"{field_name}:{token}")

    if score == 0:
        return None

    meaningful_tokens = [token for token in query_tokens if len(token) >= 2 and token != normalized_query]
    token_threshold = 2 if len(meaningful_tokens) >= 3 else 1
    if not phrase_hit and meaningful_tokens and len(matched_query_tokens) < token_threshold:
        return None

    deduped_reasons = tuple(dict.fromkeys(reasons))
    return SkillMatch(
        name=name,
        description=description,
        title=title,
        path=path,
        source=infer_source(path),
        score=score,
        reasons=deduped_reasons,
    )


def search_local_skills(query: str, skill_files: Sequence[Path], min_score: int) -> List[SkillMatch]:
    query_tokens = tokenize(query)
    matches: List[SkillMatch] = []
    for path in skill_files:
        match = score_skill(query, query_tokens, path)
        if match and match.score >= min_score:
            matches.append(match)
    matches.sort(key=lambda item: (-item.score, item.name.lower(), str(item.path)))
    return matches


def strip_ansi(text: str) -> str:
    return ANSI_ESCAPE_RE.sub("", text)


def run_remote_search(query: str) -> Tuple[int, str]:
    command = ["npx", "-y", "skills", "find", query]
    completed = subprocess.run(command, capture_output=True, text=True)
    combined = (completed.stdout or "") + (completed.stderr or "")
    return completed.returncode, strip_ansi(combined).strip()


def print_header(title: str) -> None:
    print(f"\n== {title} ==")


def main() -> int:
    args = parse_args()
    query = " ".join(args.query).strip()
    skill_dirs = candidate_skill_dirs(args.skills_dir)
    skill_files = list_skill_files(skill_dirs)
    local_matches = search_local_skills(query, skill_files, args.min_score)

    print(f"任务描述: {query}")
    print(f"扫描技能目录数: {len(skill_dirs)}")
    print(f"发现本地 SKILL.md 数: {len(skill_files)}")

    print_header("本地技能候选")
    if local_matches:
        for index, match in enumerate(local_matches[: args.limit], start=1):
            print(f"{index}. [{match.source}] {match.name} (score={match.score})")
            print(f"   路径: {match.path}")
            if match.description:
                print(f"   描述: {match.description}")
            print(f"   命中: {', '.join(match.reasons[:6])}")
        print("\n建议动作:")
        print("- 先读取排名最高的 1-2 个 `SKILL.md`。")
        print("- 若最高结果仍不贴合，再执行远程搜索或安装。")
    else:
        print("未命中达到阈值的本地技能。")

    should_run_remote = args.remote or not local_matches
    if should_run_remote:
        print_header("远程技能搜索（find-skills）")
        command = ["npx", "-y", "skills", "find", query]
        print("执行命令:")
        print(f"$ {shlex.join(command)}")
        return_code, output = run_remote_search(query)
        if output:
            print(output)
        else:
            print("远程搜索未返回内容。")
        if return_code != 0:
            print(f"\n远程搜索退出码: {return_code}", file=sys.stderr)
            return return_code
    else:
        print_header("远程搜索")
        print("已跳过；如需扩展搜索，请追加 `--remote`。")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
