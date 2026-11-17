# Email and Chat — Messages That Get Answered

Scope: anything sent to a named person and expecting a response. Business documents sent as attachments are `workplace.md`; marketing sends are `copywriting`.

**Before writing to a named person**, read their row in `~/Clawic/data/contacts/contacts.md` — preferred channel, register, and what they cut or ignore. Read `## Formats` in `~/Clawic/data/writing/memory.md` for the user's own email habits. Writing to someone whose stored preference says "no greetings, ask in line 1" with three paragraphs of context is a visible failure.

**Contents:** [The Shape](#the-shape) · [Subject Lines](#subject-lines) · [Situations](#situations) · [Cold Outreach](#cold-outreach) · [Bad News](#bad-news) · [Saying No](#saying-no) · [Chasing](#chasing) · [Apologies](#apologies) · [Introductions](#introductions) · [Chat and Async Messages](#chat-and-async-messages) · [Before Sending](#before-sending)

## The Shape

Four lines, in this order, for almost every internal email:

```
The ask, with its deadline and owner.
The one line of context that makes the ask make sense.
Anything they need in order to answer (link, number, option list).
The easy out or the next step if the answer is no.
```

Rules that hold across every situation below:

- **One ask per email.** Two asks reliably get one answer, and it will be the easier one. A second ask is a second email, or a numbered list where each item has an owner.
- **The ask is a question with a deadline**, not a status report that implies a question. "Can you approve this by Thursday?" gets a reply; "Let me know your thoughts" does not.
- **Make the answer cheap.** A yes/no beats an open question; two options beat "what do you think"; a proposed time beats "when works for you".
- **Length is a cost you impose on the reader.** Internal: 50-150 words. Cold: 75-125. Anything over 200 words is a document with an email wrapper — attach it and put the ask in the body.
- **The reply-all decision belongs in the draft**: name who is on it and why. Adding a person mid-thread requires a line saying you did.

## Subject Lines

- Front-load the identifying noun. Inbox and list views truncate at a width that varies by client and device, so the first ~40 characters must let the reader place the thread without opening it.
- Name the action when there is one: `Approval needed by Thu: Q3 contractor budget` beats `Quick question`.
- `Re:` on a genuinely new topic is how a thread becomes unfindable. New topic, new subject.
- Never `Quick question`, `Touching base`, `Following up`, `Hi`, or an empty subject. All four are unsearchable in three months.
- A subject line that already contains the whole message can end with `[EOM]` and no body — the highest-efficiency email that exists, and it works only for one-line facts.

## Situations

| Situation | Move | Trap |
|---|---|---|
| Asking a favour | Name the specific thing, the effort involved, and the deadline; offer the easy out first | Vague "pick your brain" — unbounded effort gets declined by default |
| Asking a stranger for time | Say what you want, why them specifically, and how long | Flattery before the ask; it reads as a preamble to a bigger request |
| Declining | Decision first, one reason, no door left ajar (→ Saying No) | Softening until the reader thinks it is a maybe |
| Delivering bad news | The news, then the cause, then what happens next (→ Bad News) | Burying the news under context |
| Chasing a non-reply | Forward the original with one line; assume they missed it (→ Chasing) | Passive aggression, or a summary of your previous email |
| Correcting someone senior | Their frame, the specific fact, the consequence, their call | Hedging so hard the correction is invisible |
| Apologising | What happened, the impact, the fix, no excuse (→ Apologies) | Conditional apologies ("if anyone was affected") |
| Introducing two people | Double opt-in first; then why each cares, in one line each | Cc-ing both without asking either |
| Negotiating | State your number and its basis; never split the difference in the same message | Leading with flexibility |
| Handing over work | Current state, what is blocked, where things live, who to ask | A link dump with no state description |
| Resigning or ending a relationship | Short, factual, dated, no grievance | Explaining; the letter is a record, not a conversation |
| Anything else | Ask first, context second, easy out last | — |

## Cold Outreach

Structure: **specific fact about them → the one line of relevance → a yes/no ask → an easy out.**

- The first line must be something you could only write about *this* recipient. Anything reusable there reads as a mail merge and is deleted.
- One ask, and make it small: a yes/no, a 15-minute call, a single question. A cold email asking for an hour is an email asking to be ignored.
- The easy out ("if this isn't you, no reply needed") measurably reduces the cost of not answering, which is why it makes answering more likely.
- No attachments, no images, no tracking pixels in a first contact — all three raise the spam profile and none of them help.
- Follow up once, after roughly a week, by forwarding the original with one line. A second follow-up on a cold thread is a cost with no return.
- The version that works becomes `artifacts/cold-intro-email.md` with the parts that change in `[brackets]`.

## Bad News

Order: **the news → the cause in one line → what happens next → what you need from them.**

- The news goes in the first sentence and the subject line. Delaying it does not soften it; it adds the discovery that you delayed it.
- One cause, stated plainly, without the chain of contributing factors. The chain reads as excuse-building.
- Never use the passive to hide the actor ("a decision was made"). If it was your decision, say so; the passive is read correctly by everyone.
- No apology unless you are at fault, and then a real one (→ Apologies). Sympathy is not an apology and mixing them makes both hollow.
- Name what you are doing about it before naming what you need from them.

## Saying No

- The decision comes first, in the first line. Everything after it is read as either explanation or an opening to negotiate.
- One reason, and a true one. Multiple reasons invite the reader to defeat them one at a time.
- Do not offer an alternative you do not want to be held to. "Maybe later in the year" becomes a diary entry in their calendar.
- The relationship-preserving move is speed, not softness: a fast clear no is a kindness; a slow ambiguous no wastes their planning.
- If the no is not yours to make, say whose it is and when they will decide.

## Chasing

- First chase: forward the original thread with one line — "Bumping this; still need an answer on X by Thursday." No summary, no reproach; the original is right there.
- Assume it was missed, not ignored, until the third attempt. It usually was.
- Escalate by changing channel, not by changing tone: email → chat → call. Each channel change is one attempt, and three attempts is the point at which you loop in whoever owns the decision.
- Give the consequence of continued silence as a fact, not a threat: "If I don't hear by Friday I'll proceed with option B" is information the reader can act on.
- Never `Just following up` as a subject or an opening. It says nothing and marks the sender as someone who sends filler.

## Apologies

Four parts, in order, no extra parts: **what happened · the impact on them · what you are doing · when.**

- "I'm sorry that you feel" and "if anyone was inconvenienced" are not apologies and are read as evasions.
- Do not explain unless they asked. The explanation reads as mitigation and dilutes the apology.
- One apology, once. Repeating it in the same message makes the reader manage your feelings.
- Apologise for the thing that actually cost them something, not the smallest defensible version of it.

## Introductions

- Double opt-in always: ask each side privately, with one line on who the other is and what they want. Cc-ing two strangers together imposes work on both.
- The intro message: one line on each person, one line on why now, then get out of the thread explicitly ("moving myself to bcc").
- Say what you want the outcome to be. An intro with no purpose becomes two people politely wasting a call.

## Chat and Async Messages

- **The whole ask in one message.** A standalone "hi" makes the other person wait while you type, and it is the single most-complained-about chat habit in every organisation.
- One message, not seven. Thread replies rather than firing consecutive lines into a channel.
- Ask in the channel, not the DM, when the answer is useful to others — the archive is the point.
- @-mentions are interrupts. Name one person when you need one answer; @here and @channel need a reason you could defend.
- A decision made in chat does not exist. Post the outcome as a summary message, and write it to `~/Clawic/data/projects/<project>.md` (`memory-template.md`).
- Do not write anything in chat you would not want quoted with the timestamp attached. Every chat log is discoverable.

## Before Sending

- Recipient list correct, and every `Cc` justified. Check the auto-completed address against the name you meant — wrong-recipient sends are the most common serious email error.
- The attachment is actually attached, and it is the right version.
- Every `[Name]`, `[Company]` and template placeholder replaced.
- The ask, its date, and its owner are all present and in the first screen.
- Names and titles spelled correctly, checked against `contacts.md`.
- No forwarded thread below carrying something the new recipient should not see. Trim the quoted history deliberately.

**After the exchange**, write in the same turn: a register or channel preference learned about the person to their row in `contacts.md` (`Context` cell, never a second row); a template that worked to `artifacts/<kebab-name>.md` with its `## Boxes` line; and any rule the user stated about their own email habits to `## Formats` in `memory.md`.
