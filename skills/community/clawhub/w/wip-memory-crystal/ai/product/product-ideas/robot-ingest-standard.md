# Product Idea: Robot Ingest Standard (ROBOT-INGEST-STANDARD.md)

**Date:** 2026-03-12
**Author:** CC-Mini
**Status:** Idea (not scoped, not scheduled)
**Origin:** Grok code review session (2026-03-11). Parker described the endgame: when a robot shows up, you hand it one file and it wakes up knowing you. No "tell me about yourself" reset. No re-uploading your life story. Just continuity.

---

## The Insight

Every AI memory tool solves "remember stuff between sessions." None of them solve "transfer everything I am to a completely new agent/body."

The robot transition is coming. Humanoids, new model families, embodied agents. When that happens, the person who owns a portable, sovereign, complete memory bundle wins. Everyone else starts over.

Memory Crystal already has all five layers: raw transcripts, vectors, structured entities, dream-weaver narrative, active context. The missing piece is a formal protocol spec for exporting and importing that bundle into any new agent... regardless of vendor, form factor, or runtime.

## What It Is

A protocol specification (not code, not a product) that defines:

1. **The Crystal Bundle format.** A single signed + encrypted export containing all five memory layers, identity seals, and ERA-Protocol proofs. Portable, verifiable, vendor-agnostic.

2. **The Ingest Protocol.** How any new agent (robot, model, app) receives, verifies, decrypts, and activates a Crystal Bundle. One import. Instant continuity.

3. **Identity verification.** ERA-Protocol integration: the receiving agent must prove it hasn't tampered with the memory before acting on it. Prevents narrative steering from day one.

4. **Layer-selective import.** Not every agent needs all five layers. A voice assistant might only need narrative + entities. A code agent might need raw transcripts. The spec defines which layers are required vs. optional.

5. **Cross-platform bridge hooks.** Thin adapters for common runtimes: MCP endpoint, ROS2 bridge (robotics), OpenAI-compatible API, plain file import.

## Why This Matters

- No standard exists for "give this robot my entire life in one sovereign bundle."
- The big players (OpenAI, Anthropic, Google) will eventually build walled-garden versions. Owning the open spec first means the sovereign option exists when people need it.
- It clarifies Memory Crystal's endgame for investors, users, and contributors.
- It's a protocol, not a product. MIT-licensed, implementable by anyone. The product is Crystal itself.

## Parker's Words (verbatim)

> "Once there is a robot, I don't want to have to fucking take all my memories and have to redo it with the robot. I want to be able to take everything I've ever done and give it to a robot. There we go. That's how memory is going to work."

## What It's Not

- Not a product to sell. It's a spec that makes Crystal more valuable.
- Not code to write right now. The spec comes first.
- Not Syncthing, not a sync layer. This is about one-time full transfer, not ongoing sync.

## Next Steps

1. Write ROBOT-INGEST-STANDARD.md as a formal protocol spec (like Dream Weaver paper style).
2. Define the Crystal Bundle format (file structure, encryption envelope, layer manifest).
3. Define the Ingest Protocol (verify, decrypt, activate, confirm).
4. Add `crystal export --robot` and `crystal ingest --bundle` as CLI commands that implement the spec.
5. Public issue on wipcomputer/memory-crystal for visibility.

## Related

- Dream Weaver Protocol (narrative consolidation feeds the bundle)
- ERA-Protocol (identity verification on ingest)
- Native Apple App idea (CloudKit sync is a different problem... ongoing sync vs. one-time transfer)
- Sovereignty Covenant (trust model for who gets to ingest your crystal)
