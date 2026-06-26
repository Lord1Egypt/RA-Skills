#!/usr/bin/env python3
"""
Accept a worker's claim and create an escrow to fund the work.

Step 1: Publishes TASK:ACCEPT to the board (public record).
Step 2: Creates an escrow with the chosen worker via escrow.create_escrow().

The worker receives ESCROW:CREATE (with task description) as their assignment.
No other claimants are notified — that policy belongs in the marketplace layer.

Usage:
    export SIGNAAI_BOARD="S-XXXX-XXXX-XXXX-XXXXX"
    python3 examples/accept_board_claim.py <task_id> <worker_address>

Environment:
    SIGNAAI_WORKER_PASSPHRASE  — payer passphrase (or set in script)
    SIGNAAI_BOARD              — board address
    SIGNUM_NETWORK             — mainnet (default) or testnet
"""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from board import accept_claim
from escrow import create_escrow

PASSPHRASE = os.environ.get("SIGNAAI_WORKER_PASSPHRASE", "")
if not PASSPHRASE:
    sys.exit("Set SIGNAAI_WORKER_PASSPHRASE")

if len(sys.argv) < 3:
    sys.exit("Usage: accept_board_claim.py <task_id> <worker_address>")

task_id = sys.argv[1]
worker_address = sys.argv[2]

# Task body and parameters — in production these come from your off-chain store,
# keyed by task_id.
TASK_BODY = "Summarize the top 3 news stories from signum.community this week."
AMOUNT_SIGNA = 1.0
DEADLINE_HOURS = 48

# Step 1: publish accept to board
accept_tx = accept_claim(
    passphrase=PASSPHRASE,
    task_id=task_id,
    worker_address=worker_address,
)
print(f"Claim accepted — TX: {accept_tx}")

# Step 2: create escrow — create_escrow computes task_hash internally from task_description
escrow, err = create_escrow(
    payer_passphrase=PASSPHRASE,
    worker_address=worker_address,
    amount_signa=AMOUNT_SIGNA,
    task_description=TASK_BODY,
    deadline_hours=DEADLINE_HOURS,
)
if err:
    sys.exit(f"Escrow failed: {err}")

print(f"Escrow created")
print(f"  Escrow ID: {escrow['escrow_id']}")
print()
print("The worker has been notified. Funds are held in escrow until work is submitted.")
