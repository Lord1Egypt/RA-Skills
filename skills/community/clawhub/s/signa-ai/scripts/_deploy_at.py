#!/usr/bin/env python3
"""
SignaAI AT Escrow Deployer

Deploys the SignaAIEscrow AT smart contract to Signum.
The AT holds funds trustlessly — no operator, no trust required.

Usage:
  python3 _deploy_at.py gen-preimage
  python3 _deploy_at.py deploy <payer_passphrase> <worker_address> <deadline_block> <preimage_hex>
  python3 _deploy_at.py submit <payer_passphrase> <at_address> <preimage_hex>
  python3 _deploy_at.py info <at_address>

Workflow:
  1. Generate a preimage:    python3 _deploy_at.py gen-preimage
  2. Get current block:      python3 _deploy_at.py --network mainnet info <any_at>  (or check explorer)
  3. Deploy the escrow AT:   python3 _deploy_at.py deploy "<passphrase>" <worker> <deadline_block> <preimage_hex>
                             deadline_block is an absolute block height, e.g. current_block + 360 (~24h)
  4. Fund the AT:            send SIGNA to the AT address (escrow.py does this automatically)
  5. Worker completes task, payer verifies work
  6. Payer submits preimage: python3 _deploy_at.py submit "<payer_passphrase>" <at_address> <preimage_hex>
                             This sends 1 SIGNA activation + preimage to the AT
  7. AT verifies SHA256(preimage) == stored hash → auto-releases entire balance to worker
  8. If deadline passes without correct preimage → AT auto-refunds payer
"""
import sys
import os
import struct
import hashlib
import secrets
sys.path.insert(0, os.path.dirname(__file__))
from signum_api import get_api, signa, nqt, FEE_STANDARD, fee_message, ok
from wallet import get_my_address, send_signa

# ── AT Bytecode (compiled from contracts/signaai_escrow.smart via smartc-signum-compiler 2.3.0) ──
# Source: contracts/signaai_escrow.smart
# Compiled with: #pragma maxAuxVars 1, #include APIFunctions
# Memory layout (positions 0-7 initialized by build_data_field):
#   [0] r0 (SmartC scratch, always 0)
#   [1] _counterTimestamp (getNextTx internal tracker, always 0)
#   [2] workerAddress
#   [3] deadlineBlock
#   [4] h1  [5] h2  [6] h3  [7] h4  (SHA256(preimage) split into 4 longs)
AT_CODE_HEX = (
    "30030000000033170100000000320b033504010e000000330403010000003500010d0000001b0d0000000d"
    "350703010000001e0d0000000b1ae400000003000000003414010d00000000000000320903350401090000"
    "003505010a0000003506010b0000003507010c000000331001090000003311010a0000003312010b000000"
    "3313010c000000320402331001040000003311010500000033120106000000331301070000003527010f00"
    "00001b0f000000113316010200000032030428330403010000003500010d0000001e0d0000000b1a320000"
    "00350703010000001a320000003500031000000001000000002000000000000000181000000000000000201"
    "000000003000000153316010e000000320304282a1a17000000"
)
AT_CODE_HEX = AT_CODE_HEX.replace("\n", "").replace(" ", "")

AT_DPAGES   = 1
AT_CSPAGES  = 0
AT_USPAGES  = 0
AT_MIN_ACTIVATION_NQT = 100_000_000  # 1 SIGNA


# ── Helpers ───────────────────────────────────────────────────────────────────

def encode_long_le(value):
    """Encode a 64-bit signed integer as 8 bytes little-endian hex."""
    return struct.pack('<q', value).hex()


def sha256_hex(data_hex):
    """SHA256 of hex-encoded bytes, returns hex digest."""
    return hashlib.sha256(bytes.fromhex(data_hex)).hexdigest()


def sha256_str(text):
    """SHA256 of a UTF-8 string, returns hex digest."""
    return hashlib.sha256(text.encode()).hexdigest()


def build_data_field(preimage_hex, worker_account_id, deadline_block):
    """
    Build the AT data initialization field.

    Memory layout (must match SmartC compiled output — maxAuxVars 1):
      [0] r0 = 0               — SmartC scratch register
      [1] _counterTimestamp=0  — getNextTx() internal tracker (0 = start from genesis)
      [2] workerAddress        — worker account ID (numeric)
      [3] deadlineBlock        — absolute block height for refund cutoff
      [4-7] h1..h4             — SHA256(preimage) as 4 x 64-bit little-endian longs

    Returns hex string for the 'data' parameter in createATProgram.
    """
    prefix = encode_long_le(0) + encode_long_le(0)  # r0, _counterTimestamp
    worker_encoded   = encode_long_le(worker_account_id)
    deadline_encoded = encode_long_le(deadline_block)

    hash_bytes = hashlib.sha256(bytes.fromhex(preimage_hex)).digest()
    hash_parts = []
    for i in range(4):
        chunk = hash_bytes[i*8:(i+1)*8]
        val = struct.unpack('<q', chunk)[0]
        hash_parts.append(encode_long_le(val))

    return prefix + worker_encoded + deadline_encoded + "".join(hash_parts)


def encode_preimage_message(preimage_hex):
    """
    Encode the preimage as a 32-byte message for submission to the AT.
    Signum messages are sent as hex strings of up to 32 bytes.
    Returns the hex string (padded to 64 hex chars = 32 bytes).
    """
    padded = preimage_hex.ljust(64, '0')[:64]
    return padded


# ── Core Functions ────────────────────────────────────────────────────────────

def gen_preimage():
    """Generate a cryptographically secure random preimage."""
    preimage = secrets.token_hex(32)  # 32 bytes = 256 bits
    hashed   = sha256_hex(preimage)
    return preimage, hashed


def deploy_at(payer_passphrase, worker_address, deadline_block, preimage_hex,
              escrow_id=None, network=None):
    """
    Deploy the SignaAIEscrow AT contract on Signum.
    Polls until the AT address is confirmed on-chain (up to 6 min).

    deadline_block: absolute Signum block height after which the AT refunds the payer.
    Returns AT address and transaction ID.
    """
    import time
    api = get_api(network)

    # Get worker numeric account ID
    worker_info = api.get("getAccount", account=worker_address)
    if not ok(worker_info):
        return None, f"Could not find worker account: {worker_info.get('error')}"
    worker_id = int(worker_info.get("account", 0))

    # Build data field
    data_hex = build_data_field(preimage_hex, worker_id, deadline_block)

    # AT deployment fee minimum is 0.5 SIGNA on mainnet
    deploy_fee_nqt = 50_000_000  # 0.5 SIGNA

    # Use escrow_id in name for uniqueness (alphanumeric only — Signum requirement)
    at_name = f"SIG{escrow_id}" if escrow_id else "SignaAIEscrow"

    print(f"  Deploying AT contract ({at_name})...")
    print(f"  Worker:           {worker_address}")
    print(f"  Deadline block:   {deadline_block}")
    print(f"  Hash of preimage: {sha256_hex(preimage_hex)[:16]}...")

    result = api.post(
        "createATProgram",
        secretPhrase=payer_passphrase,
        name=at_name,
        description="SignaAI agent task escrow - hash preimage release",
        code=AT_CODE_HEX,
        data=data_hex,
        dpages=AT_DPAGES,
        cspages=AT_CSPAGES,
        uspages=AT_USPAGES,
        minActivationAmountNQT=AT_MIN_ACTIVATION_NQT,
        feeNQT=deploy_fee_nqt,
    )

    if not ok(result):
        return None, f"Deployment failed: {result.get('error')}"

    tx_id = result.get("transaction")
    print(f"  Deploy TX: {tx_id}")

    # Poll until AT appears on-chain (requires block confirmation, ~4 min)
    at_address = None
    payer_address, _ = get_my_address(payer_passphrase, network)
    if payer_address:
        deadline = time.time() + 360  # 6 min timeout
        attempt = 0
        while time.time() < deadline:
            time.sleep(15)
            attempt += 1
            print(f"  Waiting for AT confirmation... ({attempt * 15}s)", flush=True)
            ats = api.get("getAccountATs", account=payer_address)
            for at in (ats.get("ats") or []):
                if at.get("name") == at_name:
                    at_address = at.get("atRS")
                    break
            if at_address:
                print(f"  AT confirmed: {at_address}")
                break

    if not at_address:
        return None, "AT not found after 6 minutes — check explorer and retry"

    return {
        "tx_id": tx_id,
        "at_address": at_address,
        "worker": worker_address,
        "deadline_block": deadline_block,
        "preimage_hash": sha256_hex(preimage_hex),
    }, None


def submit_preimage(submitter_passphrase, at_address, preimage_hex, network=None):
    """
    Submit the preimage to the AT contract to trigger payment release.
    The AT verifies SHA256(preimage) == stored hash → releases funds to worker.

    Called by the payer (via escrow.py release) — not the worker.
    """
    api = get_api(network)

    worker_address, err = get_my_address(submitter_passphrase, network)
    if err:
        return None, err

    # Send preimage as a hex message to the AT
    # Pad/truncate to 32 bytes (64 hex chars)
    message = preimage_hex.ljust(64, '0')[:64]

    print(f"  Submitting preimage to AT {at_address}...")

    result = api.post(
        "sendMoney",
        secretPhrase=submitter_passphrase,
        recipient=at_address,
        amountNQT=AT_MIN_ACTIVATION_NQT,  # must send at least activation amount
        message=message,
        messageIsText="false",
        feeNQT=fee_message(),
    )

    if not ok(result):
        return None, f"Submission failed: {result.get('error')}"

    return {
        "tx_id": result.get("transaction"),
        "at_address": at_address,
        "preimage": preimage_hex,
        "note": "AT will verify on next block — if hash matches, funds released automatically",
    }, None


def get_at_info(at_address, network=None):
    """Get AT contract state and balance."""
    api = get_api(network)

    # getAT requires numeric account ID, not RS address — resolve it first
    account = api.get("getAccount", account=at_address)
    if not ok(account):
        return None, account.get("error", "Could not find AT account")

    at_numeric_id = account.get("account")
    bal_signa = signa(account.get("balanceNQT", 0))

    result = api.get("getAT", at=at_numeric_id)
    if not ok(result):
        return None, result.get("error")

    return {
        "address": result.get("atRS", at_address),
        "name": result.get("name"),
        "description": result.get("description"),
        "balance": bal_signa,
        "finished": result.get("finished", False),
        "frozen": result.get("frozen", False),
        "creator": result.get("creatorRS"),
    }, None


# ── CLI ───────────────────────────────────────────────────────────────────────
def main():
    import argparse
    parser = argparse.ArgumentParser(description="SignaAI AT Escrow Deployer")
    parser.add_argument("--network", default=os.environ.get("SIGNUM_NETWORK", "testnet"),
                        choices=["mainnet", "testnet"])
    sub = parser.add_subparsers(dest="cmd")

    # gen-preimage
    sub.add_parser("gen-preimage", help="Generate a secure random preimage + its SHA256 hash")

    # deploy
    p = sub.add_parser("deploy", help="Deploy the escrow AT contract")
    p.add_argument("payer_passphrase")
    p.add_argument("worker_address", help="Worker agent's Signum address")
    p.add_argument("deadline_block", type=int, help="Absolute block height for refund cutoff")
    p.add_argument("preimage_hex", help="32-byte hex preimage (from gen-preimage)")

    # submit
    p = sub.add_parser("submit", help="Submit preimage to AT to release payment")
    p.add_argument("submitter_passphrase")
    p.add_argument("at_address", help="AT contract address")
    p.add_argument("preimage_hex", help="The preimage to reveal")

    # info
    p = sub.add_parser("info", help="Get AT contract state and balance")
    p.add_argument("at_address")

    args = parser.parse_args()
    os.environ["SIGNUM_NETWORK"] = args.network

    if args.cmd == "gen-preimage":
        preimage, hashed = gen_preimage()
        print(f"\nPreimage (keep secret until work is verified):")
        print(f"  {preimage}")
        print(f"\nSHA256(preimage) — stored in AT:")
        print(f"  {hashed}")
        print(f"\nStore the preimage securely. Reveal it to the worker only after verifying their work.")

    elif args.cmd == "deploy":
        print(f"Deploying SignaAI Escrow AT on {args.network}...")
        result, err = deploy_at(
            args.payer_passphrase, args.worker_address,
            args.deadline_block, args.preimage_hex,
            network=args.network,
        )
        if err:
            print(f"Error: {err}")
        else:
            print(f"\n✓ AT contract deployed")
            print(f"  AT address:   {result['at_address']}")
            print(f"  Deploy TX:    {result['tx_id']}")
            print(f"  Worker:       {result['worker']}")
            print(f"  Deadline:     block {result['deadline_block']}")
            print(f"  Preimage hash:{result['preimage_hash'][:32]}...")
            print(f"\n  Next: fund the AT by sending SIGNA to {result['at_address']}")
            print(f"  python3 wallet.py --network {args.network} send \"<passphrase>\" {result['at_address']} <amount>")

    elif args.cmd == "submit":
        print(f"Submitting preimage to AT {args.at_address}...")
        result, err = submit_preimage(
            args.submitter_passphrase, args.at_address,
            args.preimage_hex, args.network
        )
        if err:
            print(f"Error: {err}")
        else:
            print(f"\n✓ Preimage submitted")
            print(f"  TX:   {result['tx_id']}")
            print(f"  {result['note']}")

    elif args.cmd == "info":
        result, err = get_at_info(args.at_address, args.network)
        if err:
            print(f"Error: {err}")
        else:
            status = "FINISHED" if result['finished'] else ("FROZEN" if result['frozen'] else "ACTIVE")
            print(f"\nAT Contract: {result['address']}")
            print(f"  Name:     {result['name']}")
            print(f"  Creator:  {result['creator']}")
            print(f"  Balance:  {result['balance']:,.4f} SIGNA")
            print(f"  Status:   {status}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
