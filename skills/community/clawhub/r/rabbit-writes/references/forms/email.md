# Form: email

**Register:** `formal`

A form file supplies slots. Only the voice may fill them. Every quoted phrase in this file is under Tells, and every one of them is a phrase to avoid.

That register is the default for anything leaving the organization. A thread with a peer sits at `informal`, and a one-line answer to a one-line question sits at `chat`. Move the rung, never the slots: an email keeps its skeleton at every level of formality, and what changes is what goes in each slot and how much of it.

## Slots

In order. A slot the voice has nothing for stays plain or stays empty, and an empty slot is a real answer rather than a gap to fill.

- **Subject.** One line, no terminal punctuation, and it is the BLUF. If the reader acts on the subject alone and never opens the body, they should act correctly. A subject naming the topic rather than the ask has failed at the one thing it does.
- **Greeting.** One line. It is true or it is absent. There is no third option, and an untrue warm-up reads as sarcasm.
- **Body.** The conclusion, then the evidence under it. The subject already carried the BLUF, so the first body line is the ask or the decision, not a restatement of the subject.
- **Closer.** One line, from the voice. Not present in every voice.
- **Signature.** Whatever the voice defines, and nothing the voice does not.

Headers do not belong in the body unless the email is long enough that a reader would scroll past something. Below the band in the next section, they are always wrong.

## Bands

Length by purpose, measured on the body alone.

| Purpose | Band |
|---|---|
| A request, one ask | under 150 words |
| An answer to a question | as long as the answer, and no longer |
| A status update | under 250 words, or it wanted to be a document |
| A decision memo | no cap, and it earns headers |

Threading has its own rule. Answering several questions at once, quote each question and put the answer under it. Prose that answers three questions in one paragraph forces the reader to reconstruct which answer went with which question, and they will get one wrong.

## Tells

Phrases and shapes named here are the ones to avoid. Nothing in this file is a phrase to use.

- "I hope this email finds you well" and every variant. It is a greeting slot filled by a machine.
- "I wanted to reach out", "just circling back", "per my last email".
- "Please don't hesitate to reach out with any questions."
- Headers, bullets, or bold in an email under 150 words. The structure costs more attention than it saves at that length.
- A five-paragraph essay structure in a reply: an intro paragraph restating the question, three supporting paragraphs, a conclusion restating the intro.
- A closing paragraph that summarizes what the email just said. In a document that is a conclusion. In an email it is the same text twice.
- An apology as an opener when nothing needs apologizing for.
- A subject line naming the topic and not the ask: "Q3 planning" where the body asks for a headcount decision by Friday.

## What the mechanical layer sees here

Most email lands under the reliability floor that `scan.py` reports, so the stylometrics describe very little and the judgment above carries the load. The mechanical layer still catches everything in the `safety` and `fingerprint` bands at full strength, and those are the ones that matter in correspondence: a tracking parameter pasted into a link, or a chat citation marker left in a quoted block, is evidence about how the mail was written and it reaches the recipient.

At `formal` the tolerance matrix runs the extra-strict cells (promotional language, significance inflation, boilerplate clusters, future-narrative closers, generic conclusions). That is the rung doing its job: one inflated claim in an email to a client undermines everything measured beside it.
