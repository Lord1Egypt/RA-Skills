# Feedback — Editing Someone Else's Draft, and Being Edited

Scope: prose that belongs to another person. The governing constraint is that it is not yours, and every rule here follows from that. Editing the user's own draft is `revision.md`.

**Before editing a third party's draft**, read `feedback_mode` and `edit_depth` from `config.yaml`, and the relevant `style-sheets/<context>.md` if the piece belongs to a publication or client. Editing to your own taste when a house style exists is the fastest way to have a whole pass rejected.

## The Three Severities

Sort every note into one of three tiers before writing any of them down. Mixing tiers is why editorial feedback gets read as an attack: ten comma notes next to one structural objection make the structural objection invisible.

| Tier | Definition | How to deliver |
|---|---|---|
| **Blocking** | Factually wrong, legally risky, misses the brief, or the argument does not hold | Stated first, separately, with the reason. Never buried in a list |
| **Substantive** | Structure, order, missing evidence, the wrong shape for the purpose | Grouped, with the fix named — "the third section belongs before the second, because..." |
| **Preference** | Word choice, rhythm, comma style, things you would have written differently | Marked as preference explicitly, or not raised at all |

The ratio is the message: if more than about a fifth of your notes are preference-tier, you are rewriting the piece in your own voice and should stop.

## Delivering It

`feedback_mode` decides the container:

- **`rewrite`** — hand back the corrected text. Fastest for the writer, and correct when the piece is the user's own or when they asked for the fix, not the diagnosis. Include one line naming what changed at the structural level.
- **`inline`** — margin notes on their text. Correct when the writer must stay the author, or when they will resubmit for approval. Never rewrite a sentence inside an inline comment without saying why.
- **`letter`** — an editorial letter: the piece's strengths in two lines, the blocking issues, the substantive ones grouped, and the preferences omitted. Correct for a long piece, a first-time collaborator, or anything where the relationship matters as much as the draft.

Rules for all three:
- **Lead with what works, once, specifically.** Not encouragement — orientation. The writer needs to know which parts not to touch, and a generic compliment does not tell them.
- **Name the problem, not the fix, for substantive notes.** "The reader does not know why this matters until page three" leaves the solution to the author; "move paragraph six up" makes them your typist.
- **Every note carries its reason.** A note with no reason is taste, and taste is not actionable.
- **One pass, one level.** Do not line-edit a draft whose structure you are also asking to change; the line edits will be deleted (`revision.md`).

## What You May Not Touch

- Their argument, unless it is wrong. Disagreeing with a claim is a note, not an edit.
- Their voice, in either direction. An editor's job is to make the piece more like itself, not more like the editor.
- Quotations, names, numbers, citations, code (SKILL.md Rule 7).
- Deliberate rule-breaking that is doing work: fragments for pace, a comma splice, a one-word paragraph.
- The user's stored `## Never` list applies to text you write, never to text someone else wrote. Do not "fix" another writer's usage to match your user's preferences.

## Receiving Edits, and Answering an Editor

- **Sort the notes into the same three tiers** before responding to any of them. Answering the preference notes first is how the blocking one gets lost.
- Accept every preference-tier note you do not have a reason to reject. Arguing about a serial comma costs the goodwill needed for the note that matters.
- Push back once, with a reason, on substantive notes you disagree with. Then accept the editor's call — they own the publication's relationship with its readers.
- **"Fixed" and "not fixed, here's why" are the only two answers.** Silence on a note is read as compliance and produces a second round.
- When a note is right about the symptom and wrong about the fix, say so and fix the symptom. Editors are almost always right that something is wrong there.
- A note you cannot understand is a note about a passage the reader cannot understand. Rewrite the passage rather than asking what the note meant.

## Beta Readers and Non-Professional Feedback

Non-editors report symptoms, not diagnoses, and the value is entirely in the symptoms.

- **Weight what they felt, discount what they prescribe.** "I got bored around the middle" is data; "you should add a subheading" is not.
- Two readers flagging the same place is a real problem even when they disagree about its cause. One reader's dislike is noise.
- Ask for the place, not the opinion: "where did you stop, or reread, or skim?" produces usable answers where "what did you think?" produces politeness.
- Never argue with a reader's experience. They cannot be wrong about what they felt, only about why.

## Reviewing Under Constraint

- **Legal or compliance review**: mark what must change and what merely could. Reviewers who mark everything get their whole review discounted.
- **Approval chains**: agree who has veto and who has an opinion, before the draft circulates. Undeclared vetoes appear at the last minute, every time.
- **Client review**: expect the intro to be rewritten and price the round in. Record who edits and what they always change in the client's `style-sheets/<context>.md` — after two rounds it is predictable, and pre-empting it saves the round.
- **Anonymous or blind review**: comment on the text, never on the author's inferred identity.

**After a review round**, write in the same turn: what this reviewer or client always changes to their `style-sheets/<context>.md`, so the next draft pre-empts it; the reviewer's register and channel preference to their row in `contacts.md`; and an editorial letter worth reusing as a shape to `artifacts/<kebab-name>.md` with its `## Boxes` line (`memory-template.md`). If the user was the one edited, every change they accepted goes to `## Corrections` with its trait — an accepted edit is a preference stated against a concrete alternative, which is the highest-signal voice data there is (`voice.md`).
