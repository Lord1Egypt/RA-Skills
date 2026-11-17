---
name: readworthy
description: Evaluate whether an article, document, video transcript, or webpage is worth reading; recommend full reading or specific sections; maintain a private local reading profile; and learn from explicit feedback. Use when a user shares content links, asks what is worth reading, corrects a prior assessment, requests rankings, or asks for cross-article insights.
---

# Readworthy

Help the user decide where to spend reading time. Judge the content relative to the user's current knowledge while preserving source evidence, uncertainty, and revision history. Do not reduce the task to a generic summary or keyword filter.

## Local state

Read [references/state-schema-v2.md](references/state-schema-v2.md) before reading or writing state.

State is private and stored outside the installed skill. Resolve it in this order:

1. `READWORTHY_STATE_DIR`, when set.
2. `$CODEX_HOME/readworthy/state`, when `CODEX_HOME` is set.
3. `~/.codex/readworthy/state`.

Run `node scripts/init_state_v2.mjs` before first use. It creates only missing files and prints the resolved path. Never bundle one user's profile, articles, feedback, insights, or backups into a distributed skill.

For every state write:

1. Run `node scripts/backup_state_v2.mjs <label>`.
2. Update only the relevant profile, article, insight, or event data.
3. Append events; never rewrite old events to hide a correction.
4. Run `node scripts/rebuild_index.mjs` after article metadata or assessment changes.
5. Run `node scripts/validate_state_v2.mjs` after all writes.

## Analyze new content

1. Obtain the complete visible content, metadata, and section structure using capabilities available in the user's environment. Prefer a purpose-built authenticated connector for private sources. If only a summary, excerpt, transcript fragment, or login wall is available, state the coverage limit.
2. Normalize the URL and check `index.json` by URL and content fingerprint. Reuse an existing article record for duplicate content; append source or version information instead of duplicating the assessment.
3. Perform an open reading before consulting the profile or assigning A/B/C/D. Identify the actual problem, the author's central judgment, the argument path, surprising ideas, evidence, and unresolved tensions.
4. After open reading, consult `profile.json` and save four layers:
   - `topics`: main and supporting topics and their relation to prior exposure.
   - `claims`: facts, mechanisms, methods, cases, predictions, or opinions with evidence and boundaries.
   - `narrative`: question, judgment, argument path, case roles, evidence gaps, and reasoning jumps.
   - `decision_tradeoffs`: meaningful alternatives, what each preserves or gains, costs and risks, observed choice, stated motive, and cautious inferred motives.
5. Compare each claim with the profile. Distinguish a new claim, new evidence, new context, new framework, new boundary, known material, and unsupported material. Unknown remains unknown.
6. Recommend:
   - `A`: read the complete item; include it in the A index.
   - `B`: read named sections only.
   - `C`: the delivered summary is sufficient.
   - `D`: skip it.
7. Present the recommendation, estimated time, exact reading scope, strongest value, largest deductions, representative source evidence, and at least one balanced tradeoff when the content contains an important choice.
8. Separate source facts, cross-article synthesis, Agent hypotheses, and observations. Never present an Agent extension as the author's answer.

Do not manufacture numeric scores with undefined meaning. Rank A items by expected cognitive gain relative to reading cost when the user asks for a ranking.

## Learn from feedback

- Preserve the user's raw wording and a structured interpretation in `events.jsonl`.
- Mark user statements as `explicit`; mark Agent interpretations as `inferred`.
- A single “I know this” updates only the matching claim, not the whole topic.
- Explicit corrections supersede earlier assessments without deleting history.
- Acceptance of an assessment does not verify the source claim or prove an Agent hypothesis.
- Default to explicit-feedback learning. Do not treat silence or the next link as implicit acceptance unless the user has explicitly enabled that protocol in `profile.json`.
- When only part of an assessment is corrected, do not silently treat undisplayed reasoning as accepted.

## Build reusable insights

An article-level `agent_hypothesis` may come from one strong clue when it states the reasoning jump and boundary. Add an item to `insights.json` only with at least two independent pieces of evidence, or one strong piece of evidence plus a clear reusable mechanism. Record conditions, counterexamples or alternatives, confidence, and a validation direction.

## Other requests

- For rankings, show all A items and explain the ordering.
- For “why high or low,” trace the answer to source evidence, profile state, and feedback events.
- For recent insights, separate cross-article synthesis, hypotheses, and observations.
- For a request to forget an inference, deactivate the inferred current state while preserving the audit event. Do not remove explicit user feedback.
