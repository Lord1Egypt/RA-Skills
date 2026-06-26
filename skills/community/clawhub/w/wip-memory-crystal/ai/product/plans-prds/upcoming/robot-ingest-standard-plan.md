# Plan: Robot Ingest Standard Protocol Spec

**Created:** 2026-03-12
**Status:** Upcoming (not started)
**Agent:** CC-Mini
**Product Idea:** `ai/product/product-ideas/robot-ingest-standard.md`
**Public Issue:** wipcomputer/memory-crystal#17

## Goal

Write ROBOT-INGEST-STANDARD.md as a formal protocol specification. Not code. A spec that defines how any new agent (robot, model, app) receives a complete Memory Crystal bundle and wakes up with full continuity.

## Why Now

- Parker articulated the endgame clearly: "I want to take everything I've ever done and give it to a robot."
- No standard exists. The big players will build walled-garden versions. We define the open one first.
- The spec clarifies Memory Crystal's long-term vision for investors, users, and the public README.
- Dream Weaver Protocol paper set the precedent: write the spec, then implement.

## Phases

### Phase 1: Crystal Bundle Format Spec

Define the export format:
- File structure (what's in the bundle)
- Encryption envelope (AES-256-GCM, key derivation, recipient key exchange)
- Layer manifest (which of the 5 layers are included, their sizes, checksums)
- Identity seals (ERA-Protocol proofs: this bundle hasn't been tampered with)
- Versioning (bundle format version, Crystal version that created it)

Deliverable: Section 1-3 of ROBOT-INGEST-STANDARD.md

### Phase 2: Ingest Protocol Spec

Define the import flow:
1. Receive bundle (file, MCP endpoint, QR scan, AirDrop)
2. Verify signature + ERA-Protocol proof
3. Decrypt with recipient key
4. Validate layer checksums
5. Layer-selective activation (full import vs. narrative-only vs. entities-only)
6. Confirmation handshake (agent proves it loaded correctly)

Deliverable: Section 4-5 of ROBOT-INGEST-STANDARD.md

### Phase 3: Cross-Platform Bridge Spec

Define thin adapters:
- MCP endpoint: `crystal_ingest --bundle=path`
- ROS2 bridge (robotics): topic-based memory subscription
- OpenAI-compatible API: POST /v1/memory/ingest
- Plain file: just drop the .crystal file in a watched directory

Deliverable: Section 6 of ROBOT-INGEST-STANDARD.md + appendix

### Phase 4: CLI Implementation

Add two commands to Memory Crystal:
- `crystal export --robot` (creates a signed .crystal bundle)
- `crystal ingest --bundle=file.crystal` (imports and activates)

Deliverable: Code in crystal CLI + tests

## Dependencies

- Existing Crystal schema (chunks, memories, entities, capture_state tables)
- Dream Weaver narrative output (for the narrative layer)
- ERA-Protocol (for identity verification... may need to formalize this too)
- Crypto module (already has AES-256-GCM, HMAC-SHA256, HKDF)

## Out of Scope

- Syncthing integration (separate plan)
- Ongoing sync (this is one-time transfer)
- Specific robot vendor integrations (spec is vendor-agnostic)
