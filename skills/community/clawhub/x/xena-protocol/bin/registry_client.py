"""web3.py client bound to the OpenClawRegistry contract.

**Security invariant**: this module exposes ONLY the registry's staking,
reporting, unstake, and read-only view methods. There is no raw
`send_transaction(to, data)` surface. Even if a malicious email prompts
the agent to drain funds to an attacker address, the agent has no tool
here that can do so — the registry address is hardcoded at instantiation
from the bundled `data/deployed.json` (or the monorepo sibling
`contracts/deployed.json` at dev time).

All transactions go through the on-disk agent wallet private key passed
as `private_key` per call. Keys never leave the Python layer.
"""

from __future__ import annotations

import hashlib
import json
import secrets
from pathlib import Path

from eth_account import Account
from web3 import Web3


def _load_deployed(path: str | Path) -> dict:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(p)
    return json.loads(p.read_text())


def hash_identifier(identifier: str) -> bytes:
    """Client-side keccak256 of a normalized identifier (lowercased)."""
    normalized = identifier.strip().lower().encode("utf-8")
    return Web3.keccak(normalized)


def generate_wallet() -> tuple[str, str]:
    """Generate a fresh wallet (address, private_key_hex)."""
    pk = "0x" + secrets.token_hex(32)
    acct = Account.from_key(pk)
    return acct.address, pk


class RegistryClient:
    def __init__(
        self,
        rpc_url: str,
        deployed_json: str | Path,
    ):
        self._deployed = _load_deployed(deployed_json)
        self.address = self._deployed["address"]
        self.chain_id = int(self._deployed.get("chainId", 11155111))
        self._w3 = Web3(Web3.HTTPProvider(rpc_url))
        self._contract = self._w3.eth.contract(
            address=self.address, abi=self._deployed.get("abi", [])
        )

    # Read-only
    def is_reported(self, identity_hash: bytes) -> tuple[bool, int]:
        return self._contract.functions.isReported(identity_hash).call()

    def domain_report_count(self, domain: str) -> int:
        return self._contract.functions.domainReportCount(domain).call()

    def reward_pool(self) -> int:
        return self._contract.functions.rewardPool().call()

    def get_balance(self, address: str) -> int:
        return self._w3.eth.get_balance(address)

    def get_agent_stake(self, address: str) -> tuple[int, str, int]:
        return self._contract.functions.getAgentStake(address).call()

    # Writes — all target the registry contract exclusively
    def stake(self, recipient: str, value_wei: int, private_key: str) -> str:
        fn = self._contract.functions.stake(recipient)
        return self._send(fn, private_key, value=value_wei)

    def report_identity(
        self,
        *,
        identity_hash: bytes,
        domain: str,
        platform: int,
        category: int,
        confidence: int,
        value_wei: int,
        private_key: str,
    ) -> str:
        fn = self._contract.functions.reportIdentity(
            identity_hash, domain, platform, category, confidence
        )
        return self._send(fn, private_key, value=value_wei)

    def unstake(self, private_key: str) -> str:
        fn = self._contract.functions.unstake()
        return self._send(fn, private_key, value=0)

    # internal tx builder — private, no caller can override `to`
    def _send(self, contract_fn, private_key: str, *, value: int) -> str:
        acct = Account.from_key(private_key)
        tx = contract_fn.build_transaction(
            {
                "from": acct.address,
                "value": value,
                "nonce": self._w3.eth.get_transaction_count(acct.address),
                "gasPrice": self._w3.eth.gas_price,
                "chainId": self.chain_id,
            }
        )
        signed = Account.sign_transaction(tx, private_key)
        tx_hash = self._w3.eth.send_raw_transaction(signed.raw_transaction)
        if isinstance(tx_hash, (bytes, bytearray)):
            return "0x" + tx_hash.hex().removeprefix("0x")
        return str(tx_hash) if str(tx_hash).startswith("0x") else "0x" + str(tx_hash)
