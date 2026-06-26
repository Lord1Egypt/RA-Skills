# Sources of Meaning, Attention Policies, and Card Format

## What a source of meaning is

A way of living that the user finds intrinsically meaningful — not just
something they prefer or enjoy. More specific than words like "honesty"
or "authenticity"; it specifies a particular *kind* of honesty or
authenticity through what they pay attention to.

A source of meaning opens a space of possibility rather than satisfying a
preference. It's constitutive of what the user thinks a good life is —
not instrumental to some other goal.

## Attention policies — the format

Each policy is a precise thing the user can actively orient their
attention toward, not an abstract value or an outcome. The policies are
written in the user's voice (first person), as instructions to themselves
about what to notice. Format:

> **PLURAL_NOUN** + qualifier phrase

The all-caps plural noun names the kind of thing to attend to ("MOMENTS",
"SENSATIONS", "OPPORTUNITIES", "CHOICES", "PEOPLE"). The qualifier provides
the specifics.

Example, for a value about group decision-making:

```
- CHANGES in people when entrusted with the work of self-determination
- INSIGHTS that emerge through grappling with morally fraught questions
- CAPACITIES that develop when a person tries to be free and self-directed
- WISDOM that emerges in a discursive, responsible context
```

### Rules for attention policies

1. **Constitutive, not instrumental.** Every policy must be something the
   user would attend to because *attending to it is part of living well*,
   not because it serves a separate goal. A driver tracking "DRIFTS of the
   car toward the lane line" is instrumental — they care about not
   crashing, full stop. "SENSATIONS in my body that tell me whether I'm
   following what I actually believe" is constitutive — attending to that
   just *is* part of what a good life is for this person. If unsure, ask
   the user: "if there were another way to get the underlying goal, would
   you still attend to this?" If they'd drop it, it's instrumental. If
   they'd keep attending to it anyway, it's constitutive.

   Other examples:
   - Constitutive: "MOMENTS when someone drops their professional persona"
   - Instrumental: "LEADS ACQUIRED at a networking event"
   - Constitutive: "FEELINGS of capacity in my body after a meal"
   - Instrumental: "MEALS with a low calorie count"

   A source of meaning whose policies are mostly instrumental is not a
   source of meaning — it's a strategy. Push back gently and re-ask.
2. **Precise, not vague.** Someone should be able to actively look for
   the thing. Good: "tension in someone's voice", "the rhythm of
   conversation", "instincts I'm tempted to override". Too vague: "the
   energy in a room", "moments of alignment", "presence" (present to
   what?), "connection" (connected how?).
3. **From the actor's perspective.** Read like instructions the user
   gives themselves about what to notice. "SENSATIONS that point to
   misgivings I have about the current path."
4. **General words.** "strangers" not "customers". "objects" not "trees".
5. **No "meaningful" or synonyms ("deep", "profound").** Say more
   specifically what's worth attending to.
6. **Together they cohere.** 3-6 policies that fit as a single way of
   distinguishing quality in a domain — not a grab bag.

## What goes in the card

- **title** — 2-5 words. Not cheesy. Distinguishes this from similar
  cards the user might already have. Check `cards/` for collisions
  before finalizing.
- **tags** — 2-4 kebab-case shorthand tags for filtering
  (e.g. `intellectuality`, `conversation`, `parenting`).
- **story** — one sentence in the user's voice. First person, present
  continuous. Describes the exact moment that felt meaningful — not the
  resulting feeling ("...which made me feel deeply connected" — don't do
  this). No names or sensitive PII; replace with "my mom", "my friend",
  etc. Example: "Watching my mom lean over and kiss my dad on the
  forehead, beaming love and gratitude."
- **where this shows up** — concrete, recognizable situations where this
  value comes up for the user. Sentences, bullets, whatever fits. Don't
  force a count or form. E.g. "In heated dinner conversations, or late
  at night when a friend is half-formed about an idea."
- **what this is** — 2-4 paragraphs of prose explicating the value, so a
  future reader (the user later, another agent in a deliberation) can
  understand it without having been in the elicitation. Grounded in the
  story and the policies; every claim traces back. Defensive against
  likely misreadings — if "tending the quiet" could be confused with
  sentimentality, name that and rule it out. No abstract or ideological
  language; no "I value X" framings. **Don't show this prose in chat.**
  Write it into the card; the user can read it there if they want to.
- **what I pay attention to** — 3-6 attention policies in the user's
  voice, formatted per the rules above.
- **what gets in the way** — lightly cleaned-up version of the blocker
  the user named. Don't editorialize; record what they said. Form is
  whatever fits — a sentence, a few bullets, etc.

## Card template

Save to `$AGENT_VALUES_DIR/cards/<slug>.md` (or
`~/.openclaw/values/cards/<slug>.md` if unset).

```markdown
---
title: <Title>
elicited_at: <YYYY-MM-DD>
tags: [<kebab-case>, <kebab-case>]
---

## Story

<one-sentence first-person present-continuous moment>

## Where this shows up

<sentences or bullets — concrete situations>

## What this is

<2-4 paragraphs of explication>

## What I pay attention to

- <PLURAL_NOUN qualifier>
- <PLURAL_NOUN qualifier>

## What gets in the way

<the blocker, in whatever form fits>
```
