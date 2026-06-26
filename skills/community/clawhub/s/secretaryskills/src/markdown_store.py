"""
Markdown-based persistence for plans.

Saves and loads structured plan data (Goal, Milestones, AtomicTasks)
as readable Markdown files, compatible with agent memory systems.
"""

import re
from datetime import datetime
from pathlib import Path
from typing import Optional

from .engine import Goal, Milestone, AtomicTask


def _slugify(text: str, max_len: int = 60) -> str:
    """Convert text to a filesystem-safe slug."""
    slug = re.sub(r"[^\w\s-]", "", text.lower())
    slug = re.sub(r"[-\s]+", "-", slug).strip("-")
    return slug[:max_len].rstrip("-")


class PlanStore:
    """Persist and load plans as Markdown files.

    File naming: ``plans/{slug}.md`` by default.
    Each file records the goal, success criteria, alignment log,
    milestones, and atomic tasks with completion status.
    """

    def __init__(self, output_dir: str = "plans"):
        self.output_dir = Path(output_dir)

    # ── public API ─────────────────────────────────────────────────────

    def save_goal(self, goal: Goal) -> Path:
        """Save a newly locked goal as a Markdown file (milestones TBD)."""
        path = self._resolve_path(goal)
        content = self._render_goal_only(goal)
        return self._write(path, content)

    def save_plan(
        self, goal: Goal, milestones: list[Milestone],
        filepath: Optional[str] = None,
    ) -> Path:
        """Save or refresh the full plan with milestones and tasks."""
        path = Path(filepath) if filepath else self._resolve_path(goal)
        content = self._render_full(goal, milestones)
        return self._write(path, content)

    def load_plan(self, filepath: str) -> tuple[Goal, list[Milestone]]:
        """Load a plan from a Markdown file back into objects."""
        text = Path(filepath).read_text(encoding="utf-8")
        return self._parse(text)

    def update_task_status(
        self, filepath: str, task_id: str, done: bool,
    ) -> bool:
        """Toggle a single task's checkbox by its ID. Returns True if found."""
        path = Path(filepath)
        text = path.read_text(encoding="utf-8")
        marker = f"`{task_id}`"
        new_lines = []
        found = False
        for line in text.splitlines():
            if marker in line and line.strip().startswith("- ["):
                checkbox = "[x]" if done else "[ ]"
                line = re.sub(r"- \[.\]", f"- {checkbox}", line, count=1)
                found = True
            new_lines.append(line)
        if found:
            path.write_text("\n".join(new_lines), encoding="utf-8")
        return found

    def add_alignment(self, filepath: str, note: str) -> None:
        """Append an alignment record to the plan file."""
        path = Path(filepath)
        text = path.read_text(encoding="utf-8")
        ts = datetime.now().strftime("%Y-%m-%d %H:%M")
        entry = f"- {ts}: {note}"
        # Insert right after the Alignment Log heading (or before the separator)
        marker = "## 校准记录 / Alignment Log"
        if marker in text:
            # find the section and append after the last existing entry
            lines = text.splitlines()
            new_lines = []
            in_section = False
            appended = False
            for line in lines:
                new_lines.append(line)
                if line.strip() == marker:
                    in_section = True
                elif in_section and line.strip().startswith("- "):
                    pass  # existing entries, keep going
                elif in_section and not appended:
                    new_lines.append(entry)
                    appended = True
                    in_section = False
            if not appended:
                new_lines.append(entry)
            path.write_text("\n".join(new_lines), encoding="utf-8")
        else:
            # fallback: append before last ---
            text = text.replace(
                "\n---\n", f"\n{marker}\n\n{entry}\n\n---\n", 1
            )
            path.write_text(text, encoding="utf-8")

    # ── path resolution ────────────────────────────────────────────────

    def _resolve_path(self, goal: Goal) -> Path:
        slug = _slugify(goal.refined_statement)
        return self.output_dir / f"{slug}.md"

    @staticmethod
    def _write(path: Path, content: str) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    # ── rendering ──────────────────────────────────────────────────────

    def _render_goal_only(self, goal: Goal) -> str:
        return _MD_TEMPLATE_GOAL.format(
            title=goal.refined_statement,
            raw_goal=goal.raw_text,
            created=goal.created_at.strftime("%Y-%m-%d %H:%M"),
            criteria="\n".join(
                f"- {c}" for c in goal.success_criteria
            ),
        )

    def _render_full(self, goal: Goal, milestones: list[Milestone]) -> str:
        ms_blocks = []
        for ms in milestones:
            done = sum(1 for t in ms.tasks if t.done)
            total = len(ms.tasks)
            progress = f"{done}/{total}" + (" ✅" if done == total > 0 else (" 🔄" if done > 0 else " ⏳"))

            task_lines = "\n".join(
                f"  - [x] {t.description} ({t.duration_minutes} min) `{t.id}`"
                if t.done else
                f"  - [ ] {t.description} ({t.duration_minutes} min) `{t.id}`"
                for t in ms.tasks
            )

            block = _MD_MILESTONE.format(
                title=ms.title,
                description=ms.description,
                deadline=ms.deadline or "N/A",
                progress=progress,
                tasks=task_lines,
            )
            ms_blocks.append(block)

        return _MD_TEMPLATE_FULL.format(
            title=goal.refined_statement,
            raw_goal=goal.raw_text,
            created=goal.created_at.strftime("%Y-%m-%d %H:%M"),
            criteria="\n".join(
                f"- {c}" for c in goal.success_criteria
            ),
            milestones="\n\n".join(ms_blocks),
        )

    # ── parsing ────────────────────────────────────────────────────────

    def _parse(self, text: str) -> tuple[Goal, list[Milestone]]:
        lines = text.splitlines()
        title = ""
        raw_text = ""
        created_at = datetime.now()
        criteria: list[str] = []
        milestones: list[Milestone] = []
        current_ms: Optional[Milestone] = None
        in_criteria = False
        in_milestones = False

        for line in lines:
            stripped = line.strip()

            # ── title ────────────────────────────────────────────────
            m = re.match(r"^#\s+(.+)$", stripped)
            if m:
                title = m.group(1).strip()
                continue

            # ── raw goal ─────────────────────────────────────────────
            m = re.match(r"^-?\s?\*\*原始目标 / Raw Goal\*\*:\s*(.+)$", stripped)
            if m:
                raw_text = m.group(1).strip()
                continue

            m = re.match(r"^-?\s?\*\*创建时间 / Created\*\*:\s*(.+)$", stripped)
            if m:
                try:
                    created_at = datetime.strptime(
                        m.group(1).strip(), "%Y-%m-%d %H:%M"
                    )
                except ValueError:
                    pass
                continue

            # ── success criteria ─────────────────────────────────────
            if stripped == "## 成功标准 / Success Criteria":
                in_criteria = True
                continue
            if in_criteria and stripped.startswith("- "):
                criteria.append(stripped[2:])
                continue
            if in_criteria and not stripped.startswith("- ") and stripped:
                in_criteria = False

            # ── milestones ───────────────────────────────────────────
            if stripped == "---" or stripped.startswith("## 里程碑"):
                in_milestones = True
                continue

            if in_milestones:
                m = re.match(r"^###\s+(.+)$", stripped)
                if m:
                    current_ms = Milestone(
                        id=f"ms-{len(milestones) + 1}",
                        title=m.group(1).strip(),
                        description="",
                    )
                    milestones.append(current_ms)
                    continue

                if current_ms:
                    m = re.match(r"^\*\*描述 / Description\*\*:\s*(.+)$", stripped)
                    if m:
                        current_ms.description = m.group(1).strip()
                        continue

                    m = re.match(r"^\*\*截止 / Deadline\*\*:\s*(.+)$", stripped)
                    if m:
                        dl = m.group(1).strip()
                        current_ms.deadline = dl if dl != "N/A" else None
                        continue

                    # task line
                    m = re.match(
                        r"^\s*-\s+\[([ xX])\]\s+(.+?)\s+\((\d+)\s*min\)\s+`(.+?)`$",
                        stripped,
                    )
                    if m:
                        done = m.group(1) in ("x", "X")
                        desc = m.group(2).strip()
                        dur = int(m.group(3))
                        tid = m.group(4)
                        task = AtomicTask(
                            id=tid,
                            description=desc,
                            duration_minutes=dur,
                            done=done,
                        )
                        current_ms.tasks.append(task)
                        continue

        goal = Goal(
            raw_text=raw_text,
            refined_statement=title,
            success_criteria=criteria,
            created_at=created_at,
        )
        return goal, milestones


# ── Templates ────────────────────────────────────────────────────────

_MD_TEMPLATE_GOAL = """\
# {title}

- **原始目标 / Raw Goal**: {raw_goal}
- **创建时间 / Created**: {created}
- **状态 / Status**: ⏳ 进行中

## 成功标准 / Success Criteria

{criteria}

---

## 里程碑 / Milestones

*尚未拆分，请运行 `/split` 来添加里程碑和任务。*
"""

_MD_TEMPLATE_FULL = """\
# {title}

- **原始目标 / Raw Goal**: {raw_goal}
- **创建时间 / Created**: {created}
- **状态 / Status**: ⏳ 进行中

## 成功标准 / Success Criteria

{criteria}

## 校准记录 / Alignment Log

*暂无记录。*

---

## 里程碑 / Milestones

{milestones}
"""

_MD_MILESTONE = """\
### {title}

- **描述 / Description**: {description}
- **截止 / Deadline**: {deadline}
- **进度 / Progress**: {progress}

{tasks}"""
