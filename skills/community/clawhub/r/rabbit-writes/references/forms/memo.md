# Form: memo

**Register:** `formal`

A form file supplies slots. Only the voice may fill them. Every quoted phrase in this file is under Tells, and every one of them is a phrase to avoid.

An internal document that announces a decision, or asks a named group to make one, and stays on the record. The distinguishing feature is not length or tone. It is that a memo is addressed to a group rather than a person and is expected to be findable six months later by somebody who was not in the room.

If it goes to one person and expects a reply in the thread, it is an email and `forms/email.md` applies. If it recommends rather than announces, and its audience has to be persuaded rather than informed, it is a proposal.

## Slots

- **Header block.** To, From, Date, Subject. Four lines, and the subject names the decision rather than the topic.
- **The decision, or the ask.** First, before any reasoning. A reader who stops after this paragraph must not act wrongly.
- **Why now.** What changed that makes this a decision rather than a standing state. A memo with no answer here is usually a memo that did not need writing.
- **What is being asked of whom, by when.** Named groups and dates, never a passive construction that leaves the actor out.
- **Risks or what we are not doing.** Optional, and the slot that earns the reader's trust in the rest.

Headers earn their place past roughly 400 words. Below that the four blocks above are the structure.

## Bands

| Purpose | Band |
|---|---|
| An announcement | under 300 words |
| A decision with reasoning | 300 to 800 words |
| A decision memo circulated for comment | no cap, and it earns headers and a date for responses |

## Tells

Phrases and shapes named here are the ones to avoid. Nothing in this file is a phrase to use.

- "As we move forward" and "going forward" as an opener.
- "This memo serves to inform you that."
- "It has been decided that." Somebody decided. Name them.
- "We appreciate your understanding" attached to a decision the reader had no say in.
- Background before the decision. The reader who needs context will read down for it. The reader who needs to act will not read down for the ask.
- A deadline with no owner, or an owner with no deadline.
- A subject line naming the topic and not the decision.

## What the mechanical layer sees here

The `formal` rung runs its extra-strict cells: promotional language, significance inflation, boilerplate clusters, future-narrative closers, and generic conclusions. All five are the failure modes of internal announcement prose, and a memo is the shortest document where an inflated claim reaches the most people.

Most memos sit near the reliability floor `scan.py` reports, so the stylometric numbers describe little. What still applies at full strength is the whole `safety` band and every P0 fingerprint, and in an internal document those matter more than in a public one: a memo is forwarded, and whatever is concealed in it travels.

The paragraph-length number is worth ignoring on a memo built from short blocks. Read the non-list prose separately before treating it as a defect.
