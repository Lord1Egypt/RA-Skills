"""ZKP attestation tools for MCP server.

Delegates proof generation, aggregation, and verification to the Rust
oris_core module via PyO3 bindings. GIL is released during all
cryptographic operations. Memory usage is bounded via mmap streaming
in the Rust layer.

NO FALLBACK MODE. If the native module is unavailable, all ZKP
operations return explicit errors. Fake proofs are never generated.
A non-cryptographic "proof" would be accepted by nothing on-chain and
would create a false sense of security in the pipeline.
"""

from __future__ import annotations

import asyncio
import logging
from typing import Any

logger = logging.getLogger("oris.mcp.zkp")

# Load native ZKP module. Fail loudly if unavailable.
_zkp_service = None
try:
    import oris_core
    _zkp_service = oris_core.ZKPService()
    logger.info("native ZKP service loaded (Halo2 PLONK + Keccak-256)")
except (ImportError, AttributeError) as exc:
    logger.warning(
        "oris_core native module not available: %s. "
        "ZKP operations will return errors until the module is compiled.",
        exc,
    )


class ZKPAttestationService:
    """ZKP attestation service for MCP tool calls.

    All proof operations require the native Rust module. There is no
    fallback mode. Fake proofs are a security liability in a financial
    agent network and are never generated.
    """

    def __init__(self) -> None:
        self._native = _zkp_service

    def _require_native(self) -> None:
        """Raise if the native module is not loaded."""
        if self._native is None:
            raise RuntimeError(
                "ZKP operations require the oris_core native module. "
                "Build with: cd packages/oris-core && cargo build --release --features pyo3_binding"
            )

    async def generate_attestation(
        self, agent_id: str, chain: str
    ) -> dict[str, Any]:
        """Generate a KYA attestation with Halo2 PLONK proof.

        All hashing uses Keccak-256. Proof bytes, VK hash, and Merkle root
        are deterministic and reproducible on-chain.
        """
        self._require_native()

        agent_bytes = agent_id.encode("utf-8")

        result = await asyncio.to_thread(
            self._native.generate_proof, agent_bytes, chain
        )

        return {
            "proof_bytes": result["proof_bytes"].hex(),
            "public_inputs": list(result["public_inputs"]),
            "vk_hash": result["vk_hash"],
            "merkle_root": result["merkle_root"],
            "aggregation_level": result["aggregation_level"],
            "protocol": "plonk_halo2",
        }

    async def aggregate_proofs(
        self, proofs: list[bytes], public_inputs: list[bytes]
    ) -> dict[str, Any]:
        """Aggregate multiple proofs into a single super-proof.

        Uses mmap-backed streaming in Rust. RSS stays under 256MB.
        All hash outputs use Keccak-256.
        """
        self._require_native()

        result = await asyncio.to_thread(
            self._native.aggregate_proofs, proofs, public_inputs
        )

        return {
            "proof_bytes": result["proof_bytes"].hex(),
            "public_inputs": list(result["public_inputs"]),
            "vk_hash": result["vk_hash"],
            "merkle_root": result["merkle_root"],
            "aggregation_level": result["aggregation_level"],
        }

    def verify_proof(
        self, proof_bytes: bytes, public_inputs: list[int]
    ) -> bool:
        """Verify a proof. Lightweight (~1ms), no GIL release needed."""
        self._require_native()
        return self._native.verify_proof(proof_bytes, public_inputs)

    def serialize_for_contract(self, proof_bytes: bytes) -> bytes:
        """Serialize proof for Solidity verifier calldata."""
        self._require_native()
        return self._native.serialize_for_contract(proof_bytes)
