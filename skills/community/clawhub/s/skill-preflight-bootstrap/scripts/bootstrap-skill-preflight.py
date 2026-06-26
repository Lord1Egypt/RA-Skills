#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import stat
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

AGENTS_MARKER = "## 技能优先与任务前预检（强制）"

AGENTS_SECTION = """## 技能优先与任务前预检（强制）

### 强制规则
- **执行任何任务前，必须先检查当前会话已可用技能列表**，优先复用现有技能，再决定是否直接实现。
- **如果用户点名某个技能，或任务语义明显命中某个技能描述，必须先读取对应 `SKILL.md`，再继续执行任务。**
- **如果当前没有合适技能，必须先使用 `find-skills` 进行搜索**，确认是否已有可复用技能，再决定自行实现。
- 找到合适技能后，优先采用最小可行接入方案：先读取说明、复用现有脚本或模板、最后再补充必要改动。
- 若安装该技能涉及用户级或全局改动，应先确认，再执行。

### 标准流程
1. 解析任务目标、领域和交付物。
2. 先运行 `./scripts/skill-preflight.py "<任务描述>"`，检查当前本地技能是否直接匹配。
3. 若无直接匹配，使用 `./scripts/skill-preflight.py "<任务描述>" --remote` 或直接调用 `find-skills` 搜索候选技能。
4. 选定技能后先读 `SKILL.md`，按技能流程执行。
5. 若确实无可用技能，再按通用工程流程实现。

### 落地要求
- 每次任务开始时，先运行 `./scripts/skill-preflight.py "<任务描述>"`，并在首条执行说明里简要说明本次使用了哪些技能，或明确说明为什么没有可用技能。
- 具体操作说明见 `docs/skill-preflight-usage.md`。
- 对重复出现的工作流改进，优先沉淀到 `AGENTS.md` 或相关技能，而不是只在当前对话里临时处理。
- 对命令失败、用户纠正、缺失能力、流程改进，优先记录到项目级 `.learnings/`。
"""

MINIMAL_AGENTS_HEADER = """# Project Instructions

本文件记录当前仓库的通用协作规范。

"""

LEARNINGS_TEMPLATE = """# Learnings

用于记录本仓库中的纠错、经验、知识缺口和可复用最佳实践。

可选分类：`correction` | `insight` | `knowledge_gap` | `best_practice`
可选领域：`frontend` | `backend` | `infra` | `tests` | `docs` | `config`
可选状态：`pending` | `in_progress` | `resolved` | `wont_fix` | `promoted` | `promoted_to_skill`
"""

ERRORS_TEMPLATE = """# Errors

用于记录命令失败、外部集成失败和可复现的环境问题。
"""

FEATURE_REQUESTS_TEMPLATE = """# Feature Requests

用于记录当前工作流中缺失但高价值的能力，便于后续沉淀为技能、脚本或仓库规范。
"""

USAGE_DOC_TEMPLATE = """# 技能预检使用说明

这份说明面向当前仓库的协作者，目的是把“先查技能，再执行任务”的流程固定下来，减少重复实现和技能漏用。

## 先看结论

处理任何任务前，先做这三步：

1. 运行 `./scripts/skill-preflight.py "<任务描述>"`
2. 如果本地技能不贴合，再运行 `./scripts/skill-preflight.py "<任务描述>" --remote`
3. 读最相关的 `SKILL.md`，确认流程后再开始执行任务

如果没有合适技能，再按通用工程流程直接实现。

## 标准流程

### 1. 本地预检

```bash
./scripts/skill-preflight.py "优化 React 页面性能"
```

脚本会扫描这些目录：

- `./skills`
- `~/.codex/skills`
- `~/.agents/skills`
- `~/.claude/skills`

### 2. 远程搜索

```bash
./scripts/skill-preflight.py "Kubernetes 成本异常分析" --remote
```

脚本会自动调用：

```bash
npx -y skills find "Kubernetes 成本异常分析"
```

### 3. 读取技能说明

选中技能后，先读对应 `SKILL.md`，确认：

- 触发条件是否真的匹配
- 是否有现成脚本、模板、参考文件
- 有没有额外限制或推荐顺序

### 4. 开始任务

在首条执行说明里写清楚：

- 本次准备使用哪些技能
- 如果没有使用技能，原因是什么
- 是否需要把错误或经验沉淀到 `.learnings/`

## 安装远程技能

```bash
npx skills add <owner/repo@skill> -g -y
```

安装前先判断：

1. 这个技能是否会重复使用
2. 它是否真的比直接实现更省时间
3. 安装是否会影响其他项目

## `.learnings/` 什么时候写

- `LEARNINGS.md`：稳定流程、最佳实践、值得推广的经验
- `ERRORS.md`：需要调查的错误、容易复发的环境问题
- `FEATURE_REQUESTS.md`：值得后续做成脚本、hook 或技能的能力缺口

## 项目内自动提醒

当前仓库已经配置项目级提醒：

- `.codex/settings.json`
- `.claude/settings.json`

它们只影响当前仓库，不会污染全局环境。
"""

BOOTSTRAP_DOC_TEMPLATE = """# 仓库初始化模板说明

这个脚本用于把“技能预检 + 项目级 hooks + `.learnings` + 使用说明”一键落到新的仓库目录。

## 用法

```bash
./scripts/bootstrap-skill-preflight.py /path/to/target-repo
```

如需覆盖已存在的模板文件：

```bash
./scripts/bootstrap-skill-preflight.py /path/to/target-repo --force
```

先看计划但不落盘：

```bash
./scripts/bootstrap-skill-preflight.py /path/to/target-repo --dry-run
```

## 默认写入内容

- `scripts/skill-preflight.py`
- `scripts/hooks/skill-preflight-reminder.sh`
- `scripts/hooks/error-learning-reminder.sh`
- `.codex/settings.json`
- `.claude/settings.json`
- `.learnings/LEARNINGS.md`
- `.learnings/ERRORS.md`
- `.learnings/FEATURE_REQUESTS.md`
- `docs/skill-preflight-usage.md`
- `AGENTS.md` 中的技能预检片段

## 设计原则

- 只写项目级配置，不碰用户全局环境
- 已存在的 `AGENTS.md` 采用追加片段，不整文件覆盖
- 已存在的设置文件采用合并 hooks，不粗暴覆盖
- 已存在的文件默认跳过，只有 `--force` 才覆盖
"""

HOOKS_CONFIG = {
    "UserPromptSubmit": [
        {
            "matcher": "",
            "hooks": [
                {
                    "type": "command",
                    "command": "./scripts/hooks/skill-preflight-reminder.sh",
                }
            ],
        }
    ],
    "PostToolUse": [
        {
            "matcher": "Bash",
            "hooks": [
                {
                    "type": "command",
                    "command": "./scripts/hooks/error-learning-reminder.sh",
                }
            ],
        }
    ],
}

SCAFFOLD_FILES = {
    ".learnings/LEARNINGS.md": LEARNINGS_TEMPLATE,
    ".learnings/ERRORS.md": ERRORS_TEMPLATE,
    ".learnings/FEATURE_REQUESTS.md": FEATURE_REQUESTS_TEMPLATE,
    "docs/skill-preflight-usage.md": USAGE_DOC_TEMPLATE,
}

COPY_FILES = {
    "scripts/skill-preflight.py": "scripts/skill-preflight.py",
    "scripts/hooks/skill-preflight-reminder.sh": "scripts/hooks/skill-preflight-reminder.sh",
    "scripts/hooks/error-learning-reminder.sh": "scripts/hooks/error-learning-reminder.sh",
}


@dataclass
class Context:
    source_root: Path
    target_root: Path
    force: bool
    dry_run: bool
    actions: List[str]

    def log(self, message: str) -> None:
        self.actions.append(message)
        print(message)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="把技能预检工作流一键初始化到目标仓库。")
    parser.add_argument("target", help="目标仓库路径")
    parser.add_argument("--force", action="store_true", help="覆盖已存在的模板文件")
    parser.add_argument("--dry-run", action="store_true", help="只打印计划，不写入文件")
    return parser.parse_args()


def ensure_parent(path: Path, dry_run: bool) -> None:
    if dry_run:
        return
    path.parent.mkdir(parents=True, exist_ok=True)


def write_text_file(context: Context, relative_path: str, content: str) -> None:
    target = context.target_root / relative_path
    exists = target.exists()
    if exists and not context.force:
        context.log(f"SKIP  {relative_path} (已存在)")
        return
    context.log(f"WRITE {relative_path}")
    if context.dry_run:
        return
    ensure_parent(target, False)
    target.write_text(content.rstrip() + "\n", encoding="utf-8")


def copy_file(context: Context, source_relative_path: str, target_relative_path: str) -> None:
    source = context.source_root / source_relative_path
    target = context.target_root / target_relative_path
    exists = target.exists()
    if exists and not context.force:
        context.log(f"SKIP  {target_relative_path} (已存在)")
        return
    context.log(f"COPY  {target_relative_path}")
    if context.dry_run:
        return
    ensure_parent(target, False)
    shutil.copy2(source, target)
    source_mode = stat.S_IMODE(source.stat().st_mode)
    target.chmod(source_mode)


def load_json(path: Path) -> Dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"JSON 解析失败: {path} -> {exc}") from exc


def hook_exists(items: List[Dict], matcher: str, command: str) -> bool:
    for item in items:
        if item.get("matcher", "") != matcher:
            continue
        for hook in item.get("hooks", []):
            if hook.get("command") == command:
                return True
    return False


def merge_hooks_settings(existing: Dict) -> Dict:
    merged = dict(existing) if existing else {}
    hooks = merged.setdefault("hooks", {})
    for event_name, desired_entries in HOOKS_CONFIG.items():
        current_entries = hooks.setdefault(event_name, [])
        for desired_entry in desired_entries:
            matcher = desired_entry.get("matcher", "")
            commands = [hook.get("command") for hook in desired_entry.get("hooks", [])]
            if all(hook_exists(current_entries, matcher, command) for command in commands):
                continue
            current_entries.append(desired_entry)
    return merged


def write_settings(context: Context, relative_path: str) -> None:
    target = context.target_root / relative_path
    context.log(f"MERGE {relative_path}")
    if context.dry_run:
        return
    ensure_parent(target, False)
    merged = merge_hooks_settings(load_json(target))
    target.write_text(json.dumps(merged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_agents(context: Context) -> None:
    target = context.target_root / "AGENTS.md"
    if target.exists():
        current = target.read_text(encoding="utf-8")
        if AGENTS_MARKER in current:
            context.log("SKIP  AGENTS.md (已包含技能预检片段)")
            return
        context.log("APPEND AGENTS.md")
        if context.dry_run:
            return
        separator = "\n\n" if not current.endswith("\n\n") else ""
        target.write_text(current.rstrip() + separator + AGENTS_SECTION + "\n", encoding="utf-8")
        return
    context.log("WRITE AGENTS.md")
    if context.dry_run:
        return
    target.write_text(MINIMAL_AGENTS_HEADER + AGENTS_SECTION + "\n", encoding="utf-8")


def bootstrap(context: Context) -> None:
    context.log(f"目标仓库: {context.target_root}")
    context.log(f"模式: {'dry-run' if context.dry_run else 'write'}")
    context.log(f"覆盖模式: {'on' if context.force else 'off'}")
    for source_relative_path, target_relative_path in COPY_FILES.items():
        copy_file(context, source_relative_path, target_relative_path)
    for relative_path, content in SCAFFOLD_FILES.items():
        write_text_file(context, relative_path, content)
    write_settings(context, ".codex/settings.json")
    write_settings(context, ".claude/settings.json")
    update_agents(context)


def main() -> int:
    args = parse_args()
    source_root = Path(__file__).resolve().parents[1]
    target_root = Path(args.target).expanduser().resolve()
    if not target_root.exists() and not args.dry_run:
        target_root.mkdir(parents=True, exist_ok=True)
    context = Context(
        source_root=source_root,
        target_root=target_root,
        force=args.force,
        dry_run=args.dry_run,
        actions=[],
    )
    bootstrap(context)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
