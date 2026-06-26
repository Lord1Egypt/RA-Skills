#!/usr/bin/env python3
"""
SignaAI Multi-Agent Arbitration

When a payer and worker disagree on task completion, either party can open
an arbitration request. A registered arbitrator agent reviews the evidence
and issues a binding decision — RELEASE or REFUND.

All messages are on-chain: permanent, public, auditable.

Message format:
  ARBIT_OPEN:<escrow_id>:<claimant>:<reason_hash>
  ARBIT_VOTE:<escrow_id>:<decision>:<notes_hash>    (decision = RELEASE or REFUND)
  ARBIT_CLOSE:<escrow_id>:<decision>:<arbitrator>

Usage:
  python3 arbitration.py open <passphrase> <escrow_id> <arbitrator_address> <reason>
  python3 arbitration.py vote <arb_passphrase> <escrow_id> <RELEASE|REFUND> [notes]
  python3 arbitration.py status <escrow_id> <address>
  python3 arbitration.py arbitrators
"""
import sys
import os
import json
import hashlib
sys.path.insert(0, os.path.dirname(__file__))
from signum_api import get_api, signa, ts, FEE_MESSAGE, ok
from wallet import get_my_address

# ── Constants ─────────────────────────────────────────────────────────────────
ARBIT_OPEN_PREFIX  = "ARBIT_OPEN:"
ARBIT_VOTE_PREFIX  = "ARBIT_VOTE:"
ARBIT_CLOSE_PREFIX = "ARBIT_CLOSE:"

# Well-known arbitrator registry alias
ARBITRATOR_REGISTRY_ALIAS = "signaai-arbitrators"

DECISION_RELEASE = "RELEASE"
DECISION_REFUND  = "REFUND"


# ── Core Functions ────────────────────────────────────────────────────────────

def open_arbitration(passphrase, escrow_id, arbitrator_address, reason, network=None):
    """
    Open an arbitration request. Either payer or worker can call this.

    Sends an on-chain message to the arbitrator with the escrow ID and
    a hash of the reason/evidence.

    Returns the transaction ID of the arbitration request.
    """
    api = get_api(network)

    claimant_address, err = get_my_address(passphrase, network)
    if err:
        return None, err

    # Hash the reason text so it's compact on-chain; claimant keeps full text
    reason_hash = hashlib.sha256(reason.encode()).hexdigest()[:16]

    message = f"{ARBIT_OPEN_PREFIX}{escrow_id}:{claimant_address}:{reason_hash}"

    print(f"  Opening arbitration for escrow {escrow_id[:12]}...")
    print(f"  Arbitrator: {arbitrator_address}")
    print(f"  Reason hash: {reason_hash} (keep reason text for arbitrator)")

    result = api.post(
        "sendMessage",
        secretPhrase=passphrase,
        recipient=arbitrator_address,
        message=message,
        messageIsText="true",
        feeNQT=FEE_MESSAGE,
    )

    if not ok(result):
        return None, result.get("error", "Failed to open arbitration")

    return {
        "tx_id": result.get("transaction"),
        "escrow_id": escrow_id,
        "claimant": claimant_address,
        "arbitrator": arbitrator_address,
        "reason_hash": reason_hash,
        "note": "Share the full reason text with the arbitrator off-chain or via encrypted message",
    }, None


def vote_arbitration(passphrase, escrow_id, decision, notes="", network=None):
    """
    Arbitrator casts a binding vote on an escrow dispute.

    decision: "RELEASE" (pay worker) or "REFUND" (return to payer)
    notes:    brief rationale (hashed on-chain; keep full notes off-chain)

    Sends an on-chain ARBIT_VOTE message from the arbitrator's address.
    The operator (or AT in Phase 2) reads this to execute the decision.
    """
    if decision not in (DECISION_RELEASE, DECISION_REFUND):
        return None, f"Decision must be RELEASE or REFUND, got: {decision}"

    api = get_api(network)

    arb_address, err = get_my_address(passphrase, network)
    if err:
        return None, err

    notes_hash = hashlib.sha256(notes.encode()).hexdigest()[:16] if notes else "none"
    message = f"{ARBIT_VOTE_PREFIX}{escrow_id}:{decision}:{notes_hash}"

    # Arbitrator votes by sending to themselves — public, permanent record
    result = api.post(
        "sendMessage",
        secretPhrase=passphrase,
        recipient=arb_address,
        message=message,
        messageIsText="true",
        feeNQT=FEE_MESSAGE,
    )

    if not ok(result):
        return None, result.get("error", "Failed to record vote")

    return {
        "tx_id": result.get("transaction"),
        "escrow_id": escrow_id,
        "arbitrator": arb_address,
        "decision": decision,
        "notes_hash": notes_hash,
        "note": f"Decision: {decision}. Operator should now call escrow {'release' if decision == DECISION_RELEASE else 'refund'}.",
    }, None


def get_arbitration_status(escrow_id, address, network=None):
    """
    Scan an address's transaction history for arbitration messages
    related to a given escrow ID.

    Returns any open requests and votes found.
    """
    api = get_api(network)

    result = api.get("getAccountTransactions",
                     account=address,
                     firstIndex=0,
                     lastIndex=199,
                     type=1)

    txs = result.get("transactions", [])

    open_requests = []
    votes = []

    for tx in txs:
        msg = tx.get("attachment", {}).get("message", "")
        timestamp = ts(tx.get("timestamp"))
        sender = tx.get("senderRS", "")
        tx_id = tx.get("transaction", "")

        if msg.startswith(ARBIT_OPEN_PREFIX):
            parts = msg[len(ARBIT_OPEN_PREFIX):].split(":")
            if len(parts) >= 3 and parts[0] == escrow_id:
                open_requests.append({
                    "escrow_id": parts[0],
                    "claimant": parts[1],
                    "reason_hash": parts[2],
                    "timestamp": timestamp,
                    "tx_id": tx_id,
                    "from": sender,
                })

        elif msg.startswith(ARBIT_VOTE_PREFIX):
            parts = msg[len(ARBIT_VOTE_PREFIX):].split(":")
            if len(parts) >= 3 and parts[0] == escrow_id:
                votes.append({
                    "escrow_id": parts[0],
                    "decision": parts[1],
                    "notes_hash": parts[2],
                    "arbitrator": sender,
                    "timestamp": timestamp,
                    "tx_id": tx_id,
                })

    # Final decision = most recent vote (chronologically last)
    final_decision = votes[-1]["decision"] if votes else None

    return {
        "escrow_id": escrow_id,
        "open_requests": open_requests,
        "votes": votes,
        "final_decision": final_decision,
        "resolved": final_decision is not None,
    }, None


def register_arbitrator(passphrase, name, description="", network=None):
    """
    Register as a public arbitrator by setting a signaai-arb alias.
    Arbitrators build reputation through transparent, on-chain decisions.
    """
    api = get_api(network)

    address, err = get_my_address(passphrase, network)
    if err:
        return None, err

    from signum_api import FEE_ALIAS
    alias = f"signaai-arb-{name.lower().replace(' ', '').replace('-', '')}"
    metadata = {
        "type": "arbitrator",
        "name": name,
        "address": address,
        "description": description,
    }
    alias_uri = f"acct:{address};signaai-arb:{json.dumps(metadata, separators=(',', ':'))}"

    result = api.post("setAlias",
                      secretPhrase=passphrase,
                      aliasName=alias,
                      aliasURI=alias_uri,
                      feeNQT=FEE_ALIAS)

    if not ok(result):
        return None, result.get("error", "Registration failed")

    return {
        "alias": alias,
        "address": address,
        "tx_id": result.get("transaction"),
    }, None


def list_arbitrators(network=None):
    """List all registered arbitrators."""
    api = get_api(network)
    result = api.get("getAliases", aliasName="signaai-arb-", timestamp=0)
    arbitrators = []
    for alias in (result.get("aliases") or []):
        uri = alias.get("aliasURI", "")
        if "signaai-arb:" not in uri:
            continue
        metadata = {}
        try:
            metadata = json.loads(uri.split("signaai-arb:")[1])
        except:
            pass
        arbitrators.append({
            "alias": alias.get("aliasName"),
            "address": metadata.get("address", ""),
            "name": metadata.get("name", alias.get("aliasName")),
            "description": metadata.get("description", ""),
        })
    return arbitrators


# ── CLI ───────────────────────────────────────────────────────────────────────
def main():
    import argparse
    parser = argparse.ArgumentParser(description="SignaAI Multi-Agent Arbitration")
    parser.add_argument("--network", default=os.environ.get("SIGNUM_NETWORK", "testnet"),
                        choices=["mainnet", "testnet"])
    sub = parser.add_subparsers(dest="cmd")

    # open
    p = sub.add_parser("open", help="Open an arbitration request")
    p.add_argument("passphrase", help="Claimant passphrase (payer or worker)")
    p.add_argument("escrow_id", help="Escrow ID to dispute")
    p.add_argument("arbitrator_address", help="Arbitrator's Signum address")
    p.add_argument("reason", help="Reason for dispute")

    # vote
    p = sub.add_parser("vote", help="Arbitrator issues a decision")
    p.add_argument("passphrase", help="Arbitrator passphrase")
    p.add_argument("escrow_id", help="Escrow ID being arbitrated")
    p.add_argument("decision", choices=["RELEASE", "REFUND"],
                   help="RELEASE = pay worker, REFUND = return to payer")
    p.add_argument("--notes", default="", help="Rationale (hashed on-chain)")

    # status
    p = sub.add_parser("status", help="Check arbitration status for an escrow")
    p.add_argument("escrow_id")
    p.add_argument("address", help="Arbitrator's address to scan")

    # register-arbitrator
    p = sub.add_parser("register-arbitrator", help="Register as a public arbitrator")
    p.add_argument("passphrase")
    p.add_argument("name")
    p.add_argument("--description", default="")

    # arbitrators
    sub.add_parser("arbitrators", help="List all registered arbitrators")

    args = parser.parse_args()
    os.environ["SIGNUM_NETWORK"] = args.network

    if args.cmd == "open":
        result, err = open_arbitration(
            args.passphrase, args.escrow_id,
            args.arbitrator_address, args.reason, args.network
        )
        if err:
            print(f"Error: {err}")
        else:
            print(f"\n✓ Arbitration request sent")
            print(f"  TX:           {result['tx_id']}")
            print(f"  Escrow:       {result['escrow_id']}")
            print(f"  Arbitrator:   {result['arbitrator']}")
            print(f"  Reason hash:  {result['reason_hash']}")
            print(f"\n  {result['note']}")

    elif args.cmd == "vote":
        result, err = vote_arbitration(
            args.passphrase, args.escrow_id,
            args.decision, args.notes, args.network
        )
        if err:
            print(f"Error: {err}")
        else:
            print(f"\n✓ Arbitration decision recorded on-chain")
            print(f"  TX:         {result['tx_id']}")
            print(f"  Escrow:     {result['escrow_id']}")
            print(f"  Decision:   {result['decision']}")
            print(f"\n  {result['note']}")

    elif args.cmd == "status":
        result, err = get_arbitration_status(args.escrow_id, args.address, args.network)
        if err:
            print(f"Error: {err}")
        else:
            print(f"\nArbitration Status — Escrow {args.escrow_id[:16]}...")
            print(f"  Resolved:  {'Yes' if result['resolved'] else 'No'}")
            if result['final_decision']:
                print(f"  Decision:  {result['final_decision']}")
            print(f"\n  Open requests: {len(result['open_requests'])}")
            for r in result['open_requests']:
                print(f"    [{r['timestamp']}] from {r['claimant'][:20]}... reason: {r['reason_hash']}")
            print(f"\n  Votes cast: {len(result['votes'])}")
            for v in result['votes']:
                print(f"    [{v['timestamp']}] {v['arbitrator'][:20]}... → {v['decision']}")

    elif args.cmd == "register-arbitrator":
        result, err = register_arbitrator(
            args.passphrase, args.name, args.description, args.network
        )
        if err:
            print(f"Error: {err}")
        else:
            print(f"\n✓ Registered as arbitrator")
            print(f"  Alias:   {result['alias']}")
            print(f"  Address: {result['address']}")
            print(f"  TX:      {result['tx_id']}")

    elif args.cmd == "arbitrators":
        arbs = list_arbitrators(args.network)
        if not arbs:
            print("No arbitrators registered yet.")
        else:
            print(f"Registered Arbitrators ({len(arbs)}):\n")
            for a in arbs:
                print(f"  {a['name']}")
                print(f"  Address: {a['address']}")
                if a['description']:
                    print(f"  {a['description']}")
                print()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
