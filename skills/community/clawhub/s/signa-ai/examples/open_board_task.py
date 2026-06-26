#!/usr/bin/env python3
"""
Open a task on the SignaAI board.

Publishes a TASK:OPEN message to the board address so workers can discover it.
Only the SHA-256 hash of the task body is stored on-chain; the actual description
is delivered off-chain after the payer accepts a specific worker's claim.

Usage:
    export SIGNAAI_BOARD="S-XXXX-XXXX-XXXX-XXXXX"
    python3 examples/open_board_task.py

Environment:
    SIGNAAI_WORKER_PASSPHRASE  — payer passphrase (or set in script)
    SIGNAAI_BOARD              — board address
    SIGNUM_NETWORK             — mainnet (default) or testnet
"""
import os
import sys
import hashlib
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from board import open_task

PASSPHRASE = os.environ.get("SIGNAAI_WORKER_PASSPHRASE", "")
if not PASSPHRASE:
    sys.exit("Set SIGNAAI_WORKER_PASSPHRASE")

# The task body lives off-chain. Only publish its hash.
TASK_BODY = "Summarize the top 3 news stories from signum.community this week."
task_hash = hashlib.sha256(TASK_BODY.encode()).hexdigest()

task_id, tx_id = open_task(
    passphrase=PASSPHRASE,
    task_hash=task_hash,
    capability_tag="research",
    amount_signa=1.0,
    deadline_hours=48,
)

print(f"Task opened")
print(f"  Task ID:    {task_id}")
print(f"  Task hash:  {task_hash}")
print(f"  TX:         {tx_id}")
print()
print(f"Workers can now claim this task. Run claim_board_task.py with task_id={task_id}")
