# Threads, Channels, and Tickets

Scope: email threads, Slack and Discord channels, support tickets, GitHub and Jira issues, forum topics, comment sections, and group chats. The defining property is that the source is a conversation with no author and no structure — the summary supplies both.

**Before summarizing an ongoing thread**, read `## Sources` in `~/Clawic/data/summarizer/memory.md` (or `sources.md` per the `## Boxes` index) for the last cut-off point, and `~/Clawic/data/contacts/contacts.md` for who the participants are. Re-summarizing a thread from message one every time is the standard waste in this genre.

**Contents:** [State the Cut-Off](#state-the-cut-off) · [Deduplicate Before Reading](#deduplicate-before-reading) · [Reorganize by Topic](#reorganize-by-topic) · [Who Is Blocked on Whom](#who-is-blocked-on-whom) · [Email Threads](#email-threads) · [Slack and Discord Channels](#slack-and-discord-channels) · [Support Tickets and Issues](#support-tickets-and-issues) · [Forums and Comment Sections](#forums-and-comment-sections) · [Tone and Escalation](#tone-and-escalation) · [Output Shapes](#output-shapes)

## State the Cut-Off

A conversation summary is stale on arrival unless it declares its boundary. Every output opens with `<N> messages, <first timestamp> to <last timestamp>` and, where the thread is live, `thread still active`.

Without it, a reader assumes the summary is current, acts on a conclusion that was superseded twenty minutes later, and blames the summary. With it, the reader knows exactly what they are acting on.

## Deduplicate Before Reading

Conversation exports are mostly duplicate text. Removing it first is what makes the real volume tractable.

| Duplicate | Where it comes from | Handling |
|---|---|---|
| Quoted reply chains | Every email carries the whole thread beneath it | Keep only the newest message's new text; the tail is a copy |
| Signature blocks and legal footers | Every message | Strip entirely |
| Auto-replies and delivery receipts | Out-of-office, read receipts | Strip, but note an out-of-office that explains a delay |
| Bot and integration messages | CI, deploy, alerting, calendar | Strip unless the thread is *about* them |
| Reactions and acknowledgements | "+1", "thanks", emoji | Strip, but count them: 9 people agreeing is a fact worth one line |
| Reposted links and screenshots | Same artifact shared repeatedly | Keep one reference |
| Cross-posted messages | Same text in two channels | Summarize once, note both venues |

A raw email thread routinely deduplicates to 20-30% of its byte count with zero information loss. Do this before measuring source length, or the compression ratio is computed against text you were going to delete anyway.

## Reorganize by Topic

Conversations arrive in chronological order and are almost never *about* one thing at a time. A chronological digest of a busy channel is unreadable and hides the point.

1. **Cluster messages into subjects** — a channel week is typically 3-8 real subjects with interleaved messages.
2. **Within each subject, report the resolution first**, then only the reasoning that survived.
3. **Order subjects by consequence to the reader**, not by message volume or recency.
4. **Chronology survives only where causality matters** — an incident thread, an escalation, a negotiation. There, a timestamped timeline is the right shape.

## Who Is Blocked on Whom

The highest-value output of a thread summary, and the one nobody writes.

- Every subject ends in exactly one of four states: **resolved**, **awaiting a named person**, **awaiting an external party**, or **dropped** (no message in the last N days and no resolution).
- "Awaiting" needs the name and what is awaited: `awaiting Priya — the revised quote`. Without the name it is not actionable.
- **Dropped threads are a finding.** A question asked eleven days ago with no reply is the item most worth surfacing, and it is invisible in a chronological read because nothing happened.
- Unanswered questions are collected separately from open decisions: a question needs an answer, a decision needs authority.

## Email Threads

- **Read bottom-up, write top-down.** The oldest message holds the cause; the newest holds the state. Summarizing in arrival order inverts causality.
- **Reply-all forks.** A thread frequently splits into branches with different recipient sets; participants in one branch do not know what happened in the other. Say so — it explains contradictions that otherwise look like people disagreeing.
- **Subject-line drift**: the subject stops describing the content within about three replies. Never take the topic from the subject line.
- **Attachments are referenced, not summarized**, unless the user asked; note version numbers in filenames, which is often where the real disagreement lives.
- **Forwarded threads** carry an internal commentary layer above an external one — keep the two apart, and be careful about which is quotable outside the company.
- **Recipients matter.** Who was added or dropped mid-thread changes what can be said; note additions of external addresses.

## Slack and Discord Channels

- **Threads within channels are separate conversations** even though the export interleaves them. Group by `thread_ts` or the equivalent before reading.
- **Edits and deletions**: exports may show the edited text only. If the summary depends on a message that was edited, say the message was edited.
- **Pinned messages and channel topic** are the closest thing to a source of truth; check them for decisions already recorded.
- **Reactions as a voting mechanism**: in many teams a ✅ or a thumbs-up *is* the approval. Count and report them as approvals when the team uses them that way — the user's convention goes in `config.yaml` under preference areas.
- **Direct-message content pasted into a channel summary** is a privacy decision, not a formatting one; keep it out unless the user asked for it.
- Channel digests are recurring by nature — the dedup-against-last-edition rules are in `recurring.md`.

## Support Tickets and Issues

| Element | What the summary carries |
|---|---|
| Reported symptom | The user's own words, once, verbatim |
| Environment | Version, platform, configuration — the facts that make it reproducible |
| Reproduction status | Reproduced / not reproduced / intermittent, and by whom |
| Root cause | Only if stated; a hypothesis stays labelled as one |
| Resolution | What was changed, and whether the reporter confirmed |
| Workaround | Separately from the fix — readers need it before the fix ships |
| Duplicates and linked issues | Counted; `12 duplicates` is a severity signal the individual ticket lacks |
| Current owner and state | Who has it now, and what they are waiting on |

Issue-tracker prose is noisy in a specific way: the first comment states the problem, the middle is triage, and the last comment states the outcome. Read first and last, then the middle only for the cause.

## Forums and Comment Sections

- **Weight by evidence, not by votes or by volume.** Score ranks agreement, not correctness; the accepted answer can be outdated while a low-scoring comment carries the current fix.
- **Date every technical claim.** In fast-moving domains, a highly-upvoted answer from four years ago is frequently wrong now. The summary carries the date beside the claim.
- **Report the distribution of positions with counts** rather than picking a consensus: `most replies recommend X; 3 report it failing on Y`.
- **Strip the meta-conversation** — moderation, off-topic argument, and complaints about the question — entirely.

## Tone and Escalation

Conversations carry a signal that documents do not, and it is easy to either drop or over-report.

- Report escalation as **observable behavior**, not as inferred emotion: "third follow-up in two days", "CC'd the VP", "asked for a call", "raised the contract". These are facts and they are decision-relevant.
- Do not characterize participants ("Priya was frustrated"). Report what they did.
- A **quiet** thread on an urgent subject is also a signal, and it is the one most often missed.

## Output Shapes

**Thread recap:**
```
<Thread subject> — <N> messages, <first> to <last>, <participants>. <"Still active" if applicable.>

State: <resolved | awaiting <name> for <what> | dropped since <date>>
What happened: <2-4 lines, cause first>
Decided: <if anything was>
Open questions: <question — asked by whom, unanswered since when>
Omitted: <if material>
```

**Channel digest** (multiple subjects; repeat editions dedup against the last one, `recurring.md`):
```
#<channel> — <period>, <N> messages across <M> subjects.

<Subject> — <state>. <one line resolution or blocker>
<Subject> — <state>. <one line>
Unanswered: <question> (<who>, <how long>)
```

**After summarizing a thread**, record the cut-off timestamp and message count in `## Sources` in `~/Clawic/data/summarizer/memory.md` so the next edition starts where this one stopped; write the recap to `summaries/<thread>-<date>.md` when `store_summaries: full`, with any credential, invite link, or token pasted in the conversation replaced by its `<kind>:<locator>` pointer; put recurring participants in the shared `~/Clawic/data/contacts/contacts.md` by name and key only; and if the thread carries decisions for a tracked project, add them to `~/Clawic/data/projects/<project>.md`. Formats and thresholds: `memory-template.md`.
