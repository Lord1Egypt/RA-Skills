#!/usr/bin/env python3
"""Minimal autonomous agent loop with scar memory.

Run: python3 example_agent_loop.py

Shows the before/after: an agent that repeats mistakes vs one that learns.
Uses a temp directory so it leaves no mess.
"""
import sys, os, tempfile, shutil

# Add parent dir so we can import tetra_scar directly
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tetra_scar import write_scar, read_scars, reflex_check, write_narrative

# ---------------------------------------------------------------------------
# Simulated environment
# ---------------------------------------------------------------------------
DEPLOY_LOG: list[str] = []
TESTS_PASSING = False  # Flip to True after "fix tests" task


def simulate_task(task: str) -> tuple[bool, str]:
    """Fake executor. Returns (success, detail)."""
    t = task.lower()
    if "deploy" in t and not TESTS_PASSING:
        DEPLOY_LOG.append("BROKEN DEPLOY")
        return False, "Deploy failed: 3 tests red, rollback triggered"
    if "deploy" in t and TESTS_PASSING:
        DEPLOY_LOG.append("CLEAN DEPLOY")
        return True, "Deployed v1.2.0, all tests green"
    if "fix" in t and "test" in t:
        return True, "Fixed flaky auth test, suite is green"
    if "add" in t and "test" in t:
        return True, "Added 5 integration tests for payments"
    return True, f"Completed: {task}"


# ---------------------------------------------------------------------------
# Agent loop
# ---------------------------------------------------------------------------
def run_agent(tasks: list[str], memory_dir: str) -> None:
    """Run tasks with scar-aware reflex check before each one."""
    for i, task in enumerate(tasks, 1):
        print(f"\n--- Cycle {i}: \"{task}\" ---")

        # REFLEX CHECK: consult scars before acting
        scars = read_scars(memory_dir=memory_dir)
        block = reflex_check(task, scars)
        if block:
            print(f"  BLOCKED by reflex arc: {block}")
            print(f"  Agent skips this task and picks an alternative.")
            continue

        # EXECUTE
        success, detail = simulate_task(task)

        if success:
            print(f"  SUCCESS: {detail}")
            write_narrative(detail, "team", memory_dir=memory_dir)
        else:
            print(f"  FAILURE: {detail}")
            # Record the scar so we never repeat this
            scar = write_scar(
                what_broke=detail,
                never_again="Never deploy without running test suite first. "
                            "Always run tests before deployment.",
                memory_dir=memory_dir,
            )
            print(f"  SCAR RECORDED: {scar['id']}")


# ---------------------------------------------------------------------------
# Main: tell the story
# ---------------------------------------------------------------------------
def main():
    global TESTS_PASSING
    tmp = tempfile.mkdtemp(prefix="tetra_scar_demo_")

    try:
        print("=" * 60)
        print("  tetra-scar: Agent Loop Demo")
        print("  An agent that learns from failure -- permanently.")
        print("=" * 60)

        # ACT 1: Naive agent deploys without tests, fails
        print("\n### ACT 1: First deploy attempt (no scars yet)")
        TESTS_PASSING = False
        run_agent(
            ["Deploy latest changes to production"],
            memory_dir=tmp,
        )

        # ACT 2: Same agent tries to deploy again -- reflex blocks it
        print("\n### ACT 2: Agent tries to deploy again")
        print("   (scar from Act 1 is now in memory)")
        run_agent(
            ["Deploy latest changes to production without running tests"],
            memory_dir=tmp,
        )

        # ACT 3: Agent adjusts -- fixes tests first, then deploys
        print("\n### ACT 3: Agent adapts -- fix tests, then deploy")
        run_agent(["Fix failing test suite"], memory_dir=tmp)
        TESTS_PASSING = True
        # This deploy description doesn't match the scar because it
        # explicitly mentions running tests (different intent)
        run_agent(
            ["Add integration tests for payments module"],
            memory_dir=tmp,
        )
        # Direct deploy still blocked by reflex -- agent must use safe path
        print("\n### ACT 4: Even after fixing, raw deploy is still blocked")
        run_agent(
            ["Deploy without running test suite first"],
            memory_dir=tmp,
        )

        # Summary
        print("\n" + "=" * 60)
        print("  RESULT")
        print("=" * 60)
        scars = read_scars(memory_dir=tmp)
        print(f"\n  Scars in memory: {len(scars)}")
        for s in scars:
            print(f"    - {s['what_broke'][:60]}")
            print(f"      Never again: {s['never_again'][:60]}")
        print(f"\n  Deploy log: {DEPLOY_LOG}")
        print(f"  Broken deploys: {DEPLOY_LOG.count('BROKEN DEPLOY')}")
        print(f"  Clean deploys:  {DEPLOY_LOG.count('CLEAN DEPLOY')}")
        print(f"\n  The scar prevented a second broken deploy.")
        print(f"  No LLM calls were needed for the block -- pure pattern match.")

    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
