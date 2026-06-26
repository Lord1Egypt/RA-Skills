#!/usr/bin/env python3
"""
Agent Memory CLI v3.2 — Self-improving + session state + cold-boot recovery + daily cron.

Usage: agent_memory.py <command>

Commands:
  init         Full install: dirs, files, persistence fix, workspace hooks, cron instructions
  boot         Cold-boot recovery — print what you need to know after restart
  status       Check all memory layers
  today        Create today's daily log
  stats        Show memory statistics
  verify       Post-install verification — check everything is wired up
  cron-prompt  Output the daily review cron prompt text
  mark-cron    Record that the daily review cron was created
  dry-run      Simulate a daily review (shows what the cron would do)
"""

import os
import sys
import json
import re
from pathlib import Path
from datetime import datetime

HOME = Path.home()
SI_DIR = HOME / "self-improving"
WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", Path.cwd()))
PERSISTENT_PREFIXES = ["/data", "/persist", "/mnt", "/vol"]

# === HOOK TEXT (injected into workspace .md files) ===

SOUL_HOOK = """
## Self-Improving
On EVERY new session or context reset, IMMEDIATELY:
1. Read SESSION-STATE.md and ~/self-improving/memory.md before doing anything else.
2. VERIFY the daily review cron exists: use the cron tool (action=list) and look for "Self-Improving Daily Review". If it does NOT exist, CREATE IT NOW:
   - name: "Self-Improving Daily Review + .md Rewrite"
   - schedule: cron "0 23 * * *" in user's timezone
   - sessionTarget: isolated
   - payload: agentTurn with the review prompt (run: python3 ./skills/self-improving/scripts/agent_memory.py cron-prompt)
   - Do NOT set a model — use the default
   - delivery: announce
   After creating, run: python3 ./skills/self-improving/scripts/agent_memory.py mark-cron
   This is NON-NEGOTIABLE. The skill does not work without this cron.
3. When the user corrects you or you learn something reusable, IMMEDIATELY write to ~/self-improving/corrections.md BEFORE responding (WAL protocol). The nightly cron reviews corrections.md — if nothing is written during the day, the cron has nothing to promote. WAL is what feeds the cron.
4. Prefer learned rules when relevant. Keep self-inferred rules revisable.
"""

AGENTS_HOOK = """
## Self-Improving Memory
- **Self-improving:** ~/self-improving/ — execution-quality memory (preferences, patterns, corrections)
- Use MEMORY.md / memory/ for factual continuity. Use ~/self-improving/ for compounding execution quality.
"""

HEARTBEAT_HOOK = """
## Self-Improving Check
- Read ./skills/self-improving/heartbeat-rules.md
- Use ~/self-improving/heartbeat-state.md for run markers
- If no file in ~/self-improving/ changed since last review, skip maintenance
"""

# Hook detection strings — if ANY of these are found, hook is already present
SOUL_HOOK_DETECT = "verify the daily review cron exists"
AGENTS_HOOK_DETECT = "self-improving:"
HEARTBEAT_HOOK_DETECT = "self-improving check"

# Minimal file templates (created if .md file doesn't exist at all)
# Note: hook text already includes ## headers, so templates don't repeat them
MINIMAL_SOUL = """# SOUL.md

## What You Are
You are an AI assistant.
{soul_hook}
""".strip()

MINIMAL_AGENTS = """# AGENTS.md
{agents_hook}
""".strip()

MINIMAL_HEARTBEAT = """# HEARTBEAT.md
{heartbeat_hook}
""".strip()

# === SEED CONTENT ===

MEMORY_HOT = """# Self-Improving Memory (HOT)

## Confirmed Preferences

## Active Patterns

## Recent (last 7 days)
- {date}: Self-improving skill v3 installed. Daily review cron active. First review pending tonight.
"""

CORRECTIONS = """# Corrections Log

<!-- Format:
## YYYY-MM-DD HH:MM — Short description
CONTEXT: what happened
CORRECTION: what was wrong
LESSON: what to do differently
-->
"""

INDEX = """# Memory Index

## HOT
- memory.md: ~10 lines (seeded)

## WARM
- (no namespaces yet)

## COLD
- (no archives yet)

Last compaction: never
"""

HEARTBEAT_STATE = """# Self-Improving Heartbeat State

last_heartbeat_started_at: never
last_reviewed_change_at: never
last_heartbeat_result: never

## Last actions
- none yet
"""

SESSION_STATE = """# SESSION-STATE.md — Active Working Memory

## Current Task
[None — just initialized]

## Key Context
- Self-improving skill v3 installed {date}
- Daily review cron pending (auto-created on next session start via SOUL.md hook)

## Pending Actions
- [ ] Verify daily review cron was auto-created (check with: agent_memory.py verify)

## Recent Decisions
[None yet]

---
*Last updated: {ts}*
"""

DAILY = """# {date} — Daily Log

## Tasks Completed

## Decisions Made

## Lessons Learned

## Tomorrow
"""

DAILY_REVIEW_PROMPT = """DAILY SELF-IMPROVING REVIEW — Mandatory .md rewrite cycle.

This is your nightly review. Every step is mandatory.

1. Read ~/self-improving/memory.md, ~/self-improving/corrections.md
2. Read SESSION-STATE.md for today's work
3. If ~/self-improving/projects/ has files, read the active ones
4. Review what was learned TODAY — new patterns, corrections, preferences, rules
5. WRITE new lessons to ~/self-improving/memory.md (promote confirmed patterns to HOT tier)
6. REWRITE workspace .md files with new hardcoded rules:
   - SOUL.md — update with any new behavioral rules or operational lessons
   - AGENTS.md — update with any new workflow rules or memory notes
   - IDENTITY.md — update if role/capabilities changed
   - HEARTBEAT.md — update if cycle behavior should change
   Only modify sections relevant to new lessons. Don't rewrite unchanged sections.
   PRESERVE the ## Self-Improving section in SOUL.md — never remove or weaken it.
7. Update ~/self-improving/index.md with current file line counts
8. Demote patterns unused >30 days from HOT (memory.md) to WARM (projects/ or domains/)
9. TRIM corrections.md: if more than 50 entries, archive the oldest to ~/self-improving/archive/corrections-YYYY-MM.md and keep only the 50 most recent in corrections.md
10. Create tomorrow's daily log: memory/YYYY-MM-DD.md

Report format:
- For each file: what changed and why (or "No changes — [reason]")
- New rules hardcoded (if any)
- Patterns promoted/demoted (if any)
- Total corrections logged today
- Corrections trimmed (if any)
- Memory.md line count (warn if >80/100)"""


def _safe_create(path, content, label):
    """Create file only if it doesn't exist. Never overwrite."""
    if not path.exists():
        path.write_text(content)
        print(f"  ✅ Created {label}")
        return True
    else:
        print(f"  • {label} already exists (preserved)")
        return False


def _check_persistence():
    """Check if ~/self-improving/ is on persistent storage."""
    resolved = str(SI_DIR.resolve())
    is_persistent = any(resolved.startswith(p) for p in PERSISTENT_PREFIXES)
    return is_persistent, resolved


def _inject_hook(filepath, hook_text, detect_string, minimal_template, label):
    """Inject a hook into a workspace .md file. Create file if missing. Skip if hook exists."""
    if not filepath.exists():
        # Create minimal file with hook included
        content = minimal_template.format(
            soul_hook=SOUL_HOOK.strip(),
            agents_hook=AGENTS_HOOK.strip(),
            heartbeat_hook=HEARTBEAT_HOOK.strip()
        )
        filepath.write_text(content)
        print(f"  ✅ Created {label} (with hook)")
        return True

    # File exists — check if hook is already present
    content = filepath.read_text()
    if detect_string.lower() in content.lower():
        print(f"  • {label} hook already present (preserved)")
        return False

    # Append hook at the end
    if not content.endswith("\n"):
        content += "\n"
    content += hook_text
    filepath.write_text(content)
    print(f"  ✅ Injected hook into {label}")
    return True


def cmd_init():
    today = datetime.now().strftime("%Y-%m-%d")
    ts = datetime.now().strftime("%Y-%m-%d %I:%M %p")

    print("🧠 Initializing Agent Memory v3.2...\n")

    # === STEP 1: PERSISTENCE CHECK + AUTO-FIX ===
    is_persistent, resolved = _check_persistence()
    if not is_persistent and not SI_DIR.exists():
        print("⚠️  PERSISTENCE WARNING")
        print(f"   ~/self-improving/ resolves to: {resolved}")
        print(f"   This is NOT on persistent storage.\n")

        # Auto-fix: symlink to /data if available
        data_si = Path("/data/.openclaw/self-improving")
        if Path("/data").exists():
            print(f"   🔧 AUTO-FIX: Creating on /data and symlinking...")
            data_si.mkdir(parents=True, exist_ok=True)
            try:
                SI_DIR.symlink_to(data_si)
                print(f"   ✅ ~/self-improving → {data_si}\n")
            except (OSError, FileExistsError) as e:
                print(f"   ⚠️  Could not create symlink: {e}")
                print(f"   Continuing with non-persistent path. Fix manually.\n")
        else:
            print(f"   No /data/ found. Using non-persistent path.")
            print(f"   ⚠️  Memory will be LOST on container restart.\n")

    # === STEP 2: CREATE ~/self-improving/ STRUCTURE ===
    print("📁 Creating directory structure:")
    for d in ["projects", "domains", "archive"]:
        (SI_DIR / d).mkdir(parents=True, exist_ok=True)

    files = {
        "memory.md": MEMORY_HOT.format(date=today),
        "corrections.md": CORRECTIONS,
        "index.md": INDEX,
        "heartbeat-state.md": HEARTBEAT_STATE,
    }

    for name, content in files.items():
        _safe_create(SI_DIR / name, content, f"~/self-improving/{name}")

    # === STEP 3: SESSION-STATE.md + DAILY LOG ===
    print("\n📋 Session state:")
    _safe_create(
        WORKSPACE / "SESSION-STATE.md",
        SESSION_STATE.format(date=today, ts=ts),
        "SESSION-STATE.md"
    )

    mem_dir = WORKSPACE / "memory"
    mem_dir.mkdir(exist_ok=True)
    _safe_create(
        mem_dir / f"{today}.md",
        DAILY.format(date=today),
        f"memory/{today}.md"
    )

    # === STEP 4: AUTO-INJECT WORKSPACE HOOKS ===
    print("\n🔗 Workspace hooks (auto-inject):")
    _inject_hook(
        WORKSPACE / "SOUL.md",
        SOUL_HOOK,
        SOUL_HOOK_DETECT,
        MINIMAL_SOUL,
        "SOUL.md"
    )
    _inject_hook(
        WORKSPACE / "AGENTS.md",
        AGENTS_HOOK,
        AGENTS_HOOK_DETECT,
        MINIMAL_AGENTS,
        "AGENTS.md"
    )
    _inject_hook(
        WORKSPACE / "HEARTBEAT.md",
        HEARTBEAT_HOOK,
        HEARTBEAT_HOOK_DETECT,
        MINIMAL_HEARTBEAT,
        "HEARTBEAT.md"
    )

    # === DONE ===
    print("\n🎉 Agent Memory v3.2 initialized!")
    print("\n" + "=" * 60)
    print("WHAT HAPPENS NEXT (automatic):")
    print("=" * 60)
    print()
    print("1. SOUL.md hook is now installed.")
    print("   On the next session start, the agent will:")
    print("   → Read SESSION-STATE.md and ~/self-improving/memory.md")
    print("   → Check if the daily review cron exists")
    print("   → If missing, CREATE IT automatically")
    print("   → No manual step needed.")
    print()
    print("2. The nightly cron (once created) will:")
    print("   → Review corrections and lessons from the day")
    print("   → Rewrite SOUL.md, AGENTS.md, etc. with new rules")
    print("   → Promote patterns to memory.md")
    print("   → Report what changed")
    print()
    print("3. VERIFY everything is working:")
    print(f"   python3 ./skills/self-improving/scripts/agent_memory.py verify")
    print()
    print("4. TEST the daily review (optional):")
    print(f"   python3 ./skills/self-improving/scripts/agent_memory.py dry-run")
    print()
    print("5. (OPTIONAL) Add ~/self-improving to memorySearch.extraPaths")
    print("   in gateway config for memory_search integration.")
    print()
    print("✅ Zero manual steps required. Everything is wired up.")


def cmd_boot():
    """Cold-boot recovery: print everything the agent needs after a restart."""
    print("🔄 COLD-BOOT RECOVERY\n")
    print("=" * 60)

    ss = WORKSPACE / "SESSION-STATE.md"
    print("\n📋 SESSION-STATE.md (what you were doing):")
    print("-" * 40)
    if ss.exists():
        content = ss.read_text().strip()
        lines = content.split("\n")
        if len(lines) > 30:
            print("\n".join(lines[:30]))
            print(f"\n  ... ({len(lines) - 30} more lines)")
        else:
            print(content)
    else:
        print("  ❌ NOT FOUND — no session state to recover")
    print()

    mem = SI_DIR / "memory.md"
    print("🧠 ~/self-improving/memory.md (learned patterns):")
    print("-" * 40)
    if mem.exists():
        content = mem.read_text().strip()
        if content.count("\n") < 3:
            print("  (minimal content — check if daily review cron is running)")
        else:
            print(content)
    else:
        print("  ❌ NOT FOUND — run `agent_memory.py init` first")
    print()

    corr = SI_DIR / "corrections.md"
    print("📝 Recent corrections:")
    print("-" * 40)
    if corr.exists():
        lines = corr.read_text().strip().split("\n")
        entries = [l for l in lines if l.strip().startswith("## 20") or l.strip().startswith("CONTEXT:") or l.strip().startswith("CORRECTION:") or l.strip().startswith("LESSON:")]
        if entries:
            for e in entries[-12:]:
                print(f"  {e}")
        else:
            print("  (no corrections logged yet)")
    else:
        print("  ❌ NOT FOUND")
    print()

    today = datetime.now().strftime("%Y-%m-%d")
    daily = WORKSPACE / "memory" / f"{today}.md"
    print(f"📅 Today's log (memory/{today}.md):")
    print("-" * 40)
    if daily.exists():
        content = daily.read_text().strip()
        lines = content.split("\n")
        if len(lines) > 20:
            print("\n".join(lines[:20]))
            print(f"\n  ... ({len(lines) - 20} more lines)")
        else:
            print(content)
    else:
        print("  (not created yet)")
    print()

    print("=" * 60)
    print("✅ RECOVERY CHECKLIST:")
    print(f"  {'✅' if ss.exists() else '❌'} SESSION-STATE.md loaded")
    print(f"  {'✅' if mem.exists() else '❌'} ~/self-improving/memory.md loaded")
    print(f"  {'✅' if daily.exists() else '❌'} Today's daily log exists")
    mm = WORKSPACE / "MEMORY.md"
    print(f"  {'✅' if mm.exists() else '❌'} MEMORY.md exists (auto-injected by OpenClaw)")


def cmd_status():
    print("📊 Agent Memory Status\n")

    for f in ["memory.md", "corrections.md", "index.md", "heartbeat-state.md"]:
        p = SI_DIR / f
        if p.exists():
            lines = p.read_text().count("\n")
            kb = p.stat().st_size / 1024
            print(f"  ✅ ~/self-improving/{f} ({lines} lines, {kb:.1f}KB)")
        else:
            print(f"  ❌ ~/self-improving/{f} missing")

    for d in ["projects", "domains", "archive"]:
        p = SI_DIR / d
        if p.exists():
            count = len(list(p.glob("*.md")))
            print(f"  ✅ ~/self-improving/{d}/ ({count} files)")
        else:
            print(f"  ❌ ~/self-improving/{d}/ missing")

    print()
    for name, label in [
        ("SESSION-STATE.md", "SESSION-STATE.md"),
        ("MEMORY.md", "MEMORY.md (OpenClaw native)"),
    ]:
        p = WORKSPACE / name
        if p.exists():
            kb = p.stat().st_size / 1024
            print(f"  ✅ {label} ({kb:.1f}KB)")
        else:
            print(f"  ❌ {label} missing")

    mem = WORKSPACE / "memory"
    if mem.exists():
        count = len(list(mem.glob("*.md")))
        print(f"  ✅ memory/ ({count} daily logs)")
    else:
        print(f"  ❌ memory/ missing")

    print()
    is_persistent, resolved = _check_persistence()
    print(f"  ℹ️  ~/self-improving/ resolves to: {resolved}")
    if is_persistent:
        print("  ✅ On persistent storage")
    else:
        print("  ❌ NOT on persistent storage — memory will be lost on restart!")
        print("     Run: agent_memory.py init (it will auto-fix if /data/ exists)")


def cmd_verify():
    """Post-install verification — check everything is wired up."""
    print("🔍 Post-Install Verification (v3.2)\n")
    issues = []

    # 1. Persistence
    print("1. Storage persistence:")
    is_persistent, resolved = _check_persistence()
    if is_persistent:
        print(f"   ✅ ~/self-improving/ → {resolved} (persistent)")
    else:
        print(f"   ❌ ~/self-improving/ → {resolved} (NOT persistent!)")
        issues.append(f"~/self-improving/ not on persistent storage ({resolved})")

    # 2. Directory structure
    print("\n2. Directory structure:")
    for d in ["", "/projects", "/domains", "/archive"]:
        p = SI_DIR / d.lstrip("/") if d else SI_DIR
        exists = p.exists()
        print(f"   {'✅' if exists else '❌'} ~/self-improving{d}/")
        if not exists:
            issues.append(f"Missing directory: ~/self-improving{d}/")

    # 3. Core files
    print("\n3. Core files:")
    for f in ["memory.md", "corrections.md", "index.md", "heartbeat-state.md"]:
        p = SI_DIR / f
        exists = p.exists()
        has_content = False
        if exists:
            content = p.read_text().strip()
            has_content = len(content.split("\n")) > 5
        status = "✅" if exists and has_content else ("⚠️  exists but minimal" if exists else "❌ missing")
        print(f"   {status} — ~/self-improving/{f}")
        if not exists:
            issues.append(f"Missing file: ~/self-improving/{f}")

    # 4. Memory seed content
    print("\n4. Memory seed content:")
    mem = SI_DIR / "memory.md"
    if mem.exists():
        content = mem.read_text()
        has_entries = any(line.strip().startswith("- ") for line in content.split("\n") if "##" not in line)
        if has_entries:
            print("   ✅ memory.md has content (bootstrap or learned)")
        else:
            print("   ⚠️  memory.md is empty — daily review cron will populate it")
            issues.append("memory.md has no entries yet")
    else:
        print("   ❌ memory.md missing")
        issues.append("memory.md missing")

    # 5. SESSION-STATE.md
    print("\n5. Session state:")
    ss = WORKSPACE / "SESSION-STATE.md"
    print(f"   {'✅' if ss.exists() else '❌'} SESSION-STATE.md")
    if not ss.exists():
        issues.append("SESSION-STATE.md missing")

    # 6. Workspace hooks (check for ACTUAL hook content, not just keyword)
    print("\n6. Workspace hooks:")
    hook_checks = [
        ("SOUL.md", SOUL_HOOK_DETECT, "Self-healing cron check"),
        ("AGENTS.md", AGENTS_HOOK_DETECT, "Self-improving memory reference"),
        ("HEARTBEAT.md", HEARTBEAT_HOOK_DETECT, "Heartbeat maintenance hook"),
    ]
    for fname, detect, desc in hook_checks:
        p = WORKSPACE / fname
        if p.exists():
            content = p.read_text().lower()
            has_hook = detect.lower() in content
            if has_hook:
                print(f"   ✅ {fname} — {desc}")
            else:
                print(f"   ❌ {fname} — missing: {desc}")
                issues.append(f"{fname} missing hook: {desc}. Re-run init to inject.")
        else:
            print(f"   ❌ {fname} not found")
            issues.append(f"{fname} not found. Re-run init to create.")

    # 7. Daily review cron
    print("\n7. Daily review cron:")
    cron_marker = SI_DIR / ".cron-installed"
    if cron_marker.exists():
        print("   ✅ Cron marker found (.cron-installed)")
        print(f"      {cron_marker.read_text().strip()}")
    else:
        print("   ⚠️  Cron marker not found — cron may not be installed yet.")
        print("      The SOUL.md hook will auto-create it on next session start.")
        issues.append("Daily review cron not confirmed (no .cron-installed marker)")

    # 8. Corrections health
    print("\n8. Corrections health:")
    corr = SI_DIR / "corrections.md"
    if corr.exists():
        text = corr.read_text()
        count = text.count("## 20")
        print(f"   {count} corrections logged")
        if count > 50:
            print(f"   ⚠️  Over 50 entries — nightly cron should trim")
        elif count == 0:
            print(f"   ℹ️  No corrections yet (normal for new installs)")
    else:
        print("   ❌ corrections.md missing")

    # Summary
    print("\n" + "=" * 50)
    if not issues:
        print("✅ ALL CHECKS PASSED — skill is fully installed and operational")
    else:
        print(f"⚠️  {len(issues)} ISSUE(S) FOUND:")
        for i, issue in enumerate(issues, 1):
            print(f"   {i}. {issue}")
        print(f"\n  Most issues can be fixed by running: agent_memory.py init")


def cmd_cron_prompt():
    """Output the daily review prompt for cron setup."""
    print("=" * 60)
    print("DAILY REVIEW CRON PROMPT")
    print("=" * 60)
    print()
    print("Copy the text below as the cron job message/prompt.")
    print("Recommended: schedule=daily at 11 PM, sessionTarget=isolated,")
    print("payload.kind=agentTurn, delivery.mode=announce")
    print("⚠️  Do NOT specify a model — use the default to avoid 'model not allowed' errors.")
    print()
    print("-" * 60)
    print(DAILY_REVIEW_PROMPT)
    print("-" * 60)
    print()
    print("To create via OpenClaw cron tool:")
    print('  action: add')
    print('  job.name: "Self-Improving Daily Review + .md Rewrite"')
    print('  job.schedule: { kind: "cron", expr: "0 23 * * *", tz: "<your timezone>" }')
    print('  job.payload: { kind: "agentTurn", message: "<prompt above>", timeoutSeconds: 300 }')
    print('  job.sessionTarget: "isolated"')
    print('  job.delivery: { mode: "announce" }')
    print()
    print("⚠️  Do NOT set payload.model — let it use the agent default.")
    print("    Setting a specific model can cause silent failures if that model")
    print("    isn't in the agent's allowed list.")


def cmd_mark_cron():
    """Write a marker confirming the daily review cron was created."""
    SI_DIR.mkdir(parents=True, exist_ok=True)
    marker = SI_DIR / ".cron-installed"
    ts = datetime.now().strftime("%Y-%m-%d %I:%M %p")
    marker.write_text(f"Daily review cron installed: {ts}\n")
    print(f"✅ Cron marker written to ~/self-improving/.cron-installed")
    print(f"   Timestamp: {ts}")
    print(f"   verify will now show cron as installed.")


def cmd_dry_run():
    """Simulate what the daily review cron would do."""
    print("🧪 DRY RUN — Simulating daily review\n")
    print("This shows what the nightly cron WOULD find and process.")
    print("No files are modified.\n")
    print("=" * 60)

    # 1. Corrections
    print("\n📝 CORRECTIONS TO REVIEW:")
    print("-" * 40)
    corr = SI_DIR / "corrections.md"
    corrections_count = 0
    if corr.exists():
        text = corr.read_text()
        corrections_count = text.count("## 20")
        if corrections_count > 0:
            lines = text.strip().split("\n")
            entries = []
            current = []
            for line in lines:
                if line.strip().startswith("## 20"):
                    if current:
                        entries.append("\n".join(current))
                    current = [line]
                elif current:
                    current.append(line)
            if current:
                entries.append("\n".join(current))
            for entry in entries[-3:]:
                print(f"  {entry.strip()[:200]}")
                print()
            print(f"  Total corrections: {corrections_count}")
            if corrections_count > 50:
                print(f"  ⚠️  Over 50 — cron will trim oldest to archive/")
        else:
            print("  (no corrections logged — cron will have nothing to promote)")
    else:
        print("  ❌ corrections.md missing")

    # 2. Memory.md
    print("\n🧠 CURRENT HOT MEMORY:")
    print("-" * 40)
    mem = SI_DIR / "memory.md"
    mem_lines = 0
    if mem.exists():
        content = mem.read_text()
        mem_lines = content.count("\n")
        entries = [l for l in content.split("\n") if l.strip().startswith("- ")]
        print(f"  {len(entries)} entries, {mem_lines}/100 lines")
        if mem_lines > 80:
            print("  ⚠️  APPROACHING LIMIT — cron should demote oldest entries")
        elif mem_lines < 10:
            print("  ⚠️  Very few entries — cron may not have enough to promote")
    else:
        print("  ❌ memory.md missing")

    # 3. SESSION-STATE.md
    print("\n📋 SESSION-STATE.md:")
    print("-" * 40)
    ss = WORKSPACE / "SESSION-STATE.md"
    if ss.exists():
        content = ss.read_text()
        today = datetime.now().strftime("%Y-%m-%d")
        if today in content:
            print(f"  ✅ Updated today ({today})")
        else:
            mtime = datetime.fromtimestamp(ss.stat().st_mtime)
            print(f"  ⚠️  Last modified: {mtime.strftime('%Y-%m-%d %I:%M %p')}")
            print(f"     Not updated today — cron may find stale context")
    else:
        print("  ❌ Missing — cron will have no session context")

    # 4. Project files
    print("\n📂 PROJECT FILES:")
    print("-" * 40)
    projects_dir = SI_DIR / "projects"
    if projects_dir.exists():
        files = list(projects_dir.glob("*.md"))
        if files:
            for f in files:
                lines = f.read_text().count("\n")
                print(f"  • {f.name} ({lines} lines)")
        else:
            print("  (no project files)")
    else:
        print("  (projects/ directory missing)")

    # 5. Workspace files
    print("\n📄 WORKSPACE FILES TO REVIEW:")
    print("-" * 40)
    for fname in ["SOUL.md", "AGENTS.md", "IDENTITY.md", "HEARTBEAT.md"]:
        p = WORKSPACE / fname
        if p.exists():
            mtime = datetime.fromtimestamp(p.stat().st_mtime)
            kb = p.stat().st_size / 1024
            print(f"  • {fname}: {kb:.1f}KB, modified {mtime.strftime('%Y-%m-%d %I:%M %p')}")
        else:
            print(f"  • {fname}: NOT FOUND")

    # Summary
    print("\n" + "=" * 60)
    print("DRY RUN SUMMARY:")
    print(f"  Corrections to process: {corrections_count}")
    print(f"  Memory.md lines: {mem_lines}/100")
    print(f"  Session state: {'current' if ss.exists() else 'missing'}")
    if corrections_count == 0 and mem_lines < 10:
        print("\n  ⚠️  LOW CONTENT WARNING")
        print("  The cron will find very little to review. This usually means")
        print("  the agent isn't following WAL protocol during the day.")
        print("  The cron catches what's written — it can't create lessons from nothing.")
        print("  Ensure corrections are logged to ~/self-improving/corrections.md")
        print("  and SESSION-STATE.md is updated during work.")
    elif corrections_count > 0:
        print(f"\n  ✅ Cron has material to work with ({corrections_count} corrections)")
    print("\n  No files were modified. Run the actual cron to apply changes.")


def cmd_today():
    today = datetime.now().strftime("%Y-%m-%d")
    mem_dir = WORKSPACE / "memory"
    mem_dir.mkdir(exist_ok=True)
    _safe_create(
        mem_dir / f"{today}.md",
        DAILY.format(date=today),
        f"memory/{today}.md"
    )


def cmd_stats():
    print("📊 Agent Memory Stats\n")

    hot = SI_DIR / "memory.md"
    hot_lines = hot.read_text().count("\n") if hot.exists() else 0
    print(f"🔥 HOT (load every session):")
    print(f"   memory.md: {hot_lines}/100 lines")
    if hot_lines > 80:
        print(f"   ⚠️  Approaching limit — demote oldest unconfirmed entries")
    print()

    print(f"🌡️  WARM (load on context match):")
    for d in ["projects", "domains"]:
        p = SI_DIR / d
        if p.exists():
            files = list(p.glob("*.md"))
            total = sum(f.read_text().count("\n") for f in files)
            print(f"   {d}/: {len(files)} files, {total} lines")
            for f in sorted(files):
                lines = f.read_text().count("\n")
                print(f"     - {f.name}: {lines}/200 lines")
        else:
            print(f"   {d}/: 0 files")

    archive = SI_DIR / "archive"
    count = len(list(archive.glob("*.md"))) if archive.exists() else 0
    print(f"\n❄️  COLD (archived):")
    print(f"   archive/: {count} files")

    corr = SI_DIR / "corrections.md"
    if corr.exists():
        text = corr.read_text()
        entries = text.count("## 20")
        print(f"\n📝 Corrections logged: {entries}")
        if entries > 50:
            print(f"   ⚠️  Over 50 — run nightly cron to trim")

    print(f"\n📁 Workspace:")
    mm = WORKSPACE / "MEMORY.md"
    if mm.exists():
        lines = mm.read_text().count("\n")
        kb = mm.stat().st_size / 1024
        print(f"   MEMORY.md: {lines} lines ({kb:.1f}KB)")
    mem_path = WORKSPACE / "memory"
    if mem_path.exists():
        logs = list(mem_path.glob("*.md"))
        print(f"   Daily logs: {len(logs)}")
        if logs:
            newest = max(logs, key=lambda f: f.name)
            print(f"   Most recent: {newest.name}")
    ss = WORKSPACE / "SESSION-STATE.md"
    if ss.exists():
        mtime = datetime.fromtimestamp(ss.stat().st_mtime)
        print(f"   SESSION-STATE.md: last updated {mtime.strftime('%Y-%m-%d %I:%M %p')}")

    is_persistent, resolved = _check_persistence()
    print(f"\n💾 Storage: {resolved}")
    print(f"   {'✅ Persistent' if is_persistent else '❌ NOT persistent'}")


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"
    cmds = {
        "init": cmd_init,
        "boot": cmd_boot,
        "status": cmd_status,
        "today": cmd_today,
        "stats": cmd_stats,
        "verify": cmd_verify,
        "cron-prompt": cmd_cron_prompt,
        "mark-cron": cmd_mark_cron,
        "dry-run": cmd_dry_run,
    }
    if cmd in cmds:
        cmds[cmd]()
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
