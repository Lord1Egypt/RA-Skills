# Project ledger schema v2

Keep a human-readable Markdown ledger by default. JSON is optional when automated checks help. Do not force a database, parser or complete historical migration for a small checkpoint.

## Minimum useful checkpoint

Project identity; objective/scope; current status; updated time; relevant constraints and decisions with sources; exact artifact states and checks; pending operations; blockers; next executable action. Add only applicable fields. Preserve all relevant requirements even when there are many.

## Structured JSON contract

Required top-level fields: schema_version = 2, project_id, objective, status (active/paused/completed/blocked), updated_at, work_state. work_state.next_action is required except for completed projects. Record pending_operations separately from completed work.

Optional arrays: constraints, decisions, memories, lessons, artifacts, checks, relations. Every record has a unique stable id across those arrays and belongs to the ledger project. Do not use a person's private details as an ID.

Generic records use text, status, source_ref, and optionally recorded_at, valid_from, valid_to, evidence_kind (user_statement/source_observation/assistant_summary/inference), confidence_reason and depends_on. Unknown times are null; known times use ISO-8601 with timezone. recorded_at never substitutes for event/valid time.

Statuses: active, proposed, superseded, contradicted, completed, expired, uncertain, needs_recheck. Lessons may be candidate/validated/retired. An accepted or factual record needs a real source_ref; do not invent evidence to satisfy validation.

Artifacts use id, name, source_ref, version_or_fingerprint and state (source/draft/verified/rejected/superseded/needs_recheck). Preserve durable file ID and source location when available. Bind verified state to verification_scope and a matching current passing check. A version can be a real revision or an actually computed hash, never guessed.

Checks use id, status (passed/failed/pending), applicability (current/historical), scope, evidence_ref and targets: [{"id": "A-001", "version": "actual-version"}]. A historic check stays attached to its tested version. It cannot validate the artifact's newer version.

Dependencies use depends_on: [{"id": "A-001", "version": "actual-version"}]. Pin an artifact dependency to its exact version; for a decision dependency an ID is enough. Relations use from, type, to, where type is depends_on/derived_from/verified_by/affects/supersedes/contradicts. Relations supplement version-pinned dependencies; no edge is proof of no dependency.

Optional persistence metadata: canonical_item_id, base_revision, operation_id. Keep actual write receipt/version in session state or the next real checkpoint. Do not claim schema fields provide remote concurrency protection.

## v1 migration

Read old Markdown/YAML/JSON as-is. On a necessary checkpoint, add only evidenced v2 fields, keeping project identity, stable record IDs, original sources and useful history. Existing constraints, decisions, artifacts, work_state, lessons and relations remain valid concepts. Convert source/evidence to explicit source_ref/evidence_ref only when the referenced evidence is known. Preserve unmodeled fields and user edits.

Do not fabricate timestamps, versions, source IDs or passed tests. If old verified state lacks version-bound proof, preserve the old claim as historical/uncertain and mark current use needs_recheck. Do not overwrite original source artifacts. The optional helper accepts v2 JSON only; a v1 rejection means migration is needed for automated checking, not that the historical ledger is invalid.

## Optional helper limitations

ledger_guard.py is read-only and uses Python's standard library. It detects malformed records, duplicate IDs, unresolved links, project mixing, reversed known intervals, stale transitive dependencies, current checks on wrong versions and unsupported verified artifact claims. It flags a few credential patterns without printing values.

It does not retrieve evidence, persist files, measure semantic accuracy, prove graph completeness, detect every secret or enforce remote transactions. Validate those through the actual workflow. Use the same rules manually for Markdown or when Python is unavailable.
