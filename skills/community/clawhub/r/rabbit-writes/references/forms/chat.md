# Form: chat

**Register:** `chat`

A form file supplies slots. Only the voice may fill them. Every quoted phrase in this file is under Tells, and every one of them is a phrase to avoid.

Covers a DM, a Slack or Discord message, a text, an issue comment, and a reply on a comment site. One form, because they behave the same way: the reader is mid-conversation, the thread carries the context, and the message is one turn in it rather than a document.

## Slots

Mostly a list of what is not here.

- **No greeting slot.** The thread is the greeting. A greeting on turn six of a conversation reads as the start of a new one.
- **No closer slot.** Same reason. Some voices keep a sign-off in a DM and most do not, and that is the voice's call rather than this file's.
- **No signature.** Ever.
- **Body.** One thought. If there are two, that is two messages.

Break at thought boundaries, not at length. A long message that is genuinely one thought is fine, and three thoughts crammed into one paragraph is the thing the wall-of-text rule is about, which is why that rule runs at full strength in this register and is skipped in most of the others.

## Bands

| Purpose | Band |
|---|---|
| An answer | as long as the answer, usually one or two sentences |
| A question | one sentence, and the context that makes it answerable |
| A status note | under 60 words |
| Anything past about 150 words | it wanted to be an email or a document. Say so and send that instead |

That last row is a real rule and not a joke. A long chat message is a document with no subject line, no structure, and no way for the reader to find it again next week.

## Tells

Phrases and shapes named here are the ones to avoid. Nothing in this file is a phrase to use.

- "Hope you're doing well!" opening a message inside a live thread.
- "Great question!" and every acknowledgment that acknowledges nothing.
- "Let me know if you have any questions" closing a two-line message.
- Bullets and bold in a message under 60 words. Structure at that length is decoration.
- A numbered list of three items where a sentence with two commas says the same thing.
- Perfect punctuation and full capitalization from a person who writes neither. See the note below.

## What the mechanical layer sees here

Say this out loud in any report on a chat message: the mechanical layer is nearly blind here. Almost every message is under the reliability floor `scan.py` reports, so the stylometrics describe a sample too small to mean anything, and the tolerance matrix skips most of the craft rules in this register on purpose. Judgment carries essentially the whole load.

Two things still run at full strength and both matter. The `safety` band, because a concealed instruction pasted into a comment is exactly the vector that band exists for. And the P0 fingerprints, because a tracking parameter or a chat citation marker in a message is evidence about how it was written no matter how short it is.

Typos and lowercase are not defects in this form. `references/false-positives.md` says why, and it is the only place that says it: do not correct them, and do not read them as a signal about who wrote the message.
