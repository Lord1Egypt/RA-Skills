"""
Secretary Skill CLI — a reusable command-line interface.

Commands:
  /init_goal [text]   — launch the de-ambiguation engine
  /split --depth N    — hierarchically break down the locked goal
  /schedule --freq F  — map tasks onto a timeline, output cron config
  /align              — recalibrate tactical steps without losing the goal
  /status --report    — evaluate progress toward the final goal
"""

import json
import sys
from pathlib import Path
from typing import Optional

from .engine import (
    DeambiguationEngine,
    VerticalSplitter,
    CronScheduler,
    Goal,
)
from .markdown_store import PlanStore


class SecretaryCLI:
    """Interactive CLI for the Secretary Skill."""

    def __init__(self, output_dir: str = "plans"):
        self.goal: Optional[Goal] = None
        self.splitter: Optional[VerticalSplitter] = None
        self.scheduler = CronScheduler()
        self.de_engine = DeambiguationEngine()
        self.store = PlanStore(output_dir)
        self.plan_file: Optional[Path] = None

    # ── /init_goal ────────────────────────────────────────────────────

    def cmd_init_goal(self, text: str):
        """De-ambiguate a vague vision into a concrete goal — one question at a time."""
        self.de_engine.set_raw_text(text)
        print(f"\n  📝 你的目标：{text}\n")
        print("  让我陪你把这个想法理清楚。一次只聊一个问题。\n")

        while True:
            q = self.de_engine.next_question()
            if q is None:
                print("  看起来这个话题我们已经聊得差不多了。")
                break

            print(f"  ❓ {q}")
            answer = input("  > ") or "TBD"
            # Map back to the topic of the current question
            current_q = self.de_engine.QUESTION_BANK[self.de_engine._current_index]
            self.de_engine.record_answer(current_q["topic"], q, answer)

            # After each answer, give a lightweight reflection and check readiness
            print(f"  ✓ 记下了。")
            print()
            ready = input("  现在这个目标对你来说清晰了吗？清楚了就告诉我「清楚了」，还想再聊聊就按回车继续 > ").strip().lower()

            if ready in ("清楚了", "清晰了", "是", "clear", "y", "yes"):
                if self.de_engine.is_goal_clear(user_says_clear=True):
                    print("\n  ✅ 好，目标已经足够清晰，可以进入下一步了。")
                    break
                else:
                    print("  快了，还有几个关键问题聊完就更稳了——")
                    # continue loop
            print()

        self.goal = self.de_engine.lock_goal(text)
        print(f"\n  ✅ Goal Locked（目标已锁定）:")
        print(f"     {self.goal.refined_statement}\n")
        print("  判断标准：")
        for c in self.goal.success_criteria:
            print(f"     • {c}")

        save = input("\n  💾 把目标存为计划文档？(Y/n): ").strip().lower()
        if save != "n":
            self.plan_file = self.store.save_goal(self.goal)
            print(f"     已保存 → {self.plan_file}")
        return self.goal

    # ── /split ────────────────────────────────────────────────────────

    def cmd_split(self, depth: int = 2):
        """Break the locked goal into milestones and atomic tasks."""
        if self.goal is None:
            print("  ❌ No goal locked. Run /init_goal first.")
            return

        self.splitter = VerticalSplitter(self.goal, depth=depth)
        print(f"\n  🔨 Splitting goal (depth={depth})...\n")

        n_ms = int(input("  How many milestones? "))
        for i in range(n_ms):
            title = input(f"  Milestone {i+1} title: ")
            desc = input(f"  Milestone {i+1} description: ")
            dl = input(f"  Milestone {i+1} deadline (optional): ") or None
            ms = self.splitter.add_milestone(title, desc, dl)

            n_tasks = int(input(f"    Tasks for '{title}' (count): "))
            for j in range(n_tasks):
                t_desc = input(f"    Task {j+1} description: ")
                dur = input(f"    Duration min (default 120): ") or "120"
                self.splitter.add_task(ms.id, t_desc, int(dur))

        print(f"\n  ✅ {len(self.splitter.milestones)} milestones, "
              f"{sum(len(m.tasks) for m in self.splitter.milestones)} tasks")

        if self.plan_file:
            self.store.save_plan(self.goal, self.splitter.milestones,
                                 str(self.plan_file))
            print(f"     Plan updated → {self.plan_file}")
        else:
            save = input("  💾 Save this plan to a file? (Y/n): ").strip().lower()
            if save != "n":
                self.plan_file = self.store.save_plan(
                    self.goal, self.splitter.milestones)
                print(f"     Saved → {self.plan_file}")
        return self.splitter

    # ── /schedule ─────────────────────────────────────────────────────

    def cmd_schedule(self, freq: str = "daily"):
        """Generate cron automation payload from tasks."""
        if not self.splitter or not self.goal:
            print("  ❌ No goal or split data. Run /init_goal and /split first.")
            return

        jobs = []
        for ms in self.splitter.milestones:
            for task in ms.tasks:
                job = self.scheduler.schedule(
                    task, freq=freq,
                    goal_snapshot=self.goal.refined_statement,
                )
                jobs.append(self.scheduler.to_json(job))

        print(f"\n  ⏰ Cron Jobs Generated ({len(jobs)} tasks, freq={freq}):\n")
        print(json.dumps(jobs, indent=2, ensure_ascii=False))
        return jobs

    # ── /align ────────────────────────────────────────────────────────

    def cmd_align(self):
        """Recalibrate when plans change or friction occurs."""
        if self.goal is None:
            print("  ❌ No goal to align. Run /init_goal first.")
            return

        print(f"\n  🔄 Aligning...\n")
        print(f"     Original goal: {self.goal.refined_statement}")
        print(f"     Criteria: {self.goal.success_criteria}\n")

        what_changed = input("  What changed or went wrong? ")
        adjustment = input("  Proposed adjustment? ")
        note = f"{what_changed} → {adjustment}"

        self.goal.raw_text += f"\n     [align]: {note}"

        if self.plan_file:
            self.store.add_alignment(str(self.plan_file), note)
            print(f"     Alignment logged → {self.plan_file}")
        else:
            print(f"     ⚠️  No plan file to persist alignment (run /init_goal first).")

        print(f"\n  ✅ Realigned. Goal preserved: {self.goal.refined_statement}")

    # ── /status ───────────────────────────────────────────────────────

    def cmd_status(self, plan_path: Optional[str] = None):
        """Show progress toward the final goal."""
        if plan_path:
            loaded_goal, loaded_ms = self.store.load_plan(plan_path)
            self.goal = loaded_goal
            self.splitter = VerticalSplitter(loaded_goal)
            self.splitter.milestones = loaded_ms
            self.plan_file = Path(plan_path)

        if self.goal is None:
            print("  ❌ No goal set. Run /init_goal or provide --plan.")
            return

        print(f"\n  📊 Status Report\n")
        print(f"     Goal: {self.goal.refined_statement}")
        print(f"     Success Criteria: {self.goal.success_criteria}\n")

        if self.splitter and self.splitter.milestones:
            total = sum(len(m.tasks) for m in self.splitter.milestones)
            done = sum(
                1 for m in self.splitter.milestones
                for t in m.tasks if t.done
            )
            pct = (done / total * 100) if total else 0
            bar = "█" * int(pct // 10) + "░" * (10 - int(pct // 10))

            print(f"     Progress: [{bar}] {pct:.0f}%")
            print(f"     Tasks: {done}/{total} completed\n")

            for ms in self.splitter.milestones:
                print(f"     📁 {ms.title}")
                for t in ms.tasks:
                    ck = "✅" if t.done else "⬜"
                    print(f"       {ck} {t.description}  `{t.id}`")
                print()

            if self.plan_file:
                mark_done = input(
                    "  🎯 Mark a task done? (enter task id, or blank to skip): "
                ).strip()
                if mark_done:
                    found = self.store.update_task_status(
                        str(self.plan_file), mark_done, done=True)
                    if found:
                        for ms in self.splitter.milestones:
                            for t in ms.tasks:
                                if t.id == mark_done:
                                    t.done = True
                        print(f"     ✅ {mark_done} marked done.")
                    else:
                        print(f"     ⚠️  Task '{mark_done}' not found.")
        else:
            print("     No milestones defined yet.\n")
            if self.plan_file:
                print(f"     Plan file: {self.plan_file}")


def main():
    args = sys.argv[1:]

    if not args:
        print("Usage: secretary <command> [args] [--output DIR] [--plan FILE]")
        print("Commands: /init_goal, /split, /schedule, /align, /status")
        sys.exit(1)

    command = args[0]

    # global options
    output_dir = "plans"
    plan_file: Optional[str] = None
    filtered = []
    i = 1
    while i < len(args):
        if args[i] == "--output" and i + 1 < len(args):
            output_dir = args[i + 1]
            i += 2
        elif args[i] == "--plan" and i + 1 < len(args):
            plan_file = args[i + 1]
            i += 2
        else:
            filtered.append(args[i])
            i += 1

    cli = SecretaryCLI(output_dir=output_dir)

    if command == "/init_goal":
        text = " ".join(filtered) or input("Enter your goal: ")
        cli.cmd_init_goal(text)
    elif command == "/split":
        depth = int(filtered[1]) if len(filtered) > 1 and filtered[0] == "--depth" else 2
        cli.cmd_split(depth)
    elif command == "/schedule":
        freq = filtered[1] if len(filtered) > 1 and filtered[0] == "--freq" else "daily"
        cli.cmd_schedule(freq)
    elif command == "/align":
        cli.cmd_align()
    elif command == "/status":
        cli.cmd_status(plan_path=plan_file)
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
