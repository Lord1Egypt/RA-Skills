#!/usr/bin/env python3
"""
Signum Agent Escrow — AT-backed trustless task payment system

State machine:
  CREATED → SUBMITTED → RELEASED
                      → REFUNDED (if deadline passed, AT auto-refunds)

Funds flow:
  create  → payer deploys AT contract → funds AT address (money leaves payer's wallet)
  release → payer submits preimage to AT → AT auto-releases to worker

All state transitions are recorded as on-chain messages — fully auditable.
AT holds funds trustlessly; once preimage is submitted, payment cannot be cancelled.

On-chain message format:
  ESCROW:CREATE:<escrow_id>:<worker>:<amount_nqt>:<task_hash>:<deadline_block>:<at_address>
  ESCROW:SUBMIT:<escrow_id>:<result_hash>:<proof_tx>
  ESCROW:RELEASE:<escrow_id>:<worker>
  ESCROW:REFUND:<escrow_id>:<payer>

Usage:
  python3 escrow.py create <payer_passphrase> <worker_address> <amount> "<task_description>" [--deadline-hours 24]
  python3 escrow.py submit <worker_passphrase> <escrow_id> "<result_content>" [--sources "url1,url2"]
  python3 escrow.py release <payer_passphrase> <escrow_id>
  python3 escrow.py refund <payer_passphrase> <escrow_id>
  python3 escrow.py status <escrow_id>
"""
import sys
import os
import json
import hashlib
import secrets
import time
sys.path.insert(0, os.path.dirname(__file__))
from signum_api import get_api, signa, nqt, ts, fee_message, FEE_STANDARD, ok
from wallet import get_my_address, send_signa, get_transactions
from verify import hash_content, publish_proof
from _deploy_at import deploy_at as _at_deploy, submit_preimage as _at_submit, gen_preimage
from protocol import (
    build_escrow_create, build_escrow_fund, build_escrow_assign,
    build_escrow_submit, build_escrow_release, build_escrow_refund,
    parse_message, EscrowMessage,
)

# ── Constants ─────────────────────────────────────────────────────────────────
ESCROW_PREFIX    = "ESCROW:"
BLOCKS_PER_HOUR  = 15  # ~4 min per block = 15 blocks/hour
DEDUP_FILE       = os.path.expanduser("~/.openclaw/workspace/signaai-escrow-dedup.json")
DEDUP_TTL        = 3600  # seconds — ignore duplicate requests within 1 hour
RELEASE_LOG_FILE      = os.path.expanduser("~/.openclaw/workspace/signaai-release-log.json")
PENDING_RELEASES_FILE = os.path.expanduser("~/.openclaw/workspace/signaai-pending-releases.json")
PREIMAGE_DIR          = os.path.expanduser("~/.signaai/preimages")
RECEIPT_FILE          = os.path.expanduser("~/.openclaw/workspace/signaai-last-escrow-receipt.txt")

# Escrow states
STATE_CREATED   = "CREATED"
STATE_SUBMITTED = "SUBMITTED"
STATE_RELEASED  = "RELEASED"
STATE_REFUNDED  = "REFUNDED"


# ── Helpers ───────────────────────────────────────────────────────────────────

def _dedup_check(task_description):
    """
    Returns existing escrow_id if this task was already created within DEDUP_TTL.
    Returns "pending" if creation is in progress (race condition guard).
    Returns None if this is a new task — safe to proceed.
    """
    task_key = hashlib.sha256(task_description.strip().lower().encode()).hexdigest()[:16]
    try:
        if os.path.exists(DEDUP_FILE):
            with open(DEDUP_FILE) as f:
                dedup = json.load(f)
            entry = dedup.get(task_key)
            if entry:
                age = time.time() - entry["created_at"]
                ttl = 1800 if entry["escrow_id"] == "pending" else DEDUP_TTL
                if age < ttl:
                    return entry["escrow_id"]  # may be "pending" or real ID
    except Exception:
        pass
    return None

def _dedup_record(task_description, escrow_id):
    """Record a newly created escrow to prevent duplicates."""
    task_key = hashlib.sha256(task_description.strip().lower().encode()).hexdigest()[:16]
    try:
        dedup = {}
        if os.path.exists(DEDUP_FILE):
            with open(DEDUP_FILE) as f:
                dedup = json.load(f)
        # Prune old entries
        now = time.time()
        dedup = {k: v for k, v in dedup.items() if now - v["created_at"] < DEDUP_TTL}
        dedup[task_key] = {"escrow_id": escrow_id, "created_at": now}
        os.makedirs(os.path.dirname(DEDUP_FILE), exist_ok=True)
        tmp = DEDUP_FILE + ".tmp"
        with open(tmp, "w") as f:
            json.dump(dedup, f, indent=2)
        os.replace(tmp, DEDUP_FILE)
    except Exception:
        pass

def _release_check(escrow_id):
    """Return existing release TX if this escrow was already released locally. None if safe to proceed."""
    try:
        if os.path.exists(RELEASE_LOG_FILE):
            with open(RELEASE_LOG_FILE) as f:
                log = json.load(f)
            entry = log.get(escrow_id)
            if entry:
                return entry.get("tx_id")
    except Exception:
        pass
    return None

def _release_record(escrow_id, tx_id):
    """Record a completed release so repeat calls are blocked instantly."""
    try:
        log = {}
        if os.path.exists(RELEASE_LOG_FILE):
            with open(RELEASE_LOG_FILE) as f:
                log = json.load(f)
        log[escrow_id] = {"tx_id": tx_id, "released_at": time.time()}
        os.makedirs(os.path.dirname(RELEASE_LOG_FILE), exist_ok=True)
        tmp = RELEASE_LOG_FILE + ".tmp"
        with open(tmp, "w") as f:
            json.dump(log, f, indent=2)
        os.replace(tmp, RELEASE_LOG_FILE)
    except Exception:
        pass


def _save_pending_release(escrow_id, at_address, worker, amount_signa, preimage_tx):
    """Write a pending-release entry so the listener can watch for the AT payout."""
    try:
        os.makedirs(os.path.dirname(PENDING_RELEASES_FILE), exist_ok=True)
        entries = []
        if os.path.exists(PENDING_RELEASES_FILE):
            try:
                with open(PENDING_RELEASES_FILE) as f:
                    entries = json.load(f)
            except Exception:
                entries = []
        entries = [e for e in entries if e.get("escrow_id") != escrow_id]
        entries.append({
            "escrow_id":    escrow_id,
            "at_address":   at_address,
            "worker":       worker,
            "amount_signa": float(amount_signa),
            "preimage_tx":  str(preimage_tx),
            "submitted_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        })
        tmp = PENDING_RELEASES_FILE + ".tmp"
        with open(tmp, "w") as f:
            json.dump(entries, f, indent=2)
        os.replace(tmp, PENDING_RELEASES_FILE)
    except Exception:
        pass

def _format_escrow_receipt(escrow, deadline_hours=None):
    """Return the canonical receipt shown to the payer after escrow creation."""
    amount = escrow.get("amount_signa", 0)
    amount_text = f"{float(amount):g}"

    if deadline_hours is None:
        create_height = int(escrow.get("create_height") or escrow.get("current_block") or 0)
        deadline_block = int(escrow.get("deadline_block") or 0)
        if create_height and deadline_block > create_height:
            deadline_hours = round((deadline_block - create_height) / BLOCKS_PER_HOUR)
        else:
            deadline_hours = 24
    deadline_text = f"{float(deadline_hours):g}"

    return (
        "Escrow created:\n"
        f"ID: {escrow['escrow_id']}\n"
        f"Record TX: {escrow.get('record_tx') or escrow.get('create_tx')}\n"
        f"Fund TX: {escrow.get('fund_tx')}\n\n"
        f"Task sent to worker ({amount_text} SIGNA, {deadline_text}h deadline). "
        "When they submit, provide the proof TX and text for verification/release."
    )

def _store_last_receipt(receipt):
    """Persist the last create receipt so OpenClaw can recover it if stdout is lost."""
    try:
        os.makedirs(os.path.dirname(RECEIPT_FILE), exist_ok=True)
        tmp = RECEIPT_FILE + ".tmp"
        with open(tmp, "w") as f:
            f.write(receipt.rstrip() + "\n")
        os.replace(tmp, RECEIPT_FILE)
    except Exception:
        pass


def _load_tg_config():
    """Read Telegram bot token and chat ID from OpenClaw config."""
    try:
        cfg_path = os.path.expanduser("~/.openclaw/openclaw.json")
        with open(cfg_path) as f:
            cfg = json.load(f)
        tg = cfg.get("channels", {}).get("telegram", {})
        token = tg.get("botToken", "") or None
        approvers = tg.get("execApprovals", {}).get("approvers", [])
        chat_id = approvers[0] if approvers else None
        return token, chat_id
    except Exception:
        return None, None


def _send_telegram(token, chat_id, message):
    """Send a Telegram message. Silently no-ops if not configured."""
    if not token or not chat_id:
        return
    import urllib.request, urllib.parse
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
        data = urllib.parse.urlencode(payload).encode()
        urllib.request.urlopen(urllib.request.Request(url, data=data), timeout=10)
    except Exception:
        try:
            payload = {"chat_id": chat_id, "text": message}
            data = urllib.parse.urlencode(payload).encode()
            urllib.request.urlopen(urllib.request.Request(url, data=data), timeout=10)
        except Exception:
            pass


def _store_preimage(escrow_id, preimage, at_address, deploy_tx):
    """Store preimage in a per-escrow file with 0o600 permissions. Never goes on-chain."""
    try:
        os.makedirs(PREIMAGE_DIR, exist_ok=True)
        path = os.path.join(PREIMAGE_DIR, f"{escrow_id}.json")
        tmp  = path + ".tmp"
        with open(tmp, "w") as f:
            json.dump({
                "preimage":   preimage,
                "at_address": at_address,
                "deploy_tx":  deploy_tx,
                "created_at": time.time(),
            }, f, indent=2)
        os.replace(tmp, path)
        os.chmod(path, 0o600)
        os.chmod(PREIMAGE_DIR, 0o700)
    except Exception as e:
        print(f"  Warning: could not store preimage: {e}")


def _load_preimage(escrow_id):
    """Load stored preimage data for an escrow. Returns {} if not found."""
    try:
        path = os.path.join(PREIMAGE_DIR, f"{escrow_id}.json")
        if os.path.exists(path):
            with open(path) as f:
                return json.load(f)
    except Exception:
        pass
    return {}

def _find_at_payout(api, at_address, worker_address, limit=99):
    """Return an AT payout transaction to the worker, if one is visible."""
    if not at_address or not worker_address:
        return None

    at_account = api.get("getAccount", account=at_address)
    at_numeric = str(at_account.get("account", ""))

    worker_txs = api.get("getAccountTransactions",
                         account=worker_address,
                         firstIndex=0,
                         lastIndex=limit)
    for tx in (worker_txs.get("transactions") or []):
        sender_rs = tx.get("senderRS", "")
        sender_id = str(tx.get("sender", ""))
        amount_nqt = int(tx.get("amountNQT") or 0)
        if amount_nqt <= 0:
            continue
        if sender_rs == at_address or (at_numeric and sender_id == at_numeric):
            return {
                "tx_id": tx.get("transaction"),
                "amount_nqt": amount_nqt,
                "height": tx.get("height"),
            }
    return None

def _find_at_preimage_submission(api, at_address, sender_address, preimage, limit=99):
    """Return a previous preimage submission TX to the AT, if one is visible."""
    if not at_address or not sender_address or not preimage:
        return None

    sender_txs = api.get("getAccountTransactions",
                         account=sender_address,
                         firstIndex=0,
                         lastIndex=limit)
    for tx in (sender_txs.get("transactions") or []):
        msg = tx.get("attachment", {}).get("message", "")
        if tx.get("recipientRS") == at_address and msg == preimage:
            return tx.get("transaction")
    return None


def _check_onchain_escrow(escrow_id, address, network):
    """Return existing escrow dict if this escrow_id already exists on-chain. None if new."""
    api = get_api(network)
    result = api.get("getAccountTransactions",
                     account=address,
                     firstIndex=0,
                     lastIndex=49)
    txs = [tx for tx in (result.get("transactions") or [])
           if f"ESCROW:CREATE:{escrow_id}" in tx.get("attachment", {}).get("message", "")]
    if not txs:
        return None
    escrow, _ = _parse_escrow_from_txs(escrow_id, txs)
    preimage_data = _load_preimage(escrow_id)
    if preimage_data.get("at_address"):
        escrow["at_address"] = preimage_data["at_address"]
        escrow["deploy_tx"]  = preimage_data.get("deploy_tx", "")
    return escrow if escrow.get("payer") else None


def _read_telegram_config():
    """Read payer's Telegram bot token and chat ID from openclaw.json."""
    try:
        cfg_path = os.path.expanduser("~/.openclaw/openclaw.json")
        with open(cfg_path) as f:
            cfg = json.load(f)
        tg = cfg.get("channels", {}).get("telegram", {})
        token = tg.get("botToken", "") or ""
        approvers = tg.get("execApprovals", {}).get("approvers", [])
        chat_id = str(approvers[0]) if approvers else ""
        return token, chat_id
    except Exception:
        return "", ""


# ── Core Functions ────────────────────────────────────────────────────────────

def create_escrow(payer_passphrase, worker_address, amount_signa,
                  task_description, deadline_hours=24, network=None):
    """
    Create an escrow agreement on-chain.

    Steps:
    1. Generate a unique escrow ID
    2. Compute task hash (what the worker must deliver)
    3. Record escrow creation on-chain (payer → self message)
    4. Transfer funds to escrow operator wallet

    Returns escrow_id and full escrow record.
    """
    if not payer_passphrase or not str(payer_passphrase).strip():
        return None, "Payer passphrase cannot be empty"

    # Hard dedup — refuse to create a second escrow for the same task within 1 hour
    # Write "pending" BEFORE any blockchain calls — prevents race condition with parallel tool calls
    existing = _dedup_check(task_description)
    if existing and existing != "pending":
        print(f"  Duplicate detected — escrow {existing} already created for this task.")
        return {"escrow_id": existing, "duplicate": True}, None
    if existing == "pending":
        return None, "Escrow creation already in progress for this task — wait and retry."
    _dedup_record(task_description, "pending")  # reserve slot immediately

    api = get_api(network)

    # Get payer address
    payer_address, err = get_my_address(payer_passphrase, network)
    if err:
        return None, f"Could not derive payer address: {err}"

    # Get current block for deadline calculation
    status = api.get("getBlockchainStatus")
    if not ok(status):
        return None, "Could not get blockchain status"

    current_block = int(status.get("numberOfBlocks", 0))
    deadline_block = current_block + (deadline_hours * BLOCKS_PER_HOUR)

    # Hash the task description — this is what the worker must reference
    task_hash = hashlib.sha256(task_description.encode()).hexdigest()

    # Deterministic escrow_id: survives machine restarts and dedup file loss
    # Buckets to nearest hour so retries within the same hour produce the same ID
    timestamp_bucket = int(time.time() // 3600) * 3600
    escrow_id = hashlib.sha256(
        f"{payer_address}:{task_hash}:{timestamp_bucket}".encode()
    ).hexdigest()[:16]

    # On-chain idempotency: check if this escrow already exists (survives local dedup loss)
    onchain = _check_onchain_escrow(escrow_id, payer_address, network)
    if onchain:
        print(f"  On-chain escrow {escrow_id} already exists — returning it.")
        _dedup_record(task_description, escrow_id)
        return onchain, None

    try:
        amount_nqt = nqt(amount_signa)
    except ValueError as exc:
        return None, str(exc)
    if amount_nqt <= 0:
        return None, "Amount must be greater than zero"

    # Generate preimage for AT — kept secret until release
    preimage, _ = gen_preimage()

    # Emit escrow ID immediately — Claude may time out during the 4-min AT wait,
    # so print the ID before blocking so the agent can relay it to the user.
    print(f"Escrow ID: {escrow_id}", flush=True)
    print(f"(Deploying AT contract — takes ~4 minutes for block confirmation)", flush=True)

    # Step 1: Deploy AT contract — funds will be held trustlessly until release
    # AT auto-refunds to payer after deadline_block if worker never submits
    print(f"  Deploying AT escrow contract (takes ~4 min for block confirmation)...", flush=True)
    at_result, err = _at_deploy(
        payer_passphrase, worker_address,
        deadline_block, preimage,
        escrow_id=escrow_id, network=network
    )
    if err:
        return None, f"AT deployment failed: {err}"

    at_address = at_result["at_address"]
    deploy_tx  = at_result["tx_id"]

    # Step 2: Fund AT — money leaves payer's wallet into the AT contract
    print(f"  Funding AT {at_address} with {amount_signa} SIGNA...")
    fund_message = build_escrow_fund(escrow_id)
    fund_tx, err = send_signa(payer_passphrase, at_address, amount_signa,
                              message=fund_message, network=network)
    if err:
        return None, f"Failed to fund AT: {err}"

    # Store preimage locally — used at release time, never goes on-chain
    _store_preimage(escrow_id, preimage, at_address, deploy_tx)

    # Step 3: Record escrow creation on-chain (payer → self audit record)
    print(f"  Recording escrow on-chain...")
    time.sleep(2)
    message = build_escrow_create(escrow_id, worker_address, amount_nqt,
                                   task_hash, deadline_block, operator=at_address)
    record_result = api.post("sendMessage",
                             secretPhrase=payer_passphrase,
                             recipient=payer_address,
                             message=message,
                             messageIsText="true",
                             feeNQT=fee_message(message))
    if not ok(record_result):
        return None, f"Failed to record escrow: {record_result.get('error')}"
    record_tx = record_result.get("transaction")

    # Step 4a: Notify the worker via on-chain CREATE message (includes task description)
    # Primary notification path — worker listener handles ESCROW:CREATE with worker=their address
    print(f"  Sending CREATE to worker...")
    time.sleep(2)
    worker_create_msg = build_escrow_create(escrow_id, worker_address, amount_nqt,
                                             task_hash, deadline_block,
                                             operator=at_address,
                                             task_description=task_description[:900])
    create_result = api.post("sendMessage",
                              secretPhrase=payer_passphrase,
                              recipient=worker_address,
                              message=worker_create_msg,
                              messageIsText="true",
                              feeNQT=fee_message(worker_create_msg))
    if not ok(create_result):
        print(f"  Warning: worker CREATE failed: {create_result.get('error')} — falling back to ASSIGN")

    # Step 4b: Also send ASSIGN to worker (backward-compatible fallback)
    print(f"  Sending ASSIGN to worker...")
    time.sleep(2)
    notify_message = build_escrow_assign(escrow_id, task_hash,
                                          task_description[:900])
    assign_result = api.post("sendMessage",
                              secretPhrase=payer_passphrase,
                              recipient=worker_address,
                              message=notify_message,
                              messageIsText="true",
                              feeNQT=fee_message(notify_message))
    if not ok(assign_result):
        assign_err = assign_result.get("error", "unknown error")
        if not ok(create_result):
            return None, f"Failed to notify worker (both CREATE and ASSIGN failed): {assign_err}"
        print(f"  Warning: ASSIGN failed ({assign_err}) — worker will be notified via CREATE")

    escrow = {
        "escrow_id":   escrow_id,
        "state":       STATE_CREATED,
        "payer":       payer_address,
        "worker":      worker_address,
        "amount_signa": amount_signa,
        "task_description": task_description,
        "task_hash":   task_hash,
        "deadline_block": deadline_block,
        "at_address":  at_address,
        "deploy_tx":   deploy_tx,
        "record_tx":   record_tx,
        "fund_tx":     fund_tx,
        "current_block": current_block,
    }

    # Record in dedup file — prevents duplicate creation even if script is called again
    _dedup_record(task_description, escrow_id)

    return escrow, None


def submit_result(worker_passphrase, escrow_id, result_content,
                  sources=None, recipient_address=None, network=None):
    """
    Worker submits completed task result on-chain.

    1. Hash the result content
    2. Publish hash to Signum (verifiable proof)
    3. Send submission message to escrow record
    """
    if not worker_passphrase or not str(worker_passphrase).strip():
        return None, "Worker passphrase cannot be empty"

    api = get_api(network)

    worker_address, err = get_my_address(worker_passphrase, network)
    if err:
        return None, err

    # Hash the result
    hashes = hash_content(result_content, sources)
    result_hash = hashes["content_hash"]

    # Publish proof on-chain first
    print(f"  Publishing result proof on-chain...")
    proof, err = publish_proof(worker_passphrase, result_hash,
                               hashes["sources_hash"],
                               label=f"escrow-{escrow_id}",
                               network=network)
    if err:
        return None, f"Failed to publish proof: {err}"

    time.sleep(2)

    submission, err = submit_proof(
        worker_passphrase, escrow_id, result_hash, proof["tx_id"],
        recipient_address=recipient_address, network=network
    )
    if err:
        return None, err
    submit_tx = submission["submit_tx"]

    return {
        "escrow_id": escrow_id,
        "worker": worker_address,
        "result_hash": result_hash,
        "proof_tx": proof["tx_id"],
        "submit_tx": submit_tx,
        "state": STATE_SUBMITTED,
    }, None


def submit_proof(worker_passphrase, escrow_id, result_hash, proof_tx,
                 recipient_address=None, network=None):
    """
    Submit an already-stamped result proof to escrow without stamping again.

    The autonomous listener stamps and self-verifies first, then calls this so
    a successful task produces one SIGPROOF and one ESCROW:SUBMIT.
    """
    if not worker_passphrase or not str(worker_passphrase).strip():
        return None, "Worker passphrase cannot be empty"
    if not result_hash:
        return None, "result_hash is required"
    if not proof_tx:
        return None, "proof_tx is required"

    api = get_api(network)
    worker_address, err = get_my_address(worker_passphrase, network)
    if err:
        return None, err

    recipient_address = str(recipient_address or worker_address).strip()
    if not recipient_address:
        return None, "recipient_address cannot be empty"

    message = build_escrow_submit(escrow_id, result_hash, proof_tx)
    print(f"  Submitting result to escrow...")
    submit_result_tx = api.post("sendMessage",
                                secretPhrase=worker_passphrase,
                                recipient=recipient_address,
                                message=message,
                                messageIsText="true",
                                feeNQT=fee_message(message))
    if not ok(submit_result_tx):
        return None, f"Failed to submit result: {submit_result_tx.get('error')}"

    return {
        "escrow_id": escrow_id,
        "worker": worker_address,
        "recipient": recipient_address,
        "result_hash": result_hash,
        "proof_tx": proof_tx,
        "submit_tx": submit_result_tx.get("transaction"),
        "state": STATE_SUBMITTED,
    }, None


def release_payment(operator_passphrase, escrow_id, network=None):
    """
    Release escrow funds to worker after verifying result hash matches.
    Called by operator after confirming submission is valid.

    In AT version: this happens automatically when hash matches.
    """
    if not operator_passphrase or not str(operator_passphrase).strip():
        return None, "Operator passphrase cannot be empty"

    # Local dedup — no network call needed, blocks repeat releases instantly
    existing_tx = _release_check(escrow_id)
    if existing_tx:
        return None, f"Escrow already released — TX: {existing_tx}. Nothing to do."

    api = get_api(network)

    operator_address, err = get_my_address(operator_passphrase, network)
    if err:
        return None, err

    # Secondary check: on-chain state
    escrow_data, err = get_escrow_status(escrow_id, address=operator_address, network=network)
    if err:
        return None, err

    worker = escrow_data.get("worker")
    amount = escrow_data.get("amount_signa", 0)

    if not worker:
        return None, "Could not determine worker address from escrow record"

    preimage_data = _load_preimage(escrow_id)
    preimage   = preimage_data.get("preimage")
    at_address = escrow_data.get("at_address") or preimage_data.get("at_address")

    if at_address:
        payout = _find_at_payout(api, at_address, worker)
        if payout:
            _release_record(escrow_id, payout["tx_id"])  # backfill local log
            return None, f"Escrow already released by AT - TX: {payout['tx_id']}. Nothing to do."

        pending_release_tx = _find_at_preimage_submission(
            api, at_address, operator_address, preimage
        )
        if pending_release_tx:
            return None, (f"AT release already submitted - TX: {pending_release_tx}. "
                          "Waiting for AT payout.")

    if escrow_data["state"] == STATE_RELEASED:
        release_tx = escrow_data.get("release_tx", "unknown")
        _release_record(escrow_id, release_tx)  # backfill local log
        return None, f"Escrow already released — TX: {release_tx}. Nothing to do."

    if escrow_data["state"] == STATE_REFUNDED:
        return None, f"Escrow already refunded. Nothing to do."

    if escrow_data["state"] != STATE_SUBMITTED:
        return None, f"Escrow not in SUBMITTED state (current: {escrow_data['state']})"

    # Verify proof TX hash matches submitted hash — no full text needed
    submitted_hash = escrow_data.get("submitted_hash", "")
    proof_tx_id = escrow_data.get("proof_tx", "")

    if submitted_hash and proof_tx_id:
        print(f"  Verifying proof hash on-chain...")
        proof_tx = api.get("getTransaction", transaction=proof_tx_id)
        if ok(proof_tx):
            proof_msg = proof_tx.get("attachment", {}).get("message", "")
            # SIGPROOF:v1:<content_hash>:<sources_hash>
            parts = proof_msg.split(":")
            onchain_hash = parts[2] if len(parts) > 2 else ""
            if onchain_hash and submitted_hash != onchain_hash:
                return None, (f"Hash mismatch — submitted: {submitted_hash[:16]}... "
                              f"on-chain proof: {onchain_hash[:16]}... "
                              f"Worker's proof TX does not match their submission.")
            print(f"  Hash verified ✓")
        else:
            print(f"  Warning: could not fetch proof TX {proof_tx_id} — skipping hash check")

    if preimage and at_address:
        # AT release: submit preimage → AT verifies hash → auto-releases to worker
        # Once submitted, payer cannot cancel — AT executes on next block
        print(f"  Submitting preimage to AT {at_address}...")
        at_result, err = _at_submit(operator_passphrase, at_address, preimage, network)
        if err:
            return None, f"AT release failed: {err}"
        tx_id = at_result["tx_id"]
        print(f"  Preimage submitted — AT will release {amount} SIGNA to worker on next block (~4 min)")
        _save_pending_release(escrow_id, at_address, worker, amount, tx_id)
        state = "PREIMAGE_SUBMITTED"
    else:
        # Phase 1 fallback: direct payment (legacy escrows without AT)
        print(f"  No AT found for this escrow — using direct payment...")
        print(f"  Releasing {amount} SIGNA to {worker}...")
        release_message = build_escrow_release(escrow_id, worker)
        tx_id, err = send_signa(operator_passphrase, worker, amount,
                                message=release_message, network=network)
        if err:
            return None, f"Release failed: {err}"
        # Direct payment has actually moved funds, so dedup future releases.
        _release_record(escrow_id, tx_id)
        state = STATE_RELEASED

    return {
        "escrow_id":  escrow_id,
        "state":      state,
        "worker":     worker,
        "amount_signa": amount,
        "tx_id":      tx_id,
        "at_address": at_address or "",
    }, None


def refund_escrow(operator_passphrase, escrow_id, network=None):
    """
    Refund escrow to payer if deadline has passed without valid submission.
    """
    api = get_api(network)

    operator_address, err = get_my_address(operator_passphrase, network)
    if err:
        return None, err

    escrow_data, err = get_escrow_status(escrow_id, address=operator_address, network=network)
    if err:
        return None, err

    if escrow_data["state"] == STATE_RELEASED:
        return None, "Escrow already released — cannot refund"

    # Check deadline
    status = api.get("getBlockchainStatus")
    current_block = int(status.get("numberOfBlocks", 0))
    deadline_block = escrow_data.get("deadline_block", 0)

    if current_block < deadline_block and escrow_data["state"] != STATE_CREATED:
        blocks_left = deadline_block - current_block
        hours_left = blocks_left / BLOCKS_PER_HOUR
        return None, f"Deadline not reached — {blocks_left} blocks ({hours_left:.1f}h) remaining"

    payer = escrow_data.get("payer")
    amount = escrow_data.get("amount_signa", 0)

    if not payer:
        return None, "Could not determine payer address"

    print(f"  Refunding {amount} SIGNA to {payer}...")
    refund_message = build_escrow_refund(escrow_id, payer)
    tx_id, err = send_signa(operator_passphrase, payer, amount,
                            message=refund_message, network=network)
    if err:
        return None, f"Refund failed: {err}"

    return {
        "escrow_id": escrow_id,
        "state": STATE_REFUNDED,
        "payer": payer,
        "amount_signa": amount,
        "tx_id": tx_id,
    }, None


def get_escrow_status(escrow_id, address=None, network=None):
    """
    Reconstruct escrow state from on-chain messages.
    Scans transaction history for ESCROW: messages matching the escrow_id.
    """
    api = get_api(network)

    # If no address provided, use the dev wallet (escrow operator)
    # In production: query the AT contract directly
    if not address:
        # Try to find the escrow in recent transactions
        # For prototype, we scan a known address
        return _scan_for_escrow(escrow_id, network)

    result = api.get("getAccountTransactions",
                     account=address,
                     firstIndex=0,
                     lastIndex=99)

    txs = result.get("transactions", [])
    escrow, err = _parse_escrow_from_txs(escrow_id, txs)

    # If we found a worker address different from the scanned address,
    # also scan the worker's transactions to pick up SUBMIT messages
    worker = escrow.get("worker")
    if worker and worker != address and escrow.get("state") == STATE_CREATED:
        worker_result = api.get("getAccountTransactions",
                                account=worker,
                                firstIndex=0,
                                lastIndex=99)
        worker_txs = worker_result.get("transactions", [])
        escrow2, _ = _parse_escrow_from_txs(escrow_id, worker_txs)
        # Merge — keep base data from first scan, take higher state from worker scan
        if escrow2.get("state") in (STATE_SUBMITTED, STATE_RELEASED, STATE_REFUNDED):
            escrow.update({k: v for k, v in escrow2.items()
                           if k not in ("payer", "worker", "amount_nqt", "amount_signa",
                                        "task_hash", "deadline_block", "create_tx", "created_at")})

    if escrow.get("at_address") and escrow.get("worker") and escrow.get("state") in (STATE_CREATED, STATE_SUBMITTED):
        payout = _find_at_payout(api, escrow["at_address"], escrow["worker"])
        if payout:
            escrow["state"] = STATE_RELEASED
            escrow["release_tx"] = payout["tx_id"]
            escrow["released_amount_nqt"] = payout["amount_nqt"]
            escrow["released_at_height"] = payout["height"]

    return escrow, err


def _scan_for_escrow(escrow_id, network=None):
    """Scan recent chain transactions for an escrow record."""
    api = get_api(network)

    # This is a simplified scan — in production use an indexed store
    result = api.get("getUnconfirmedTransactions")
    txs = result.get("unconfirmedTransactions", [])

    state, err = _parse_escrow_from_txs(escrow_id, txs)
    if state and state.get("state"):
        return state, None

    return {"escrow_id": escrow_id, "state": "UNKNOWN",
            "note": "Provide --address to scan a specific account"}, None


def _parse_escrow_from_txs(escrow_id, transactions):
    """Parse escrow state from a list of transactions."""
    # State priority — higher index wins
    STATE_RANK = {STATE_CREATED: 0, STATE_SUBMITTED: 1,
                  STATE_RELEASED: 2, STATE_REFUNDED: 2}

    escrow = {"escrow_id": escrow_id, "state": "UNKNOWN"}
    best_rank = -1

    for tx in transactions:
        msg = tx.get("attachment", {}).get("message", "")
        if not msg.startswith(ESCROW_PREFIX):
            continue
        if escrow_id not in msg:
            continue

        try:
            parsed = parse_message(msg)
        except Exception:
            continue
        if not isinstance(parsed, EscrowMessage):
            continue
        if parsed.escrow_id != escrow_id:
            continue

        action = parsed.action

        if action == "CREATE":
            escrow.update({
                "payer":          tx.get("senderRS"),
                "worker":         parsed.worker,
                "amount_nqt":     parsed.amount_nqt,
                "amount_signa":   parsed.amount_nqt / 100_000_000,
                "task_hash":      parsed.task_hash,
                "deadline_block": parsed.deadline_block,
                "at_address":     parsed.operator,
                "create_tx":      tx.get("transaction"),
                "record_tx":      tx.get("transaction"),
                "create_height":  tx.get("height"),
                "created_at":     ts(tx.get("timestamp")),
            })
            if STATE_RANK[STATE_CREATED] > best_rank:
                escrow["state"] = STATE_CREATED
                best_rank = STATE_RANK[STATE_CREATED]
        elif action == "FUND":
            escrow.update({
                "fund_tx":   tx.get("transaction"),
                "funded_at": ts(tx.get("timestamp")),
            })
        elif action == "SUBMIT":
            if STATE_RANK[STATE_SUBMITTED] > best_rank:
                escrow.update({
                    "state":        STATE_SUBMITTED,
                    "submitted_hash": parsed.result_hash,
                    "proof_tx":     parsed.proof_tx,
                    "submit_tx":    tx.get("transaction"),
                    "submitted_at": ts(tx.get("timestamp")),
                    "submitted_by": tx.get("senderRS"),
                })
                best_rank = STATE_RANK[STATE_SUBMITTED]
        elif action == "RELEASE":
            if STATE_RANK[STATE_RELEASED] > best_rank:
                escrow.update({
                    "state":       STATE_RELEASED,
                    "release_tx":  tx.get("transaction"),
                    "released_at": ts(tx.get("timestamp")),
                })
                best_rank = STATE_RANK[STATE_RELEASED]
        elif action == "REFUND":
            if STATE_RANK[STATE_REFUNDED] > best_rank:
                escrow.update({
                    "state":       STATE_REFUNDED,
                    "refund_tx":   tx.get("transaction"),
                    "refunded_at": ts(tx.get("timestamp")),
                })
                best_rank = STATE_RANK[STATE_REFUNDED]

    return escrow, None


# ── CLI ───────────────────────────────────────────────────────────────────────
def main():
    import argparse
    parser = argparse.ArgumentParser(description="Signum Agent Escrow")
    parser.add_argument("--network", default=os.environ.get("SIGNUM_NETWORK", "testnet"),
                        choices=["mainnet", "testnet"])
    sub = parser.add_subparsers(dest="cmd")

    # create
    p = sub.add_parser("create", help="Create a new escrow")
    p.add_argument("payer_passphrase")
    p.add_argument("worker_address")
    p.add_argument("amount", type=float, help="SIGNA amount")
    p.add_argument("task_description")
    p.add_argument("--deadline-hours", type=int, default=24)

    # submit
    p = sub.add_parser("submit", help="Worker submits completed result")
    p.add_argument("worker_passphrase")
    p.add_argument("escrow_id")
    p.add_argument("result_content")
    p.add_argument("--sources", default="")
    p.add_argument("--recipient", default=None,
                   help="Payer address to receive the ESCROW:SUBMIT marker")

    # release
    p = sub.add_parser("release", help="Release payment to worker")
    p.add_argument("operator_passphrase")
    p.add_argument("escrow_id")

    # refund
    p = sub.add_parser("refund", help="Refund payment to payer")
    p.add_argument("operator_passphrase")
    p.add_argument("escrow_id")

    # status
    p = sub.add_parser("status", help="Check escrow status")
    p.add_argument("escrow_id")
    p.add_argument("--address", default=None)

    # receipt
    p = sub.add_parser("receipt", help="Print canonical escrow creation receipt")
    p.add_argument("escrow_id")
    p.add_argument("--address", required=True, help="Payer address to scan")

    args = parser.parse_args()
    os.environ["SIGNUM_NETWORK"] = args.network

    if args.cmd == "create":
        print(f"Creating escrow on {args.network}...")
        result, err = create_escrow(
            args.payer_passphrase, args.worker_address, args.amount,
            args.task_description, args.deadline_hours, args.network
        )
        if err:
            print(f"Error: {err}")
        else:
            receipt = _format_escrow_receipt(result, deadline_hours=args.deadline_hours)
            _store_last_receipt(receipt)
            tg_token, tg_chat_id = _load_tg_config()
            _send_telegram(tg_token, tg_chat_id,
                           f"🔐 *Escrow Created*\n"
                           f"ID: `{result['escrow_id']}`\n"
                           f"Record TX: `{result.get('record_tx') or result.get('create_tx')}`\n"
                           f"Fund TX: `{result.get('fund_tx')}`\n\n"
                           f"Task sent to worker ({float(args.amount):g} SIGNA, "
                           f"{float(args.deadline_hours):g}h deadline).")
            print()
            print(receipt, flush=True)

    elif args.cmd == "submit":
        sources = [s.strip() for s in args.sources.split(",") if s.strip()]
        print(f"Submitting result for escrow {args.escrow_id}...")
        result, err = submit_result(
            args.worker_passphrase, args.escrow_id,
            args.result_content, sources,
            recipient_address=args.recipient, network=args.network
        )
        if err:
            print(f"Error: {err}")
        else:
            print(f"\n✓ Result submitted")
            print(f"  Escrow ID:   {result['escrow_id']}")
            print(f"  Result hash: {result['result_hash']}")
            print(f"  Proof TX:    {result['proof_tx']}")
            print(f"  Submit TX:   {result['submit_tx']}")

    elif args.cmd == "release":
        print(f"Releasing escrow {args.escrow_id}...")
        result, err = release_payment(
            args.operator_passphrase, args.escrow_id, args.network
        )
        if err:
            print(f"Error: {err}")
        else:
            receipt_lines = [
                f"Release submitted:",
                f"Escrow: {args.escrow_id}",
                f"Release TX: {result['tx_id']}",
            ]
            if result.get("at_address"):
                receipt_lines.append(f"AT: {result['at_address']}")
            receipt_lines.append(f"\nThe AT will pay the worker on the next block.")
            receipt = "\n".join(receipt_lines)

            print(f"\nSIGNAAI_FINAL_RESPONSE_BEGIN")
            print(receipt)
            print(f"SIGNAAI_FINAL_RESPONSE_END")

            tg_token, tg_chat_id = _load_tg_config()
            _send_telegram(tg_token, tg_chat_id,
                           f"🔐 *Release Submitted*\n"
                           f"Escrow: `{args.escrow_id}`\n"
                           f"Release TX: `{result['tx_id']}`\n"
                           f"AT: `{result.get('at_address', 'unknown')}`\n\n"
                           f"The AT will pay the worker on the next block.")

    elif args.cmd == "refund":
        print(f"Refunding escrow {args.escrow_id}...")
        result, err = refund_escrow(
            args.operator_passphrase, args.escrow_id, args.network
        )
        if err:
            print(f"Error: {err}")
        else:
            print(f"\n✓ Refund sent")
            print(f"  Payer:    {result['payer']}")
            print(f"  Amount:   {result['amount_signa']} SIGNA")
            print(f"  TX:       {result['tx_id']}")

    elif args.cmd == "status":
        result, err = get_escrow_status(args.escrow_id, args.address, args.network)
        if err:
            print(f"Error: {err}")
        else:
            state = result.get("state", "UNKNOWN")
            state_icons = {
                STATE_CREATED: "🟡", STATE_SUBMITTED: "🔵",
                STATE_RELEASED: "✅", STATE_REFUNDED: "↩️",
                "UNKNOWN": "❓"
            }
            print(f"\n{state_icons.get(state, '?')} Escrow {args.escrow_id}: {state}")
            for k, v in result.items():
                if k not in ("escrow_id", "state") and v:
                    print(f"  {k:<20} {v}")
    elif args.cmd == "receipt":
        result, err = get_escrow_status(args.escrow_id, args.address, args.network)
        if err:
            print(f"Error: {err}")
        elif result.get("state") == "UNKNOWN":
            print(f"Error: escrow {args.escrow_id} not found for {args.address}")
        elif not result.get("fund_tx"):
            print(f"Error: fund TX not found for escrow {args.escrow_id}")
        else:
            receipt = _format_escrow_receipt(result)
            _store_last_receipt(receipt)
            print(receipt)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
