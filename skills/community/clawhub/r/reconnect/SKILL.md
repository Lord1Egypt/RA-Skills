---
name: reconnect
description: Help people expand their professional networks by discovering relevant peers, collaborators, mentors, and communities, reconnecting with existing contacts, resolving public profiles, and tracking explicitly authorised LinkedIn invitations. Use for goal-based networking, alumni or colleague reconnection, conference follow-up, and resumable outreach batches.
---

# Reconnect

Help the user build useful professional relationships around their goals. Start
from a topic, field, professional role, event, community, existing contacts, or roster.
A prior relationship, course, employer, or private archive is not required.

Read [network-plan.md](references/network-plan.md) when starting a new project or
changing its audience. Resolve a private project directory for its preferences,
sources, candidate records, batch reservations, and outcome ledger. Use the user's
current context to fill known preferences rather than conducting a long intake.

## Start with the requested mode

- **Find:** read [discovery.md](references/discovery.md). Search and record candidates
  with source URLs, dates, supporting and conflicting evidence.
- **Prepare:** read [tracking.md](references/tracking.md). Refresh source state, import
  candidates, and reserve a stable batch. Show unresolved identity or eligibility
  issues. An evidence score orders review; it is not a probability.
- **Connect:** read [linkedin.md](references/linkedin.md). Resolve the specific
  recipients covered by the user's instruction, check each live profile, perform
  permitted authorised actions, and verify the resulting state.
- **Reconcile/resume:** audit uncertain outcomes before retrying. Update the project's
  canonical contact tracker as well as the batch ledger. Never equate opening a
  profile, pressing a button, or a timeout with a successfully sent invitation.

The core accepts generic candidate JSON. Keep source-specific adapters and private
project instructions in the user's project, outside the distributable skill. An
adapter may read a permitted CRM export, address book, event list, or community
database and emit this format; it must preserve provenance and existing exclusions.

## Decisions that must survive sessions

Keep identity evidence, relevance to the user's goal, review priority, contact relationship,
and group membership separate. A confirmed identity may be ineligible for this
campaign. One profile can map to multiple archival identities: deduplicate by
canonical destination and preserve all underlying source IDs.

Respect the actual scope of user approval. An explicit instruction to send an
identified batch persists across interruptions; do not repeatedly ask for the same
approval. If recipients or purpose change, resolve that change first. Do not infer
outreach authority from approval to research, export, or install this skill.

Use existing browser skills and supported browser tools in the current harness.
Keep authenticated LinkedIn work sequential in one tab. Do not invent a universally
safe numerical sending limit, simulate human behaviour to evade detection, bypass
challenges, or schedule an unrestricted outreach campaign. Stop on platform warnings,
limits, restrictions, or identity challenges and report the concrete state.

Preserve each project's choice of invitation note, tone, and sender identity.
If a note is requested, use a specific truthful reason to connect and the user's
voice. Never imply a prior meeting, shared affiliation, endorsement, or familiarity
without evidence. Never submit an old private email to satisfy an identity
challenge without specific authorisation and evidence that it is appropriate.

## Included helper

`scripts/reconnect.py` uses Python's standard library. It imports evidence records,
deduplicates destinations, reserves batches transactionally, records observations,
and exports reviewable JSON. It makes no network calls and does not operate LinkedIn.
The agent performs research and permitted browser actions; the helper preserves
their evidence and outcomes. See [tracking.md](references/tracking.md) for commands.

Discovery can use public websites and professional platforms. The bundled ledger
currently tracks LinkedIn person-profile destinations; other channels require their
own supported tools and project integration. Do not claim a universal social API.

Keep generated databases and batch outputs in the private project, never in an
installed skill or its distributable snapshots. Do not commit, push, or publish
personal data as a side effect of using this skill.
