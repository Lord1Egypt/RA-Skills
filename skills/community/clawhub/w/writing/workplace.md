# Workplace Documents — Memos, Proposals, Updates, Reviews

Scope: documents written inside an organisation, where the reader is busy, senior, or both, and the document is a decision instrument rather than a piece of prose. Emails are `emails.md`; technical documentation is `documentation`.

**Before writing into an ongoing project**, read `~/Clawic/data/projects/<project>.md` — its goal, status, milestones and prior decisions. A status update that contradicts a decision recorded there, or an announcement that repeats a milestone already reported, is the visible symptom of not reading it. Read `contacts.md` for anyone named as an approver or owner.

**Contents:** [The Rule for Every Document Here](#the-rule-for-every-document-here) · [Memo](#memo) · [Proposal](#proposal) · [Executive Summary](#executive-summary) · [Status Update](#status-update) · [Announcement](#announcement) · [Incident and Postmortem Comms](#incident-and-postmortem-comms) · [Performance Review and Feedback](#performance-review-and-feedback) · [Meeting Notes and Decision Records](#meeting-notes-and-decision-records) · [Handover](#handover)

## The Rule for Every Document Here

**A reader who stops after the first paragraph must act correctly.** Everything else in this file is that rule applied to a document type. Senior readers read the first paragraph, skim the headings, and read the section that touches their area. A document that requires linear reading is a document that will be misread.

Three consequences:
- The recommendation, decision or headline number goes first. Reasoning is support, and support comes after the thing it supports.
- Every section must be skippable without changing what the reader does.
- The document names its owner and its date at the top. Undated documents circulate for years.

## Memo

One page, roughly 500 words, BLUF shape.

```
Recommendation      one sentence, with the decision being asked for
Why                 the two or three reasons, strongest first
What was rejected   the alternatives and the specific reason each lost
Cost and risk       the number, and the thing most likely to go wrong
Next step           who does what, by when
```

- The alternatives section is what makes a memo credible. A memo with one option is an announcement pretending to be a decision document.
- Name the decision being requested explicitly: approve, fund, choose between A and B, or note. Readers cannot supply this and will supply the wrong one.
- Numbers carry their unit and their basis. "Saves 40%" is unusable; "saves ~18k EUR/year, from the 2026 run rate" is a claim someone can check.
- Appendices exist so the body can stay one page. Anything a reader might want but most will not goes there.

## Proposal

For external or cross-team work where money or scope is at stake.

- **Open in their words.** The problem statement should be recognisable to the person who described it, using their vocabulary. A proposal that reframes the problem in your terms in paragraph one reads as a pitch for something they did not ask for.
- **Scope names exclusions.** What is *not* included prevents the argument that otherwise happens at delivery. This is the highest-value paragraph in the document.
- **Price with its unit and its assumptions** — what the number depends on, and what changes it.
- **Risk section, honest.** The one that names a real risk and how it is handled beats the one that claims none.
- **Assumptions, listed.** Every assumption that, if false, changes the price or the timeline.
- Timeline in dates, not durations. "Six weeks" starts whenever; "by 14 September, assuming a kick-off by 4 August" is a commitment on both sides.

## Executive Summary

150-300 words, and it must stand alone with the deck or report deleted.

SCQA shape (Minto): situation the reader agrees with → the complication that changed → the question that raises → the answer.

- Write it last, from the finished document. Written first, it summarises what you intended rather than what you found.
- The answer goes in the first two sentences. A summary that summarises the *structure* of the report ("this report examines...") is worthless.
- Numbers in the summary must match the body exactly. This is where mismatches get discovered, in front of the audience.

## Status Update

100-200 words. Same shape every time — the value is in comparability across weeks.

```
Shipped     what changed since the last update, in outcomes not activities
Blocked     what is stuck, who unblocks it, and by when it becomes a problem
Next        what happens before the next update
Ask         one thing you need, or "nothing"
```

- **Outcomes, not activity.** "Attended three meetings on the migration" is activity; "migration plan agreed, starts Monday" is an outcome. Nobody can act on activity.
- Bad news arrives in the update it happened in, not the one after. A slip reported late costs more trust than the slip.
- A blocked item with no named owner is not blocked, it is abandoned.
- Consistency of shape beats completeness: an update that changes format every week cannot be read diagonally.

## Announcement

- The change, the date it takes effect, and what the reader must do — in the first three lines.
- Then who it affects, and explicitly who it does not. Half the replies to any announcement are "does this apply to me".
- Then the reason, in one paragraph. Reasons after the change are read; reasons before it delay the change and get skipped.
- Then where questions go, naming a person or a channel.
- No enthusiasm the audience does not share. "We're excited to announce" ahead of bad news is read as contempt.

## Incident and Postmortem Comms

Two different documents, often confused:

**During** — the status page or the channel update. Every update carries: what is affected, what is not, what is being done, and when the next update comes. Give the next-update time even when there is nothing new; the silence is what escalates.

**After** — the postmortem. Timeline with timestamps, impact quantified, root cause, contributing factors, and actions with owners and dates.

- Blameless means naming systems and decisions, not people. "The deploy skipped the check" not "X skipped the check".
- Quantify impact in the reader's units: minutes of downtime, requests failed, customers affected, money.
- "Human error" is not a root cause; it is where the analysis stopped. Ask what made the error possible and easy.
- Actions without an owner and a date are a wish list, and everyone reading knows it.

## Performance Review and Feedback

- **Behaviour, impact, then the ask.** "In the March review you rewrote the spec twice after sign-off (behaviour); the release slipped a week and two teams re-planned (impact); freeze the spec at sign-off and raise changes as a separate decision (ask)."
- Specific and dated beats general. Feedback with no example is unactionable and is heard as a personality judgement.
- Never sandwich. The praise-criticism-praise pattern is transparent, and it teaches the reader to discount praise.
- Separate the assessment from the development plan; mixing them means neither is read properly.
- Write nothing you would not say in the room. These documents are read by more people, and for longer, than the writer expects.

## Meeting Notes and Decision Records

- Notes record **decisions and actions**, not discussion. A transcript is not notes and nobody reads it.
- Format: decision, who decided, date; then actions with owner and date; then, briefly, options rejected and why.
- Post them within the day, in the place the team looks, and name anyone with an action.
- **A decision recorded nowhere did not happen.** It will be re-made, differently, within a quarter — which is why the decision goes into `~/Clawic/data/projects/<project>.md`, not only into the notes.

## Handover

The document written when work changes hands. It exists for the person who will have a question at a bad moment.

- Current state: what is done, what is in flight, what is stalled and why.
- Where things live: repositories, documents, accounts, credentials as *pointers only* (`env:`, `1password:`, never the value).
- Who to ask: names and what each person owns, cross-referenced to `contacts.md`.
- Known traps: the things that are not written down anywhere else. This is the whole value of the document.
- Open decisions with the context needed to make them.

**After the session**, write in the same turn: a decision, milestone or status change to `~/Clawic/data/projects/<project>.md` (never duplicating a person record — the person goes to `contacts.md` and is named here); a document format the organisation requires to `style-sheets/<context>.md`; and a memo, brief, handover or postmortem that will be re-read to `artifacts/<kebab-name>.md` with its `## Boxes` line (`memory-template.md`).
