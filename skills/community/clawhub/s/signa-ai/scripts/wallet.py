#!/usr/bin/env python3
"""
Signum Wallet — account info, balance, send SIGNA, transaction history.

Usage:
  python3 wallet.py balance <address>
  python3 wallet.py send <passphrase> <recipient> <amount> [message]
  python3 wallet.py history <address> [--limit 10]
  python3 wallet.py status
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from signum_api import get_api, signa, nqt, ts, fmt_address, FEE_STANDARD, fee_message, FEE_AT, ok, EXPLORER_URL


def get_account(address, network=None):
    """Get full account info."""
    api = get_api(network)
    return api.get("getAccount", account=address)


def get_balance(address, network=None):
    """Get confirmed SIGNA balance."""
    api = get_api(network)
    result = api.get("getAccount", account=address)
    if not ok(result):
        return None, result.get("error")
    bal = signa(result.get("balanceNQT", 0))
    unconf = signa(result.get("unconfirmedBalanceNQT", 0))
    return {"confirmed": bal, "unconfirmed": unconf, "address": result.get("accountRS")}, None


def send_signa(passphrase, recipient, amount_signa, message=None,
               recipient_public_key=None, network=None):
    """
    Send SIGNA to a recipient.
    Returns transaction ID on success.
    """
    api = get_api(network)
    try:
        amount_nqt = nqt(amount_signa)
    except ValueError as exc:
        return None, str(exc)
    if amount_nqt <= 0:
        return None, "Amount must be greater than zero"

    # Check if recipient is an AT (smart contract) — requires higher minimum fee
    acct = api.get("getAccount", account=recipient)
    is_at = acct.get("isAT", False)
    fee = fee_message(message) if message else (FEE_AT if is_at else FEE_STANDARD)

    params = {
        "secretPhrase": passphrase,
        "recipient": recipient,
        "amountNQT": amount_nqt,
        "feeNQT": fee,
    }

    if message:
        params["message"] = message
        params["messageIsText"] = "true"

    if recipient_public_key:
        params["recipientPublicKey"] = recipient_public_key

    result = api.post("sendMoney", **params)
    if not ok(result):
        return None, result.get("error", "Transaction failed")

    tx_id = result.get("transaction")
    return tx_id, None


def get_transactions(address, limit=10, network=None):
    """Get recent transactions for an address."""
    api = get_api(network)
    result = api.get("getAccountTransactions",
                     account=address,
                     firstIndex=0,
                     lastIndex=limit - 1,
                     type=0)  # type 0 = payment transactions
    if not ok(result):
        return [], result.get("error")

    txs = []
    for tx in result.get("transactions", []):
        txs.append({
            "id": tx.get("transaction"),
            "timestamp": ts(tx.get("timestamp")),
            "sender": tx.get("senderRS", tx.get("sender")),
            "recipient": tx.get("recipientRS", tx.get("recipient")),
            "amount": signa(tx.get("amountNQT", 0)),
            "fee": signa(tx.get("feeNQT", 0)),
            "confirmations": tx.get("confirmations", 0),
            "message": tx.get("attachment", {}).get("message", ""),
        })
    return txs, None


def get_my_address(passphrase, network=None):
    """Derive the address for a given passphrase (without sending anything)."""
    if not passphrase or not str(passphrase).strip():
        return None, "Passphrase cannot be empty"
    try:
        from signum_crypto import generate_sign_keys
    except ImportError as exc:
        return None, f"Local key derivation unavailable: {exc}"

    keys = generate_sign_keys(passphrase)
    api = get_api(network)
    result = api.get("getAccountId", publicKey=keys["publicKey"])
    if not ok(result):
        return None, result.get("error")
    return result.get("accountRS"), None


# ── CLI ───────────────────────────────────────────────────────────────────────
def main():
    import argparse
    parser = argparse.ArgumentParser(description="Signum Wallet")
    parser.add_argument("--network", default=os.environ.get("SIGNUM_NETWORK", "testnet"),
                        choices=["mainnet", "testnet"])
    sub = parser.add_subparsers(dest="cmd")

    # balance
    p = sub.add_parser("balance", help="Check account balance")
    p.add_argument("address")

    # send
    p = sub.add_parser("send", help="Send SIGNA")
    p.add_argument("passphrase")
    p.add_argument("recipient")
    p.add_argument("amount", type=float)
    p.add_argument("message", nargs="?", default=None)

    # history
    p = sub.add_parser("history", help="Transaction history")
    p.add_argument("address")
    p.add_argument("--limit", type=int, default=10)

    # myaddress
    p = sub.add_parser("myaddress", help="Get address for a passphrase")
    p.add_argument("passphrase")

    # status
    sub.add_parser("status", help="Node status")

    args = parser.parse_args()

    os.environ["SIGNUM_NETWORK"] = args.network
    api = get_api(args.network)

    if args.cmd == "balance":
        bal, err = get_balance(args.address, args.network)
        if err:
            print(f"Error: {err}")
        else:
            print(f"Address:     {bal['address']}")
            print(f"Balance:     {bal['confirmed']:,.4f} SIGNA")
            if bal['unconfirmed'] != bal['confirmed']:
                print(f"Unconfirmed: {bal['unconfirmed']:,.4f} SIGNA")

    elif args.cmd == "send":
        print(f"Sending {args.amount} SIGNA to {args.recipient}...")
        tx_id, err = send_signa(args.passphrase, args.recipient, args.amount,
                                args.message, args.network)
        if err:
            print(f"Error: {err}")
        else:
            print(f"✓ Transaction broadcast: {tx_id}")
            print(f"  View: {EXPLORER_URL}/tx/{tx_id}")

    elif args.cmd == "history":
        txs, err = get_transactions(args.address, args.limit, args.network)
        if err:
            print(f"Error: {err}")
        else:
            print(f"{'DATE':<18} {'FROM/TO':<20} {'AMOUNT':>12} {'MSG'}")
            print("-" * 65)
            for tx in txs:
                direction = "← " + tx['sender'][:16] if tx['recipient'] and args.address.replace("SIGNA-","") in tx['recipient'] else "→ " + (tx['recipient'] or '')[:16]
                print(f"{tx['timestamp']:<18} {direction:<20} {tx['amount']:>11.4f}Σ  {tx['message'][:20]}")

    elif args.cmd == "myaddress":
        addr, err = get_my_address(args.passphrase, args.network)
        if err:
            print(f"Error: {err}")
        else:
            print(f"Address: {addr}")

    elif args.cmd == "status":
        status = api.get("getBlockchainStatus")
        print(f"Network: {args.network}")
        print(f"Node:    {api.active_node}")
        print(f"Blocks:  {status.get('numberOfBlocks', '?'):,}")
        print(f"Version: {status.get('version', '?')}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
