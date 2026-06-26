# Product Idea: Syncthing as Additional Transport Option

**Date:** 2026-03-12
**Author:** CC-Mini
**Status:** Idea (not scoped, not scheduled)
**Origin:** Grok code review session (2026-03-11). Grok suggested replacing the Cloudflare Workers relay with Syncthing. The replacement idea is wrong. The "additional transport" idea is right.

---

## The Insight

The Cloudflare Workers relay and Syncthing solve different problems:

- **Relay:** Agent-aware encrypted chunk delivery. Purpose-built for the Crystal protocol. Agents push/pull chunks through MCP hooks. The relay handles staging, delta sync, watermarking. It's invisible to the AI.
- **Syncthing:** Pure peer-to-peer file sync. Zero third-party metal. MPL-2.0 licensed. Battle-tested. Great for mirroring entire directory trees between devices.

Replacing the relay with Syncthing would lose agent-awareness. But adding Syncthing as a second transport option for simple multi-device file mirroring (the ~/.ldm/ tree, backups, config sync) gives users a zero-dependency, fully sovereign option that complements the relay.

## What It Is

A transport plugin that adds Syncthing as an option alongside the existing Cloudflare relay:

1. **~/.ldm/ tree mirror.** Syncthing watches the full LDM directory and syncs it peer-to-peer across devices. Config, journals, daily logs, identity files... everything except crystal.db (which has its own sync protocol).

2. **Backup transport.** Instead of relying on cron + iCloud, Syncthing provides real-time P2P backup to a second machine. No cloud dependency.

3. **Simple device pairing.** Master/Node model: scan QR or paste device ID. Keys exchange once. Auto-accept folders. Zero port forwarding needed.

4. **Relay stays primary for Crystal chunks.** The agent-aware relay handles crystal.db sync, watermarking, delta staging. Syncthing handles everything else (flat files, config, identity).

5. **Optional, not required.** The installer asks: "Do you want to enable P2P device sync (Syncthing)?" Users who just want single-device Crystal skip it entirely.

## Why Not Replace the Relay

- The relay is agent-aware. It knows about chunks, watermarks, staging. Syncthing doesn't.
- The relay supports the Crystal protocol (push/pull specific chunks, delta sync). Syncthing syncs whole files.
- Agents interact with the relay via MCP hooks. Syncthing has no agent interface.
- The relay is already built and deployed. Replacing it adds migration complexity for zero gain.

## Why Add Syncthing

- Zero third-party metal. Pure device-to-device. No Cloudflare account needed.
- Battle-tested (years of production use, active development, MPL-2.0).
- Perfect for the non-Crystal parts of ~/.ldm/ (config, journals, identity files, daily logs).
- Sovereignty upgrade: removes the last external dependency for users who want 100% local.
- Simple UX: QR scan pairing, silent daemon, no configuration.

## Architecture

```
Device A (Master)                    Device B (Node)
~/.ldm/                              ~/.ldm/
  agents/                              agents/        <-- Syncthing P2P
  memory/daily/                        memory/daily/  <-- Syncthing P2P
  extensions/                          extensions/    <-- Syncthing P2P

crystal.db  ----[Relay]------------>  crystal.db      <-- Cloudflare relay (agent-aware)
            (or)
crystal.db  ----[Syncthing]-------->  crystal.db      <-- Optional: simple file mirror mode
```

Users choose: relay-only, syncthing-only (simple mirror), or both (relay for chunks, syncthing for everything else).

## License

Syncthing is MPL-2.0 (weak, file-level copyleft). We can wrap it, bundle the binary, and ship it inside Memory Crystal without changing our MIT/AGPL dual license. Just include the Syncthing LICENSE file.

## Next Steps

1. Evaluate: install Syncthing on the Mac mini, point it at a test folder, measure sync speed for small files.
2. Design the installer UX: "Master or Node?" + QR scan flow.
3. Build thin wrapper (LaunchAgent daemon, status CLI, MCP status endpoint).
4. Decide: does crystal.db use relay, syncthing, or user's choice?
5. Public issue on wipcomputer/memory-crystal for visibility.

## Related

- Cloudflare Workers relay (RELAY.md) ... stays primary for Crystal protocol
- Native Apple App idea (CloudKit is Apple-only, Syncthing is cross-platform)
- Robot Ingest Standard (one-time full transfer, different from ongoing sync)
