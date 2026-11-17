#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build a compact cold-start handoff card for new conversations or new computers.

输出位置三级：`--out` 参数 → 外部项目根/学习记录/（若解析到项目根）→ 技能包内 handoff/。
项目根不存在时照样生成卡片，只是"当前状态/最近学习/待办"三节标注为缺失并给出
设置 `SIMAGUANG_PROJECT_DIR` 的指引——不再静默写到一个不存在的绝对路径。
"""

import argparse
import datetime
from pathlib import Path

import project_paths


def head(path: Path, n: int = 25) -> str:
    if not path.exists():
        return f"[missing] {path.name}"
    return "\n".join(path.read_text(encoding="utf-8", errors="ignore").splitlines()[:n])


def tail(path: Path, n: int = 30) -> str:
    if not path.exists():
        return f"[missing] {path.name}"
    return "\n".join(path.read_text(encoding="utf-8", errors="ignore").splitlines()[-n:])


def pending(path: Path, keywords=("下一步", "待提供", "待训练", "仍待")) -> str:
    if not path.exists():
        return f"[missing] {path.name}"
    lines = [
        line.strip()
        for line in path.read_text(encoding="utf-8", errors="ignore").splitlines()
        if any(k in line for k in keywords)
    ]
    return "\n".join(lines[-12:]) or "无待办"


def main() -> int:
    parser = argparse.ArgumentParser(description="生成冷启动交接卡。")
    parser.add_argument("--out", help="输出文件路径（默认：项目根/学习记录/ 或 包内 handoff/）")
    args = parser.parse_args()

    date = datetime.date.today().isoformat()
    root = project_paths.find_project_dir()
    if args.out:
        out = Path(args.out).expanduser()
    elif root:
        out = root / "学习记录" / f"交接卡-{date}.md"
    else:
        out = Path(__file__).resolve().parent.parent / "handoff" / f"交接卡-{date}.md"

    if root:
        learning = root / "学习记录"
        state_file = root / "PIPELINE_STATE.md"
        cold_start = [
            "1. 读取项目 `AGENTS.md`，按身份和项目规则执行。",
            "2. 读取 `PIPELINE_STATE.md`，确认当前阶段和最近并入。",
            "3. 读取 `学习记录/学习日志.md` 与 `学习记录/LESSONS.md`。",
            "4. 运行 `python3 scripts/check_integration.py` 验证技能完整性。",
        ]
        current_state = head(state_file, 20)
        recent = tail(learning / "学习日志.md", 25)
        todo = pending(state_file)
    else:
        cold_start = [
            "1. 读取技能包 `SKILL.md`，按协议索引按需加载 `references/`。",
            "2. 需要外部项目根（`书籍蒸馏/`、`学习记录/`）时，先设置 `SIMAGUANG_PROJECT_DIR`。",
            "3. 运行 `python3 scripts/self_test.py` 验证技能包完整性。",
        ]
        current_state = "[no project dir]\n" + project_paths.project_dir_help()
        recent = "[no project dir] 学习日志在外部项目内，未设置 SIMAGUANG_PROJECT_DIR 时不可读。"
        todo = "[no project dir] 待办记在外部项目 PIPELINE_STATE.md 内。"

    parts = [
        f"# 司马光综合思维交接卡（{date}）",
        "",
        (f"- 项目根：`{root}`" if root else "- 项目根：未解析到（技能包按独立模式运行）"),
        "",
        "## 冷启动顺序",
        "",
        *cold_start,
        "",
        "## 当前状态",
        "",
        "```text",
        current_state,
        "```",
        "",
        "## 最近学习",
        "",
        "```text",
        recent,
        "```",
        "",
        "## 待办",
        "",
        "```text",
        todo,
        "```",
        "",
        "## 换电脑迁移",
        "",
        "1. 复制技能包目录本身即可独立使用（协议、模板、脚本都在包内）。",
        "2. 若仍有外部项目：复制该项目目录，并设置 `SIMAGUANG_PROJECT_DIR` 指向它。",
        "3. 名人图片缓存位于 `~/.cache/simaguang-celebrity/`（可重建，不必迁移）。",
        "4. 新机器装好后跑 `python3 scripts/self_test.py`，确认无缺失。",
        "",
        "生成时间：",
        date,
        "",
    ]
    text = "\n".join(parts)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    print(f"output: {out}")
    if not root:
        print(project_paths.project_dir_help())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
