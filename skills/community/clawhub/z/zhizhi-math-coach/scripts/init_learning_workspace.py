#!/usr/bin/env python3
"""Initialize a personal learning workspace for zhizhi-math-coach."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from learning_workspace_config import default_config  # noqa: E402


DEFAULT_TEXTBOOK_INDEX = "https://github.com/TapXWorld/ChinaTextbook/tree/master/小学/数学/人教版"


def school_year_for(today: dt.date) -> str:
    start = today.year if today.month >= 9 else today.year - 1
    return f"{start}-{start + 1}"


def write_file(path: Path, content: str, force: bool, written: list[Path], skipped: list[Path]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not force:
        skipped.append(path)
        return
    path.write_text(content.strip() + "\n", encoding="utf-8")
    written.append(path)


def looks_like_source_repo(path: Path) -> bool:
    return (path / "docs" / "openclaw-release.md").exists() and (path / "examples" / "student-workspace").exists()


def gitignore_template() -> str:
    return """
.DS_Store
*.log
__pycache__/
*.pyc
.venv/
venv/
.idea/
.zhizhi-math-coach/run-log.jsonl

# Installed skills can be reinstalled from ClawHub.
skills/

# Optional large or sensitive raw inputs
uploads/raw/
ocr-output/raw/
textbooks/*.pdf
"""


def readme_template(repo_name: str) -> str:
    return f"""
# {repo_name}

This is a personal learning repository for `zhizhi-math-coach`.

Open this repository as the OpenClaw workspace for daily grading, diagnosis, worksheet generation, and learning-record updates.

## Directory Roles

- `memory/`: long-term and short-term learning memory.
- `curriculum/`: grade, semester, textbook, calendar, and progress scope.
- `knowledge-points/`: reusable explanation cards and mastery rules.
- `weak-points/`: durable weak-point history.
- `mistakes/`: school and system-generated mistake books.
- `records/`: dated diagnosis and progress records.
- `worksheets/`: generated worksheet specs, printable student PDF/HTML, and answer keys.
- `site/`: optional child-facing public pages only.

## Public Repository Mode

If this repository is public for GitHub Pages, every tracked file is viewable on GitHub, not only `site/`. Non-collaborators cannot push by default, so public viewing does not let others edit `main`. Keep collaborators empty, protect `main` against force pushes and deletion, and avoid required-pull-request rules if OpenClaw should push directly.

Recommended ruleset: `main protect`, Active, bypass `Deploy keys` and `Repository admin` as `Always allow`, target `main` or `Default`, enable `Restrict updates`, `Restrict deletions`, and `Block force pushes`, and leave PR/status/signed-commit/deployment requirements disabled.

After Pages and the writable Deploy key are configured, new generated worksheets should be automatically published:

```bash
python3 skills/zhizhi-math-coach/scripts/publish_and_wait_pages.py \
  worksheets/<date-topic> \
  --workspace . \
  --base-url https://<user>.github.io/{repo_name}
```

Generated worksheets should produce `worksheet.pdf` first when Chrome/Chromium is available. Use the PDF for immediate printing or file delivery; Pages is an optional public link.

## Daily Use

Run OpenClaw in this repository and invoke:

```text
$zhizhi-math-coach 批改这张练习卷，记录薄弱项。
$zhizhi-math-coach 根据最近错题生成变式练习。
```

Sync to GitHub explicitly:

```bash
git add curriculum knowledge-points memory mistakes records weak-points worksheets site
git commit -m "Update learning records"
git push
```

## GitHub Sync Setup

OpenClaw may not have GitHub CLI, saved credentials, or a provider-level token setting. Prefer a repository-scoped GitHub Deploy key:

```bash
python3 skills/zhizhi-math-coach/scripts/prepare_github_deploy_key.py \
  --workspace . \
  --configure-remote
```

If `origin` is not configured yet, add the repository explicitly:

```bash
python3 skills/zhizhi-math-coach/scripts/prepare_github_deploy_key.py \
  --workspace . \
  --github-owner <user> \
  --repo {repo_name} \
  --configure-remote
```

Send only the printed public key to the parent. The parent adds it in GitHub repository Settings -> Deploy keys -> Add deploy key, with `Allow write access` enabled.

After the key is added:

```bash
python3 skills/zhizhi-math-coach/scripts/check_git_sync.py --workspace . --check-push
```

If this repository is public, commit only files that are safe to expose.
"""


def long_term_template(args: argparse.Namespace, today: dt.date) -> str:
    return f"""
# Long-Term Memory

## Student

- Display name: {args.student_name}
- Education system: {args.education_system}
- School entry year: {args.school_entry_year}
- Current grade baseline on {today.isoformat()}: {args.grade}{args.semester}
- Textbook: {args.textbook_edition}数学{args.textbook_volume}
- Semester rule:
  - September 1 to January 31: first semester.
  - February 1 to August 31: second semester.

## Stable Preferences

- Parent-facing output should be concise Chinese.
- Child-facing worksheets should not include answers.
- Answers and grading rules stay in `answer-key.md`.
- Worksheets are printable PDF/HTML generated from `worksheet-spec.json`.
- Practice should target the cause of mistakes, not only repeat the same surface topic.
- Parent explanations should include a short script and quick verification questions.

## Stable Learning Rules

- Separate reading/modeling mistakes from calculation mistakes.
- Track school mistakes and generated-worksheet mistakes separately.
- Repaired weak points need spaced review before they are marked mastered.
- Do not generate out-of-scope content unless the parent explicitly asks for preview.
"""


def short_term_template(args: argparse.Namespace) -> str:
    return f"""
# Short-Term Memory

## Active Observations

- Initial setup created for {args.grade}{args.semester}.
- Replace this section with recent evidence from real worksheets and school work.

## Active Priorities

1. Confirm current school progress.
2. Grade the next completed worksheet or wrong-question batch.
3. Identify high-confidence weak points before generating targeted practice.
4. Keep scheduled reminders suggestion-only unless the parent confirms action.

## Pending Checks

- Confirm whether mistakes are conceptual, reading/modeling, calculation fluency, expression, or checking-habit issues.
"""


def active_context_template(args: argparse.Namespace, today: dt.date) -> str:
    return f"""
# Active Context

- Updated: {today.isoformat()}
- Default grading mode: fast_grade_light_record
- Current grade/semester: {args.grade}{args.semester}
- Current scope: 待填写

## Active Weak Points

- 待记录

## Daily Grading Notes

- Ordinary photo grading should use this file first, then only open matching history files when needed.
- Keep this file compact. Move durable evidence into `records/`, `mistakes/`, and `weak-points/`.
"""


def local_memory_rules_template() -> str:
    return """
# Local Memory Rules

## Fast Read Order

Before grading a photo or wrong-question batch, read:

1. `memory/active-context.md`
2. `curriculum/profile.md`
3. `references/grading-diagnosis-rubric.md` from the installed skill

If `memory/active-context.md` is missing, stale, or incomplete, then read:

1. `memory/long-term.md`
2. `memory/short-term.md`
3. `records/learning-progress.md`
4. `curriculum/progress.md`

Read `curriculum/school-calendar.md` only when the semester, exam window, or break phase is unclear.

After the first image pass identifies wrong or uncertain items, read only matching history files:

- Relevant `weak-points/*.md`
- Relevant mistake book entries
- Relevant `knowledge-points/*.md` only when creating or updating a reusable explanation card

Use filename/topic search first, and do not scan full history directories for ordinary daily grading.

## Write Rules

- Put stable preferences in `memory/long-term.md`.
- Put compact current grading context in `memory/active-context.md`.
- Put active observations and next checks in `memory/short-term.md`.
- Put textbook, school calendar, and learned-scope changes in `curriculum/`.
- Put reusable explanation cards in `knowledge-points/`.
- Put dated evidence in `records/`.
- Put reusable weak-point history in `weak-points/`.
- Put wrong or uncertain items in the relevant mistake book.

## Promotion Rule

Promote a short-term observation to long-term memory only when it has repeated evidence or the parent explicitly says it should persist.
"""


def profile_template(args: argparse.Namespace) -> str:
    return f"""
# Curriculum Profile

## Student Scope

- Education system: {args.education_system}
- Grade: {args.grade}
- Semester: {args.semester}
- School year: {args.school_year}
- Subject: 数学
- Textbook edition: {args.textbook_edition}
- Textbook volume: {args.textbook_volume}
- External textbook index: {args.textbook_index}

## Current Scope

- Current unit: 待填写
- Learned topics: 待填写
- Not-yet-learned topics: 待填写

## Boundary

Use the source as a curriculum reference only. Do not copy textbook PDFs, screenshots, or problem sets into this workspace.
"""


def school_calendar_template(args: argparse.Namespace, today: dt.date) -> str:
    return f"""
# School Calendar

## Defaults

- School year: {args.school_year}
- School entry year: {args.school_entry_year}
- First semester: {args.school_year.split("-")[0]}-09-01 to {args.school_year.split("-")[1]}-01-31
- Second semester: {args.school_year.split("-")[1]}-02-01 to {args.school_year.split("-")[1]}-08-31
- Initialized date: {today.isoformat()}
- Current inferred grade/semester: {args.grade}{args.semester}

## Local Overrides

- Midterm window: 待填写
- Final window: 待填写
- Winter break: 待填写
- Summer break: 待填写

## Phase Rules

- Normal semester: use current school progress.
- Final window: prioritize all-semester mistake review.
- Winter break: repair first-semester weak points.
- Summer break: review the whole school year and lightly preview next grade.
"""


def progress_template(args: argparse.Namespace, today: dt.date) -> str:
    return f"""
# Curriculum Progress

## Current Status

- Date: {today.isoformat()}
- Grade/Semester: {args.grade}{args.semester}
- Term phase: 待确认
- Current textbook scope: 待填写

## Learned Topics

- 待填写

## Pending Or Not Yet Confirmed

- Confirm real school progress before generating broad review worksheets.

## Exam Scope

- Midterm scope: 待填写
- Final scope: 待填写
"""


def scope_template() -> str:
    return """
# Curriculum Scope

Replace this table with the real textbook and school scope.

| Unit | Knowledge Points | Typical Practice | Notes |
| --- | --- | --- | --- |
| 待填写 | 待填写 | 待填写 | 待填写 |

## Linked Knowledge Points

- Add files under `knowledge-points/` as reusable explanation cards are created.
"""


def mistakes_index_template() -> str:
    return """
# Mistake Book Index

## Files

- `mistakes/school-mistakes.md`: school papers, weekly tests, teacher handouts, official homework.
- `mistakes/system-mistakes.md`: worksheets generated by `zhizhi-math-coach`.

## Required Fields

Each entry should include:

`日期 / 学期 / 学期时间段 / 来源类型 / 来源文件 / 题号 / 题目 / 孩子答案 / 正确答案 / 错题类型 / 可能原因 / 对应薄弱项 / 复发判断 / 复练状态 / 后续处理`

## Semester Rule

- September 1 to January 31: first semester.
- February 1 to August 31: second semester.

For exam review, filter by semester, then group by weak point and recurrence status.
"""


def empty_book_template(title: str) -> str:
    return f"""
# {title}

## Entries

No entries yet.
"""


def learning_progress_template(args: argparse.Namespace, today: dt.date) -> str:
    return f"""
# Learning Progress

## Current Overview

Initialized phase: `{args.school_year} / {args.grade} / {args.semester}`

| Weak Point | Status | Latest Evidence Date | Relapse Count | Recent Evidence | Next Step |
| --- | --- | --- | --- | --- | --- |
| 待记录 | observing | {today.isoformat()} | 0 | initialized workspace | grade first worksheet or wrong-question batch |

## Dated Records

| Date | Type | Source/Topic | Result | Finding | Next Step |
| --- | --- | --- | --- | --- | --- |
| {today.isoformat()} | setup | workspace | initialized | personal learning workspace created | fill profile and grade first evidence |
"""


def directory_readme(title: str, body: str) -> str:
    return f"""
# {title}

{body}
"""


def build_files(args: argparse.Namespace, today: dt.date) -> dict[str, str]:
    repo_name = args.workspace.resolve().name
    config = default_config(args.workspace, student_name=args.student_name, timezone=args.timezone)
    return {
        "README.md": readme_template(repo_name),
        ".gitignore": gitignore_template(),
        ".zhizhi-math-coach/config.json": json.dumps(config, ensure_ascii=False, indent=2),
        "memory/long-term.md": long_term_template(args, today),
        "memory/active-context.md": active_context_template(args, today),
        "memory/short-term.md": short_term_template(args),
        "memory/local-memory-rules.md": local_memory_rules_template(),
        "curriculum/profile.md": profile_template(args),
        "curriculum/school-calendar.md": school_calendar_template(args, today),
        "curriculum/progress.md": progress_template(args, today),
        "curriculum/scope.md": scope_template(),
        "mistakes/index.md": mistakes_index_template(),
        "mistakes/school-mistakes.md": empty_book_template("School Mistakes"),
        "mistakes/system-mistakes.md": empty_book_template("System Worksheet Mistakes"),
        "records/learning-progress.md": learning_progress_template(args, today),
        "knowledge-points/README.md": directory_readme(
            "Knowledge Points",
            "Store reusable parent explanation cards, student summaries, doing tips, common errors, and mastery evidence here.",
        ),
        "weak-points/README.md": directory_readme(
            "Weak Points",
            "Store durable weak-point records here. Update existing weak-point files when relapse, transfer failure, or spaced forgetting appears.",
        ),
        "worksheets/README.md": directory_readme(
            "Worksheets",
            "Store generated worksheet specs, printable child-facing PDF/HTML, and answer keys in dated subdirectories.",
        ),
        "site/README.md": directory_readme(
            "Public Site",
            "Only publish child-facing worksheet PDF/HTML here. Do not place answer keys, records, memory, uploads, or textbook-derived raw material in this directory.",
        ),
    }


def parse_args() -> argparse.Namespace:
    today = dt.date.today()
    parser = argparse.ArgumentParser(description="Initialize a zhizhi-math-coach personal learning workspace.")
    parser.add_argument("--workspace", type=Path, default=Path("."), help="Personal learning repository root. Defaults to current directory.")
    parser.add_argument("--student-name", default="孩子", help="Display name or nickname to store in memory.")
    parser.add_argument("--education-system", default="中国大陆小学")
    parser.add_argument("--school-entry-year", default=str(today.year if today.month >= 9 else today.year - 1))
    parser.add_argument("--school-year", default=school_year_for(today), help="School year, for example 2025-2026.")
    parser.add_argument("--grade", default="一年级")
    parser.add_argument("--semester", default="下学期")
    parser.add_argument("--textbook-edition", default="人教版")
    parser.add_argument("--textbook-volume", default="一年级下册")
    parser.add_argument("--textbook-index", default=DEFAULT_TEXTBOOK_INDEX)
    parser.add_argument("--timezone", default="Asia/Shanghai", help="IANA timezone for scheduled reminders, for example Asia/Shanghai.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files. Use carefully.")
    parser.add_argument(
        "--allow-source-repo",
        action="store_true",
        help="Allow initialization inside the reusable skill source repository. Intended only for sanitized development examples.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    args.workspace = args.workspace.resolve()
    today = dt.date.today()
    files = build_files(args, today)
    written: list[Path] = []
    skipped: list[Path] = []

    args.workspace.mkdir(parents=True, exist_ok=True)
    if looks_like_source_repo(args.workspace) and not args.allow_source_repo:
        print(
            "error: workspace looks like the reusable zhizhi-math-coach-openclaw source repository; "
            "initialize a separate personal learning repository instead, or pass --allow-source-repo for sanitized development work",
            file=sys.stderr,
        )
        return 2

    for rel_path, content in files.items():
        write_file(args.workspace / rel_path, content, args.force, written, skipped)

    print(f"workspace: {args.workspace}")
    print(f"written: {len(written)}")
    for path in written:
        print(f"  + {path.relative_to(args.workspace)}")
    if skipped:
        print(f"skipped existing files: {len(skipped)}")
        for path in skipped:
            print(f"  = {path.relative_to(args.workspace)}")
        print("use --force to overwrite existing files")
    print("next: review curriculum/profile.md and memory/long-term.md, then commit from the personal repository")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
