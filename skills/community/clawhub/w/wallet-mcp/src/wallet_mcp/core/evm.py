"""
EVM wallet operations: generation, balance, native token transfer.
Supports Ethereum, BSC, Polygon, Arbitrum, and any EVM-compatible chain.
"""
import os
from typing import Optional

DEFAULT_RPC = os.getenv("EVM_RPC_URL", "https://mainnet.infura.io/v3/9aa3d95b3bc440fa88ea12eaa4456161")


def generate_evm_wallet() -> dict:
    """Generate a new EVM wallet. Returns {address, private_key}."""
    from eth_account import Account
    acct = Account.create()
    return {"address": acct.address, "private_key": acct.key.hex()}


def get_evm_balance(address: str, rpc_url: str = DEFAULT_RPC) -> float:
    """Return native token balance in ETH (or chain native unit)."""
    from web3 import Web3
    rpc_url = rpc_url or DEFAULT_RPC
    w3 = Web3(Web3.HTTPProvider(rpc_url))
    if not w3.is_connected():
        raise ConnectionError(f"Cannot connect to RPC: {rpc_url}")
    bal = w3.eth.get_balance(Web3.to_checksum_address(address))
    return float(w3.from_wei(bal, "ether"))


def get_evm_balances_batch(addresses: list[str], rpc_url: str = DEFAULT_RPC) -> list[dict]:
    """Fetch balances for multiple EVM addresses."""
    from web3 import Web3
    rpc_url = rpc_url or DEFAULT_RPC
    w3 = Web3(Web3.HTTPProvider(rpc_url))
    if not w3.is_connected():
        raise ConnectionError(f"Cannot connect to RPC: {rpc_url}")
    results = []
    for addr in addresses:
        try:
            bal = w3.eth.get_balance(Web3.to_checksum_address(addr))
            results.append({"address": addr, "balance": float(w3.from_wei(bal, "ether")), "status": "ok"})
        except Exception as e:
            results.append({"address": addr, "balance": None, "status": "error", "error": str(e)})
    return results


_ERC20_ABI = [
    {"inputs": [{"name": "account", "type": "address"}], "name": "balanceOf",
     "outputs": [{"name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"},
    {"inputs": [], "name": "decimals",
     "outputs": [{"name": "", "type": "uint8"}], "stateMutability": "view", "type": "function"},
    {"inputs": [], "name": "symbol",
     "outputs": [{"name": "", "type": "string"}], "stateMutability": "view", "type": "function"},
]


def get_erc20_balances_batch(
    addresses: list[str],
    token_contract: str,
    rpc_url: str = DEFAULT_RPC,
) -> list[dict]:
    """
    Fetch ERC-20 token balances for multiple addresses.

    Returns list of {address, balance, symbol, status} — balance is human-readable (divided by decimals).
    """
    from web3 import Web3

    rpc_url = rpc_url or DEFAULT_RPC
    w3 = Web3(Web3.HTTPProvider(rpc_url))
    if not w3.is_connected():
        raise ConnectionError(f"Cannot connect to RPC: {rpc_url}")

    contract = w3.eth.contract(
        address=Web3.to_checksum_address(token_contract),
        abi=_ERC20_ABI,
    )
    try:
        decimals = contract.functions.decimals().call()
    except Exception:
        decimals = 18
    try:
        symbol = contract.functions.symbol().call()
    except Exception:
        symbol = "???"

    results = []
    for addr in addresses:
        try:
            raw = contract.functions.balanceOf(Web3.to_checksum_address(addr)).call()
            balance = raw / (10 ** decimals)
            results.append({"address": addr, "balance": round(balance, decimals), "symbol": symbol, "status": "ok"})
        except Exception as e:
            results.append({"address": addr, "balance": None, "symbol": symbol, "status": "error", "error": str(e)})
    return results


def sweep_eth_wallet(
    from_private_key: str,
    to_address: str,
    rpc_url: str = DEFAULT_RPC,
) -> dict:
    """
    Send all ETH from `from_private_key` wallet to `to_address`, deducting gas cost.
    Returns {address, sent_eth, tx_hash, status} or {address, status, reason}.
    """
    from web3 import Web3
    from eth_account import Account

    rpc_url = rpc_url or DEFAULT_RPC
    w3      = Web3(Web3.HTTPProvider(rpc_url))
    if not w3.is_connected():
        raise ConnectionError(f"Cannot connect to RPC: {rpc_url}")

    key     = from_private_key if from_private_key.startswith("0x") else f"0x{from_private_key}"
    acct    = Account.from_key(key)
    to_cs   = Web3.to_checksum_address(to_address)
    balance = w3.eth.get_balance(acct.address)
    gp      = w3.eth.gas_price
    gas_cost = 21_000 * gp
    sendable = balance - gas_cost

    if sendable <= 0:
        return {"address": acct.address, "status": "skipped", "reason": "insufficient balance"}

    tx = {
        "to":       to_cs,
        "value":    sendable,
        "gas":      21_000,
        "gasPrice": gp,
        "nonce":    w3.eth.get_transaction_count(acct.address),
        "chainId":  w3.eth.chain_id,
    }
    signed   = acct.sign_transaction(tx)
    tx_hash  = w3.eth.send_raw_transaction(signed.raw_transaction).hex()
    sent_eth = float(w3.from_wei(sendable, "ether"))
    return {"address": acct.address, "sent_eth": sent_eth, "tx_hash": tx_hash, "status": "swept"}


def send_eth(
    from_private_key: str,
    to_address: str,
    amount_eth: float,
    rpc_url: str = DEFAULT_RPC,
    gas_price_gwei: Optional[float] = None,
) -> str:
    """Send native token. Returns tx hash string."""
    from web3 import Web3
    from eth_account import Account

    rpc_url = rpc_url or DEFAULT_RPC
    w3 = Web3(Web3.HTTPProvider(rpc_url))
    if not w3.is_connected():
        raise ConnectionError(f"Cannot connect to RPC: {rpc_url}")

    key = from_private_key if from_private_key.startswith("0x") else f"0x{from_private_key}"
    acct = Account.from_key(key)
    to_cs = Web3.to_checksum_address(to_address)

    nonce = w3.eth.get_transaction_count(acct.address)
    gp = w3.to_wei(gas_price_gwei, "gwei") if gas_price_gwei else w3.eth.gas_price

    tx = {
        "to": to_cs,
        "value": w3.to_wei(amount_eth, "ether"),
        "gas": 21000,
        "gasPrice": gp,
        "nonce": nonce,
        "chainId": w3.eth.chain_id,
    }
    signed = acct.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    return tx_hash.hex()
