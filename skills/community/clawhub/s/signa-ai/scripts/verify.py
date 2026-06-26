#!/usr/bin/env python3
"""
Signum Verifiable Outputs — hash content, publish proof on-chain, verify later.

How it works:
  1. BEFORE delivering: hash your output + sources → get a fingerprint
  2. PUBLISH: send the hash to Signum blockchain → gets a timestamp + TX ID
  3. DELIVER: give the recipient your output AND the TX ID
  4. VERIFY: anyone can check the output hash matches the on-chain record

This is the lightweight alternative to zkML:
  - No special hardware, no ZK circuits
  - Costs ~$0.000007 per proof (at current SIGNA price)
  - Immutable, timestamped, publicly auditable
  - Proves what was said, when, and that it hasn't been altered

Usage:
  python3 verify.py hash <content> [--sources "url1,url2"]
  python3 verify.py publish <passphrase> <content_hash> [--label "task description"]
  python3 verify.py verify <content> <tx_id> [--sources "url1,url2"]
  python3 verify.py proofs <address> [--limit 20]
"""
import sys
import os
import json
import hashlib
sys.path.insert(0, os.path.dirname(__file__))
from signum_api import get_api, ts, fee_message, ok, EXPLORER_URL
from wallet import get_my_address
from protocol import build_sigproof, parse_sigproof
from protocol import PROOF_PREFIX


def hash_content(content, sources=None):
    """
    Generate a SHA-256 fingerprint of content + sources.

    content: the text/data being proven (string or bytes)
    sources: list of source URLs or identifiers used to produce content

    Returns:
      content_hash: SHA-256 of content only
      sources_hash: SHA-256 of sorted sources (reproducible)
      combined_hash: SHA-256 of content + sources together

    Canonical artifact: raw UTF-8 bytes of the content string, no normalization.
    Content must be identical byte-for-byte at stamp time and verify time.
    """
    if isinstance(content, str):
        content = content.encode('utf-8')

    content_hash = hashlib.sha256(content).hexdigest()

    sources = sorted(sources or [])
    sources_str = "|".join(sources).encode('utf-8')
    sources_hash = hashlib.sha256(sources_str).hexdigest()

    combined = hashlib.sha256(content + sources_str).hexdigest()

    return {
        "content_hash": content_hash,
        "sources_hash": sources_hash,
        "combined_hash": combined,
        "sources": sources,
    }


def publish_proof(passphrase, content_hash, sources_hash="", label="", network=None):
    """
    Publish a content hash to Signum blockchain.
    Returns tx_id — this is your proof receipt.

    The on-chain record contains:
      - The hash (immutable)
      - A timestamp (from block time)
      - The publishing agent's address
      - An optional label
    """
    api = get_api(network)
    address, err = get_my_address(passphrase, network)
    if err:
        return None, err

    # Build proof message
    message = build_sigproof(content_hash, sources_hash, label)

    result = api.post("sendMessage",
                      secretPhrase=passphrase,
                      recipient=address,  # self-message = public proof record
                      message=message,
                      messageIsText="true",
                      feeNQT=fee_message(message))

    if not ok(result):
        return None, result.get("error", "Failed to publish proof")

    return {
        "tx_id": result.get("transaction"),
        "address": address,
        "content_hash": content_hash,
        "sources_hash": sources_hash,
        "label": label,
    }, None


def verify_proof(content, tx_id, sources=None, network=None):
    """
    Verify that content matches an on-chain proof.

    Steps:
      1. Hash the provided content + sources
      2. Look up the on-chain transaction
      3. Compare the hashes

    Returns:
      verified: True/False
      details: dict with match info and on-chain timestamp
    """
    api = get_api(network)

    # Hash the provided content
    hashes = hash_content(content, sources)

    # Fetch the on-chain transaction
    tx = api.get("getTransaction", transaction=tx_id)
    if not ok(tx):
        return False, {"error": f"Transaction not found: {tx_id}"}

    # Extract the proof from the message
    msg = tx.get("attachment", {}).get("message", "")
    if not msg.startswith(PROOF_PREFIX):
        return False, {"error": "Transaction does not contain a SIGPROOF record"}

    try:
        proof = parse_sigproof(msg)
    except Exception:
        return False, {"error": "Malformed proof record"}

    onchain_content_hash = proof.content_hash
    onchain_sources_hash = proof.sources_hash

    content_match = hashes["content_hash"] == onchain_content_hash
    sources_match = (not onchain_sources_hash or
                     hashes["sources_hash"] == onchain_sources_hash)

    verified = content_match and sources_match

    return verified, {
        "verified": verified,
        "content_match": content_match,
        "sources_match": sources_match,
        "timestamp": ts(tx.get("timestamp")),
        "publisher": tx.get("senderRS", tx.get("sender")),
        "block": tx.get("block"),
        "onchain_content_hash": onchain_content_hash,
        "computed_content_hash": hashes["content_hash"],
        "label": proof.label,
    }


def get_proofs(address, limit=20, network=None):
    """Get all proof records published by an address."""
    api = get_api(network)

    result = api.get("getAccountTransactions",
                     account=address,
                     numberOfTransactions=limit,
                     type=1)  # messaging transactions

    proofs = []
    for tx in (result.get("transactions") or []):
        msg = tx.get("attachment", {}).get("message", "")
        if msg.startswith(PROOF_PREFIX):
            try:
                proof = parse_sigproof(msg)
            except Exception:
                continue
            proofs.append({
                "tx_id": tx.get("transaction"),
                "timestamp": ts(tx.get("timestamp")),
                "content_hash": proof.content_hash,
                "label": proof.label,
                "confirmations": tx.get("confirmations", 0),
            })

    return proofs


# ── CLI ───────────────────────────────────────────────────────────────────────
def main():
    import argparse
    parser = argparse.ArgumentParser(description="Signum Verifiable Outputs")
    parser.add_argument("--network", default=os.environ.get("SIGNUM_NETWORK", "testnet"),
                        choices=["mainnet", "testnet"])
    sub = parser.add_subparsers(dest="cmd")

    p = sub.add_parser("hash", help="Hash content (no blockchain call)")
    p.add_argument("content")
    p.add_argument("--sources", default="", help="Comma-separated source URLs")

    p = sub.add_parser("publish", help="Publish a proof on-chain")
    p.add_argument("passphrase")
    p.add_argument("content_hash")
    p.add_argument("--sources-hash", default="")
    p.add_argument("--label", default="")

    p = sub.add_parser("verify", help="Verify content against an on-chain proof")
    p.add_argument("content")
    p.add_argument("tx_id")
    p.add_argument("--sources", default="")

    p = sub.add_parser("proofs", help="List proofs published by an address")
    p.add_argument("address")
    p.add_argument("--limit", type=int, default=20)

    # Convenience: hash + publish in one step
    p = sub.add_parser("stamp", help="Hash content and publish proof in one step")
    p.add_argument("passphrase")
    p.add_argument("content")
    p.add_argument("--sources", default="")
    p.add_argument("--label", default="")

    args = parser.parse_args()
    os.environ["SIGNUM_NETWORK"] = args.network

    if args.cmd == "hash":
        sources = [s.strip() for s in args.sources.split(",") if s.strip()]
        h = hash_content(args.content, sources)
        print(f"Content hash:  {h['content_hash']}")
        print(f"Sources hash:  {h['sources_hash']}")
        print(f"Combined hash: {h['combined_hash']}")
        if sources:
            print(f"Sources ({len(sources)}): {', '.join(sources)}")

    elif args.cmd == "publish":
        result, err = publish_proof(args.passphrase, args.content_hash,
                                    args.sources_hash, args.label, args.network)
        if err:
            print(f"Error: {err}")
        else:
            print(f"✓ Proof published on-chain")
            print(f"  TX ID:   {result['tx_id']}")
            print(f"  Hash:    {result['content_hash']}")
            print(f"  Address: {result['address']}")
            print(f"  View:    {EXPLORER_URL}/tx/{result['tx_id']}")

    elif args.cmd == "stamp":
        sources = [s.strip() for s in args.sources.split(",") if s.strip()]
        h = hash_content(args.content, sources)
        print(f"Content hash: {h['content_hash']}")
        result, err = publish_proof(args.passphrase, h['content_hash'],
                                    h['sources_hash'], args.label, args.network)
        if err:
            print(f"Error publishing: {err}")
        else:
            print(f"✓ Proof stamped on-chain")
            print(f"  TX ID: {result['tx_id']}")
            print(f"  Give the recipient this TX ID to verify your output.")
            print(f"  View:  {EXPLORER_URL}/tx/{result['tx_id']}")

    elif args.cmd == "verify":
        sources = [s.strip() for s in args.sources.split(",") if s.strip()]
        verified, details = verify_proof(args.content, args.tx_id, sources, args.network)
        if "error" in details:
            print(f"Error: {details['error']}")
        elif verified:
            print(f"✓ VERIFIED — content matches on-chain proof")
            print(f"  Timestamp:  {details['timestamp']}")
            print(f"  Publisher:  {details['publisher']}")
            print(f"  Block:      {details['block']}")
        else:
            print(f"✗ VERIFICATION FAILED")
            print(f"  Content match: {details['content_match']}")
            print(f"  Sources match: {details['sources_match']}")
            print(f"  On-chain hash: {details['onchain_content_hash']}")
            print(f"  Computed hash: {details['computed_content_hash']}")

    elif args.cmd == "proofs":
        proofs = get_proofs(args.address, args.limit, args.network)
        if not proofs:
            print("No proofs found.")
        else:
            print(f"{'TIMESTAMP':<18} {'TX ID':<20} {'HASH':<16} {'LABEL'}")
            print("-" * 75)
            for p in proofs:
                print(f"{p['timestamp']:<18} {p['tx_id']:<20} {p['content_hash'][:14]}...  {p['label']}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
