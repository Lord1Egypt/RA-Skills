# Meetings, Calls, and Interviews

Scope: you have a transcript, notes, or a recording of people talking, and someone needs to know what happened. The output is three lists, not a narrative.

**Before summarizing a recurring meeting**, read `## Sources` in `~/Clawic/data/summarizer/memory.md` (or `sources.md` if the `## Boxes` index points there) for the previous edition, and `glossary.md` for the project names and acronyms the transcript will mangle. A recap that reintroduces context the attendees have had for six weeks is padding.

**Contents:** [The Three Lists](#the-three-lists) · [Decision vs Discussion](#decision-vs-discussion) · [Action Items](#action-items) · [Reading Order](#reading-order) · [Speakers and Attribution](#speakers-and-attribution) · [Transcript Defects](#transcript-defects) · [Meeting Types](#meeting-types) · [Interviews and User Research](#interviews-and-user-research) · [The Recap Shape](#the-recap-shape)

## The Three Lists

Every meeting recap resolves into exactly three buckets. Anything that fits none of them is context and is cut first.

| Bucket | Test | Failure if wrong |
|---|---|---|
| **Decided** | Someone with authority stated a choice and nobody reopened it before the meeting ended | A "decision" gets re-litigated next week and the recap gets blamed |
| **Assigned** | Owner + verb + date, all three present | An ownerless intention produces zero follow-through |
| **Open** | A question raised and not answered, or a decision blocked on something named | Silently dropped, it resurfaces as a surprise a month later |

Order in the output: Decided, Assigned, Open. Everything else — background, tangents, the demo that worked — is at most one line under Context, and only when a non-attendee reads it.

## Decision vs Discussion

The verbs are the tell. Language of intent is not a decision.

| Utterance | Status | Why |
|---|---|---|
| "We're going with Postgres." | Decided | Declarative, present tense, no condition |
| "I think we should probably go with Postgres." | Open | Modal + hedge; it is a proposal |
| "Let's go with Postgres unless infra objects." | Decided, conditional | Keep the condition attached: "pending infra sign-off" |
| "Nobody objected." | Open | Silence is not assent in a room of eight; note who was absent |
| "We'll circle back." | Open | The canonical parked item; give it an owner or it is lost |
| "Fine, do it your way." | Decided, contested | Decided with a named dissent — the dissent survives (SKILL.md Rule 4) |

Two people asserting different decisions on the same subject means the meeting produced no decision on it. Write it as open, name both positions, and do not pick.

## Action Items

`owner + verb + object + date`. Missing any of the four demotes it to Open.

- **Owner is a person, never a team.** "Platform will look at it" is unassigned. If the transcript names only a team, write `owner: unassigned (Platform)` and let the reader see the gap.
- **Date is absolute.** "Next Tuesday" resolves against the meeting date; if the meeting date is unknown, keep the phrase verbatim and say the meeting date is unknown. Never emit a relative date into an undated document.
- **Verb is falsifiable.** "Look into", "think about", "sync on" cannot be marked done. Push to the observable outcome the speaker actually meant: "post the benchmark numbers in #infra".
- **Implicit commitments count.** "I'll get you that by Friday" is an action item even if nobody wrote it down; scanning for first-person future tense catches most of them.
- **A commitment made by someone not in the room is not an action item**, it is an open dependency.

## Reading Order

Transcripts violate every reading heuristic that works on documents.

1. **Read the last 20% first.** Decisions land at the end, after the discussion that produced them. A single pass from the top spends most of its attention on exploration that got discarded.
2. **Then scan for first-person future tense** ("I'll", "I can take", "let me") — this is the action-item pass, and it is a keyword scan, not a comprehension pass.
3. **Then read the middle for the reasons.** The middle holds the tradeoff that explains the decision, which is what a non-attendee needs and an attendee does not.
4. **Read the opening last, if at all.** Agenda review and status round-robins compress to nothing.

Airtime is not importance. The subject with the most minutes is usually the one nobody could resolve; the decision that mattered took forty seconds.

## Speakers and Attribution

- Attribute anything contested, anything projected, and anything a person committed to. Do not attribute uncontroversial factual statements — "Speaker 3 said the deploy is on Thursday" is noise if nobody disputes it.
- **Diarization labels are unreliable.** `Speaker 2` swaps mid-transcript when two voices are close, and overlapping speech gets merged into whoever was louder. Anchor identity on self-introductions and on names other people use, then map labels to names once at the top and use names throughout.
- **Crosstalk lines** (`[inaudible]`, interleaved half-sentences) are the highest-risk region in the file: a decision stated over someone else's sentence is frequently mis-attributed. If the decision sits in crosstalk, mark it uncertain rather than guessing the speaker.
- With `store_summaries` other than `none`, attendees who are named recipients or recurring counterparts get a row in the shared `~/Clawic/data/contacts/contacts.md`, keyed by lowercase email and updated in place, and the recap references them by name only.

## Transcript Defects

| Defect | Signature | Handling |
|---|---|---|
| ASR proper-noun mangling | Product and person names drift ("Kubernetes" → "Cooper Nettie's") | Repair against `glossary.md`; add any new recurring term to it in the same turn |
| Speaker-label swap | A speaker's stance flips mid-meeting with no transition | Re-anchor on names spoken aloud; if unresolvable, drop attribution rather than invent it |
| Missing first minutes | Recording started late; the agenda is absent | Say so in the header; the decision may reference context you never saw |
| Filler and repetition | 20-40% of raw conversational transcript is filler, restarts, and backchannel | Remove wholesale; it is the one deletion with zero information cost |
| Numbers spoken aloud | "fifteen hundred" vs "1,500", "point five" vs "0.5" | Normalize to digits and confirm the magnitude reads sensibly in context |
| Two meetings in one file | Back-to-back calls recorded continuously | Split before summarizing; a merged recap attributes decisions to the wrong meeting |

## Meeting Types

| Type | What the recap is for | Keep | Cut |
|---|---|---|---|
| Standup | Blockers only | Blocked items and who unblocks them | Every "no blockers" |
| 1:1 | Commitments and concerns | Actions, raised risks, career items | Small talk, status already tracked elsewhere |
| Project sync | State change since last sync | Deltas, new risks, decisions | Anything identical to the previous edition (`recurring.md`) |
| Design review | The decision and the rejected options | Chosen approach, rejected alternatives with why | The exploration that led nowhere |
| Incident review | Timeline and actions | Timestamped sequence, contributing causes, preventive actions with owners | Blame, speculation stated as fact |
| Board or investor call | Commitments and numbers | Figures stated, guidance given, questions asked by whom | Presentation narration |
| Sales or client call | What was promised | Promises made, objections raised, next step with date | Rapport building |
| All-hands | What changed for the listener | Policy and org changes, dates | Motivational framing |
| Interview (hiring) | Evidence per criterion | Signals mapped to criteria, verbatim answers on decisive points | Interviewer talking |
| Anything else | Decisions and commitments | The Three Lists | Everything else |

## Interviews and User Research

Research interviews invert the rule that the summarizer does not judge: the finding *is* the synthesis. It still separates layers.

- **Quote, paraphrase, interpretation — three separate layers.** A verbatim quote in quotation marks with the speaker ID; a paraphrase unquoted; your inference labelled as inference. Collapsing them is how one participant's offhand remark becomes "users want X".
- **Count before you generalize.** "3 of 8 participants" beats "several participants" and prevents a single vivid interview from carrying a claim.
- **Keep the question that produced the answer.** A leading question changes what the answer means, and the answer alone hides it.
- Cross-interview synthesis is `multi-source.md`; one interview at a time here.

## The Recap Shape

```
Meeting — <name>, <date>, <duration>. Attendees: <names>. Source: <transcript | notes>, cut-off <timestamp if partial>.

Decided
- <decision> — <one-line why>. <condition, if any>. <dissent, if any>.

Assigned
- <owner> — <verb + object> — <absolute date>.

Open
- <question or blocked decision> — blocked on <what/who>.

Context (only for readers who were absent)
- <≤3 lines>

Omitted: <what was cut, if material>
```

With `markers: emoji`, section labels take their emoji; with `markers: none`, the labels stay and the formatting goes. The four sections never disappear — an empty one is written as "Decided: none", because "no decisions were made" is itself the finding of many meetings.

**After a recap, write it.** The summary goes to `~/Clawic/data/summarizer/summaries/<meeting>-<date>.md` when `store_summaries: full`; the source row goes to `## Sources` in `memory.md` either way (unless `store_summaries: none`); any term the transcript mangled goes to `glossary.md`; any recurring attendee goes to the shared `~/Clawic/data/contacts/contacts.md`; a recurring meeting's cadence goes to the `## Due` table; and if the meeting belongs to a tracked project, its decisions go to `~/Clawic/data/projects/<project>.md`. Formats and thresholds: `memory-template.md`.
