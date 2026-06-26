# Epistemic Block Format

## Schema

```json
{
  "id": "BLOCK-001",
  "version": "1.0",
  "timestamp": "2026-02-17T07:00:00Z",
  "question": "Original question",
  "context_refs": ["BLOCK-000"],
  "pipeline": {
    "generators": [
      {
        "model": "grok-4-1-fast",
        "model_family": "xai",
        "proposal": "...",
        "confidence": 0.75
      }
    ],
    "critique": {
      "model": "claude-opus-4-6",
      "blind_spots": ["..."],
      "contradictions": ["..."],
      "risk_factors": ["..."]
    },
    "synthesis": {
      "model": "claude-opus-4-6",
      "consensus": "...",
      "confidence": 0.78,
      "dissent": ["..."],
      "action_items": ["..."]
    }
  },
  "metrics": {
    "mdi": 0.56,
    "consensus_score": 0.78,
    "duration_seconds": 185
  },
  "parent_hashes": [],
  "content_hash": "sha256:..."
}
```

## Key Fields

- **mdi** (Model Diversity Index): 0-1, measures independence across model families. >0.5 = good diversity.
- **consensus_score**: 0-1, agreement level. >0.7 = strong consensus.
- **dissent**: Explicit minority positions preserved (not suppressed).
- **content_hash**: SHA-256 of canonical JSON for integrity verification.
- **context_refs**: DAG links to parent blocks (95% standalone, 5% chained).

## Lifecycle

`draft` → `pending` → `final` → `retracted`

Blocks can be challenged within 48h of finalization.

## Size

- Typical: 3-12 KB
- Hard limit: 50 KB (use summaries, not full text)
- Storage: Local JSON Phase 1, IPFS Phase 3
