---
name: "worldlines-scenario-authoring"
description: "WorldLines scenario creation and revision with clear multi-agent dialogue, validation, and real-model playtesting."
---

# WorldLines Scenario Authoring

Use this procedure when creating or revising a WorldLines world, scene flow, Soul dialogue, or player-facing presentation.

## Procedure

1. Read the installed WorldLines authoring skills from the active package before editing, including world/game, Soul, entity, and narrative guidance; locate their current paths instead of assuming a package layout. Complete when the applicable authoring contracts and current runtime version are identified.

2. Resolve the writable world root to `~/.worldlines/worlds/<world-id>/`; keep the WorldLines engine checkout and installed package read-only. Read the current world state, scene contracts, Soul voice files, player profile, and World Agent instructions. Complete when every planned write is scoped to the owned-world root.

3. Separate player-facing presentation into four visible channels: a compact turn header, narration, labeled dialogue, and short choices. Begin each turn with time/location/deadline, participants including communication medium, and the immediate problem. Label every speaker switch with name, role, and location or medium; never require the player to infer speakers from prose. Complete when the display contract is encoded in authoring data and World Agent instructions.

4. Give each Soul a stable role-language contract: first-person pronoun, form of address, register, sentence endings, professional vocabulary, forbidden styles, and one short positive example. Keep speaker-specific terms from crossing into another Soul's voice. Complete when each Soul remains identifiable even if visible speaker labels are removed.

5. Preserve autonomy while adding narrative pull. For every scene, define a dramatic question, immediate costs, character desires or refusals, and an outside escalation that proceeds without waiting for the player. Tie technical facts to a named character's responsibility or loss; include choices about trust and risk, not only destinations. Complete when the scene can advance through refusal or alternatives without becoming a script.

6. Add regression tests for the authored contracts: opening context, speaker labels, role-language markers, hidden-name boundaries, internal-tag exclusion, scene hooks, and any exact state invariants. Run JSON validation, the WorldLines validator, entity indexing, scene-harness tests, and MCP health checks. Complete when the world is playable with no blockers and every project test passes.

7. Copy the world into a disposable test root and run several real-model turns through the same launcher players use. Exercise the opening, direct questions to different Souls, a scene transition, and a consequential choice. Inspect rendered text, trace, clock, ledger, journal, and tool errors. Reject unlabeled dialogue, invented facts or durations, leaked internal blocks or unrevealed names, unnatural language contamination, oversized prose, or inconsistent role language. Complete when a fresh run satisfies both machine checks and reader-level clarity.

8. Apply findings only to the owned-world source, rerun the smallest affected tests, then repeat a fresh-model smoke turn so revised system instructions enter a new context. Move disposable test copies to Trash and leave existing saves unchanged unless explicitly requested. Complete when the source world is indexed, launcher-visible, and the verification evidence is recorded.

9. For proposed UI or system extensions, trace the requested action end to end before estimating work: UI guard and payload, local and hosted HTTP validation, player-intent construction, turn execution, audit/history rendering, and undo boundary. Look for dormant engine concepts that upstream layers currently block, and distinguish an OSS UI change from a proprietary-engine API change. Keep this analysis as design only until the user explicitly requests implementation. Complete when the smallest required cross-boundary contract and ownership of each change are identified.

10. When adapting or embedding source material, classify each exact work separately before copying text: public-domain literary source, later film or screenplay, modern derivative, or user-supplied reference. Record title, author, edition or URL, and provenance; never transfer the legal status of an original work to a later adaptation. Store full text only when its status or supplied-use basis permits it, and keep plot/content borrowing separate from style reference. Complete when every embedded source has a documented basis and no adaptation lineage has been conflated.

11. For latency or concurrency questions, trace the live turn path in the installed runtime before relying on configuration names, old comments, or design documents. Follow World Agent tool dispatch through Soul invocation, model response, heartbeat, and final integration; identify each blocking wait and verify whether loops actually schedule concurrent work. Treat legacy fields such as concurrency caps only as hypotheses until the current call path proves parallel execution. Complete when the latency estimate names which stages are serial, which can overlap safely, and which require proprietary-engine changes.

## Acceptance criteria

- A player can identify who is speaking and what is happening at a glance.
- Labels and role language provide redundant speaker identification.
- NPC autonomy remains intact; presentation rules do not prescribe their decisions.
- Static validation and actual model play both pass.
- Engine source, installed packages, credentials, and existing saves remain untouched unless separately authorized.
