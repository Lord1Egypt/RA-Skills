"""
Smart Poller — test script
Run: python3 test.py
"""

from poller import TaskParser

# ── Sample task board content (generic demo data) ──────────────────────────
SAMPLE_BOARD = """
[TASK-DEMO-001] [Test] Verify task board polling
Assign: agent_a → agent_b  |  Priority: medium  |  Status: pending
Due: 2026-03-16  |  Created: 2026-03-16 11:30
Description: Verify that the poller correctly reads and parses pending tasks.

[TASK-DEMO-002] [Search] Look up latest API docs
Assign: agent_a → agent_b  |  Priority: high  |  Status: pending
Due: 2026-03-17  |  Created: 2026-03-17 09:00
Description: Search for the latest Feishu Docs API documentation.

[agent_b completed] TASK-DEMO-001 | Time: 2026/3/16 12:00:00 | Result: Verification successful
"""

def test_parser():
    tasks = TaskParser.parse_tasks(SAMPLE_BOARD, "agent_b")
    print(f"Parsed {len(tasks)} pending task(s):")
    for t in tasks:
        print(f"  - {t['id']}: {t['title']} (priority: {t['priority']})")
    # TASK-DEMO-001 should be excluded (already completed)
    assert all(t['id'] != 'TASK-DEMO-001' for t in tasks), "Completed task should be filtered out"
    print("✅ All tests passed")

if __name__ == "__main__":
    test_parser()
