#!/usr/bin/env python3
"""
Claim an open task on the SignaAI board.

Publishes TASK:CLAIM to the board. Multiple workers can claim the same task.
The payer decides which claim to accept — this script makes no selection.

Usage:
    export SIGNAAI_BOARD="S-XXXX-XXXX-XXXX-XXXXX"
    python3 examples/claim_board_task.py <task_id>

Environment:
    SIGNAAI_WORKER_PASSPHRASE  — worker passphrase (or set in script)
    SIGNAAI_BOARD              — board address
    SIGNUM_NETWORK             — mainnet (default) or testnet
"""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from board import claim_task

PASSPHRASE = os.environ.get("SIGNAAI_WORKER_PASSPHRASE", "")
if not PASSPHRASE:
    sys.exit("Set SIGNAAI_WORKER_PASSPHRASE")

if len(sys.argv) < 2:
    sys.exit("Usage: claim_board_task.py <task_id>")

task_id = sys.argv[1]

tx_id = claim_task(passphrase=PASSPHRASE, task_id=task_id)

print(f"Claim submitted")
print(f"  Task ID: {task_id}")
print(f"  TX:      {tx_id}")
print()
print("Wait for the payer to accept your claim.")
print("If accepted, you will receive an escrow assignment from the payer.")
