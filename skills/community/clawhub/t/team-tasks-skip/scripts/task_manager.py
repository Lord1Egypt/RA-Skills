#!/usr/bin/env python3
"""Team Tasks — shared JSON task manager for multi-agent pipelines.

Supports two modes:
  Mode A (linear):  Fixed pipeline order, auto-advance on done
  Mode B (dag):     Tasks declare dependsOn, parallel dispatch when deps met
  Mode C (debate):  Multi-agent position + cross-review workflow

Commands:
  init      Create a new project (--mode linear|dag|debate)
  add       Add a task to a DAG project
  add-debater Add a debater to a debate project
  round     Debate round actions (start/collect/cross-review/synthesize)
  status    Show current pipeline/DAG status
  assign    Set task description for a stage/task
  update    Update stage/task status (pending/in-progress/done/failed)
  next      Get next actionable stage (linear mode)
  ready     Get all tasks whose dependencies are met (dag mode)
  log       Append a log entry to a stage/task
  result    Set the output/result of a stage/task
  reset     Reset a stage/task (or all) back to pending
  history   Show full log history for a stage/task
  graph     Show DAG dependency graph (dag mode)
  list      List all projects
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone

DEFAULT_PIPELINE = ["code-agent", "test-agent", "docs-agent", "monitor-bot"]
TASKS_DIR = os.environ.get("TEAM_TASKS_DIR", "/home/ubuntu/clawd/data/team-tasks")


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def task_file(project: str) -> str:
    return os.path.join(TASKS_DIR, f"{project}.json")


def load_project(project: str) -> dict:
    path = task_file(project)
    if not os.path.exists(path):
        print(f"Error: project '{project}' not found at {path}", file=sys.stderr)
        sys.exit(1)
    with open(path) as f:
        return json.load(f)


def save_project(project: str, data: dict):
    path = task_file(project)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def make_stage(agent_id: str, task: str = "", depends_on: list = None) -> dict:
    stage = {
        "agent": agent_id,
        "status": "pending",
        "task": task,
        "startedAt": None,
        "completedAt": None,
        "output": "",
        "logs": [],
    }
    if depends_on is not None:
        stage["dependsOn"] = depends_on
    return stage


def get_mode(data: dict) -> str:
    return data.get("mode", "linear")


def is_dag(data: dict) -> bool:
    return get_mode(data) == "dag"


def is_debate(data: dict) -> bool:
    return get_mode(data) == "debate"


def ensure_stage_mode(data: dict, command: str):
    if is_debate(data):
        print(
            f"Error: '{command}' is not supported for debate mode projects.",
            file=sys.stderr,
        )
        sys.exit(1)


def ensure_debate_mode(data: dict, command: str):
    if not is_debate(data):
        print(
            f"Error: '{command}' is only for debate mode projects. Use 'init --mode debate'.",
            file=sys.stderr,
        )
        sys.exit(1)


def compute_ready_tasks(data: dict) -> list:
    """Return task IDs whose dependencies are all done and status is pending."""
    ready = []
    for task_id, task in data["stages"].items():
        if task["status"] != "pending":
            continue
        deps = task.get("dependsOn", [])
        all_deps_done = all(
            data["stages"].get(d, {}).get("status") in ("done", "skipped")
            for d in deps
        )
        if all_deps_done:
            ready.append(task_id)
    return ready


def check_dag_completion(data: dict):
    """Update project status based on DAG task states."""
    all_tasks = data["stages"]
    statuses = [t["status"] for t in all_tasks.values()]

    if all(s in ("done", "skipped") for s in statuses):
        data["status"] = "completed"
    elif any(s == "failed" for s in statuses):
        # Check if any ready tasks remain despite failure
        ready = compute_ready_tasks(data)
        if not ready and not any(s == "in-progress" for s in statuses):
            data["status"] = "blocked"
    elif any(s in ("in-progress", "pending") for s in statuses):
        data["status"] = "active"


def detect_cycles(data: dict) -> list:
    """Detect cycles in DAG using DFS. Returns list of nodes in cycle or empty list."""
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {tid: WHITE for tid in data["stages"]}
    path = []

    def dfs(node):
        color[node] = GRAY
        path.append(node)
        for dep in data["stages"].get(node, {}).get("dependsOn", []):
            if dep not in color:
                continue
            if color[dep] == GRAY:
                cycle_start = path.index(dep)
                return path[cycle_start:]
            if color[dep] == WHITE:
                result = dfs(dep)
                if result:
                    return result
        path.pop()
        color[node] = BLACK
        return []

    for tid in data["stages"]:
        if color[tid] == WHITE:
            result = dfs(tid)
            if result:
                return result
    return []


# ── Commands ────────────────────────────────────────────────────────

def cmd_init(args):
    """Create a new project."""
    project = args.project
    path = task_file(project)
    if os.path.exists(path) and not args.force:
        print(f"Error: project '{project}' already exists. Use --force to overwrite.", file=sys.stderr)
        sys.exit(1)

    mode = args.mode or "linear"
    goal = args.goal or ""

    workspace = args.workspace or ""

    if mode == "linear":
        pipeline = args.pipeline.split(",") if args.pipeline else DEFAULT_PIPELINE
        stages = {}
        for agent in pipeline:
            stages[agent] = make_stage(agent)
        data = {
            "project": project,
            "goal": goal,
            "created": now_iso(),
            "updated": now_iso(),
            "status": "active",
            "mode": "linear",
            "workspace": workspace,
            "pipeline": pipeline,
            "currentStage": pipeline[0] if pipeline else None,
            "stages": stages,
        }
    elif mode == "dag":
        data = {
            "project": project,
            "goal": goal,
            "created": now_iso(),
            "updated": now_iso(),
            "status": "active",
            "mode": "dag",
            "workspace": workspace,
            "stages": {},
        }
    elif mode == "debate":
        data = {
            "project": project,
            "goal": goal,
            "created": now_iso(),
            "updated": now_iso(),
            "status": "active",
            "mode": "debate",
            "workspace": workspace,
            "debaters": {},
            "rounds": [],
            "currentRound": 0,
        }
    else:
        print(f"Error: mode must be 'linear', 'dag', or 'debate'", file=sys.stderr)
        sys.exit(1)

    save_project(project, data)
    print(json.dumps(data, indent=2, ensure_ascii=False))


def _debate_current_round(data: dict) -> tuple[int, dict] | tuple[None, None]:
    idx = data.get("currentRound", 0) - 1
    if idx < 0 or idx >= len(data.get("rounds", [])):
        return None, None
    return idx, data["rounds"][idx]


def _debate_record_response(data: dict, agent_id: str, round_idx: int, content: str):
    debater = data["debaters"][agent_id]
    responses = debater.setdefault("responses", [])
    round_type = data["rounds"][round_idx]["type"]
    round_num = round_idx + 1

    existing = None
    for item in responses:
        if item.get("round") == round_num and item.get("type") == round_type:
            existing = item
            break

    if existing is None:
        responses.append(
            {
                "round": round_num,
                "type": round_type,
                "response": content,
                "time": now_iso(),
            }
        )
    else:
        existing["response"] = content
        existing["time"] = now_iso()


def _debate_role(data: dict, agent_id: str) -> str:
    role = data["debaters"].get(agent_id, {}).get("role", "")
    return role or "no role specified"


def _all_debaters_responded(data: dict, round_data: dict) -> bool:
    return all(agent in round_data["responses"] for agent in data["debaters"])


def cmd_add_debater(args):
    """Add a debater to a debate project."""
    data = load_project(args.project)
    ensure_debate_mode(data, "add-debater")

    if data.get("rounds"):
        print("Error: cannot add debaters after rounds have started", file=sys.stderr)
        sys.exit(1)

    agent_id = args.agent_id
    if agent_id in data["debaters"]:
        print(f"Error: debater '{agent_id}' already exists", file=sys.stderr)
        sys.exit(1)

    data["debaters"][agent_id] = {
        "role": args.role or "",
        "responses": [],
    }
    data["updated"] = now_iso()
    save_project(args.project, data)
    role_str = f" ({args.role})" if args.role else ""
    print(f"✅ Added debater '{agent_id}'{role_str}")


def cmd_round(args):
    """Debate round actions: start/collect/cross-review/synthesize."""
    data = load_project(args.project)
    ensure_debate_mode(data, "round")
    action = args.action

    if action == "start":
        if not data.get("debaters"):
            print("Error: add at least one debater first", file=sys.stderr)
            sys.exit(1)
        if data.get("rounds"):
            print("Error: initial round already started", file=sys.stderr)
            sys.exit(1)

        round_data = {
            "type": "initial",
            "status": "in-progress",
            "responses": {},
            "startedAt": now_iso(),
            "completedAt": None,
        }
        data["rounds"].append(round_data)
        data["currentRound"] = 1
        data["updated"] = now_iso()
        save_project(args.project, data)

        question = data.get("goal", "")
        print("🗣️  Debate Round 1 (initial) started\n")
        for agent_id in data["debaters"]:
            role = _debate_role(data, agent_id)
            print(f"Agent: {agent_id} ({role})")
            print(f"Question: {question}")
            print("Task: Provide your position and supporting reasoning.\n")
        return

    if action == "collect":
        if not args.agent_id or args.content is None:
            print("Error: usage: round <project> collect <agent-id> \"text\"", file=sys.stderr)
            sys.exit(1)

        round_idx, round_data = _debate_current_round(data)
        if round_data is None:
            print("Error: no active round. Run 'round <project> start' first.", file=sys.stderr)
            sys.exit(1)
        if round_data["status"] != "in-progress":
            print("Error: current round is not accepting responses", file=sys.stderr)
            sys.exit(1)
        if args.agent_id not in data["debaters"]:
            print(f"Error: debater '{args.agent_id}' not found", file=sys.stderr)
            sys.exit(1)

        round_data["responses"][args.agent_id] = args.content
        _debate_record_response(data, args.agent_id, round_idx, args.content)

        if _all_debaters_responded(data, round_data):
            round_data["status"] = "done"
            round_data["completedAt"] = now_iso()
            print(
                f"✅ Collected response from {args.agent_id}. "
                f"Round {round_idx + 1} ({round_data['type']}) is complete."
            )
            if round_data["type"] == "initial":
                print("➡️  Next: round <project> cross-review")
            elif round_data["type"] == "cross-review":
                print("➡️  Next: round <project> synthesize")
        else:
            missing = [a for a in data["debaters"] if a not in round_data["responses"]]
            print(f"✅ Collected response from {args.agent_id}. Waiting for: {', '.join(missing)}")

        data["updated"] = now_iso()
        save_project(args.project, data)
        return

    if action == "cross-review":
        if not data.get("rounds"):
            print("Error: initial round not started", file=sys.stderr)
            sys.exit(1)
        initial = data["rounds"][0]
        if initial["type"] != "initial":
            print("Error: invalid debate state: first round is not initial", file=sys.stderr)
            sys.exit(1)
        if initial["status"] != "done":
            print("Error: complete initial round responses before cross-review", file=sys.stderr)
            sys.exit(1)

        if len(data["rounds"]) == 1:
            cross = {
                "type": "cross-review",
                "status": "in-progress",
                "responses": {},
                "startedAt": now_iso(),
                "completedAt": None,
            }
            data["rounds"].append(cross)
            data["currentRound"] = 2
        else:
            cross = data["rounds"][1]
            if cross["type"] != "cross-review":
                print("Error: invalid debate state: second round is not cross-review", file=sys.stderr)
                sys.exit(1)
            data["currentRound"] = 2

        data["updated"] = now_iso()
        save_project(args.project, data)

        print("🔁 Cross-review prompts\n")
        for agent_id in data["debaters"]:
            role = _debate_role(data, agent_id)
            own = initial["responses"].get(agent_id, "")
            print(f"Agent: {agent_id} ({role})")
            print(f"Your previous response: {own}\n")
            print("Other debaters' responses:")
            others = [a for a in data["debaters"] if a != agent_id]
            if not others:
                print("- (none)")
            else:
                for other_id in others:
                    other_role = _debate_role(data, other_id)
                    other_resp = initial["responses"].get(other_id, "")
                    print(f"- {other_id} ({other_role}): {other_resp}")
            print(
                "\nTask: Review the other responses. Do you agree or disagree? "
                "What did they miss? Update your position if needed.\n"
            )
        return

    if action == "synthesize":
        if not data.get("rounds"):
            print("Error: no rounds found. Start with 'round <project> start'.", file=sys.stderr)
            sys.exit(1)

        initial = data["rounds"][0]
        cross = data["rounds"][1] if len(data["rounds"]) > 1 else None

        if initial["status"] != "done":
            print("Error: initial round is incomplete", file=sys.stderr)
            sys.exit(1)
        if cross and cross["type"] == "cross-review" and cross["status"] == "done":
            data["status"] = "completed"

        data["updated"] = now_iso()
        save_project(args.project, data)

        print(f"🧾 Synthesis package for {data['project']}")
        if data.get("goal"):
            print(f"Question: {data['goal']}")
        print("\nInitial positions:")
        for agent_id in data["debaters"]:
            role = _debate_role(data, agent_id)
            response = initial["responses"].get(agent_id, "(missing)")
            print(f"- {agent_id} ({role}): {response}")

        print("\nCross-reviews:")
        if not cross or cross.get("type") != "cross-review":
            print("- (cross-review round not started)")
        else:
            for agent_id in data["debaters"]:
                role = _debate_role(data, agent_id)
                review = cross["responses"].get(agent_id, "(missing)")
                print(f"- {agent_id} ({role}): {review}")

        print(
            "\nTask: Synthesize the strongest points, resolve disagreements, "
            "and produce a final recommendation."
        )
        return

    print(f"Error: unknown round action '{action}'", file=sys.stderr)
    sys.exit(1)


def cmd_add(args):
    """Add a task to a DAG project."""
    data = load_project(args.project)
    ensure_stage_mode(data, "add")
    if not is_dag(data):
        print("Error: 'add' is only for DAG mode projects. Use 'init --mode dag'.", file=sys.stderr)
        sys.exit(1)

    task_id = args.task_id
    if task_id in data["stages"]:
        print(f"Error: task '{task_id}' already exists", file=sys.stderr)
        sys.exit(1)

    agent = args.agent or task_id
    depends_on = args.depends.split(",") if args.depends else []
    task_desc = args.desc or ""

    # Validate dependencies exist
    for dep in depends_on:
        if dep not in data["stages"]:
            print(f"Error: dependency '{dep}' not found. Add it first.", file=sys.stderr)
            sys.exit(1)

    data["stages"][task_id] = make_stage(agent, task_desc, depends_on)

    # Check for cycles
    cycles = detect_cycles(data)
    if cycles:
        del data["stages"][task_id]
        print(f"Error: adding '{task_id}' creates a cycle: {' → '.join(cycles + [cycles[0]])}", file=sys.stderr)
        sys.exit(1)

    data["updated"] = now_iso()
    save_project(args.project, data)
    dep_str = f" (depends on: {', '.join(depends_on)})" if depends_on else " (no dependencies — root task)"
    print(f"✅ Added task '{task_id}' → agent: {agent}{dep_str}")


def cmd_status(args):
    """Show current project status."""
    data = load_project(args.project)

    if args.json:
        print(json.dumps(data, indent=2, ensure_ascii=False))
        return

    mode = get_mode(data)
    print(f"📋 Project: {data['project']}")
    if data.get("goal"):
        print(f"🎯 Goal: {data['goal']}")
    print(f"📊 Status: {data['status']}  |  Mode: {mode}")
    if data.get("workspace"):
        print(f"🗂️  Workspace: {data['workspace']}")

    if mode == "linear":
        print(f"▶️  Current: {data.get('currentStage', 'N/A')}")
    print()

    status_icons = {
        "pending": "⬜",
        "in-progress": "🔄",
        "done": "✅",
        "failed": "❌",
        "skipped": "⏭️",
    }

    if mode == "debate":
        debaters = data.get("debaters", {})
        rounds = data.get("rounds", [])
        print(f"  👥 Debaters: {len(debaters)}")
        for agent_id, info in debaters.items():
            role = info.get("role") or "no role specified"
            print(f"  - {agent_id}: {role}")

        if not rounds:
            print("\n  🟡 No rounds started")
            return

        print()
        for idx, round_data in enumerate(rounds, start=1):
            rtype = round_data.get("type", "?")
            rstatus = round_data.get("status", "pending")
            responses = round_data.get("responses", {})
            print(f"  🔹 Round {idx}: {rtype} [{rstatus}] ({len(responses)}/{len(debaters)} responses)")
            for agent_id, response in responses.items():
                preview = response[:80]
                if len(response) > 80:
                    preview += "..."
                print(f"     {agent_id}: {preview}")
        return

    if mode == "dag":
        ready = compute_ready_tasks(data)
        # Topological-ish display: roots first, then by depth
        displayed = set()

        def display_task(tid, indent=0):
            if tid in displayed:
                return
            displayed.add(tid)
            task = data["stages"].get(tid, {})
            icon = status_icons.get(task.get("status", "pending"), "❓")
            ready_mark = " 🟢 READY" if tid in ready else ""
            deps = task.get("dependsOn", [])
            dep_str = f" ← [{', '.join(deps)}]" if deps else ""
            prefix = "  " * indent
            print(f"{prefix}  {icon} {tid} ({task.get('agent', '?')}): {task.get('status', 'pending')}{ready_mark}{dep_str}")
            task_preview = task.get("task", "")[:60]
            if task_preview:
                print(f"{prefix}     Task: {task_preview}{'...' if len(task.get('task', '')) > 60 else ''}")
            if task.get("output"):
                out_preview = task["output"][:80]
                print(f"{prefix}     Output: {out_preview}{'...' if len(task['output']) > 80 else ''}")

        # Display root tasks first, then tasks with deps
        roots = [tid for tid, t in data["stages"].items() if not t.get("dependsOn")]
        non_roots = [tid for tid, t in data["stages"].items() if t.get("dependsOn")]
        for tid in roots:
            display_task(tid)
        for tid in non_roots:
            display_task(tid)

        if ready:
            print(f"\n  🟢 Ready to dispatch: {', '.join(ready)}")

    else:  # linear
        for i, agent in enumerate(data.get("pipeline", [])):
            stage = data["stages"].get(agent, {})
            icon = status_icons.get(stage.get("status", "pending"), "❓")
            task_preview = stage.get("task", "")[:60]
            if len(stage.get("task", "")) > 60:
                task_preview += "..."
            print(f"  {icon} {agent}: {stage.get('status', 'pending')}")
            if task_preview:
                print(f"     Task: {task_preview}")
            if stage.get("output"):
                out_preview = stage["output"][:80]
                if len(stage["output"]) > 80:
                    out_preview += "..."
                print(f"     Output: {out_preview}")

    # Progress bar
    all_tasks = list(data["stages"].values())
    done_count = sum(1 for t in all_tasks if t.get("status") in ("done", "skipped"))
    total = len(all_tasks)
    if total:
        bar = "█" * done_count + "░" * (total - done_count)
        print(f"\n  Progress: [{bar}] {done_count}/{total}")


def cmd_assign(args):
    """Set task description for a stage/task."""
    data = load_project(args.project)
    ensure_stage_mode(data, "assign")
    stage_id = args.stage
    if stage_id not in data["stages"]:
        print(f"Error: stage '{stage_id}' not found", file=sys.stderr)
        sys.exit(1)

    data["stages"][stage_id]["task"] = args.task
    data["updated"] = now_iso()
    save_project(args.project, data)
    print(f"✅ Assigned task to {stage_id}")


def cmd_update(args):
    """Update stage/task status."""
    data = load_project(args.project)
    ensure_stage_mode(data, "update")
    stage_id = args.stage
    new_status = args.status

    if stage_id not in data["stages"]:
        print(f"Error: stage '{stage_id}' not found", file=sys.stderr)
        sys.exit(1)

    valid = ("pending", "in-progress", "done", "failed", "skipped")
    if new_status not in valid:
        print(f"Error: status must be one of {valid}", file=sys.stderr)
        sys.exit(1)

    stage = data["stages"][stage_id]
    old_status = stage["status"]
    stage["status"] = new_status

    if new_status == "in-progress" and not stage["startedAt"]:
        stage["startedAt"] = now_iso()
    elif new_status in ("done", "failed", "skipped"):
        stage["completedAt"] = now_iso()

    stage["logs"].append({
        "time": now_iso(),
        "event": f"status: {old_status} → {new_status}",
    })

    if is_dag(data):
        # DAG mode: check completion and show newly ready tasks
        check_dag_completion(data)
        data["updated"] = now_iso()
        save_project(args.project, data)
        print(f"✅ {stage_id}: {old_status} → {new_status}")

        if new_status == "done":
            ready = compute_ready_tasks(data)
            if ready:
                print(f"🟢 Unblocked: {', '.join(ready)}")
            elif data["status"] == "completed":
                print("🎉 All tasks completed!")
        elif new_status == "failed":
            # Show what's still runnable despite the failure
            ready = compute_ready_tasks(data)
            if ready:
                print(f"⚠️  Failed, but these tasks can still run: {', '.join(ready)}")
            else:
                print(f"❌ Pipeline blocked — no tasks can proceed")
    else:
        # Linear mode: auto-advance currentStage
        if new_status == "done":
            pipeline = data.get("pipeline", [])
            idx = pipeline.index(stage_id) if stage_id in pipeline else -1
            if idx >= 0 and idx < len(pipeline) - 1:
                data["currentStage"] = pipeline[idx + 1]
            elif idx == len(pipeline) - 1:
                data["status"] = "completed"
                data["currentStage"] = None
        elif new_status == "failed":
            data["status"] = "blocked"

        data["updated"] = now_iso()
        save_project(args.project, data)
        print(f"✅ {stage_id}: {old_status} → {new_status}")

        if new_status == "done" and data.get("currentStage"):
            print(f"▶️  Next: {data['currentStage']}")
        elif data["status"] == "completed":
            print("🎉 Pipeline completed!")


def cmd_next(args):
    """Get next actionable stage (linear mode)."""
    data = load_project(args.project)
    ensure_stage_mode(data, "next")

    if is_dag(data):
        # In DAG mode, redirect to ready
        return cmd_ready(args)

    current = data.get("currentStage")
    if not current:
        if data["status"] == "completed":
            print("🎉 Pipeline completed — no pending stages")
        else:
            print("❌ No current stage (pipeline may be blocked)")
        return

    stage = data["stages"].get(current, {})
    result = {
        "stage": current,
        "agent": stage.get("agent", current),
        "task": stage.get("task", ""),
        "status": stage.get("status", "pending"),
        "workspace": data.get("workspace", ""),
    }

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"▶️  Next stage: {current}")
        print(f"   Agent: {result['agent']}")
        print(f"   Status: {result['status']}")
        if result["workspace"]:
            print(f"   Workspace: {result['workspace']}")
        if result["task"]:
            print(f"   Task: {result['task']}")


def cmd_ready(args):
    """Get all tasks whose dependencies are met (dag mode)."""
    data = load_project(args.project)
    ensure_stage_mode(data, "ready")

    if not is_dag(data):
        print("Hint: 'ready' is for DAG mode. Use 'next' for linear pipelines.")
        return cmd_next(args)

    if data["status"] == "completed":
        print("🎉 All tasks completed — nothing to dispatch")
        return

    ready = compute_ready_tasks(data)

    if not ready:
        in_progress = [tid for tid, t in data["stages"].items() if t["status"] == "in-progress"]
        if in_progress:
            print(f"⏳ No ready tasks — waiting for: {', '.join(in_progress)}")
        else:
            print("❌ No ready tasks (pipeline may be blocked)")
        return

    results = []
    for tid in ready:
        task = data["stages"][tid]
        deps = task.get("dependsOn", [])
        dep_outputs = {}
        for d in deps:
            dep_task = data["stages"].get(d, {})
            if dep_task.get("output"):
                dep_outputs[d] = dep_task["output"]

        entry = {
            "taskId": tid,
            "agent": task.get("agent", tid),
            "task": task.get("task", ""),
            "dependsOn": deps,
            "depOutputs": dep_outputs,
            "workspace": data.get("workspace", ""),
        }
        results.append(entry)

    if getattr(args, "json", False):
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        print(f"🟢 Ready to dispatch ({len(results)} task{'s' if len(results) > 1 else ''}):\n")
        for r in results:
            deps_str = f" ← [{', '.join(r['dependsOn'])}]" if r["dependsOn"] else ""
            print(f"  📌 {r['taskId']} → agent: {r['agent']}{deps_str}")
            if r["workspace"]:
                print(f"     Workspace: {r['workspace']}")
            if r["task"]:
                print(f"     Task: {r['task'][:80]}{'...' if len(r['task']) > 80 else ''}")
            if r["depOutputs"]:
                print(f"     Dep outputs:")
                for dep_id, out in r["depOutputs"].items():
                    print(f"       {dep_id}: {out[:60]}{'...' if len(out) > 60 else ''}")
            print()


def cmd_log(args):
    """Append a log entry to a stage/task."""
    data = load_project(args.project)
    ensure_stage_mode(data, "log")
    stage_id = args.stage

    if stage_id not in data["stages"]:
        print(f"Error: stage '{stage_id}' not found", file=sys.stderr)
        sys.exit(1)

    data["stages"][stage_id]["logs"].append({
        "time": now_iso(),
        "event": args.message,
    })
    data["updated"] = now_iso()
    save_project(args.project, data)
    print(f"📝 Log added to {stage_id}")


def cmd_result(args):
    """Set stage/task output/result."""
    data = load_project(args.project)
    ensure_stage_mode(data, "result")
    stage_id = args.stage

    if stage_id not in data["stages"]:
        print(f"Error: stage '{stage_id}' not found", file=sys.stderr)
        sys.exit(1)

    data["stages"][stage_id]["output"] = args.output
    data["updated"] = now_iso()
    save_project(args.project, data)
    print(f"✅ Result saved for {stage_id}")


def cmd_reset(args):
    """Reset stage/task(s) to pending."""
    data = load_project(args.project)
    ensure_stage_mode(data, "reset")

    if args.all:
        targets = list(data["stages"].keys())
    elif args.stage:
        targets = [args.stage]
    else:
        print("Error: specify a stage or use --all", file=sys.stderr)
        sys.exit(1)

    for stage_id in targets:
        if stage_id not in data["stages"]:
            continue
        data["stages"][stage_id]["status"] = "pending"
        data["stages"][stage_id]["startedAt"] = None
        data["stages"][stage_id]["completedAt"] = None
        data["stages"][stage_id]["output"] = ""
        data["stages"][stage_id]["logs"].append({
            "time": now_iso(),
            "event": "reset to pending",
        })

    if not is_dag(data):
        data["currentStage"] = data["pipeline"][0] if data.get("pipeline") else None
    data["status"] = "active"
    data["updated"] = now_iso()
    save_project(args.project, data)
    print(f"🔄 Reset: {', '.join(targets)}")


def cmd_history(args):
    """Show log history for a stage/task."""
    data = load_project(args.project)
    ensure_stage_mode(data, "history")
    stage_id = args.stage

    if stage_id not in data["stages"]:
        print(f"Error: stage '{stage_id}' not found", file=sys.stderr)
        sys.exit(1)

    logs = data["stages"][stage_id]["logs"]
    if not logs:
        print(f"No logs for {stage_id}")
        return

    print(f"📜 History for {stage_id}:")
    for entry in logs:
        print(f"  [{entry['time']}] {entry['event']}")


def cmd_graph(args):
    """Show DAG dependency graph."""
    data = load_project(args.project)
    ensure_stage_mode(data, "graph")

    if not is_dag(data):
        print("Graph view is only for DAG mode projects.")
        return

    status_icons = {
        "pending": "⬜",
        "in-progress": "🔄",
        "done": "✅",
        "failed": "❌",
        "skipped": "⏭️",
    }

    # Find roots (no deps)
    roots = [tid for tid, t in data["stages"].items() if not t.get("dependsOn")]
    # Find what each task unblocks
    children = {tid: [] for tid in data["stages"]}
    for tid, t in data["stages"].items():
        for dep in t.get("dependsOn", []):
            if dep in children:
                children[dep].append(tid)

    print(f"📋 {data['project']} — DAG Graph\n")

    visited = set()
    def print_tree(tid, prefix="", is_last=True):
        if tid in visited:
            icon = status_icons.get(data["stages"][tid]["status"], "❓")
            print(f"{prefix}{'└─' if is_last else '├─'} {icon} {tid} (↑ see above)")
            return
        visited.add(tid)

        task = data["stages"][tid]
        icon = status_icons.get(task["status"], "❓")
        connector = "└─" if is_last else "├─"
        agent = task.get("agent", "?")
        print(f"{prefix}{connector} {icon} {tid} [{agent}]")

        kids = children.get(tid, [])
        for i, child in enumerate(kids):
            child_prefix = prefix + ("   " if is_last else "│  ")
            print_tree(child, child_prefix, i == len(kids) - 1)

    for i, root in enumerate(roots):
        print_tree(root, "", i == len(roots) - 1)

    # Show orphans (tasks with deps that aren't reachable from roots)
    orphans = set(data["stages"].keys()) - visited
    if orphans:
        print(f"\n  ⚠️  Unreachable tasks: {', '.join(orphans)}")

    # Summary
    all_tasks = list(data["stages"].values())
    done = sum(1 for t in all_tasks if t["status"] in ("done", "skipped"))
    total = len(all_tasks)
    bar = "█" * done + "░" * (total - done)
    print(f"\n  Progress: [{bar}] {done}/{total}")


def cmd_list(args):
    """List all projects."""
    os.makedirs(TASKS_DIR, exist_ok=True)
    files = [f for f in os.listdir(TASKS_DIR) if f.endswith(".json")]
    if not files:
        print("No projects found.")
        return

    for f in sorted(files):
        name = f.replace(".json", "")
        try:
            with open(os.path.join(TASKS_DIR, f)) as fh:
                data = json.load(fh)
            goal = data.get("goal", "")[:50]
            status = data.get("status", "unknown")
            mode = data.get("mode", "linear")
            done = sum(1 for t in data.get("stages", {}).values()
                       if t.get("status") in ("done", "skipped"))
            total = len(data.get("stages", {}))
            print(f"  {name} [{status}] ({done}/{total}) mode={mode} {goal}")
        except Exception:
            print(f"  {name} [error reading]")


# ── Main ────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Team Tasks — multi-agent pipeline & DAG manager")
    sub = parser.add_subparsers(dest="command", help="Command")

    # init
    p = sub.add_parser("init", help="Create a new project")
    p.add_argument("project", help="Project name (slug)")
    p.add_argument("--goal", "-g", help="Project goal description")
    p.add_argument("--mode", "-m", choices=["linear", "dag", "debate"], default="linear",
                   help="Pipeline mode: linear (sequential), dag (dependency graph), or debate")
    p.add_argument("--pipeline", "-p", help="Comma-separated agent order (linear mode only)")
    p.add_argument("--workspace", "-w", help="Shared workspace path for all agents")
    p.add_argument("--force", "-f", action="store_true", help="Overwrite existing project")

    # add (dag only)
    p = sub.add_parser("add", help="Add a task to DAG project")
    p.add_argument("project", help="Project name")
    p.add_argument("task_id", help="Task ID (unique)")
    p.add_argument("--agent", "-a", help="Agent to assign (defaults to task_id)")
    p.add_argument("--depends", "-d", help="Comma-separated dependency task IDs")
    p.add_argument("--desc", help="Task description")

    # add-debater (debate only)
    p = sub.add_parser("add-debater", help="Add a debater to debate project")
    p.add_argument("project", help="Project name")
    p.add_argument("agent_id", help="Debater agent ID")
    p.add_argument("--role", "-r", help="Debater role/perspective")

    # round (debate only)
    p = sub.add_parser("round", help="Debate round actions")
    p.add_argument("project", help="Project name")
    p.add_argument("action", choices=["start", "collect", "cross-review", "synthesize"],
                   help="Round action")
    p.add_argument("agent_id", nargs="?", help="Debater agent ID (collect only)")
    p.add_argument("content", nargs="?", help="Response/review text (collect only)")

    # status
    p = sub.add_parser("status", help="Show project status")
    p.add_argument("project", help="Project name")
    p.add_argument("--json", "-j", action="store_true", help="Output raw JSON")

    # assign
    p = sub.add_parser("assign", help="Set task for a stage")
    p.add_argument("project", help="Project name")
    p.add_argument("stage", help="Stage/task ID")
    p.add_argument("task", help="Task description")

    # update
    p = sub.add_parser("update", help="Update stage/task status")
    p.add_argument("project", help="Project name")
    p.add_argument("stage", help="Stage/task ID")
    p.add_argument("status", help="New status: pending|in-progress|done|failed|skipped")

    # next (linear)
    p = sub.add_parser("next", help="Get next stage (linear) or ready tasks (dag)")
    p.add_argument("project", help="Project name")
    p.add_argument("--json", "-j", action="store_true", help="Output JSON")

    # ready (dag)
    p = sub.add_parser("ready", help="Get all dispatchable tasks (dag mode)")
    p.add_argument("project", help="Project name")
    p.add_argument("--json", "-j", action="store_true", help="Output JSON")

    # log
    p = sub.add_parser("log", help="Add log entry")
    p.add_argument("project", help="Project name")
    p.add_argument("stage", help="Stage/task ID")
    p.add_argument("message", help="Log message")

    # result
    p = sub.add_parser("result", help="Set stage/task output")
    p.add_argument("project", help="Project name")
    p.add_argument("stage", help="Stage/task ID")
    p.add_argument("output", help="Output/result text")

    # reset
    p = sub.add_parser("reset", help="Reset stage/task(s)")
    p.add_argument("project", help="Project name")
    p.add_argument("stage", nargs="?", help="Stage to reset (or --all)")
    p.add_argument("--all", "-a", action="store_true", help="Reset all")

    # history
    p = sub.add_parser("history", help="Show stage/task log history")
    p.add_argument("project", help="Project name")
    p.add_argument("stage", help="Stage/task ID")

    # graph (dag)
    p = sub.add_parser("graph", help="Show DAG dependency tree")
    p.add_argument("project", help="Project name")

    # list
    sub.add_parser("list", help="List all projects")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    cmds = {
        "init": cmd_init,
        "add": cmd_add,
        "add-debater": cmd_add_debater,
        "round": cmd_round,
        "status": cmd_status,
        "assign": cmd_assign,
        "update": cmd_update,
        "next": cmd_next,
        "ready": cmd_ready,
        "log": cmd_log,
        "result": cmd_result,
        "reset": cmd_reset,
        "history": cmd_history,
        "graph": cmd_graph,
        "list": cmd_list,
    }
    cmds[args.command](args)


if __name__ == "__main__":
    main()
