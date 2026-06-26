"""
Solana wallet operations: generation, SOL transfer, SPL token account management.
"""
import os
import base58
from typing import Optional

DEFAULT_RPC = os.getenv("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com")
LAMPORTS_PER_SOL = 1_000_000_000


# ── Keypair helpers ────────────────────────────────────────────────────────

def generate_solana_wallet() -> dict:
    """Generate a new Solana keypair. Private key is base58-encoded 64-byte secret."""
    from solders.keypair import Keypair
    kp = Keypair()
    return {
        "address":     str(kp.pubkey()),
        "private_key": base58.b58encode(bytes(kp)).decode(),
    }


def _keypair(private_key_b58: str):
    from solders.keypair import Keypair
    return Keypair.from_bytes(base58.b58decode(private_key_b58))


# ── Balance ────────────────────────────────────────────────────────────────

def get_sol_balance(address: str, rpc_url: str = DEFAULT_RPC) -> float:
    from solana.rpc.api import Client
    from solders.pubkey import Pubkey
    rpc_url = rpc_url or DEFAULT_RPC
    resp = Client(rpc_url).get_balance(Pubkey.from_string(address))
    return resp.value / LAMPORTS_PER_SOL


def get_sol_balances_batch(addresses: list[str], rpc_url: str = DEFAULT_RPC) -> list[dict]:
    from solana.rpc.api import Client
    from solders.pubkey import Pubkey
    rpc_url = rpc_url or DEFAULT_RPC
    client = Client(rpc_url)
    results = []
    for addr in addresses:
        try:
            bal = client.get_balance(Pubkey.from_string(addr)).value / LAMPORTS_PER_SOL
            results.append({"address": addr, "balance": bal, "status": "ok"})
        except Exception as e:
            results.append({"address": addr, "balance": None, "status": "error", "error": str(e)})
    return results


# ── Transfer ───────────────────────────────────────────────────────────────

def send_sol(
    from_private_key_b58: str,
    to_address: str,
    amount_sol: float,
    rpc_url: str = DEFAULT_RPC,
) -> str:
    """Transfer SOL. Returns transaction signature."""
    from solana.rpc.api import Client
    from solana.rpc.types import TxOpts
    from solders.pubkey import Pubkey
    from solders.system_program import transfer, TransferParams
    from solders.transaction import Transaction
    from solders.message import Message

    rpc_url = rpc_url or DEFAULT_RPC
    client  = Client(rpc_url)
    sender  = _keypair(from_private_key_b58)
    to_pub  = Pubkey.from_string(to_address)
    lamps   = int(amount_sol * LAMPORTS_PER_SOL)
    bh      = client.get_latest_blockhash().value.blockhash

    ix  = transfer(TransferParams(from_pubkey=sender.pubkey(), to_pubkey=to_pub, lamports=lamps))
    msg = Message.new_with_blockhash([ix], sender.pubkey(), bh)
    tx  = Transaction([sender], msg, bh)

    result = client.send_transaction(tx, opts=TxOpts(skip_preflight=False, preflight_commitment="confirmed"))
    return str(result.value)


# ── Token Account Closer ───────────────────────────────────────────────────

_TOKEN_PROGRAM = "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"
_RENT_PER_ACCOUNT = 0.00203928  # approximate SOL rent for one token account


def get_token_accounts(owner_address: str, rpc_url: str = DEFAULT_RPC) -> list[dict]:
    """
    Return all SPL token accounts for `owner_address`.

    Tries jsonParsed encoding first (returns rich data).
    Falls back to base64 binary parsing if the installed solana-py version
    does not accept the encoding kwarg.
    """
    from solana.rpc.api import Client
    from solana.rpc.types import TokenAccountOpts
    from solders.pubkey import Pubkey

    rpc_url = rpc_url or DEFAULT_RPC
    client  = Client(rpc_url)
    owner   = Pubkey.from_string(owner_address)
    TOKEN   = Pubkey.from_string(_TOKEN_PROGRAM)
    opts    = TokenAccountOpts(program_id=TOKEN)

    # Try jsonParsed (works on solana-py versions that accept encoding kwarg)
    try:
        resp = client.get_token_accounts_by_owner(owner, opts, encoding="jsonParsed")
        return _parse_token_accounts_json(resp)
    except TypeError:
        pass  # encoding kwarg not supported — fall through to binary parse

    # Fallback: default base64 encoding + manual binary decode
    resp = client.get_token_accounts_by_owner(owner, opts)
    return _parse_token_accounts_binary(resp, client)


def _parse_token_accounts_json(resp) -> list[dict]:
    accounts = []
    if not resp.value:
        return accounts
    for acc in resp.value:
        try:
            data = acc.account.data
            if isinstance(data, dict):
                parsed = data.get("parsed", {})
            elif hasattr(data, "parsed"):
                parsed = data.parsed
            else:
                continue
            info   = parsed.get("info", {}) if isinstance(parsed, dict) else {}
            amount = info.get("tokenAmount", {})
            if not info or not amount:
                continue
            accounts.append({
                "pubkey":   str(acc.pubkey),
                "mint":     info.get("mint", ""),
                "amount":   int(amount.get("amount", 0)),
                "decimals": int(amount.get("decimals", 0)),
            })
        except (KeyError, TypeError, AttributeError):
            continue
    return accounts


def _parse_token_accounts_binary(resp, client) -> list[dict]:
    """
    Parse base64-encoded SPL Token account data (165-byte layout).
    Bytes 0-31: mint pubkey  |  bytes 64-71: amount (u64 LE)
    Decimals fetched from the Mint account via get_token_supply (cached).
    """
    import base64
    import struct
    from solders.pubkey import Pubkey

    accounts     = []
    mint_decimals: dict[str, int] = {}

    if not resp.value:
        return accounts

    for acc in resp.value:
        try:
            raw = acc.account.data
            if isinstance(raw, (list, tuple)) and raw:
                data_bytes = base64.b64decode(raw[0])
            elif isinstance(raw, (bytes, bytearray)):
                data_bytes = bytes(raw)
            else:
                continue

            if len(data_bytes) < 72:
                continue

            mint_pubkey = str(Pubkey.from_bytes(data_bytes[0:32]))
            amount      = struct.unpack_from("<Q", data_bytes, 64)[0]

            if mint_pubkey not in mint_decimals:
                try:
                    supply = client.get_token_supply(Pubkey.from_string(mint_pubkey))
                    mint_decimals[mint_pubkey] = supply.value.decimals
                except Exception:
                    mint_decimals[mint_pubkey] = 0

            accounts.append({
                "pubkey":   str(acc.pubkey),
                "mint":     mint_pubkey,
                "amount":   amount,
                "decimals": mint_decimals[mint_pubkey],
            })
        except Exception:
            continue
    return accounts


def get_spl_balances_batch(
    addresses: list[str],
    mint: Optional[str] = None,
    rpc_url: str = DEFAULT_RPC,
) -> list[dict]:
    """
    Fetch SPL token balances for multiple Solana wallets.

    Args:
        addresses: list of wallet public keys
        mint:      filter to a specific token mint address (optional — all tokens if omitted)
        rpc_url:   custom RPC URL

    Returns list of {address, tokens: [{mint, symbol, balance, decimals}], status}.
    """
    rpc_url = rpc_url or DEFAULT_RPC
    results = []
    for addr in addresses:
        try:
            accounts = get_token_accounts(addr, rpc_url)
            if mint:
                accounts = [a for a in accounts if a.get("mint") == mint]
            tokens = [
                {
                    "mint":     a["mint"],
                    "balance":  round(a["amount"] / (10 ** a["decimals"]), a["decimals"]) if a["decimals"] else a["amount"],
                    "decimals": a["decimals"],
                }
                for a in accounts
            ]
            results.append({"address": addr, "tokens": tokens, "status": "ok"})
        except Exception as e:
            results.append({"address": addr, "tokens": [], "status": "error", "error": str(e)})
    return results


def sweep_sol_wallet(
    private_key_b58: str,
    to_address: str,
    rpc_url: str = DEFAULT_RPC,
    leave_lamports: int = 5000,
) -> dict:
    """
    Send all SOL from `private_key_b58` wallet to `to_address`,
    keeping `leave_lamports` to cover the transaction fee.
    Returns {address, sent_sol, tx_hash, status} or {address, status, reason}.
    """
    from solana.rpc.api import Client
    from solders.pubkey import Pubkey

    rpc_url = rpc_url or DEFAULT_RPC
    client  = Client(rpc_url)
    sender  = _keypair(private_key_b58)
    address = str(sender.pubkey())

    balance_lamps = client.get_balance(sender.pubkey()).value
    sendable      = balance_lamps - leave_lamports

    if sendable <= 0:
        return {"address": address, "status": "skipped", "reason": "insufficient balance"}

    tx_hash  = send_sol(private_key_b58, to_address, sendable / LAMPORTS_PER_SOL, rpc_url)
    sent_sol = round(sendable / LAMPORTS_PER_SOL, 9)
    return {"address": address, "sent_sol": sent_sol, "tx_hash": tx_hash, "status": "swept"}


def close_token_accounts(
    private_key_b58: str,
    rpc_url: str = DEFAULT_RPC,
    close_non_empty: bool = False,
) -> dict:
    """
    Close empty SPL token accounts to reclaim rent SOL.
    Set close_non_empty=True to also close accounts with token balances.
    """
    from solana.rpc.api import Client
    from solana.rpc.types import TxOpts
    from solders.pubkey import Pubkey
    from solders.instruction import Instruction, AccountMeta
    from solders.transaction import Transaction
    from solders.message import Message

    rpc_url = rpc_url or DEFAULT_RPC
    TOKEN_PROG = Pubkey.from_string(_TOKEN_PROGRAM)
    CLOSE_IX   = bytes([9])   # CloseAccount opcode

    sender = _keypair(private_key_b58)
    owner  = str(sender.pubkey())

    all_accounts = get_token_accounts(owner, rpc_url)
    to_close     = [a for a in all_accounts if close_non_empty or a["amount"] == 0]

    if not to_close:
        return {"closed": 0, "skipped": len(all_accounts), "failed": 0,
                "total_found": len(all_accounts), "reclaimed_sol_estimate": 0.0}

    client  = Client(rpc_url)
    closed  = 0
    failed  = 0

    for acc in to_close:
        try:
            bh  = client.get_latest_blockhash().value.blockhash
            pub = Pubkey.from_string(acc["pubkey"])
            keys = [
                AccountMeta(pubkey=pub,           is_signer=False, is_writable=True),
                AccountMeta(pubkey=sender.pubkey(), is_signer=False, is_writable=True),
                AccountMeta(pubkey=sender.pubkey(), is_signer=True,  is_writable=False),
            ]
            ix  = Instruction(TOKEN_PROG, CLOSE_IX, keys)
            msg = Message.new_with_blockhash([ix], sender.pubkey(), bh)
            tx  = Transaction([sender], msg, bh)
            client.send_transaction(tx, opts=TxOpts(skip_preflight=True))
            closed += 1
        except Exception:
            failed += 1

    return {
        "closed":                 closed,
        "failed":                 failed,
        "skipped":                len(all_accounts) - len(to_close),
        "total_found":            len(all_accounts),
        "reclaimed_sol_estimate": round(closed * _RENT_PER_ACCOUNT, 6),
    }
