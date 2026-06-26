#!/usr/bin/env python3
"""
SignaAI Task Listener — autonomous worker daemon.

Detection:
  Primary:  WebSocket (ws://localhost:8126/events) — real-time mempool detection
  Fallback: HTTP polling against public nodes (every 120s)

Execution (when signaai-worker.json is configured):
  On new ESCROW:ASSIGN →
    1. Call LLM (Anthropic Claude Haiku) to research the task
    2. Stamp result hash on Signum blockchain
    3. Wait for block confirmation (~4 min, polls every 30s)
    4. Self-verify stamp
    5. Submit result to escrow
    6. Notify payer via Telegram with TX IDs

Fallback (when no worker config):
  Trigger OpenClaw agent via /hooks/agent (requires manual approval)

Worker config: ~/.openclaw/signaai-worker.json
  {
    "passphrase": "your worker passphrase",
    "apiKey": ""    ← optional, falls back to ANTHROPIC_API_KEY env var
  }

Run continuously (launchd):
  python3 listener.py --address S-44S7-32XB-5DM5-5AL3K

Run once (test):
  python3 listener.py --address S-44S7-32XB-5DM5-5AL3K --once

Force polling mode:
  python3 listener.py --address S-44S7-32XB-5DM5-5AL3K --no-websocket
"""

import argparse
import base64
import fcntl
import hashlib
import json
import os
import queue
import socket
import struct
import subprocess
import sys
import threading
import time
import urllib.request
import urllib.parse
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))
from signum_api import get_api, ts, ok, NODES, USER_AGENT, fee_message
from protocol import parse_message, EscrowMessage

ESCROW_ASSIGN_PREFIX = "ESCROW:ASSIGN"
ESCROW_RESULT_PREFIX = "ESCROW:RESULT:"
STATE_FILE            = os.path.expanduser("~/.openclaw/workspace/signaai-listener-state.json")
TRIGGER_FILE          = os.path.expanduser("~/.openclaw/workspace/signaai-pending-tasks.json")
TRIGGER_LOCK          = TRIGGER_FILE + ".lock"
RESULT_INBOX_FILE     = os.path.expanduser("~/.openclaw/workspace/signaai-result-inbox.json")
RESULT_INBOX_LOCK     = RESULT_INBOX_FILE + ".lock"
PENDING_RELEASES_FILE    = os.path.expanduser("~/.openclaw/workspace/signaai-pending-releases.json")
PENDING_AUTO_RELEASE_FILE = os.path.expanduser("~/.openclaw/workspace/signaai-auto-release-queue.json")
DISPUTE_FILE             = os.path.expanduser("~/.openclaw/workspace/signaai-disputes.json")
LISTENER_LOCK_DIR        = os.path.expanduser("~/.openclaw/workspace")

REVIEW_MINUTES = int(os.environ.get("SIGNAAI_REVIEW_MINUTES", "10"))
AUTO_RELEASE   = os.environ.get("SIGNAAI_AUTO_RELEASE", "true").lower() == "true"

# Single-worker task queue — processes one escrow at a time, no parallel races
_task_queue = queue.Queue()

def _task_worker():
    """Background thread that drains the task queue one at a time."""
    while True:
        fn, args = _task_queue.get()
        try:
            fn(*args)
        except Exception as e:
            log(f"Task worker error: {e}")
        finally:
            _task_queue.task_done()

_worker_thread = threading.Thread(target=_task_worker, daemon=True)
_worker_thread.start()
OPENCLAW_CFG  = os.path.expanduser("~/.openclaw/openclaw.json")
WORKER_CFG    = os.path.expanduser("~/.openclaw/signaai-worker.json")

WS_HOST = "localhost"
WS_PORT = 8126
WS_PATH = "/events"

POLL_INTERVAL    = 120   # seconds between fallback polls
CONFIRM_POLL     = 30    # seconds between confirmation checks
CONFIRM_TIMEOUT  = 1200  # max seconds to wait for confirmation (20 min)
RESULT_CHUNK_BYTES = 600  # stays under Signum's practical message-size limit
_listener_lock_handle = None


# ── Logging ───────────────────────────────────────────────────────────────────

def now():
    return datetime.now().strftime("%H:%M:%S")

def log(msg):
    print(f"[{now()}] {msg}", flush=True)

def git_commit():
    """Return the checked-out git commit for startup diagnostics."""
    skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    try:
        return subprocess.check_output(
            ["git", "-C", skill_dir, "rev-parse", "--short", "HEAD"],
            text=True,
            stderr=subprocess.DEVNULL,
            timeout=3,
        ).strip()
    except Exception:
        return "unknown"

def acquire_listener_lock(network):
    """
    Hold an exclusive per-network lock for the listener process lifetime.

    This prevents a launchd daemon and a manual foreground listener from both
    processing the same escrow stream and writing contradictory log lines.
    """
    global _listener_lock_handle
    os.makedirs(LISTENER_LOCK_DIR, exist_ok=True)
    lock_path = os.path.join(LISTENER_LOCK_DIR, f"signaai-listener-{network}.lock")
    lock = open(lock_path, "a+")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        lock.seek(0)
        existing = lock.read().strip() or "unknown pid"
        print(f"Another SignaAI listener is already running for {network}: {existing}", flush=True)
        print("Stop the existing listener before starting a foreground copy.", flush=True)
        sys.exit(2)

    lock.seek(0)
    lock.truncate()
    lock.write(f"pid={os.getpid()} script={os.path.abspath(__file__)} commit={git_commit()}\n")
    lock.flush()
    _listener_lock_handle = lock
    return lock_path


# ── State / trigger file helpers ──────────────────────────────────────────────

def load_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE) as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return {"processed_txs": []}
    return {"processed_txs": []}

def save_state(state):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    tmp = STATE_FILE + ".tmp"
    with open(tmp, "w") as f:
        json.dump(state, f, indent=2)
    os.replace(tmp, STATE_FILE)

def load_pending():
    if os.path.exists(TRIGGER_FILE):
        try:
            with open(TRIGGER_FILE) as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return []
    return []

def save_pending(tasks):
    os.makedirs(os.path.dirname(TRIGGER_FILE), exist_ok=True)
    tmp = TRIGGER_FILE + ".tmp"
    with open(tmp, "w") as f:
        json.dump(tasks, f, indent=2)
    os.replace(tmp, TRIGGER_FILE)

def with_pending_lock(mutator):
    """Run a pending-task mutation under a process-wide file lock."""
    os.makedirs(os.path.dirname(TRIGGER_FILE), exist_ok=True)
    with open(TRIGGER_LOCK, "a+") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        try:
            tasks = load_pending()
            result = mutator(tasks)
            save_pending(tasks)
            return result
        finally:
            fcntl.flock(lock, fcntl.LOCK_UN)

def claim_pending_task(task):
    """Atomically claim a task so duplicate listeners/events cannot queue it."""
    def mutate(tasks):
        for existing in tasks:
            same_tx = existing.get("tx_id") == task.get("tx_id")
            same_escrow = existing.get("escrow_id") == task.get("escrow_id")
            if same_tx or same_escrow:
                return False, existing.get("status", "unknown")
        tasks.append(task)
        return True, "claimed"
    return with_pending_lock(mutate)

def update_pending_task(escrow_id, **updates):
    """Atomically update the saved task record for an escrow."""
    def mutate(tasks):
        updated = False
        for task in tasks:
            if task.get("escrow_id") == escrow_id:
                task.update(updates)
                task["updated_at"] = datetime.now().isoformat()
                updated = True
        return updated
    return with_pending_lock(mutate)

def chain_has_worker_submission(escrow_id, address, network):
    """Return the worker's existing ESCROW:SUBMIT tx, if one is already on-chain."""
    api = get_api(network)
    result = api.get("getAccountTransactions",
                     account=address,
                     firstIndex=0,
                     lastIndex=199)
    if not ok(result):
        log(f"Startup retry check failed for {escrow_id}: {result.get('error', 'unknown error')}")
        return None

    for tx in (result.get("transactions") or []):
        msg = tx.get("attachment", {}).get("message", "")
        try:
            parsed = parse_message(msg)
        except Exception:
            continue
        if not isinstance(parsed, EscrowMessage):
            continue
        if parsed.escrow_id == escrow_id and parsed.action == "SUBMIT":
            return tx.get("transaction")
    return None

def startup_retry_candidates(address, network):
    """
    Return stale pending/in_progress tasks that still need work.

    This path runs before the daemon starts watching new transactions, so it
    must do its own dedup and chain reconciliation instead of blindly re-queueing
    every saved pending row.
    """
    tasks = load_pending()
    seen = set()
    retries = []
    changed = False
    now_iso = datetime.now().isoformat()

    for task in tasks:
        status = task.get("status")
        if status not in ("pending", "in_progress"):
            continue

        escrow_id = task.get("escrow_id", "")
        task_desc = task.get("task_description", "")
        if not escrow_id or not task_desc:
            task["status"] = "skipped_invalid"
            task["skipped_at"] = now_iso
            changed = True
            continue

        if escrow_id in seen:
            task["status"] = "skipped_duplicate"
            task["skipped_at"] = now_iso
            changed = True
            continue
        seen.add(escrow_id)

        saved_submit_tx = str(task.get("submit_tx", "")).strip()
        if saved_submit_tx:
            task["status"] = "chain_submitted"
            task["updated_at"] = now_iso
            changed = True
            log(f"Startup retry skipped {escrow_id}: saved submit TX exists ({saved_submit_tx})")
            continue

        submit_tx = chain_has_worker_submission(escrow_id, address, network)
        if submit_tx:
            task["status"] = "chain_submitted"
            task["submit_tx"] = submit_tx
            task["updated_at"] = now_iso
            changed = True
            log(f"Startup retry skipped {escrow_id}: already submitted on-chain ({submit_tx})")
            continue

        retries.append(task)

    if changed:
        save_pending(tasks)
    return retries


# ── Result delivery helpers ──────────────────────────────────────────────────

def load_result_inbox():
    if os.path.exists(RESULT_INBOX_FILE):
        try:
            with open(RESULT_INBOX_FILE) as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return {"escrows": {}}
    return {"escrows": {}}

def save_result_inbox(inbox):
    os.makedirs(os.path.dirname(RESULT_INBOX_FILE), exist_ok=True)
    tmp = RESULT_INBOX_FILE + ".tmp"
    with open(tmp, "w") as f:
        json.dump(inbox, f, indent=2)
    os.replace(tmp, RESULT_INBOX_FILE)

def with_result_inbox_lock(mutator):
    os.makedirs(os.path.dirname(RESULT_INBOX_FILE), exist_ok=True)
    with open(RESULT_INBOX_LOCK, "a+") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        try:
            inbox = load_result_inbox()
            result = mutator(inbox)
            save_result_inbox(inbox)
            return result
        finally:
            fcntl.flock(lock, fcntl.LOCK_UN)

def _result_record(inbox, escrow_id):
    escrows = inbox.setdefault("escrows", {})
    return escrows.setdefault(escrow_id, {
        "escrow_id": escrow_id,
        "chunks": {},
        "notified": False,
    })

def result_chunks(result_text):
    data = result_text.encode("utf-8")
    chunks = [data[i:i + RESULT_CHUNK_BYTES]
              for i in range(0, len(data), RESULT_CHUNK_BYTES)]
    return chunks or [b""]

def build_result_chunk_message(escrow_id, index, total, chunk):
    payload = base64.urlsafe_b64encode(chunk).decode("ascii").rstrip("=")
    return f"{ESCROW_RESULT_PREFIX}{escrow_id}:{index}:{total}:{payload}"

def parse_result_chunk_message(message):
    parts = message.split(":", 5)
    if len(parts) != 6 or parts[0] != "ESCROW" or parts[1] != "RESULT":
        raise ValueError("not an ESCROW:RESULT message")
    escrow_id = parts[2]
    index = int(parts[3])
    total = int(parts[4])
    payload = parts[5]
    if index < 1 or total < 1 or index > total:
        raise ValueError("invalid result chunk index")
    padding = "=" * (-len(payload) % 4)
    chunk = base64.urlsafe_b64decode((payload + padding).encode("ascii"))
    return escrow_id, index, total, chunk

def publish_result_chunks(passphrase, recipient, escrow_id, result_text, network):
    """Deliver the result text to the payer account as chunked on-chain messages."""
    api = get_api(network)
    tx_ids = []
    chunks = result_chunks(result_text)
    total = len(chunks)

    for index, chunk in enumerate(chunks, start=1):
        message = build_result_chunk_message(escrow_id, index, total, chunk)
        sent = api.post("sendMessage",
                        secretPhrase=passphrase,
                        recipient=recipient,
                        message=message,
                        messageIsText="true",
                        feeNQT=fee_message(message))
        if not ok(sent):
            return tx_ids, sent.get("error", "Failed to send result chunk")
        tx_ids.append(sent.get("transaction"))
        time.sleep(1)

    return tx_ids, None

def update_result_submit(escrow_id, submit_tx, result_hash, proof_tx, sender):
    now_iso = datetime.now().isoformat()

    def mutate(inbox):
        record = _result_record(inbox, escrow_id)
        record.update({
            "submit_tx": str(submit_tx),
            "result_hash": result_hash,
            "proof_tx": str(proof_tx),
            "worker": sender,
            "updated_at": now_iso,
        })
        return record.copy()

    return with_result_inbox_lock(mutate)

def update_result_chunk(escrow_id, index, total, chunk, tx_id, sender):
    now_iso = datetime.now().isoformat()
    encoded = base64.urlsafe_b64encode(chunk).decode("ascii").rstrip("=")

    def mutate(inbox):
        record = _result_record(inbox, escrow_id)
        record["total_chunks"] = total
        record.setdefault("chunks", {})[str(index)] = encoded
        record.setdefault("chunk_txs", {})[str(index)] = str(tx_id)
        record["worker"] = sender
        record["updated_at"] = now_iso
        return record.copy()

    return with_result_inbox_lock(mutate)

def mark_result_notified(escrow_id):
    def mutate(inbox):
        record = _result_record(inbox, escrow_id)
        if record.get("notified"):
            return False
        record["notified"] = True
        record["notified_at"] = datetime.now().isoformat()
        return True

    return with_result_inbox_lock(mutate)

def assemble_result(record):
    total = int(record.get("total_chunks") or 0)
    chunks = record.get("chunks") or {}
    if total < 1 or len(chunks) < total:
        return None

    data = b""
    for index in range(1, total + 1):
        payload = chunks.get(str(index))
        if payload is None:
            return None
        padding = "=" * (-len(payload) % 4)
        data += base64.urlsafe_b64decode((payload + padding).encode("ascii"))
    return data.decode("utf-8")

def maybe_notify_payer_result(escrow_id, tg_token, tg_chat_id, network):
    record = load_result_inbox().get("escrows", {}).get(escrow_id, {})
    if record.get("notified") or not record.get("submit_tx"):
        return False

    result_text = assemble_result(record)
    if result_text is None:
        return False

    computed_hash = hashlib.sha256(result_text.encode("utf-8")).hexdigest()
    expected_hash = str(record.get("result_hash", ""))
    hash_ok = computed_hash == expected_hash

    proof_ok = False
    try:
        from verify import verify_proof
        proof_ok, _details = verify_proof(result_text, record.get("proof_tx"), network=network)
    except Exception as e:
        log(f"[{escrow_id}] Proof verification error before payer notify: {e}")

    status_line = "verified" if hash_ok and proof_ok else "verification failed"
    result_preview = result_text[:3000] + "..." if len(result_text) > 3000 else result_text
    delivered = send_telegram(tg_token, tg_chat_id, (
        f"✅ *SignaAI Task Complete*\n"
        f"Escrow: `{escrow_id}`\n\n"
        f"*Research Result:*\n{result_preview}\n\n"
        f"Stamp TX: `{record.get('proof_tx')}`\n"
        f"Submit TX: `{record.get('submit_tx')}`\n"
        f"Result hash: `{status_line}`\n\n"
        f"Payment review window: {REVIEW_MINUTES} minutes.\n"
        f"Auto-release scheduled unless disputed.\n\n"
        f"To block payment, reply:\n"
        f"Dispute escrow {escrow_id}"
    ), kind=f"payer_task_complete:{escrow_id}")

    if delivered:
        mark_result_notified(escrow_id)
        log(f"[{escrow_id}] Payer notified with delivered result")
        _queue_auto_release(escrow_id, record)
    return delivered

# ── Auto-release queue ───────────────────────────────────────────────────────

def _queue_auto_release(escrow_id, record):
    """Add escrow to auto-release queue after result is verified and payer notified."""
    if not AUTO_RELEASE:
        return
    release_after = time.time() + REVIEW_MINUTES * 60
    try:
        queue = {}
        if os.path.exists(PENDING_AUTO_RELEASE_FILE):
            with open(PENDING_AUTO_RELEASE_FILE) as f:
                queue = json.load(f)
        if escrow_id not in queue:
            queue[escrow_id] = {
                "release_after": release_after,
                "result_hash":   record.get("result_hash"),
                "proof_tx":      record.get("proof_tx"),
                "submit_tx":     record.get("submit_tx"),
                "status":        "pending_review",
            }
            with open(PENDING_AUTO_RELEASE_FILE, "w") as f:
                json.dump(queue, f, indent=2)
            log(f"[{escrow_id}] Auto-release queued in {REVIEW_MINUTES}m")
    except Exception as e:
        log(f"[{escrow_id}] Failed to queue auto-release: {e}")


def _is_disputed(escrow_id):
    """Check if payer has disputed this escrow."""
    try:
        if os.path.exists(DISPUTE_FILE):
            with open(DISPUTE_FILE) as f:
                disputes = json.load(f)
            return escrow_id in disputes
    except Exception:
        pass
    return False


def check_auto_releases(network, tg_token, tg_chat_id):
    """Fire pending auto-releases whose review window has passed."""
    if not AUTO_RELEASE or not os.path.exists(PENDING_AUTO_RELEASE_FILE):
        return
    try:
        with open(PENDING_AUTO_RELEASE_FILE) as f:
            queue = json.load(f)
    except Exception:
        return

    now = time.time()
    changed = False
    for escrow_id, entry in list(queue.items()):
        if entry.get("status") != "pending_review":
            continue
        if now < entry.get("release_after", float("inf")):
            continue
        if _is_disputed(escrow_id):
            log(f"[{escrow_id}] Auto-release skipped — disputed")
            queue[escrow_id]["status"] = "disputed"
            changed = True
            continue

        log(f"[{escrow_id}] Review window passed — auto-releasing...")
        try:
            sys.path.insert(0, os.path.dirname(__file__))
            from escrow import release_payment
            worker_cfg = {}
            if os.path.exists(WORKER_CFG):
                with open(WORKER_CFG) as f:
                    worker_cfg = json.load(f)
            passphrase = worker_cfg.get("passphrase", "")
            if not passphrase:
                log(f"[{escrow_id}] Auto-release failed — no passphrase in worker config")
                continue

            result, err = release_payment(passphrase, escrow_id, network)
            if err:
                log(f"[{escrow_id}] Auto-release error: {err}")
                queue[escrow_id]["status"] = "error"
            else:
                log(f"[{escrow_id}] Auto-released — TX: {result.get('tx_id')}")
                queue[escrow_id]["status"] = "released"
                at_line = f"\nAT: `{result['at_address']}`" if result.get('at_address') else ""
                send_telegram(tg_token, tg_chat_id,
                    f"🔐 *Release Submitted*\n"
                    f"Escrow: `{escrow_id}`\n"
                    f"Release TX: `{result.get('tx_id')}`{at_line}\n\n"
                    f"The AT will pay the worker on the next block.",
                    kind=f"auto_release:{escrow_id}"
                )
        except Exception as e:
            log(f"[{escrow_id}] Auto-release exception: {e}")
        changed = True

    if changed:
        with open(PENDING_AUTO_RELEASE_FILE, "w") as f:
            json.dump(queue, f, indent=2)


# ── AT payout watcher ────────────────────────────────────────────────────────

def _check_at_payout(entry, api):
    """Return payout TX info if the AT has paid out to the worker, else None."""
    at_address = entry.get("at_address", "")
    worker     = entry.get("worker", "")
    if not at_address or not worker:
        return None

    at_account = api.get("getAccount", account=at_address)
    if not ok(at_account):
        return None

    bal_nqt = int(at_account.get("balanceNQT", 0) or 0)
    if bal_nqt > 10_000_000:  # still holds > 0.1 SIGNA — not paid out yet
        return None

    # AT is drained — find payout TX in worker's recent incoming transactions
    at_numeric  = str(at_account.get("account", ""))
    worker_txs  = api.get("getAccountTransactions", account=worker,
                          firstIndex=0, lastIndex=49)
    if not ok(worker_txs):
        return None

    for tx in (worker_txs.get("transactions") or []):
        sender_id = str(tx.get("sender", ""))
        sender_rs = tx.get("senderRS", "")
        if sender_id == at_numeric or sender_rs == at_address:
            return {
                "tx_id":      tx.get("transaction"),
                "amount_nqt": int(tx.get("amountNQT", 0) or 0),
                "height":     tx.get("height"),
            }
    return None


def check_pending_releases(network, tg_token, tg_chat_id):
    """
    Check if any pending AT releases have paid out and notify the payer (MK).
    Runs on every poll cycle and every new block.
    """
    if not os.path.exists(PENDING_RELEASES_FILE):
        return

    try:
        with open(PENDING_RELEASES_FILE) as f:
            entries = json.load(f)
    except Exception:
        return

    if not entries:
        return

    api = get_api(network)
    remaining = []

    for entry in entries:
        escrow_id = entry.get("escrow_id", "?")
        payout = _check_at_payout(entry, api)

        if payout is None:
            remaining.append(entry)
            continue

        amount_signa = payout["amount_nqt"] / 100_000_000
        release_tx   = payout.get("tx_id", "unknown")
        worker       = entry.get("worker", "unknown")

        log(f"[{escrow_id}] AT payout confirmed — {amount_signa:.4f} SIGNA → {worker}")

        send_telegram(tg_token, tg_chat_id, (
            f"✅ *Escrow Released*\n"
            f"Escrow: `{escrow_id}`\n\n"
            f"Worker received: `{amount_signa:.4f} SIGNA`\n"
            f"Release TX: `{release_tx}`"
        ), kind=f"release_confirmed:{escrow_id}")

    try:
        tmp = PENDING_RELEASES_FILE + ".tmp"
        with open(tmp, "w") as f:
            json.dump(remaining, f, indent=2)
        os.replace(tmp, PENDING_RELEASES_FILE)
    except Exception:
        pass


# ── Config ────────────────────────────────────────────────────────────────────

def load_openclaw_config():
    """Read Telegram and hooks config from OpenClaw config."""
    try:
        with open(OPENCLAW_CFG) as f:
            cfg = json.load(f)
        tg = cfg.get("channels", {}).get("telegram", {})
        tg_token = tg.get("botToken", "") or None
        approvers = tg.get("execApprovals", {}).get("approvers", [])
        tg_chat_id = approvers[0] if approvers else None

        hooks = cfg.get("hooks", {})
        hook_enabled = hooks.get("enabled", False)
        hook_token = hooks.get("token", "") if hook_enabled else None
        hook_path = hooks.get("path", "/hooks")
        gw_port = cfg.get("gateway", {}).get("port", 18789)

        return tg_token, tg_chat_id, hook_token, hook_path, gw_port
    except Exception:
        return None, None, None, "/hooks", 18789

OPENCLAW_MODELS = os.path.expanduser("~/.openclaw/agents/main/agent/models.json")

ENV_VARS = {
    # provider prefix → env var name (fallback if models.json not present)
    "xai":       "XAI_API_KEY",
    "openai":    "OPENAI_API_KEY",
    "anthropic": "ANTHROPIC_API_KEY",
    "groq":      "GROQ_API_KEY",
    "ollama":    None,  # no key needed
}

def load_openclaw_llm():
    """
    Read the active LLM provider, model, base URL, and API key from OpenClaw config.

    Primary source: ~/.openclaw/agents/main/agent/models.json
      — OpenClaw stores API keys here, readable by launchd daemons.

    Fallback: env vars (XAI_API_KEY etc.) for interactive shells.

    Returns (provider, model, base_url, api_key) or None if can't determine.
    """
    try:
        with open(OPENCLAW_CFG) as f:
            cfg = json.load(f)

        # e.g. "xai/grok-4" or "groq/llama-3.3-70b-versatile"
        primary = cfg.get("agents", {}).get("defaults", {}).get("model", {}).get("primary", "")
        if "/" not in primary:
            return None

        provider, model_id = primary.split("/", 1)

        # Read baseUrl and apiKey from models.json (where OpenClaw stores them)
        base_url = ""
        api_key  = ""
        try:
            with open(OPENCLAW_MODELS) as f:
                models_cfg = json.load(f)
            prov = models_cfg.get("providers", {}).get(provider, {})
            base_url = prov.get("baseUrl", "")
            api_key  = prov.get("apiKey", "")
        except Exception:
            pass

        # Fallback: env var (interactive shells)
        if not api_key:
            env_var = ENV_VARS.get(provider)
            api_key = os.environ.get(env_var, "") if env_var else ""

        if not base_url:
            base_url, _ = LLM_PROVIDERS.get(provider, LLM_PROVIDERS["xai"])

        if not api_key and provider != "ollama":
            return None

        return provider, model_id, base_url, api_key
    except Exception:
        return None


def load_worker_config():
    """
    Load agent config from signaai-worker.json.

    Any agent can act as payer or worker — role is determined by context:
      - ESCROW:ASSIGN  → worker role (execute task, submit result)
      - Payers call escrow.py create directly (dedup prevents duplicates)

    LLM provider/model/key are read from OpenClaw's models.json automatically.
    Only passphrase is required in signaai-worker.json.
    """
    if not os.path.exists(WORKER_CFG):
        return None
    try:
        with open(WORKER_CFG) as f:
            cfg = json.load(f)
        passphrase = str(cfg.get("passphrase", "")).strip()
        if not passphrase:
            return None

        llm = load_openclaw_llm()
        if not llm:
            log("Could not load LLM config from OpenClaw — is a provider configured?")
            return None

        provider, model_id, base_url, api_key = llm
        cfg["passphrase"] = passphrase
        cfg["provider"]   = provider
        cfg["model"]      = model_id
        cfg["baseUrl"]    = base_url
        cfg["apiKey"]     = api_key
        return cfg
    except Exception as e:
        log(f"Agent config error: {e}")
        return None


# ── Telegram ──────────────────────────────────────────────────────────────────

def send_telegram(token, chat_id, message, kind="message"):
    if not token or not chat_id:
        return False
    def post(parse_mode):
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": message
        }
        if parse_mode:
            payload["parse_mode"] = parse_mode
        data = urllib.parse.urlencode(payload).encode()
        response = urllib.request.urlopen(
            urllib.request.Request(url, data=data), timeout=10
        )
        return json.loads(response.read().decode("utf-8"))

    try:
        payload = post("Markdown")
        message_id = payload.get("result", {}).get("message_id", "?")
        log(f"Telegram sent ({kind}) message_id={message_id}")
        return True
    except Exception as e:
        log(f"Telegram Markdown send failed ({kind}): {e}; retrying plain text")
        try:
            payload = post(None)
            message_id = payload.get("result", {}).get("message_id", "?")
            log(f"Telegram sent ({kind}) message_id={message_id} plain_text=true")
            return True
        except Exception as plain_error:
            log(f"Telegram send failed ({kind}): {plain_error}")
            return False


# ── Hooks fallback (OpenClaw agent trigger) ───────────────────────────────────

def trigger_agent(hook_token, hook_path, gw_port, escrow_id, sender,
                  worker_address, task_hash, task_description=""):
    """POST to OpenClaw /hooks/agent — fallback when no worker config."""
    if not hook_token:
        return
    try:
        skill_dir = os.path.expanduser("~/.openclaw/workspace/skills/signaai/scripts")
        task_hint = f'Task: "{task_description[:200]}"' if task_description else f"task_hash: {task_hash[:16]}..."
        message = (
            f"New SignaAI task assigned to you.\n\n"
            f"Escrow ID: {escrow_id}\n"
            f"Payer: {sender}\n"
            f"Your wallet: {worker_address}\n"
            f"{task_hint}\n\n"
            f"Run these steps IN ORDER. Use ONLY --network mainnet flag. "
            f"NEVER use SIGNUM_NETWORK= prefix. NEVER output placeholder values.\n\n"
            f"1. python3 {skill_dir}/escrow.py --network mainnet status {escrow_id} --address {worker_address}\n"
            f"2. Research the task.\n"
            f"3. python3 {skill_dir}/verify.py --network mainnet stamp \"<passphrase>\" \"<result>\"\n"
            f"4. Wait 4 minutes.\n"
            f"5. python3 {skill_dir}/verify.py --network mainnet verify \"<result>\" <stamp_tx>\n"
            f"6. python3 {skill_dir}/escrow.py --network mainnet submit \"<passphrase>\" {escrow_id} \"<result>\"\n\n"
            f"Show actual TX IDs from script output only."
        )
        url = f"http://127.0.0.1:{gw_port}{hook_path}/agent"
        data = json.dumps({
            "message": message,
            "name": "SignaAI Worker",
            "agentId": "main",
            "timeoutSeconds": 900,
        }).encode()
        req = urllib.request.Request(url, data=data, headers={
            "Authorization": f"Bearer {hook_token}",
            "Content-Type": "application/json",
        })
        urllib.request.urlopen(req, timeout=10)
        log(f"Agent triggered via hooks API for escrow {escrow_id}")
    except Exception as e:
        log(f"Hooks trigger failed: {e}")


# ── Autonomous execution ──────────────────────────────────────────────────────

LLM_PROVIDERS = {
    # provider  → (base_url, default_model)
    "xai":       ("https://api.x.ai/v1",                  "grok-3-mini"),
    "openai":    ("https://api.openai.com/v1",             "gpt-4o-mini"),
    "groq":      ("https://api.groq.com/openai/v1",        "llama-3.3-70b-versatile"),
    "anthropic": (None,                                    "claude-haiku-4-5-20251001"),  # separate handler
    "ollama":    ("http://localhost:11434/v1",             "llama3.1:8b"),               # no key needed
}

def call_llm(task_description, api_key, provider="xai", model=None, base_url=None):
    """
    Call LLM to research a task. Returns result text.

    provider/model/base_url are read from openclaw.json via load_openclaw_llm().
    Falls back to LLM_PROVIDERS defaults if base_url not supplied.

    Supported providers: xai, openai, groq, anthropic, ollama
    All except anthropic use the OpenAI-compatible /chat/completions endpoint.
    """
    prompt = (
        "You are a research assistant. Complete this task thoroughly and accurately. "
        "Cite any specific facts, figures, or sources you use.\n\n"
        f"Task: {task_description}"
    )

    if provider == "anthropic":
        url = "https://api.anthropic.com/v1/messages"
        data = json.dumps({
            "model": model or "claude-haiku-4-5-20251001",
            "max_tokens": 1500,
            "messages": [{"role": "user", "content": prompt}]
        }).encode()
        req = urllib.request.Request(url, data=data, headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        })
        resp = json.loads(urllib.request.urlopen(req, timeout=120).read())
        return resp["content"][0]["text"]

    # All other providers: OpenAI-compatible
    # Use base_url from openclaw.json if available, otherwise fall back to defaults
    if not base_url:
        base_url, _ = LLM_PROVIDERS.get(provider, LLM_PROVIDERS["xai"])
    if not model:
        _, model = LLM_PROVIDERS.get(provider, LLM_PROVIDERS["xai"])

    url = f"{base_url}/chat/completions"
    headers = {"content-type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    data = json.dumps({
        "model": model,
        "max_tokens": 1500,
        "messages": [{"role": "user", "content": prompt}]
    }).encode()
    req = urllib.request.Request(url, data=data, headers=headers)
    resp = json.loads(urllib.request.urlopen(req, timeout=120).read())
    return resp["choices"][0]["message"]["content"]


def get_transaction_any_node(tx_id, network):
    """
    Fetch a transaction from the active API node, then fan out to peers if it is
    still propagating. Public Signum nodes can briefly disagree on fresh TX IDs.
    """
    api = get_api(network)
    result = api.get("getTransaction", transaction=str(tx_id))
    active_node = getattr(api, "active_node", "?")
    if ok(result) or "Unknown transaction" not in str(result.get("error", "")):
        return result, active_node

    params = urllib.parse.urlencode({
        "requestType": "getTransaction",
        "transaction": str(tx_id),
    })
    for node in NODES.get(network, []):
        if node == active_node:
            continue
        try:
            req = urllib.request.Request(
                f"{node}/api?{params}",
                headers={"User-Agent": USER_AGENT},
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                peer_result = json.loads(resp.read())
            if "errorDescription" in peer_result:
                peer_result = {
                    "error": peer_result["errorDescription"],
                    "errorCode": peer_result.get("errorCode"),
                }
            if ok(peer_result):
                return peer_result, node
        except Exception:
            continue
    return result, active_node


def wait_for_confirmation(tx_id, network):
    """Poll until TX has at least 1 confirmation. Returns True/False."""
    deadline = time.time() + CONFIRM_TIMEOUT
    attempt = 0
    while time.time() < deadline:
        result, node = get_transaction_any_node(tx_id, network)
        if ok(result):
            confirmations = int(result.get("confirmations", 0) or 0)
            height = int(result.get("height", 2147483647) or 2147483647)
            if confirmations >= 1:
                log(f"  TX {tx_id} confirmed on {network} via {node} "
                    f"(height={height}, confirmations={confirmations})")
                return True
            if height == 2147483647:
                status = "seen in mempool"
            else:
                status = f"mined at height {height}, waiting for confirmation"
        else:
            status = result.get("error", "unknown error")
        elapsed = attempt * CONFIRM_POLL
        log(f"  Waiting for block confirmation... ({elapsed}s elapsed, "
            f"network={network}, node={node}, status={status})")
        time.sleep(CONFIRM_POLL)
        attempt += 1
    return False


def execute_task_autonomously(escrow_id, assign_tx_id, task_description, sender, worker_address,
                               network, worker_cfg, tg_token, tg_chat_id):
    """
    Full autonomous task execution in a background thread.
    The LLM does the research. Python handles all blockchain operations.
    No exec calls, no approval prompts, no hallucinated TX IDs.
    """
    from verify import hash_content, publish_proof, verify_proof
    from escrow import submit_proof

    passphrase = worker_cfg["passphrase"]
    api_key    = worker_cfg["apiKey"]
    provider   = worker_cfg.get("provider", "xai")
    model      = worker_cfg.get("model")
    base_url   = worker_cfg.get("baseUrl")

    log(f"[{escrow_id}] Autonomous execution starting")
    log(f"[{escrow_id}] Task: {task_description[:100]}...")
    update_pending_task(escrow_id, status="in_progress", started_at=datetime.now().isoformat())

    def fail(reason):
        log(f"[{escrow_id}] FAILED: {reason}")
        update_pending_task(escrow_id, status="failed", error=reason,
                            failed_at=datetime.now().isoformat())
        send_telegram(tg_token, tg_chat_id,
                      f"❌ *SignaAI Task Failed*\nEscrow: `{escrow_id}`\n{reason}",
                      kind=f"task_failed:{escrow_id}")

    # Step 0: Confirm the assignment TX is on-chain before doing any work
    # Prevents executing tasks from dropped or orphaned transactions
    if assign_tx_id:
        log(f"[{escrow_id}] Waiting for assignment TX to confirm...")
        if not wait_for_confirmation(assign_tx_id, network):
            fail(f"Assignment TX {assign_tx_id} not confirmed — task may have been dropped")
            return
        log(f"[{escrow_id}] Assignment confirmed ✓")

    # Step 1: Research via LLM
    if not api_key and provider != "ollama":
        env_var = ENV_VARS.get(provider, "API key")
        fail(f"No API key — set {env_var} environment variable")
        return
    try:
        log(f"[{escrow_id}] Calling LLM ({provider}/{model}) for research...")
        result = call_llm(task_description, api_key, provider, model=model, base_url=base_url)
        log(f"[{escrow_id}] Research complete ({len(result)} chars)")
    except Exception as e:
        fail(f"LLM call failed: {e}")
        return

    # Step 2: Stamp result on-chain
    try:
        log(f"[{escrow_id}] Stamping result on Signum...")
        hashes = hash_content(result)
        proof, err = publish_proof(passphrase, hashes["content_hash"],
                                   hashes["sources_hash"],
                                   label=f"escrow-{escrow_id}",
                                   network=network)
        if err:
            raise Exception(err)
        stamp_tx   = proof["tx_id"]
        result_hash = hashes["content_hash"]
        log(f"[{escrow_id}] Stamp TX: {stamp_tx}")
    except Exception as e:
        fail(f"Stamp failed: {e}")
        return

    # Step 3: Wait for block confirmation
    log(f"[{escrow_id}] Waiting for stamp to confirm (~4 min)...")
    if not wait_for_confirmation(stamp_tx, network):
        fail(f"Stamp TX not confirmed after {CONFIRM_TIMEOUT}s — TX: {stamp_tx}")
        return
    log(f"[{escrow_id}] Stamp confirmed ✓")

    # Step 4: Self-verify
    try:
        log(f"[{escrow_id}] Self-verifying stamp...")
        verified, details = verify_proof(result, stamp_tx, network=network)
        if not verified:
            raise Exception(f"Hash mismatch: {details.get('onchain_content_hash', '?')} vs {details.get('computed_content_hash', '?')}")
        log(f"[{escrow_id}] Self-verified ✓")
    except Exception as e:
        fail(f"Self-verify failed: {e}")
        return

    # Step 5: Deliver result text to the payer's account as chunked messages.
    # The payer-side listener reassembles these chunks and notifies MK locally.
    result_chunk_txs = []
    try:
        log(f"[{escrow_id}] Delivering result chunks to payer {sender}...")
        result_chunk_txs, err = publish_result_chunks(passphrase, sender, escrow_id,
                                                      result, network)
        if err:
            raise Exception(err)
        log(f"[{escrow_id}] Result chunks sent: {', '.join(map(str, result_chunk_txs))}")
    except Exception as e:
        update_pending_task(escrow_id, status="result_delivery_failed",
                            stamp_tx=stamp_tx,
                            result_hash=result_hash, error=str(e),
                            failed_at=datetime.now().isoformat())
        send_telegram(tg_token, tg_chat_id,
                      f"⚠️ *SignaAI Result Delivery Failed*\n"
                      f"Escrow: `{escrow_id}`\n"
                      f"Stamp TX: `{stamp_tx}`\n"
                      f"{e}",
                      kind=f"result_delivery_failed:{escrow_id}")
        return

    # Step 6: Submit to escrow. Send the marker to the payer so their listener
    # can detect completion without relying on the worker's local Telegram.
    try:
        log(f"[{escrow_id}] Submitting to escrow...")
        submission, err = submit_proof(passphrase, escrow_id, result_hash, stamp_tx,
                                       recipient_address=sender, network=network)
        if err:
            raise Exception(err)
        submit_tx = submission["submit_tx"]
        log(f"[{escrow_id}] Submit TX: {submit_tx}")
    except Exception as e:
        fail(f"Submit failed after result delivery: {e}")
        return

    # Step 7: Local worker receipt only. The full result goes to the payer-side
    # listener so the agent that created the escrow gets the completion message.
    send_telegram(tg_token, tg_chat_id, (
        f"✅ *SignaAI Task Submitted*\n"
        f"Escrow: `{escrow_id}`\n\n"
        f"Result delivered to payer: `{sender}`\n"
        f"Stamp TX: `{stamp_tx}`\n"
        f"Submit TX: `{submit_tx}`"
    ), kind=f"task_submitted:{escrow_id}")

    update_pending_task(escrow_id, status="complete", stamp_tx=stamp_tx,
                        submit_tx=submit_tx, result_hash=result_hash,
                        result_chunk_txs=result_chunk_txs,
                        completed_at=datetime.now().isoformat())

    log(f"[{escrow_id}] Complete ✓  stamp={stamp_tx}  submit={submit_tx}")


# ── Transaction handler ───────────────────────────────────────────────────────

def handle_transaction(tx, address, network, state, tg_token, tg_chat_id,
                       hook_token=None, hook_path="/hooks", gw_port=18789,
                       worker_cfg=None):
    """
    Handle SignaAI messages destined for our address.

    - ESCROW:ASSIGN: worker-side task execution
    - ESCROW:SUBMIT / ESCROW:RESULT: payer-side completion inbox

    Returns True if a relevant message was recorded.
    """
    tx_id = str(tx.get("transaction", tx.get("id", "")))
    if not tx_id:
        return False

    processed = set(state.get("processed_txs", []))
    if tx_id in processed:
        return False

    processed.add(tx_id)
    state["processed_txs"] = list(processed)[-500:]

    recipient = tx.get("recipientRS", tx.get("recipient", ""))
    if address not in recipient:
        return False

    msg = tx.get("attachment", {}).get("message", "")
    sender = tx.get("senderRS", tx.get("sender", "unknown"))

    if msg.startswith(ESCROW_RESULT_PREFIX):
        try:
            escrow_id, index, total, chunk = parse_result_chunk_message(msg)
        except Exception as e:
            log(f"Malformed result chunk in TX {tx_id}: {e}")
            return False
        update_result_chunk(escrow_id, index, total, chunk, tx_id, sender)
        log(f"Result chunk {index}/{total} received for escrow {escrow_id} (TX {tx_id})")
        maybe_notify_payer_result(escrow_id, tg_token, tg_chat_id, network)
        return True

    try:
        parsed = parse_message(msg)
    except Exception:
        return False
    if not isinstance(parsed, EscrowMessage):
        return False

    if parsed.action == "SUBMIT":
        escrow_id = parsed.escrow_id
        update_result_submit(escrow_id, tx_id, parsed.result_hash,
                             parsed.proof_tx, sender)
        log(f"Escrow submission received — escrow {escrow_id} from {sender} "
            f"(proof {parsed.proof_tx}, TX {tx_id})")
        maybe_notify_payer_result(escrow_id, tg_token, tg_chat_id, network)
        return True

    if parsed.action == "CREATE" and parsed.worker == address and parsed.task_description:
        # Worker received a CREATE with task description — treat as task assignment
        escrow_id        = parsed.escrow_id
        task_hash        = parsed.task_hash
        task_description = parsed.task_description
        log(f"CREATE task — escrow {escrow_id} from {sender} (TX {tx_id})")
    elif parsed.action != "ASSIGN":
        return False
    else:
        escrow_id        = parsed.escrow_id
        task_hash        = parsed.task_hash
        task_description = parsed.task_description

    task = {
        "escrow_id":        escrow_id,
        "tx_id":            tx_id,
        "sender":           sender,
        "task_description": task_description,
        "timestamp":        ts(tx.get("timestamp", 0)),
        "raw_message":      msg,
        "detected_at":      datetime.now().isoformat(),
        "status":           "pending",
    }

    claimed, status = claim_pending_task(task)
    if not claimed:
        log(f"Duplicate task ignored — escrow {escrow_id} already {status} (TX {tx_id})")
        return False

    log(f"New task — escrow {escrow_id} from {sender} (TX {tx_id})")

    new_task_notified = send_telegram(tg_token, tg_chat_id, (
        f"*SignaAI: New Task*\n"
        f"Escrow: `{escrow_id}`\n"
        f"From: `{sender}`\n\n"
        f"{'Processing autonomously...' if worker_cfg and task_description else 'Triggering agent...'}"
    ), kind=f"new_task:{escrow_id}")
    if new_task_notified:
        update_pending_task(escrow_id, notified_at=datetime.now().isoformat())
        time.sleep(2)

    if worker_cfg and task_description:
        # Queue task for sequential processing — one at a time, no parallel races
        notify_token   = tg_token
        notify_chat_id = tg_chat_id
        queue_depth = _task_queue.qsize()
        if queue_depth > 0:
            log(f"Task queued (position {queue_depth + 1}) — escrow {escrow_id}")
        _task_queue.put((execute_task_autonomously, (
            escrow_id, tx_id, task_description, sender, address,
            network, worker_cfg, notify_token, notify_chat_id
        )))
    else:
        # Fallback: trigger OpenClaw agent via hooks API
        if not task_description:
            log(f"  No task description in ASSIGN message — falling back to agent trigger")
        trigger_agent(hook_token, hook_path, gw_port, escrow_id, sender,
                      address, task_hash, task_description)

    return True


def fetch_and_check(tx_id, address, network, state, tg_token, tg_chat_id,
                    hook_token=None, hook_path="/hooks", gw_port=18789,
                    worker_cfg=None):
    """Fetch a full transaction by ID then run handle_transaction on it."""
    api = get_api(network)
    result = api.get("getTransaction", transaction=str(tx_id))
    if not ok(result):
        log(f"Could not fetch TX {tx_id}: {result.get('error', 'unknown error')}")
        return False
    return handle_transaction(result, address, network, state, tg_token, tg_chat_id,
                              hook_token, hook_path, gw_port, worker_cfg)


# ── Minimal WebSocket client (stdlib only) ────────────────────────────────────

def _recv_exact(sock, n):
    buf = b""
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk:
            raise ConnectionError("Connection closed")
        buf += chunk
    return buf

def _ws_recv_frame(sock):
    header = _recv_exact(sock, 2)
    opcode = header[0] & 0x0F
    masked = (header[1] & 0x80) != 0
    length = header[1] & 0x7F

    if length == 126:
        length = struct.unpack(">H", _recv_exact(sock, 2))[0]
    elif length == 127:
        length = struct.unpack(">Q", _recv_exact(sock, 8))[0]

    mask_key = _recv_exact(sock, 4) if masked else b""
    payload  = _recv_exact(sock, length)

    if masked:
        payload = bytes(payload[i] ^ mask_key[i % 4] for i in range(len(payload)))

    return opcode, payload

def _ws_send_pong(sock, payload=b""):
    mask_key = os.urandom(4)
    masked = bytes(payload[i] ^ mask_key[i % 4] for i in range(len(payload)))
    sock.sendall(bytes([0x8A, 0x80 | len(payload)]) + mask_key + masked)

def ws_connect(host, port, path):
    key = base64.b64encode(os.urandom(16)).decode()
    sock = socket.create_connection((host, port), timeout=10)
    sock.settimeout(90)
    sock.sendall((
        f"GET {path} HTTP/1.1\r\n"
        f"Host: {host}:{port}\r\n"
        f"Upgrade: websocket\r\n"
        f"Connection: Upgrade\r\n"
        f"Sec-WebSocket-Key: {key}\r\n"
        f"Sec-WebSocket-Version: 13\r\n\r\n"
    ).encode())
    resp = b""
    while b"\r\n\r\n" not in resp:
        resp += sock.recv(1)
    if b"101" not in resp:
        sock.close()
        raise ConnectionError(f"WebSocket upgrade failed: {resp[:80]}")
    return sock


# ── WebSocket event loop ──────────────────────────────────────────────────────

def run_websocket(address, network, state, tg_token, tg_chat_id,
                  hook_token=None, hook_path="/hooks", gw_port=18789,
                  worker_cfg=None):
    """
    Connect to local node WebSocket and process events.
    Returns True  → reconnect (transient error).
    Returns False → fall back to polling (node not available).
    """
    try:
        sock = ws_connect(WS_HOST, WS_PORT, WS_PATH)
    except (ConnectionRefusedError, OSError):
        return False

    log(f"WebSocket connected — ws://{WS_HOST}:{WS_PORT}{WS_PATH}")

    try:
        while True:
            opcode, payload = _ws_recv_frame(sock)

            if opcode == 0x9:
                _ws_send_pong(sock, payload)
                continue
            if opcode == 0x8:
                log("WebSocket closed by node")
                return True
            if opcode != 0x1:
                continue

            try:
                event = json.loads(payload.decode("utf-8"))
            except (json.JSONDecodeError, UnicodeDecodeError):
                continue

            etype    = event.get("e", "")
            epayload = event.get("p", {})

            if etype == "CONNECTED":
                local  = epayload.get("localHeight", "?")
                total  = epayload.get("globalHeight", "?")
                pct    = f"{local/total*100:.1f}%" if isinstance(local, int) and isinstance(total, int) and total else "?"
                syncing = epayload.get("isSyncing", False)
                log(f"Node: {epayload.get('networkName','?')} height={local}/{total} ({pct}) "
                    f"{'— syncing' if syncing else '— synced'}")

            elif etype == "HEARTBEAT":
                pass

            elif etype == "BLOCK_PUSHED":
                local   = epayload.get("localHeight", 0)
                total   = epayload.get("globalHeight", 0)
                syncing = local < total
                if not syncing:
                    log(f"Block {local} pushed")
                    check_pending_releases(network, tg_token, tg_chat_id)
                    check_auto_releases(network, tg_token, tg_chat_id)
                elif local % 10000 == 0:
                    pct = f"{local/total*100:.1f}%" if total else "?"
                    log(f"Syncing... {local}/{total} ({pct})")

            elif etype == "PENDING_TRANSACTIONS_ADDED":
                tx_ids = epayload.get("transactionIds", [])
                if not tx_ids:
                    continue
                log(f"{len(tx_ids)} pending TX(s) — checking...")
                found = sum(
                    fetch_and_check(tid, address, network, state, tg_token, tg_chat_id,
                                    hook_token, hook_path, gw_port, worker_cfg)
                    for tid in tx_ids
                )
                save_state(state)
                if not found:
                    log("No new tasks in batch")

    except (ConnectionError, socket.timeout, OSError) as e:
        log(f"WebSocket error: {e}")
        return True
    finally:
        try:
            sock.close()
        except Exception:
            pass


# ── Polling fallback ──────────────────────────────────────────────────────────

def poll_once(address, network, state, tg_token, tg_chat_id,
              hook_token=None, hook_path="/hooks", gw_port=18789,
              worker_cfg=None):
    api = get_api(network)
    result = api.get("getAccountTransactions",
                     account=address,
                     firstIndex="0",
                     lastIndex="49")
    if not ok(result):
        log(f"API error: {result.get('error')}")
        return

    found = sum(
        handle_transaction(tx, address, network, state, tg_token, tg_chat_id,
                           hook_token, hook_path, gw_port, worker_cfg)
        for tx in (result.get("transactions") or [])
    )
    save_state(state)
    if not found:
        log("No new tasks")
    check_pending_releases(network, tg_token, tg_chat_id)
    check_auto_releases(network, tg_token, tg_chat_id)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="SignaAI Autonomous Worker Daemon")
    parser.add_argument("--address",       default=None,   help="Wallet address to monitor (derived from signaai-worker.json if omitted)")
    parser.add_argument("--network",       default="mainnet", choices=["mainnet", "testnet"])
    parser.add_argument("--poll-interval", type=int, default=POLL_INTERVAL)
    parser.add_argument("--once",          action="store_true", help="Poll once and exit")
    parser.add_argument("--no-websocket",  action="store_true", help="Force polling mode")
    args = parser.parse_args()

    lock_path = acquire_listener_lock(args.network)

    tg_token, tg_chat_id, hook_token, hook_path, gw_port = load_openclaw_config()
    worker_cfg = load_worker_config()

    # Derive address from worker config if not supplied on the command line
    if not args.address:
        if not worker_cfg:
            parser.error("--address is required when no signaai-worker.json is present")
        from wallet import get_my_address
        addr, err = get_my_address(worker_cfg["passphrase"], args.network)
        if err:
            parser.error(f"Could not derive address from worker config: {err}")
        args.address = addr

    print(f"SignaAI Listener starting", flush=True)
    print(f"  PID:         {os.getpid()}", flush=True)
    print(f"  Script:      {os.path.abspath(__file__)}", flush=True)
    print(f"  Commit:      {git_commit()}", flush=True)
    print(f"  Address:     {args.address}", flush=True)
    print(f"  Network:     {args.network}", flush=True)
    print(f"  Lock:        {lock_path}", flush=True)
    print(f"  Tasks:       {TRIGGER_FILE}", flush=True)
    print(f"  Confirm wait:{CONFIRM_TIMEOUT}s ({CONFIRM_POLL}s poll)", flush=True)
    print(f"  Telegram:    {'enabled' if tg_token else 'disabled'}", flush=True)
    if worker_cfg:
        print(f"  Mode:        AUTONOMOUS — payer + worker (any agent can be either)", flush=True)
        provider = worker_cfg.get("provider", "?")
        model    = worker_cfg.get("model", "?")
        has_key  = bool(worker_cfg.get("apiKey")) or provider == "ollama"
        env_hint = ENV_VARS.get(provider, "API key")
        print(f"  LLM:         {provider}/{model} ({'ready' if has_key else f'NO API KEY — set {env_hint}'})", flush=True)
    else:
        print(f"  Mode:        agent trigger (configure {WORKER_CFG} for autonomous)", flush=True)
    print(flush=True)

    state = load_state()

    # On startup: re-queue any tasks that were pending when the daemon last stopped
    if worker_cfg:
        retries = startup_retry_candidates(args.address, args.network)
        if retries:
            log(f"Retrying {len(retries)} pending task(s) from previous session...")
            for task in retries:
                escrow_id = task.get("escrow_id", "")
                task_desc = task.get("task_description", "")
                sender    = task.get("sender", "")
                if not escrow_id or not task_desc:
                    continue
                log(f"  Re-queuing escrow {escrow_id}")
                _task_queue.put((execute_task_autonomously, (
                    escrow_id, task.get("tx_id", ""), task_desc, sender, args.address,
                    args.network, worker_cfg, tg_token, tg_chat_id
                )))

    if args.once:
        poll_once(args.address, args.network, state, tg_token, tg_chat_id,
                  hook_token, hook_path, gw_port, worker_cfg)
        return

    if args.no_websocket:
        print(f"  Connection:  polling every {args.poll_interval}s", flush=True)
        while True:
            state = load_state()
            poll_once(args.address, args.network, state, tg_token, tg_chat_id,
                      hook_token, hook_path, gw_port, worker_cfg)
            time.sleep(args.poll_interval)

    print(f"  Connection:  WebSocket → polling fallback", flush=True)
    print(flush=True)

    ws_available  = True
    reconnect_delay = 5

    while True:
        state = load_state()

        if ws_available:
            should_reconnect = run_websocket(
                args.address, args.network, state, tg_token, tg_chat_id,
                hook_token, hook_path, gw_port, worker_cfg
            )
            if should_reconnect:
                log(f"Reconnecting in {reconnect_delay}s...")
                time.sleep(reconnect_delay)
                reconnect_delay = min(reconnect_delay * 2, 60)
                continue
            else:
                log(f"Node unavailable — polling every {args.poll_interval}s")
                ws_available = False
                reconnect_delay = 5

        poll_once(args.address, args.network, state, tg_token, tg_chat_id,
                  hook_token, hook_path, gw_port, worker_cfg)
        time.sleep(args.poll_interval)

        # Check if node came back online
        try:
            s = socket.create_connection((WS_HOST, WS_PORT), timeout=3)
            s.close()
            log("Node back online — switching to WebSocket")
            ws_available = True
        except OSError:
            pass


if __name__ == "__main__":
    main()
