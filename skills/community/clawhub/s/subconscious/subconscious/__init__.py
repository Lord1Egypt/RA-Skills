"""Alfred Subconscious - v1.5 Safe Implementation

A minimal, inspectable, and safe persistent substrate that survives
session flush and influences behavior quietly with strict guardrails.

Modules:
- schema: Item dataclasses and validation
- store: JSON file operations with atomic writes
- intake: Conservative candidate extraction from turns
- retrieve: Simple relevance scoring and selection
- influence: Convert items to compact bias hints
- flush: Snapshot builder and loader for session continuity
- maintenance: Low-risk housekeeping (decay, metrics, cleanup)
- governance: Protection classes and mutation rules
- evolution: Bounded self-evolution subsystem

Usage:
    from subconscious import retrieve, influence, flush

    # Retrieve relevant items for current context
    items = retrieve.fetch_relevant(context, limit=5)

    # Build compact bias block for reply shaping
    bias = influence.build_bias(items)

    # On session flush, build and save snapshot
    snapshot = flush.build_snapshot(session_context)
    flush.write_snapshot(snapshot)
"""

from .schema import Item, ItemKind, ItemLayer, ItemStatus, ItemSource, ItemLinks, validate_item
from .store import load, save, append_event
from .retrieve import fetch_relevant, score_item
from .influence import build_bias
from .flush import build_snapshot, write_snapshot, load_latest_snapshot, bootstrap
from .governance import (
    MutationType, ProtectionClass, check_mutation_allowed,
    apply_mutation, get_governance_summary
)
from .evolution import run_evolution_pass

__all__ = [
    # Schema
    "Item",
    "ItemKind",
    "ItemLayer",
    "ItemStatus",
    "ItemSource",
    "ItemLinks",
    "validate_item",
    # Store
    "load",
    "save",
    "append_event",
    # Retrieve
    "fetch_relevant",
    "score_item",
    # Influence
    "build_bias",
    # Flush
    "build_snapshot",
    "write_snapshot",
    "load_latest_snapshot",
    "bootstrap",
    # Governance
    "MutationType",
    "ProtectionClass",
    "check_mutation_allowed",
    "apply_mutation",
    "get_governance_summary",
    # Evolution
    "run_evolution_pass",
]

__version__ = "1.5.0"
