#!/usr/bin/env python3
"""
Session Reflect — 增量提取 Claude Code sessions 到 Obsidian Vault

命令:
    python3 extract_sessions.py init              # 初始化配置
    python3 extract_sessions.py sync              # 增量同步新 session
    python3 extract_sessions.py backfill          # 回填所有历史 session
    python3 extract_sessions.py backfill --weekly  # 按周回填
    python3 extract_sessions.py status            # 查看同步状态
"""

import json
import re
import sys
import argparse
from pathlib import Path
from datetime import datetime, timezone
from collections import defaultdict


CONFIG_DIR = Path.home() / ".config" / "session-reflect"
CONFIG_FILE = CONFIG_DIR / "config.json"
STATE_FILE = CONFIG_DIR / "state.json"
SESSIONS_DIR = Path.home() / ".claude" / "projects"

# ── 敏感信息过滤 ──

SENSITIVE_PATTERNS = [
    (re.compile(r'sk-[a-zA-Z0-9_-]{20,}'), '[API_KEY_REDACTED]'),
    (re.compile(r'key-[a-zA-Z0-9_-]{20,}'), '[API_KEY_REDACTED]'),
    (re.compile(r'ghp_[a-zA-Z0-9]{36,}'), '[GITHUB_TOKEN_REDACTED]'),
    (re.compile(r'gho_[a-zA-Z0-9]{36,}'), '[GITHUB_TOKEN_REDACTED]'),
    (re.compile(r'xox[bp]-[a-zA-Z0-9-]+'), '[SLACK_TOKEN_REDACTED]'),
    (re.compile(r'AKIA[0-9A-Z]{16}'), '[AWS_KEY_REDACTED]'),
    (re.compile(r'eyJ[a-zA-Z0-9_-]{50,}\.[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+'), '[JWT_REDACTED]'),
    (re.compile(r'Bearer\s+[a-zA-Z0-9_.-]{20,}'), '[BEARER_TOKEN_REDACTED]'),
    (re.compile(r'password\s*[=:]\s*["\']?[^\s"\']{8,}["\']?'), '[PASSWORD_REDACTED]'),
    (re.compile(r'secret\s*[=:]\s*["\']?[^\s"\']{8,}["\']?'), '[SECRET_REDACTED]'),
]

SYSTEM_TAGS = [
    'system-reminder', 'observed_from_primary_session',
    'user-prompt-submit-hook', 'command-name',
    'task-notification', 'task-id',
    'EXTREMELY_IMPORTANT', 'SUBAGENT-STOP', 'EXTREMELY-IMPORTANT',
]
_tags_joined = '|'.join(SYSTEM_TAGS)
SYSTEM_TAG_PATTERN = re.compile(
    rf'<(?:{_tags_joined})\b[^>]*>[\s\S]*?</(?:{_tags_joined})>'
    rf'|<(?:{_tags_joined})\b[^>]*/>'
    rf'|<(?:{_tags_joined})\b[^>]*>(?:(?!</).)*$',
    re.MULTILINE,
)
CODE_BLOCK_PATTERN = re.compile(r'```[\s\S]*?```')
MAX_MESSAGE_LENGTH = 2000


# ── 配置管理 ──

def load_config() -> dict:
    if CONFIG_FILE.exists():
        return json.loads(CONFIG_FILE.read_text())
    return {}


def save_config(config: dict) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(config, ensure_ascii=False, indent=2))


def load_state() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"processed_files": {}}


def save_state(state: dict) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2))


# ── 文本处理 ──

def sanitize(text: str) -> str:
    text = SYSTEM_TAG_PATTERN.sub('', text)

    parts = CODE_BLOCK_PATTERN.split(text)
    code_blocks = CODE_BLOCK_PATTERN.findall(text)

    cleaned_parts = []
    for i, part in enumerate(parts):
        for pattern, replacement in SENSITIVE_PATTERNS:
            part = pattern.sub(replacement, part)
        cleaned_parts.append(part)
        if i < len(code_blocks):
            cleaned_parts.append('[CODE_BLOCK]')

    text = ''.join(cleaned_parts)

    if len(text) > MAX_MESSAGE_LENGTH:
        text = text[:MAX_MESSAGE_LENGTH] + '\n...[截断]'

    return text.strip()


def extract_user_text(message: dict) -> str | None:
    msg = message.get("message", {})
    if not isinstance(msg, dict):
        return None

    content = msg.get("content", "")

    if isinstance(content, str):
        return content.strip() if content.strip() else None

    if isinstance(content, list):
        texts = []
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                text = block.get("text", "").strip()
                if text:
                    texts.append(text)
        return "\n".join(texts) if texts else None

    return None


# ── Session 提取 ──

def parse_session_file(filepath: Path) -> list[str]:
    """从单个 session 文件提取用户消息"""
    messages = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                except json.JSONDecodeError:
                    continue

                if data.get("type") != "user":
                    continue

                text = extract_user_text(data)
                if not text:
                    continue

                text = sanitize(text)

                if len(text) < 5:
                    continue

                # 过滤 claude-mem observer 系统提示和其他 boilerplate
                skip_prefixes = (
                    'Hello memory agent',
                    'PROGRESS SUMMARY CHECKPOINT',
                    'You are a Claude-Mem',
                    'Continue the conversation from where',
                    'This session is being continued',
                    'Respond in this XML format',
                    'IMPORTANT! DO NOT do any work',
                )
                if any(text.startswith(prefix) for prefix in skip_prefixes):
                    continue
                # 跳过 local-command-caveat 开头的消息
                if '<local-command-caveat>' in text[:100]:
                    continue

                messages.append(text)
    except (OSError, UnicodeDecodeError):
        pass
    return messages


def get_project_name(filepath: Path) -> str:
    name = filepath.parent.name
    name = name.replace("-Users-wh-coding-", "").replace("-Users-wh-", "")
    return "home" if name == "-" else name


def get_session_date(filepath: Path) -> str | None:
    try:
        mtime = filepath.stat().st_mtime
        dt = datetime.fromtimestamp(mtime, tz=timezone.utc)
        return dt.strftime("%Y-%m-%d")
    except OSError:
        return None


def get_week_key(date_str: str) -> str:
    """返回 ISO 周标识，如 2026-W14"""
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    iso = dt.isocalendar()
    return f"{iso[0]}-W{iso[1]:02d}"


def discover_session_files() -> list[Path]:
    if not SESSIONS_DIR.exists():
        return []
    return sorted(
        (p for p in SESSIONS_DIR.rglob("*.jsonl") if "subagents" not in str(p)),
        key=lambda p: p.stat().st_mtime,
    )


def find_new_sessions(state: dict) -> list[Path]:
    """找出未处理过的 session 文件"""
    processed = state.get("processed_files", {})
    new_files = []

    for filepath in discover_session_files():
        key = str(filepath)
        mtime = str(filepath.stat().st_mtime)
        if processed.get(key) == mtime:
            continue
        new_files.append(filepath)

    return new_files


def mark_processed(state: dict, filepath: Path) -> None:
    state.setdefault("processed_files", {})[str(filepath)] = str(filepath.stat().st_mtime)


# ── 输出生成 ──

def generate_daily_md(date: str, sessions: list[dict]) -> str:
    """生成单日的 session 摘录 MD"""
    projects = sorted(set(s["project"] for s in sessions))
    total = sum(len(s["messages"]) for s in sessions)

    lines = [
        "---",
        f"date: {date}",
        "type: session-digest",
        f"projects: [{', '.join(projects)}]",
        f"message_count: {total}",
        f"session_count: {len(sessions)}",
        "---",
        "",
        f"# 对话记录 — {date}",
        "",
    ]

    for s in sessions:
        lines.append(f"## {s['project']}")
        lines.append("")
        for msg in s["messages"]:
            lines.append(f"> {msg}")
            lines.append("")

    return "\n".join(lines)


def generate_weekly_md(week_key: str, daily_data: dict[str, list[dict]]) -> str:
    """生成单周的 session 摘录 MD"""
    all_projects = set()
    total_messages = 0
    total_sessions = 0

    for sessions in daily_data.values():
        for s in sessions:
            all_projects.add(s["project"])
            total_messages += len(s["messages"])
            total_sessions += 1

    dates = sorted(daily_data.keys())

    lines = [
        "---",
        f"week: {week_key}",
        "type: session-digest-weekly",
        f"period: {dates[0]} ~ {dates[-1]}",
        f"projects: [{', '.join(sorted(all_projects))}]",
        f"message_count: {total_messages}",
        f"session_count: {total_sessions}",
        "---",
        "",
        f"# 对话记录 — {week_key}",
        "",
    ]

    for date in dates:
        lines.append(f"## {date}")
        lines.append("")
        for s in daily_data[date]:
            lines.append(f"### {s['project']}")
            lines.append("")
            for msg in s["messages"]:
                lines.append(f"> {msg}")
                lines.append("")

    return "\n".join(lines)


def write_to_vault(vault_path: Path, filename: str, content: str) -> Path:
    digest_dir = vault_path / "对话记录"
    digest_dir.mkdir(parents=True, exist_ok=True)
    filepath = digest_dir / filename
    filepath.write_text(content, encoding="utf-8")
    return filepath


# ── 命令实现 ──

def cmd_init(args: argparse.Namespace) -> None:
    config = load_config()

    if args.vault:
        vault_path = Path(args.vault).expanduser().resolve()
    else:
        print("请输入你的 Obsidian Vault 绝对路径（例如 /Users/you/my-vault）:")
        user_input = input("> ").strip()
        if not user_input:
            print("错误: 必须指定 Vault 路径。", file=sys.stderr)
            sys.exit(1)
        vault_path = Path(user_input).expanduser().resolve()

    if not vault_path.exists():
        print(f"路径不存在: {vault_path}", file=sys.stderr)
        sys.exit(1)

    # 二次确认
    print(f"\n确认 Obsidian Vault 路径: {vault_path}")
    confirm = input("正确吗？(y/n): ").strip().lower()
    if confirm != "y":
        print("已取消。")
        sys.exit(0)

    config["vault_path"] = str(vault_path)
    save_config(config)

    # 创建目录结构
    (vault_path / "对话记录").mkdir(exist_ok=True)
    (vault_path / "自我观察").mkdir(exist_ok=True)
    (vault_path / "自我观察" / "画像").mkdir(exist_ok=True)

    print(f"初始化完成:")
    print(f"  Vault: {vault_path}")
    print(f"  配置: {CONFIG_FILE}")
    print(f"  状态: {STATE_FILE}")
    print(f"\n下一步:")
    print(f"  python3 {__file__} backfill          # 回填历史（按天）")
    print(f"  python3 {__file__} backfill --weekly  # 回填历史（按周）")
    print(f"  python3 {__file__} sync               # 增量同步")


def cmd_sync(args: argparse.Namespace) -> None:
    config = load_config()
    vault_path = config.get("vault_path")
    if not vault_path:
        print("未初始化，请先运行: python3 extract_sessions.py init", file=sys.stderr)
        sys.exit(1)

    vault_path = Path(vault_path)
    state = load_state()
    new_files = find_new_sessions(state)

    if not new_files:
        print("没有新的 session 需要同步。")
        return

    # 按日期分组
    daily: dict[str, list[dict]] = defaultdict(list)

    for filepath in new_files:
        date = get_session_date(filepath)
        if not date:
            mark_processed(state, filepath)
            continue

        messages = parse_session_file(filepath)
        if not messages:
            mark_processed(state, filepath)
            continue

        project = get_project_name(filepath)
        daily[date].append({"project": project, "messages": messages})
        mark_processed(state, filepath)

    # 写入 vault（按天追加或创建）
    written = 0
    for date, sessions in sorted(daily.items()):
        filename = f"{date}.md"
        existing_file = vault_path / "对话记录" / filename

        if existing_file.exists():
            # 追加到已有文件
            existing = existing_file.read_text(encoding="utf-8")
            new_content = []
            for s in sessions:
                new_content.append(f"\n## {s['project']}\n")
                for msg in s["messages"]:
                    new_content.append(f"> {msg}\n")
            existing_file.write_text(
                existing + "\n" + "\n".join(new_content),
                encoding="utf-8",
            )
        else:
            content = generate_daily_md(date, sessions)
            write_to_vault(vault_path, filename, content)

        written += 1

    save_state(state)
    total_msgs = sum(len(m) for sessions in daily.values() for s in sessions for m in s["messages"])
    print(f"同步完成: {len(new_files)} 个 session → {written} 个文件, 共 {total_msgs} 条消息")


def cmd_backfill(args: argparse.Namespace) -> None:
    config = load_config()
    vault_path = config.get("vault_path")
    if not vault_path:
        print("未初始化，请先运行: python3 extract_sessions.py init", file=sys.stderr)
        sys.exit(1)

    vault_path = Path(vault_path)
    state = load_state()
    all_files = discover_session_files()

    if not all_files:
        print("没有找到任何 session 文件。")
        return

    print(f"发现 {len(all_files)} 个 session 文件，开始回填...")

    # 收集所有数据
    daily: dict[str, list[dict]] = defaultdict(list)

    for i, filepath in enumerate(all_files):
        if (i + 1) % 500 == 0:
            print(f"  处理中... {i + 1}/{len(all_files)}", file=sys.stderr)

        date = get_session_date(filepath)
        if not date:
            mark_processed(state, filepath)
            continue

        messages = parse_session_file(filepath)
        if not messages:
            mark_processed(state, filepath)
            continue

        project = get_project_name(filepath)
        daily[date].append({"project": project, "messages": messages})
        mark_processed(state, filepath)

    if not daily:
        print("所有 session 都没有有效的用户消息。")
        save_state(state)
        return

    # 按天或按周写入
    written = 0
    if args.weekly:
        weekly: dict[str, dict[str, list[dict]]] = defaultdict(lambda: defaultdict(list))
        for date, sessions in daily.items():
            week_key = get_week_key(date)
            weekly[week_key][date].extend(sessions)

        for week_key, week_data in sorted(weekly.items()):
            content = generate_weekly_md(week_key, dict(week_data))
            write_to_vault(vault_path, f"{week_key}.md", content)
            written += 1
    else:
        for date, sessions in sorted(daily.items()):
            content = generate_daily_md(date, sessions)
            write_to_vault(vault_path, f"{date}.md", content)
            written += 1

    save_state(state)
    total_msgs = sum(len(s["messages"]) for sessions in daily.values() for s in sessions)
    total_dates = len(daily)
    print(f"回填完成:")
    print(f"  时间跨度: {min(daily.keys())} ~ {max(daily.keys())} ({total_dates} 天)")
    print(f"  生成文件: {written} 个")
    print(f"  消息总数: {total_msgs}")
    print(f"  输出目录: {vault_path / '对话记录'}")


def cmd_status(args: argparse.Namespace) -> None:
    config = load_config()
    state = load_state()

    vault_path = config.get("vault_path", "未配置")
    processed = len(state.get("processed_files", {}))
    total = len(discover_session_files())
    pending = total - processed

    print(f"Session Reflect 状态:")
    print(f"  Vault 路径: {vault_path}")
    print(f"  配置文件:   {CONFIG_FILE}")
    print(f"  Session 总数: {total}")
    print(f"  已处理:       {processed}")
    print(f"  待同步:       {pending}")

    if vault_path != "未配置":
        digest_dir = Path(vault_path) / "对话记录"
        if digest_dir.exists():
            md_count = len(list(digest_dir.glob("*.md")))
            print(f"  Vault 记录文件: {md_count}")


# ── 入口 ──

def main():
    parser = argparse.ArgumentParser(
        description="Session Reflect — 增量提取 Claude Code sessions 到 Obsidian Vault"
    )
    sub = parser.add_subparsers(dest="command")

    p_init = sub.add_parser("init", help="初始化配置")
    p_init.add_argument("--vault", type=str, help="Obsidian Vault 路径")

    p_sync = sub.add_parser("sync", help="增量同步新 session")

    p_backfill = sub.add_parser("backfill", help="回填所有历史 session")
    p_backfill.add_argument("--weekly", action="store_true", help="按周合并（默认按天）")

    p_status = sub.add_parser("status", help="查看同步状态")

    args = parser.parse_args()

    commands = {
        "init": cmd_init,
        "sync": cmd_sync,
        "backfill": cmd_backfill,
        "status": cmd_status,
    }

    if args.command in commands:
        commands[args.command](args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
