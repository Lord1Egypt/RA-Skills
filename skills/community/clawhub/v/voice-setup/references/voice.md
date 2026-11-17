# Voice

> "Taste is boundaries." — Ruben Hassid, *I am just a text file*

Models do not lack taste. They lack *specific* taste. Given no constraints, they produce the statistical average, which is the same mechanism that generates every pattern in `patterns.md`. The fix is not a better adjective in a prompt. It is a durable file describing one person's refusals.

**Roughly 80% of a good voice profile is what the writer will not do.** Preferences are easy to state and weak in effect. Refusals are specific, checkable, and rare, which is what makes them a fingerprint.

---

## The precedence rule

A user-supplied writing sample or voice profile **outranks every style rule in this skill**, including the em-dash guidance in `patterns.md` §49.

If the sample uses em dashes, keep them at roughly the sample's frequency. If the writer says "stuff" and "things", keep that register rather than upgrading their vocabulary. If they open three paragraphs with "So," and it is characteristic, leave it.

Matching the author always beats scrubbing the tell.

---

## Using a sample

When the user pastes their own previous writing:

1. **Read the sample before touching the draft.** Note sentence-length pattern, contraction rate, paragraph openings, punctuation habits, recurring phrases, transitions, and level of polish.
2. **Check the sample for contamination.** If the sample itself carries P0 fingerprints, the writer may have pasted AI-assisted work. Say so, ask, and exclude those patterns from what you replicate. Never inherit a tell into a profile.
3. **Match the habits, do not just delete tells.** Regularizing a deliberate quirk is a failure even when it scores clean.
4. Run `python3 scripts/scan.py sample.md --json` to get the writer's actual burstiness, type-token ratio, sentence-length distribution, and em-dash rate. Those become the targets for the rewrite, replacing this skill's defaults.

---

## Building a profile

Ask the questions below and write the answers to a markdown file the user owns, outside this skill. One file, read first, portable across tools.

Inside the `rabbit-writes` plugin this is already built: profiles live in `../rabbit-writes/voices/`, `voices/ACTIVE` names the current one, and the `voice-setup` skill runs the interview and writes both files. Use that instead of hand-rolling. The rest of this section is the underlying method, and it applies wherever the profile ends up.

Weight the interview toward sections 3, 5, and 6. Those carry the signal.

### 1. Beliefs
- What do you believe about your subject that most people in your field do not?
- What argument do you find yourself making repeatedly?
- What do you refuse to pretend to be uncertain about?

### 2. Mechanics
- Contractions: always, never, or by register?
- Sentence length: what does your natural range look like?
- Do you use em dashes, semicolons, parentheses, the Oxford comma? Answer honestly rather than correctly.
- Paragraph length. Do you write one-sentence paragraphs?
- Headings: sentence case, title case, or none?
- First person: I, we, you, or absent?

### 3. Aesthetic crimes *(weight this heavily)*
- What words make you close a tab?
- What openings do you refuse to write?
- What endings? (Kickers? Summaries? Calls to action?)
- What formatting do you consider a tell of a bad writer?
- Name three phrases you would never use even if they were accurate.

### 4. Voice
- Who do you sound like when you are writing well?
- Who do you sound like when you are writing badly?
- How much do you hedge? What does hedging look like when you do it on purpose?
- Do you use humor? What kind, and where does it go?
- Profanity: yes, no, sparingly?

### 5. Structure
- Do you lead with the conclusion or build to it?
- Do you use examples, analogies, data, or anecdote as your default evidence?
- How do you transition? (Explicit connectives, white space, or nothing?)
- How long is a piece before you split it?

### 6. Hard nos *(weight this heavily)*
- What claims will you not make?
- What tone will you not adopt, even for a client?
- What would embarrass you to publish under your name?
- What would a reader who knows you notice immediately as not-you?

### 7. Red flags
- When a draft of yours goes wrong, how does it go wrong?
- What is your most common self-edit?
- What do you always cut on a second pass?

### Profile shape

```markdown
# Voice: <name>

## Dimensions
formality: 0.3        # 0 casual, 1 formal
confidence: 0.8       # 0 hedging, 1 assertive
warmth: 0.5           # 0 clinical, 1 friendly
energy: 0.4           # 0 measured, 1 enthusiastic
complexity: 0.6       # 0 simple, 1 sophisticated

## Measured from samples
avg_sentence_words: 17
sentence_length_sd: 9
burstiness: 0.68
type_token_ratio: 0.58
em_dashes_per_1000w: 4
contraction_rate: high

## Never
- <the aesthetic crimes, verbatim>
- <the hard nos>

## Always
- <the mechanics and structural defaults>

## Signature moves
- <the two or three things a reader would recognize>

## Authenticity markers
- acknowledges uncertainty: yes/no
- shows tradeoffs: yes/no
- uses specific numbers: yes/no
- names constraints: yes/no

## Known contamination
- <tells found in the source samples, excluded from replication>
```

---

## The fingerprint, and the distance to it

Everything above is a rule a document either breaks or does not. A draft can clear every one of them, break no ban, use no em dash, stay under the paragraph cap, and still sound like nobody. That gap is the whole reason this engine is not just a linter, and until now nothing measured it.

The fingerprint is the measurement. `measure_voice.py` builds it from the same samples the profile came from and writes it beside the profile:

```bash
python3 skills/voice-setup/scripts/measure_voice.py a.md b.md c.md \
  --name <voice> --write-fingerprint
```

That gives a profile three files instead of two: `<name>.md` for what a person reads, `<name>.rules.json` for what a regex enforces, and `<name>.fingerprint.json` for what a distance measures. `scan.py --voice <name>` finds the third automatically and reports the distance.

**What it measures.** Function-word rates, z-scored against the writer's baseline and averaged, which is Burrows' Delta, the standard authorship-attribution distance. Function words on purpose: content words are about the topic, and a voice has to survive a change of topic. "also" against "additionally", the contraction rate, how often a sentence opens with "but". That is the connective tissue where a generic register creeps back in, and it is exactly what no ban list reaches.

**What makes the number readable.** The fingerprint carries its own calibration: each sample's distance to a fingerprint built from the other samples. A raw Delta means nothing on its own. "0.97, where this writer's own pieces sit within 0.61 of each other" is a claim somebody can act on.

| verdict | reading |
|---|---|
| `in_range` | at or under the writer's own band. Indistinguishable from another sample of theirs by this measure |
| `near` | under 1.5x the band. Drifting. Read the contributors |
| `out_of_range` | past that. This does not sound like the profile's owner |

**What it is not.** It is a P2 signal and it is never enforced. A writer is allowed to sound unlike themselves on purpose, and the measure cannot tell that from a conversion that did not land. It is also not an authorship verdict, for every reason `references/false-positives.md` gives. Under 250 words it is reported with the number and no finding, because below that the rates are sampling noise.

**The half that says what to change.** Every reported distance names the markers responsible, with the direction and both rates:

```
voice-distance   Register distance 0.97, this writer's own samples sit under 0.61
                 Furthest markers: furthermore +16.4sd, therefore +16.4sd, however +9.2sd
```

That is what a conversion pass reads. A bare distance says a document is wrong and not what to change.

**Use it as the attainment check, and there is a script for that.** `attain.py` takes both documents and does the whole comparison:

```bash
python3 skills/rabbit-writes/scripts/attain.py before.md after.md --voice <name>
```

It reports the distance both ways and each of the six measures with its gap in the writer's own sample sd, signed, because "10 sd under the profile" and "10 sd over it" call for opposite edits. Five verdicts, and only two of them mean somebody did something wrong:

| verdict | reading |
|---|---|
| `landed` | the register moved, not only the punctuation |
| `partial` | some of it arrived. Each missed measure is a rewrite target |
| `flat` | the distance barely moved and no measure moved a full sd. Mechanics fixed, register untouched |
| `regressed` | something moved away from the profile |
| `unpaired` | one document, so this says where it sits and not whether an edit landed |

`flat` is what the script exists for: a pass that fixed eleven mechanical hits and moved the distance from 0.97 to 0.95 changed the punctuation and not the voice, and every rule passed, so no rule-by-rule report can see it. `--check` exits 1 on `flat` and `regressed` and never on `missed`, because a measure the document cannot reach without inventing content is guardrail 1 working rather than a defect.

**And the other direction.** `voice-caricature` fires when a document is *more* characteristic than the writer's own samples: two measures past the range their own pieces cover, in the direction they already lean away from everybody else. That is the overshoot this file's own warning is about, wearing this writer's clothes instead of a generic humanizer's. It is P2, never enforced, and it means read the samples again and ask whether this is a piece they would write or the profile turned up.

The naive form of that rule does not work and the number is worth knowing: "any measure outside the sample min-max" fires on 95.5% of held-out documents by the same writer at three samples. `rwlib/stylometry.py` carries the four qualifications that bring it to 0.1%, each with the measurement that put it there.

**The shape targets, for the pass before the rewrite.** `attain.py --plan` turns the stored sentence distribution into a per-paragraph band: "five sentences, at least one under 9 words, at least one over 29, median around 16". That is a constraint a rewrite can hold and a later run can check, and it is the replacement for "vary your sentences", which is a weak instruction and survives every vocabulary fix because it is not a constraint at all. It is a band and never a script. A sampled list of exact per-sentence word counts is unhittable, and chasing one manufactures the cadence `references/false-positives.md` calls a new fingerprint rather than the absence of one.

**Exemplars.** `--with-exemplars` embeds the writer's own paragraphs in the fingerprint, and `stylometry.nearest_exemplars` returns the three closest in register and shape to whatever is being rewritten. A profile describes and an exemplar demonstrates. Opt in, because it copies somebody's prose into a file that then travels with the plugin, so ask them first.

---

## Blending

A blend has two halves, and only one of them is a script.

**The rules file is mechanical.** `python3 scripts/rwlib/voices.py --blend a b --weight 0.7` prints the blended rules on stdout and its conflicts on stderr. Bans union, so the stricter refusal wins, because refusals are the part that has to hold. Every mechanic with a stricter side takes it whatever the weight says: a blend that can drop a refusal is a blend nobody can rely on, and the weight is a statement about emphasis rather than permission. The lineage is written into the file as a `blend` key.

The weight only breaks genuine ties, where one profile wants `require` and the other `forbid`, or one writes `dmy` and the other `mdy`. Those are reported by name, because silently picking one writer's date format out of two is a choice the person whose name goes on the profile has to see.

**The markdown is not.** The dimensions are the part people mean when they say blending: `0.7 × technical.formality + 0.3 × casual.formality`. Nothing reads those numbers. They sit in a fenced block in the profile markdown as instructions to a writer, and no threshold in this engine is derived from them, so interpolating them is authoring work you do by hand. Structural defaults come from the highest-weighted profile the same way.

Do both. A blended rules file on its own enforces punctuation and describes nobody.

---

## Authenticity markers

Sterile is as detectable as slop. But personality is genre-gated: apply this to essays, posts, opinion, and personal writing. For encyclopedic, technical, legal, or reference text, **neutral and plain is the correct human voice.** Do not inject opinions or first person there.

Where voice belongs, the marks of a real writer are:

- acknowledged uncertainty and unresolved tension
- stated tradeoffs, including ones that cut against the argument
- specific numbers, dates, and names
- named constraints ("we had two weeks and one engineer")
- an aside the writer could defend
- one thought left unfinished

**And the hard limit:** none of these may be *added* to text that did not have them. If the source has no `I`, the rewrite has no `I`. If the source has no anecdote, do not write one. You may not add stance, personality, or fact.

The limit is on content, not on form. Reordering, splitting, merging, and rewriting sentences are all allowed, and in a voice conversion they are the work. The test is whether you can point at the sentence in the source that carries the claim, the stance, or the feeling. If you can, reshaping it is fair. If you cannot, you added it.

That constraint is what separates restoring a voice from installing one.
