# Voice: <name>

> Copy this file to `voices/<yourname>.md`, fill it in, delete the guidance in
> angle brackets, then `echo "<yourname>" > voices/ACTIVE`.
>
> Or invoke the `voice-setup` skill and let it interview you.
>
> **Only put things here that would be wrong for someone else.** "Avoid passive
> voice" and "cut filler" belong to the engine and apply to everyone. If a rule
> is true of good writing generally, leave it out. A profile that restates the
> engine drifts out of sync with it.
>
> Weight this file toward the Hard nos. Taste is boundaries, and roughly 80% of
> a working profile is refusals. Preferences are easy to state and weak in
> effect. Refusals are specific, checkable, and rare, which is what makes them a
> fingerprint.

## The three essentials (if you forget everything else)

<Three rules you would keep if you could keep only three. Write them as
instructions to an editor, not as adjectives about yourself. "Lead with the
conclusion, then the evidence" is usable. "I'm direct" is not.>

1.
2.
3.

## Voice in one line

<The ratio or tension that defines your register, plus its failure mode. Naming
the failure mode is the useful half: "80% substance, 20% warmth, and the failure
is dropping the 20% and reading as cold.">

## Dimensions

```
formality: 0.5        # 0 casual, 1 formal
confidence: 0.5       # 0 hedging, 1 assertive
warmth: 0.5           # 0 clinical, 1 friendly
energy: 0.5           # 0 measured, 1 enthusiastic
complexity: 0.5       # 0 simple, 1 sophisticated
```

## Measured from samples

<Fill these from `scan.py --json` run on three or four things you actually
wrote. What people believe about their writing and what the numbers say differ
more often than not. Delete the section if you have no samples yet.>

```
avg_sentence_words:
sentence_length_sd:
burstiness:
mattr:
em_dashes_per_1000w:
contraction_rate:
```

---

## Structure

<How you organize. Where the conclusion goes. When you use headers, bullets,
numbered steps. How you handle attachments, multiple questions, and instructions.
How you transition between paragraphs.>

## Delivering hard news

<Your actual procedure. What softens, what never softens, and where the line
between blunt and cruel sits for you.>

---

## Mechanics

**Sentences:** <Length, rhythm, what happens to them under emotion.>

**Punctuation:** <Em dashes, semicolons, Oxford comma, ellipses, exclamation
points. Answer honestly rather than correctly. If you use em dashes, say so and
the engine will stop stripping them.>

**Formatting:** <Paragraph length. Line breaks. Bold and italic. Signature block.>

**Connectors:** <Which joining words you reach for, and which read wrong to you.>

**Certainty:** <Your vocabulary for degrees of confidence, and what you do when
you don't know something.>

**Numbers and dates:** <Precision expectations. Date format.>

**Openers:** <How you start. What makes an opener false rather than warm.>

**Closers:** <Sign-offs by register, verbatim.>

**Owning mistakes:** <The exact shape of your correction.>

---

## Tone and warmth

<How warmth actually shows up in your writing, with an example sentence. Most
people's warmth tool is not what they expect it to be.>

## Register

<How you shift by audience, channel, seniority, and whether you're on the clock.
Which markers appear in one register and never in another.>

<Then fill the table below, which is the per-form half. `references/forms/` says
what slots a form has and never what goes in them, because a form file that
supplied a greeting would open every user's email the same way. This table is
where you fill them, and it is the only place that may. Leave a cell blank and
the slot stays plain, which is a real answer.>

| Register | Opener | Closer | What else changes |
|---|---|---|---|
| `chat` | | | |
| `informal` | | | |
| `blog` | | | |
| `formal` | | | |

<The genre columns take a row only if you write them differently.
`scripts/registers.json` names them and most people do not need them all.>

The enforceable half of this section goes in `<name>.rules.json`, in two keys
that already exist: `mechanics_by_register` for a mechanic that moves by
register, and `applies_to_registers` on a `banned_regex` or `required_when`
entry for a rule that only applies to some. A register cannot soften a rule you
wrote. It selects among the rules you wrote, which runs the other way.

## Humor

<Kind, target, and the conditions under which it stays spoken rather than
written.>

---

## Hard nos

<The heaviest section. Words, phrases, moves, tones, and claims you will not
write. Be specific enough that a script could check some of them, then put those
in `<name>.rules.json`.>

- What words make you close a tab?
- What openings do you refuse to write?
- What endings?
- What claims will you not make?
- What tone will you not adopt, even for a client?
- What would a reader who knows you spot immediately as not-you?

## Signature moves

<Two or three things a reader would recognize as yours. Optional, and easy to
overdo: an editor that installs these on every draft has installed a tic, not a
voice.>

---

## Modes

<If you write differently for different purposes, name each mode and say what
"good" means inside it.>

## The final check

<The question you ask yourself before sending.>

---

## Quick reference card

<Nothing new goes here. It is the sheet to keep open while drafting, and every
line on it should be argued for somewhere above. See the same section in
`whit3rabbit.md` for a filled-in one.>

- **Always:** <Extracted from answers — core habits to follow>
- **Never:** <Extracted from answers — specific things to avoid>
- **Signature Phrases & Structures:** <Actual examples provided during interview/samples>
- **Litmus Test:** "Does this sound like something I would actually write — or does it sound like an AI trying very hard to imitate me?"

---

## Anti-overfitting guide

<Which rules above are absolute and which are tendencies. Worth filling in: a
profile whose rules all read as equally binding is one an editor will apply
equally, and the result is a caricature. `whit3rabbit.md` has a worked one.>

- **Spirit Over Letter:** Internalize the author's taste, don't mechanically force every pattern into one piece.
- **Frequency Guidance:**
  - **HARD RULE:** Never violate (mostly in Hard nos / JSON bans).
  - **STRONG TENDENCY:** Do this 70–80% of the time, breaking occasionally is fine.
  - **LIGHT PREFERENCE:** Nice to have when context fits.
- **What Matters Most:**
  1. Single most important belief about writing:
  2. The primary pattern that makes this voice unique:
  3. The #1 thing never to do:
