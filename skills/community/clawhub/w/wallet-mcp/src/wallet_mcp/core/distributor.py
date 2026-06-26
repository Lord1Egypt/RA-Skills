"""
Multi-wallet distributor: send native token from one source to a group.
Supports SOL and ETH/EVM, randomized amounts, random delays, and retry.
"""
from typing import Optional
from .utils import setup_logging, random_delay, random_amount, retry

_log = setup_logging()


def sweep_native_multi(
    wallets: list[dict],
    to_address: str,
    chain: str,
    rpc_url: Optional[str] = None,
    leave_lamports: int = 5000,
    delay_min: int = 1,
    delay_max: int = 10,
    retry_attempts: int = 3,
) -> dict:
    """
    Sweep all native tokens from every wallet in `wallets` to `to_address`.
    Each wallet dict must have an 'address' and 'private_key' field.

    Args:
        wallets:        list of wallet dicts with private_key
        to_address:     destination address
        chain:          'solana' or 'evm'
        rpc_url:        custom RPC (falls back to env/default)
        leave_lamports: lamports to keep in each Solana wallet for fees (default 5000)
        delay_min/max:  seconds between sweeps
        retry_attempts: retry count per failed sweep

    Returns:
        {status, chain, to_address, total, swept, skipped, failed, total_swept, results}
    """
    chain = chain.lower()
    if chain == "solana":
        from .solana import sweep_sol_wallet, DEFAULT_RPC
        def _sweep(w):
            return sweep_sol_wallet(w["private_key"], to_address, rpc_url or DEFAULT_RPC, leave_lamports)
        amount_key = "sent_sol"
    elif chain == "evm":
        from .evm import sweep_eth_wallet, DEFAULT_RPC
        def _sweep(w):
            return sweep_eth_wallet(w["private_key"], to_address, rpc_url or DEFAULT_RPC)
        amount_key = "sent_eth"
    else:
        raise ValueError(f"Unsupported chain: {chain}")

    results = []
    swept   = 0
    skipped = 0
    failed  = 0
    total_swept = 0.0

    for i, wallet in enumerate(wallets):
        def _do(w=wallet):
            return _sweep(w)

        try:
            r = retry(_do, attempts=retry_attempts, delay=5)
            results.append(r)
            if r["status"] == "swept":
                swept += 1
                total_swept += r.get(amount_key, 0.0)
                _log.info(f"[{i+1}/{len(wallets)}] Swept {r.get(amount_key)} {chain} from {r['address']} | {r.get('tx_hash')}")
            else:
                skipped += 1
                _log.debug(f"[{i+1}/{len(wallets)}] Skipped {r['address']}: {r.get('reason')}")
        except Exception as e:
            results.append({"address": wallet.get("address", "?"), "status": "failed", "error": str(e)})
            failed += 1
            _log.error(f"[{i+1}/{len(wallets)}] Failed {wallet.get('address')}: {e}")

        if i < len(wallets) - 1:
            random_delay(delay_min, delay_max)

    return {
        "status":        "success" if failed == 0 else "partial",
        "chain":         chain,
        "to_address":    to_address,
        "total":         len(wallets),
        "swept":         swept,
        "skipped":       skipped,
        "failed":        failed,
        "total_swept":   round(total_swept, 9),
        "results":       results,
    }


def send_native_multi(
    from_private_key: str,
    recipients: list[dict],
    amount: float,
    chain: str,
    rpc_url: Optional[str] = None,
    randomize: bool = False,
    delay_min: int = 1,
    delay_max: int = 30,
    retry_attempts: int = 3,
) -> dict:
    """
    Send native token from one source wallet to all recipients.

    Args:
        from_private_key: private key of sender (base58 for Solana, hex for EVM)
        recipients:       list of wallet dicts (must each have 'address')
        amount:           base amount per wallet (SOL or ETH)
        chain:            'solana' or 'evm'
        rpc_url:          custom RPC (falls back to env/default)
        randomize:        if True, randomize each send ±10%
        delay_min/max:    seconds to sleep between sends
        retry_attempts:   retry count per failed send

    Returns:
        {status, chain, total, sent, failed, results}
    """
    chain = chain.lower()
    if chain == "solana":
        from .solana import send_sol, DEFAULT_RPC
        send_fn, default_rpc = send_sol, DEFAULT_RPC
    elif chain == "evm":
        from .evm import send_eth, DEFAULT_RPC
        send_fn, default_rpc = send_eth, DEFAULT_RPC
    else:
        raise ValueError(f"Unsupported chain: {chain}")

    rpc     = rpc_url or default_rpc
    results = []
    sent    = 0
    failed  = 0

    for i, wallet in enumerate(recipients):
        to_addr   = wallet["address"]
        send_amt  = random_amount(amount) if randomize else amount

        def _do(addr=to_addr, amt=send_amt):
            return send_fn(from_private_key, addr, amt, rpc)

        try:
            tx_hash = retry(_do, attempts=retry_attempts, delay=5)
            results.append({"address": to_addr, "amount": send_amt, "tx_hash": tx_hash, "status": "sent"})
            sent += 1
            _log.info(f"[{i+1}/{len(recipients)}] {send_amt} {chain} → {to_addr} | {tx_hash}")
        except Exception as e:
            results.append({"address": to_addr, "amount": send_amt, "tx_hash": None, "status": "failed", "error": str(e)})
            failed += 1
            _log.error(f"[{i+1}/{len(recipients)}] Failed → {to_addr}: {e}")

        if i < len(recipients) - 1:
            random_delay(delay_min, delay_max)

    return {
        "status":  "success" if failed == 0 else "partial",
        "chain":   chain,
        "total":   len(recipients),
        "sent":    sent,
        "failed":  failed,
        "results": results,
    }
