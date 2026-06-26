"""
Wallet generator: create N wallets for EVM or Solana and persist to CSV.
"""
from .utils import now_iso, setup_logging

_log = setup_logging()


def generate_wallets(chain: str, count: int, label: str, tags: str = "") -> list[dict]:
    """
    Generate `count` wallets for `chain` ('solana' | 'evm').
    Saves to CSV and returns list of wallet dicts.
    """
    from .storage import save_wallets_batch, load_wallets

    chain = chain.lower()
    if chain not in ("solana", "evm"):
        raise ValueError(f"Unsupported chain '{chain}'. Choose 'solana' or 'evm'.")
    if not (1 <= count <= 10_000):
        raise ValueError("count must be between 1 and 10,000.")

    gen_fn = (
        _import("wallet_mcp.core.evm",    "generate_evm_wallet")
        if chain == "evm"
        else _import("wallet_mcp.core.solana", "generate_solana_wallet")
    )

    now      = now_iso()
    existing = {w["address"] for w in load_wallets()}
    wallets  = []

    for _ in range(count):
        w = gen_fn()
        if w["address"] in existing:
            _log.warning(f"Duplicate address skipped: {w['address']}")
            continue
        existing.add(w["address"])
        wallets.append({
            "address":     w["address"],
            "private_key": w["private_key"],
            "chain":       chain,
            "label":       label,
            "tags":        tags,
            "created_at":  now,
        })

    save_wallets_batch(wallets)
    _log.info(f"Generated {len(wallets)} {chain} wallets | label={label}")
    return wallets


def _import(module: str, fn: str):
    import importlib
    return getattr(importlib.import_module(module), fn)
