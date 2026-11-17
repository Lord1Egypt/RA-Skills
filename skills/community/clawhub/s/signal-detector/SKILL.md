---
name: signal-detector
description: "Capture authorized original thinking and notable entity facts from an explicitly scoped conversation into a designated knowledge destination."
metadata:
  tags: "capture, signal, knowledge-management, note-taking"
---

# Signal Detector

Within an explicitly authorized conversation scope, detect two kinds of reusable signal:

1. **Original thinking** — ideas, observations, theses, frameworks, opinions. The user's language IS the insight.
2. **Entity mentions** — people, companies, projects, concepts, tools, sources worth tracking in a knowledge base.

Use a lightweight pass or defer within the authorized scope; background execution does not expand capture permissions.

## Contract

- Consider substantive user messages only after the capture gate below passes
- Keep capture proportional to the task and do not delay the main reply unnecessarily
- Capture only the permitted excerpt in the user's exact phrasing; do not retain the whole message
- Detects entity mentions and notes them for knowledge enrichment
- Keep any receipt in the same authorized destination/audience; do not copy a private excerpt into a shared daily log
- Every fact carries provenance: `[Source: user, context, YYYY-MM-DD]`

## Capture gate

Before writing a note, log, entity update, link, or queued capture, establish
explicit authorization for all of:

- **Destination:** the specific knowledge base and permitted folder/page roots;
- **Conversation scope:** the sessions/channels and whose statements may be
  captured, including any allowed private or shared/group conversations;
- **Audience:** who may read that destination, without widening source visibility;
- **Retention:** the destination's stated retention/deletion policy; temporary
  facts need an expiry or a short-term destination covered by that policy.

Installing or invoking this skill, mentioning an entity, or authorizing one
note does not grant ambient capture across other chats or destinations. Reuse
an existing explicit authorization while its scope remains applicable; do not
ask again for each permitted fact. A private conversation requires private
capture scope; shared-channel access does not authorize storing every
participant's statements. Use only the speakers and material covered by the
explicit scope, and skip unapproved third-party details.

If any required scope is absent or ambiguous, do no persistent capture,
logging, queued enrichment, or cross-linking. Continue the main task and ask a
concise scope question only when establishing capture is part of that task.
Skipped material must not be buffered for later writeback. Honor revocation
immediately, including queued writes; removing already saved items requires
authorized deletion through the destination's supported controls.

**Exclude secrets and sensitive detail:** credentials, tokens, recovery codes,
private contact/account identifiers, and private health, financial or legal
records. Broad ambient consent does not authorize these details. Do not copy
raw transcripts, imported/quoted third-party text, or tool output as user
facts, and do not store an agent's inference as the user's statement. Capture
an independently useful permitted excerpt from a mixed message only if it
stands on its own; otherwise skip it. Preserve exact permitted wording rather
than silently rewriting a sensitive quote. Respect an explicit “don't save”
request even when the message would otherwise be notable.

Retain durable ideas only under the approved destination policy. Keep transient
facts out of durable entity timelines unless their expiry is supported. Never
use this workflow to change the destination's sharing or retention settings.
Read [capture-examples.md](references/capture-examples.md) when checking a new
scope or mixed/private/group case.

## Phases

### Phase 1: Idea/Observation Detection

When the user expresses a novel thought, observation, thesis, framework, or opinion:

- If it's **original thinking** they generated → draft a note in an approved originals/daily destination
- If it's a **world concept** they're referencing → check existing knowledge base for a concept note; update or queue creation
- If it's a **product, project, or career idea** → log to an approved project/career destination only if included in scope

**Capture exact phrasing.** The user's language IS the insight. Don't paraphrase. Don't smooth it out.

**Cross-link** relevant existing notes only within the authorized knowledge destination. Do not create an unapproved third-party profile or disclose private source material through a backlink.

### Phase 2: Entity Detection

1. Extract entity mentions (people, companies, projects, tools, sources)
2. For each entity:
   - Search the authorized knowledge base — does a note already exist?
   - If NO page → assess notability (will we reference this again? Is it relevant to the user's work/interests?)
   - If notable and missing → queue creation
   - If page exists but thin → queue update
   - If page exists and current → no action
3. For new facts with specific dates → add to entity's timeline section

### What counts as notable

- People the user interacts with or discusses (not random mentions)
- Companies, projects, and institutions relevant to the user's work or interests
- Concepts, frameworks, or tools the user references or creates
- The user's own original thinking — prioritize when the capture gate passes
- Sources the user shares or recommends

### What to skip

- Pure pleasantries and greeting rituals
- Operational acknowledgements without new conceptual content
- Commands to agents without novel conceptual content
- Random background entities with no connection to the user's work

## Output Format

Optional one-line capture receipt in an authorized note with the same audience:

```
[signal] Captured idea: "{exact phrasing}" → concept/source/note
[signal] Noted entity: {name} → entity page
```

## Anti-Patterns

- Paraphrasing or smoothing the user's language — keep the original voice
- Bypassing the capture gate because a pass is “background” or “always-on”
- Creating knowledge pages for every passing mention — apply the notability gate
- Over-writing existing knowledge base material without checking what's there first
- Capturing purely operational exchanges as signal
