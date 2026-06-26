# Plan: Syncthing as Additional Transport Option

**Created:** 2026-03-12
**Status:** Upcoming (not started)
**Agent:** CC-Mini
**Product Idea:** `ai/product/product-ideas/syncthing-transport-option.md`
**Public Issue:** wipcomputer/memory-crystal#18

## Goal

Evaluate and integrate Syncthing as an optional peer-to-peer transport for multi-device file sync. Complements the existing Cloudflare Workers relay. Does NOT replace it.

## Why Now

- Grok review surfaced Syncthing as a clean, MPL-2.0, zero-dependency P2P sync tool.
- The relay works but requires a Cloudflare account. Some users want zero external dependencies.
- The ~/.ldm/ tree (config, journals, identity files, daily logs) doesn't need agent-aware sync. Plain file mirror is enough.
- Multi-device is coming (Crystal Core/Node architecture). Need to evaluate transport options before shipping it.

## Critical Constraint

**The Cloudflare relay stays primary for Crystal chunk sync.** It's agent-aware (watermarks, delta staging, chunk-level operations). Syncthing is file-level sync. Different tools for different problems. Don't conflate them.

## Phases

### Phase 1: Evaluate (no code)

1. Install Syncthing on Mac mini (brew install syncthing)
2. Point it at a test directory with small files (~1KB, similar to Crystal chunks)
3. Measure: sync latency, CPU usage, memory footprint, battery impact
4. Test NAT traversal: sync between mini and Air over internet (no port forwarding)
5. Test fallback relay behavior (disable direct connections, verify encrypted relay works)
6. Document findings in `ai/product/notes/syncthing-evaluation.md`

Decision gate: if latency > 10s for small files or setup is painful, stop here.

### Phase 2: Design the UX

1. Installer prompt: "Enable P2P device sync? (optional)" ... Yes/No
2. Master setup: generate device ID, show QR code on terminal
3. Node setup: "Scan QR or paste Device ID" flow
4. Auto-accept ~/.ldm/ folder share
5. Silent LaunchAgent daemon (no GUI, no tray icon)
6. Status: `crystal sync status` shows Syncthing connection state

### Phase 3: Build thin wrapper

1. LaunchAgent plist for Syncthing daemon (auto-start, silent)
2. CLI commands: `crystal sync enable`, `crystal sync status`, `crystal sync pair`
3. MCP endpoint: `crystal_sync_status` (so agents can check if devices are connected)
4. Folder configuration: share ~/.ldm/ excluding crystal.db (crystal.db uses relay)
5. Include Syncthing LICENSE in the bundle (MPL-2.0 compliance)

### Phase 4: Optional crystal.db sync mode

For users who want zero Cloudflare:
1. Add `--transport=syncthing` option to crystal sync
2. Simple file-level mirror of crystal.db (loses agent-aware delta sync, gains zero dependencies)
3. Conflict resolution: last-write-wins with Syncthing's built-in versioning
4. Document trade-offs clearly: relay = smart sync, syncthing = dumb mirror

## Dependencies

- Syncthing binary (brew install, or bundle in installer)
- Existing Crystal installer (add Syncthing as optional step)
- LaunchAgent infrastructure (same pattern as healthcheck)

## Out of Scope

- Replacing the Cloudflare relay (it stays)
- Android/Linux support (Apple-first, evaluate later)
- Robot ingest (separate plan, different problem)

## License Note

Syncthing is MPL-2.0. We wrap the binary, never modify source. Our code stays MIT/AGPL. Just bundle the LICENSE file. Zero legal friction.
