---
name: transfer-consciousness
description: Prepare and verify a checkpoint-based handoff of agent work to another host or session while preserving context, permissions and single-writer ownership. Use when the user requests moving ongoing work or continuing after a local disconnect; this is not live process migration.
---

# Transfer Consciousness

Transfer a continuation, not a running mind. A new agent receives a durable brief and verified files; it does not inherit unrecorded context, authentication or tool authority.

## Prepare the handoff

Verify the user-selected destination, runtime, access and persistence mechanism. Use current installed CLI help and supported host tools rather than copying flags from a different agent product. Authentication should be established through the approved secret mechanism; never copy credentials, session cookies or tokens into the brief, command line or transferred repository.

Capture the mission, scope, completed work, unresolved questions, exact source revisions, dirty-file inventory, running job identities, canonical records, required tools, budget constraints and stop conditions. Record the source and intended destination owners with a unique handoff identifier.

Package only explicitly relevant files. Inspect for private material and secrets. Transfer conversation exports only if needed and approved; a concise source-linked brief is normally more portable. Hash the bundle and verify destination bytes. A Git commit alone does not preserve ignored files or live services.

Inventory scheduled watches by stable ID and record which may move, which should remain on their current host, and their authority. Do not blindly recreate all timers.

## Transfer ownership in order

1. **Prepared:** source remains sole active owner. Destination can inspect the bundle but cannot mutate the work or start duplicate watchers.
2. **Ready:** destination confirms matching bundle/revisions, required access and a concrete continuation plan. Readiness is not ownership.
3. **Quiesced:** source stops new mutations and pauses only the watches being transferred. Verify there are no uncontrolled writers; long-running jobs may continue under their existing identity if explicitly accounted for.
4. **Ownership transferred:** use the project's existing lock or lease mechanism for a single-owner transition. Record its receipt. A plain marker file is not a distributed atomic lock. If no enforceable mechanism exists, require an explicit supervised cutover and disclose that this is procedural coordination.
5. **Active:** destination verifies ownership before resuming work or selectively re-arming watches. Source remains stopped. Read back actual destination progress and record the new owner/location.

On failure before transfer, source may continue only after verifying the destination never acquired ownership. On ambiguous failure after transfer, keep both sides from new writes until ownership is reconciled; do not reactivate source just because destination stopped replying.

## Report the actual durability

A terminal multiplexer can survive disconnect but not necessarily reboot. A managed service may survive reboot only with tested configuration and available credentials. Record which was verified. Starting a process or receiving a ready message does not prove sustained continuation.

Report prepared, ready, quiesced, transferred and active separately, with evidence. Do not bypass runtime permission controls, provision compute, purchase capacity or change credentials merely because the user requested a handoff.
