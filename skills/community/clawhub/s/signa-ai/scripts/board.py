#!/usr/bin/env python3
"""
SignaAI Task Board — protocol primitives for open task discovery.

A board is any Signum account used as an append-only event feed.
Anyone can run a board. Set SIGNAAI_BOARD to the default board address,
or pass board_address explicitly to any function.

These helpers publish and read TASK: protocol messages. They contain no
matching logic, no ranking, and no marketplace policy. That belongs in
the layer above. Builders use these primitives to construct whatever
marketplace rules they need.

Typical flow:
    1. Payer calls open_task()  → TASK:OPEN published to board
    2. Workers call claim_task() → TASK:CLAIM published to board
    3. Marketplace layer (off-chain) surfaces claims to payer
    4. Payer calls accept_claim() → TASK:ACCEPT published to board
    5. Payer calls escrow.create_escrow() with the accepted worker
    6. Existing escrow / proof / release flow handles payment

Usage:
    python3 board.py open   <passphrase> <task_hash> <capability> <amount_signa> [--deadline-hours 24]
    python3 board.py claim  <passphrase> <task_id>
    python3 board.py accept <passphrase> <task_id> <worker_address>
    python3 board.py cancel <passphrase> <task_id>
    python3 board.py tasks  [--capability research] [--limit 20]
    python3 board.py claims <task_id>
"""
import os
import sys
import hashlib
import time
sys.path.insert(0, os.path.dirname(__file__))

from signum_api import get_api, nqt, signa, ok, fee_message, ts, EXPLORER_URL
from wallet import get_my_address
from protocol import (
    build_task_open, build_task_claim, build_task_accept, build_task_cancel,
    parse_task, TaskMessage, TASK_PREFIX, ProtocolError,
)

# ── Board address resolution ──────────────────────────────────────────────────

SIGNAAI_BOARD = os.environ.get("SIGNAAI_BOARD", "")
BLOCKS_PER_HOUR = 15   # ~4-minute blocks on Signum mainnet


def _resolve_board(board_address):
    addr = board_address or SIGNAAI_BOARD
    if not addr:
        raise ValueError(
            "board_address is required. Pass it explicitly or set the "
            "SIGNAAI_BOARD environment variable to a Signum address."
        )
    return addr


def _task_id(payer_address, task_hash):
    """Deterministic but unique task ID: short hash of payer + task_hash + nanosecond timestamp."""
    raw = f"{payer_address}:{task_hash}:{time.time_ns()}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


# ── Write helpers ─────────────────────────────────────────────────────────────

def open_task(passphrase, task_hash, capability_tag="",
              amount_signa=0, deadline_hours=24,
              task_summary="", board_address=None, network=None):
    """
    Publish a task opening to the board.

    The task body is NOT stored on-chain — only task_hash. Off-chain
    delivery of the task description happens after the payer calls
    accept_claim() and creates an escrow with the chosen worker.

    Returns:
        (task_id, tx_id)  on success
        raises ValueError / RuntimeError on failure
    """
    board = _resolve_board(board_address)
    api = get_api(network)

    payer_address, err = get_my_address(passphrase, network)
    if err:
        raise ValueError(f"Could not derive payer address: {err}")

    current_block = api.get("getBlockchainStatus").get("numberOfBlocks", 0)
    deadline_block = int(current_block) + int(deadline_hours * BLOCKS_PER_HOUR)

    task_id = _task_id(payer_address, task_hash)
    amount_nqt = nqt(amount_signa) if amount_signa else 0

    message = build_task_open(task_id, payer_address, capability_tag,
                              amount_nqt, deadline_block, task_hash,
                              task_summary=task_summary)
    result = api.post("sendMessage",
                      secretPhrase=passphrase,
                      recipient=board,
                      message=message,
                      messageIsText="true",
                      feeNQT=fee_message(message))
    if not ok(result):
        raise RuntimeError(f"open_task failed: {result.get('error')}")

    return task_id, result["transaction"]


def claim_task(passphrase, task_id, board_address=None, network=None):
    """
    Express intent to work on an open task.

    Multiple workers may claim the same task simultaneously. The payer
    decides which claim to accept — this function makes no selection.

    Returns:
        tx_id  on success
        raises RuntimeError on failure
    """
    board = _resolve_board(board_address)
    api = get_api(network)

    worker_address, err = get_my_address(passphrase, network)
    if err:
        raise ValueError(f"Could not derive worker address: {err}")

    message = build_task_claim(task_id, worker_address)
    result = api.post("sendMessage",
                      secretPhrase=passphrase,
                      recipient=board,
                      message=message,
                      messageIsText="true",
                      feeNQT=fee_message(message))
    if not ok(result):
        raise RuntimeError(f"claim_task failed: {result.get('error')}")

    return result["transaction"]


def accept_claim(passphrase, task_id, worker_address,
                 board_address=None, network=None):
    """
    Accept a specific worker's claim on a task.

    This publishes TASK:ACCEPT to the board — a public on-chain record.
    After calling this, call escrow.create_escrow() with the same worker
    to fund and initiate the work.

    Returns:
        tx_id  on success
        raises RuntimeError on failure
    """
    board = _resolve_board(board_address)
    api = get_api(network)

    message = build_task_accept(task_id, worker_address)
    result = api.post("sendMessage",
                      secretPhrase=passphrase,
                      recipient=board,
                      message=message,
                      messageIsText="true",
                      feeNQT=fee_message(message))
    if not ok(result):
        raise RuntimeError(f"accept_claim failed: {result.get('error')}")

    return result["transaction"]


def cancel_task(passphrase, task_id, board_address=None, network=None):
    """
    Cancel an open task. Publishes TASK:CANCEL to the board.

    This is an advisory signal — no funds are held at the board level.
    If an escrow was already created, cancel it separately via escrow.py.

    Returns:
        tx_id  on success
        raises RuntimeError on failure
    """
    board = _resolve_board(board_address)
    api = get_api(network)

    message = build_task_cancel(task_id)
    result = api.post("sendMessage",
                      secretPhrase=passphrase,
                      recipient=board,
                      message=message,
                      messageIsText="true",
                      feeNQT=fee_message(message))
    if not ok(result):
        raise RuntimeError(f"cancel_task failed: {result.get('error')}")

    return result["transaction"]


# ── Read helpers ──────────────────────────────────────────────────────────────

def _scan_board(board_address, network, limit):
    """Fetch recent transactions at the board address and parse TASK: messages."""
    api = get_api(network)
    result = api.get("getAccountTransactions",
                     account=board_address,
                     firstIndex=0,
                     lastIndex=min(limit - 1, 499),
                     type=1)   # type 1 = messaging
    if not ok(result):
        raise RuntimeError(f"Could not read board: {result.get('error')}")

    events = []
    for tx in (result.get("transactions") or []):
        msg = tx.get("attachment", {}).get("message", "")
        if not msg.startswith(TASK_PREFIX):
            continue
        try:
            parsed = parse_task(msg)
        except ProtocolError:
            continue
        events.append({
            "tx_id":     tx.get("transaction"),
            "sender":    tx.get("senderRS", tx.get("sender", "")),
            "timestamp": ts(tx.get("timestamp", 0)),
            "block":     tx.get("block"),
            "action":    parsed.action,
            "task_id":   parsed.task_id,
            "task":      parsed,
        })
    return events


def list_tasks(board_address=None, capability_tag=None,
               limit=50, network=None):
    """
    Return TASK:OPEN events on the board, newest first.

    Each entry is a dict:
        tx_id, sender, timestamp, block, action, task_id, task (TaskMessage)

    Filter by capability_tag if provided. No marketplace logic applied —
    cancelled/accepted tasks are still returned; callers filter as needed.
    """
    board = _resolve_board(board_address)
    events = _scan_board(board, network, limit)
    opens = [e for e in events if e["action"] == "OPEN"]
    if capability_tag:
        opens = [e for e in opens if e["task"].capability_tag == capability_tag]
    return opens


def get_claims(task_id, board_address=None, limit=50, network=None):
    """
    Return all TASK:CLAIM events for a given task_id, newest first.

    Each entry is a dict:
        tx_id, sender, timestamp, block, action, task_id, task (TaskMessage)

    No selection logic — all claims are returned. The caller decides
    which claim to accept.
    """
    board = _resolve_board(board_address)
    events = _scan_board(board, network, limit)
    return [e for e in events if e["action"] == "CLAIM" and e["task_id"] == task_id]


def get_board_events(board_address=None, limit=100, network=None):
    """
    Return all TASK: events on the board, newest first.

    Useful for building an indexer or monitoring tool. Returns OPEN,
    CLAIM, ACCEPT, and CANCEL events together — no filtering.
    """
    board = _resolve_board(board_address)
    return _scan_board(board, network, limit)


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    import argparse
    parser = argparse.ArgumentParser(description="SignaAI Task Board")
    parser.add_argument("--network", default=os.environ.get("SIGNUM_NETWORK", "mainnet"),
                        choices=["mainnet", "testnet"])
    parser.add_argument("--board", default=None,
                        help="Board address (overrides SIGNAAI_BOARD env var)")
    sub = parser.add_subparsers(dest="cmd")

    p = sub.add_parser("open", help="Publish a task opening")
    p.add_argument("passphrase")
    p.add_argument("task_hash", help="SHA-256 of the task body (off-chain)")
    p.add_argument("capability", nargs="?", default="",
                   help="Capability tag, e.g. research, code, data")
    p.add_argument("amount", nargs="?", type=float, default=0,
                   help="Offered payment in SIGNA")
    p.add_argument("--deadline-hours", type=int, default=24)
    p.add_argument("--summary", default="", help="Short public description (max 200 chars)")

    p = sub.add_parser("claim", help="Claim an open task")
    p.add_argument("passphrase")
    p.add_argument("task_id")

    p = sub.add_parser("accept", help="Accept a worker's claim")
    p.add_argument("passphrase")
    p.add_argument("task_id")
    p.add_argument("worker_address")

    p = sub.add_parser("cancel", help="Cancel an open task")
    p.add_argument("passphrase")
    p.add_argument("task_id")

    p = sub.add_parser("tasks", help="List open tasks on the board")
    p.add_argument("--capability", default=None)
    p.add_argument("--limit", type=int, default=20)

    p = sub.add_parser("claims", help="List claims for a task")
    p.add_argument("task_id")
    p.add_argument("--limit", type=int, default=20)

    p = sub.add_parser("events", help="Show all board events")
    p.add_argument("--limit", type=int, default=50)

    args = parser.parse_args()
    os.environ["SIGNUM_NETWORK"] = args.network

    board = args.board if hasattr(args, "board") else None

    try:
        if args.cmd == "open":
            task_id, tx_id = open_task(
                args.passphrase, args.task_hash, args.capability,
                args.amount, args.deadline_hours,
                getattr(args, "summary", ""), board, args.network)
            print(f"Task opened")
            print(f"  Task ID: {task_id}")
            print(f"  TX:      {tx_id}")
            print(f"  View:    {EXPLORER_URL}/tx/{tx_id}")

        elif args.cmd == "claim":
            tx_id = claim_task(args.passphrase, args.task_id, board, args.network)
            print(f"Claim submitted — TX: {tx_id}")

        elif args.cmd == "accept":
            tx_id = accept_claim(args.passphrase, args.task_id,
                                 args.worker_address, board, args.network)
            print(f"Claim accepted — worker: {args.worker_address}  TX: {tx_id}")
            print(f"Next step: create escrow with this worker via escrow.py")

        elif args.cmd == "cancel":
            tx_id = cancel_task(args.passphrase, args.task_id, board, args.network)
            print(f"Task cancelled — TX: {tx_id}")

        elif args.cmd == "tasks":
            tasks = list_tasks(board, args.capability, args.limit, args.network)
            if not tasks:
                print("No open tasks found.")
            else:
                print(f"{'TIMESTAMP':<18} {'TASK ID':<18} {'CAP':<12} {'SIGNA':>8}  PAYER")
                print("-" * 72)
                for e in tasks:
                    t = e["task"]
                    summary = f"  {t.task_summary}" if t.task_summary else ""
                    print(f"{e['timestamp']:<18} {t.task_id:<18} "
                          f"{t.capability_tag:<12} {signa(t.amount_nqt):>8.2f}  {t.payer_address}{summary}")

        elif args.cmd == "claims":
            claims = get_claims(args.task_id, board, args.limit, args.network)
            if not claims:
                print(f"No claims found for task {args.task_id}")
            else:
                print(f"Claims for task {args.task_id}:")
                for e in claims:
                    print(f"  {e['timestamp']}  {e['task'].worker_address}  TX: {e['tx_id']}")

        elif args.cmd == "events":
            events = get_board_events(board, args.limit, args.network)
            if not events:
                print("No board events found.")
            else:
                for e in events:
                    print(f"{e['timestamp']}  {e['action']:<8} {e['task_id']}  {e['sender']}")

        else:
            parser.print_help()

    except (ValueError, RuntimeError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
