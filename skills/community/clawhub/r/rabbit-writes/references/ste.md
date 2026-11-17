# ASD-STE100 Simplified Technical English

> ASD-STE100 Issue 9 (2025-01-15), the aerospace controlled-language standard.
> Used in aircraft maintenance, procedure writing, and regulatory
> documentation since 1983.

All findings are **report-only**: every `ste-*` id is P1 or P2, so `--check`
still gates on P0 alone, and nothing here is mechanically fixed. The rewrite
(splitting long sentences, reordering conditions) is a judgment call, and
usually a language model task.

## Default and advisory

The layer runs in two bands, and only one of them is opt-in.

**Mechanical, on in every scan.** Five checks that count something: the two
sentence caps, the paragraph cap, the condition order, and the semicolon.
A count is a measurement rather than an opinion, which is the whole reason
they run by default. `MECHANICAL_IDS` in `rwlib/ste.py` is the list.

**Advisory, behind `--ste`.** Six checks driven by a word list: the modals,
the -ing openers, the banned verbs, the phrasal verbs, the passive, and the
`ai_slop` vocabulary. All P2. A word list is a judgment about vocabulary,
and the aerospace judgment is not everybody's.

```bash
python3 scan.py doc.md              # the mechanical five
python3 scan.py doc.md --ste        # the mechanical five plus the advisory six
python3 scan.py doc.md --no-ste     # neither
```

Register tolerances apply to the mechanical band the way they apply to
everything else, and they are the reason a default-on band is bearable:
`chat`, `informal` and `linkedin` skip all five, `academic` skips the
descriptive cap on the evidence of its own corpus, and the rest carry
measured allowances.
`scripts/registers.json` holds the numbers and where each came from. The
advisory band carries no cells, because a tolerance on a rule nobody sees
by default is a number nothing calibrates.

The checks run over the same exempted copy every other band reads. Fenced
code, inline code spans, and quoted examples are never flagged, and a
semicolon inside a code block is not a finding (running with `--no-exempt`
disables all markup blanking across the engine, in which case raw text is
scored). They also run ahead of the
suppression pass, so a `rabbit-allow` comment reaches them like any other
finding.

The vocabulary lives in `scripts/ste_lexicon.json`, rebuilt from the official
Issue 9 PDF: the dictionary table was parsed programmatically and every claim
in the file that cites a rule number or a dictionary ruling was checked back
against the extracted text. The file's own `_comment` fields carry the
provenance.

## Text classification

Before the sentence-length rule applies, each paragraph classifies itself:

| Class | Indicators | Sentence limit |
|---|---|---|
| **Procedural** | Steps, instructions, imperatives, "how to", numbered lists | 20 words (Rule 5.1) |
| **Descriptive** | Explanations, definitions, "the system does X", overview sections | 25 words (Rule 6.3) |

`--ste-mode procedural` or `--ste-mode descriptive` forces the limit for the
whole document. The limits themselves are data, read from the lexicon's
`punctuation_and_word_count` block, because Rules 5.1 and 6.3 carry the
numbers and a second copy in code is a second calibration.

The other checks apply in both modes: the two STE text types disagree about
sentence length and about nothing else this layer checks.

## What is checked

### 1. Sentence length

Procedural text: max 20 words. Descriptive text: max 25 words. Numbers,
numbers with units, abbreviations, and code spans each count as one word
(Rule 8.6), and hyphenated groups count as one (Rule 8.7).

```
# Violation
Run the deployment script which installs all dependencies and sets up the environment and configures the service for you.

# Compliant
Run the deployment script. It installs all dependencies. It sets up the environment.
```

### 2. Approved modal verbs only

Allowed: `can`, `will`, `must`. Banned: `should`, `would`, `may`, `might`,
`could`, `shall`.

Two of the rulings are worth knowing exactly. `could` sits inside `CAN`'s
own verb-form group and the same dictionary entry then bans it for showing
possibility. And `might` has no dictionary entry at all: it is
banned by the unlisted-word default, not by an explicit ruling.

The month is not the modal: "Released in May 2026" and "May 5" stand down,
"You may restart it" fires.

```
# Violation
You should verify that the config is loaded.

# Compliant
Make sure that the config is loaded.
```

### 3. No -ing verb after a comma

STE bans -ing forms as clause openers. This catches the common
"..., making it easy to..." pattern. Gerunds as nouns are fine:
"Running the script is safe."

```
# Violation
Install the package, making it available globally.

# Compliant
Install the package. It is then available globally.
```

### 4. Condition before command

Required conditions come before the action (`if`, `when`, `unless`). The
check fires only on imperatives: a declarative sentence that happens to carry
a command verb mid-sentence is not a command, and a condition that opens the
next sentence is not this sentence's trailing clause.

```
# Violation
Do X if Y is true.

# Compliant
If Y is true, do X.
```

### 5. Banned verbs

`check`, `verify`, `confirm`, and `ensure` are all ruled `MAKE SURE (v)` in
the Part 2 dictionary. Replace with "make sure that" (verify a state),
"examine" (look for faults), or "measure" (get a value).

### 6. Phrasal verbs

Rule 9.3 is a productive-grammar constraint, not a word list: do not combine
two approved words into a phrase whose meaning is not the approved meaning of
its parts. The standard says outright that phrasal verbs are not usually
listed in the dictionary, so there is no lookup table to enforce. The scanner
flags exactly the rule's own worked examples ("put out" for extinguish,
"give off" for release) and stands down for its named approved exceptions
(`PUT ON`, `COME ON`, `GO OFF`, each restricted to one sense). The general
constraint is left to the writer, because that is where the standard leaves
it.

### 7. Passive voice

STE prefers active voice (and Rule 3.4 bans the auxiliary constructions that
produce most passives). Rewrite with `you`, `we`, or the actor as subject.
P2, advisory: adjectival participles and passives read the same to a regex.

```
# Violation
The configuration is loaded by the system.

# Compliant
The system loads the configuration.
```

### 8. Semicolons

Rule 8.1: all standard punctuation except the semicolon. Write two sentences
instead. The `;` closing an HTML entity is markup and does not count.

### 9. Paragraph length

Rule 6.6: six sentences to a paragraph, and three in a procedure. The check
counts prose blocks only. A ten-item bullet list is ten sentences by the
splitter and is also Rule 6.6's own answer to a long paragraph, so flagging
it would report the fix as the problem. `is_prose_block` decides, the same
notion of a paragraph the rest of the engine uses.

```
# Violation
One paragraph carrying seven or more sentences of explanation.

# Compliant
Two paragraphs, or a vertical list where the sentences are steps.
```

### 10. Vocabulary

The `ai_slop` block flags AI-overused words and filler ("simply", "leverage",
"in order to", "it's important to"). This block is deliberately outside the
standard: the words are not in the ASD dictionary, and the file's own
comment says where they came from.

## What is data but not checked

Three lexicon tables are reference material for a writer or a model prompt,
and no checker reads them. Each says so in its own `_comment`:

- `banned_words_software`: the dictionary rulings for `run`, `execute`,
  `display`, `render`, `present`, `destroy`, `drop`, and the `delete`
  priority order (the dictionary bans it for `erase`/`remove`, Rule 1.12
  lists it as a technical-verb fallback, and the rule itself resolves the
  tension: the approved verb wins when it fits).
- `technical_verb_categories`: Rule 1.12's "Computer processes and
  applications" verb list, the most software-relevant paragraph in the
  standard. A technical verb is legal only when no approved dictionary verb
  covers the same instruction.
- `recurring_errors`: verified Part 2 rulings for the words writers get
  wrong most (`however` to `but`, `therefore` to `thus`, `perform` to `do`,
  the three senses of `complete`). Several need sense discrimination no
  regex can do, which is why the table informs a rewrite rather than a
  check.

Rules the standard carries that this layer does not check: the six allowed
verb forms and the perfect-tense ban (Rules 3.2 and 3.4, partially visible
through the passive check), the one-word-one-meaning principle, and the
contraction ban (Rule 4.2). If a check for one of these lands, it lands in
`rwlib/ste.py` with a test and a corpus number, not in this file first.

## Voice priority

A voice profile outranks this layer, because the profile is a ruling about
one person's prose and the standard is a default. Three mechanics decide,
and `scan.py` applies them where it applies `double_hyphen` (`rwlib/voices.py`
holds the vocabulary):

| Mechanic | Effect |
|---|---|
| `semicolon` (either value) | `ste-no-punctuation` stands down. `allow` is the writer's own sentence shape, and `forbid` already reports every occurrence as `voice-semicolon` at the profile's own priority. |
| `max_paragraph_sentences` | `ste-paragraph-sentences` stands down. The profile's cap raises `voice-paragraph-length` on the same block. |
| `max_sentence_words` | Replaces the 20 and 25 word caps outright, in both directions. The finding id still follows classification, and the label prints the number in force. |

The satoshi profile is the worked example. His whitepaper raises 30 sentence
findings against the STE caps and 8 against his own measured p95 of 35 words,
which are the sentences long by his standards rather than by aerospace ones.

## Suppression

STE findings suppress the same way as every other finding, with the
engine's own comment syntax:

```
<!-- rabbit-allow: ste-sentence-procedural (spec quote, kept verbatim) -->
```

The comment must name the finding id and carry a reason in parentheses. See
`rwlib/suppress.py` for the mechanism, including why the safety band refuses
it.

## Finding IDs

| ID | Band | Priority | Description |
|---|---|---|---|
| `ste-sentence-procedural` | mechanical | P1 | Procedural sentence over 20 words |
| `ste-sentence-descriptive` | mechanical | P1 | Descriptive sentence over 25 words |
| `ste-paragraph-sentences` | mechanical | P1 | Prose paragraph over six sentences |
| `ste-condition-order` | mechanical | P1 | Condition after command verb |
| `ste-no-punctuation` | mechanical | P2 | Semicolon used |
| `ste-modal` | advisory | P2 | Banned modal verb |
| `ste-ing-verb` | advisory | P2 | -ing verb after comma |
| `ste-banned-verb` | advisory | P2 | Banned verb used as verb |
| `ste-phrasal-verb` | advisory | P2 | A phrasal verb Rule 9.3 itself names |
| `ste-passive` | advisory | P2 | Passive voice construction |
| `ste-vocab` | advisory | P2 | AI-overused vocabulary item |

The semicolon is P2 in a band of P1s because a ban on one punctuation mark
is a style stance rather than a count of anything. Every advisory id is P2
for the same reason, one level down from where they shipped.

The ids and priorities live in `STE_PRIORITIES` in `rwlib/ste.py`, and
`STE_FINDING_IDS` derives from it, so the two cannot disagree. The
`suppression-*` ids belong to `rwlib/lexicon.py` and are deliberately not
restated there.

## Official standard

ASD-STE100 Simplified Technical English, Issue 9 (2025-01-15),
[asd-ste100.org](https://asd-ste100.org), free download. The shipped lexicon
was built from that PDF directly.

## Sources and references

- [ASD-STE100 official specification](https://asd-ste100.org): the
  authoritative standard, and the source the shipped lexicon was parsed
  from.
- [AminBlg/SimpleEnglish](https://github.com/AminBlg/SimpleEnglish): an
  agent skill that applies ASD-STE100 to LLM-generated documentation, and
  the inspiration for this layer. It uses a 53-rule agent-driven approach
  against this module's deterministic scanner, and its
  [`word-swaps.md`](https://github.com/AminBlg/SimpleEnglish/blob/main/skills/simple-english/references/word-swaps.md)
  is the source of the `ai_slop` block.
