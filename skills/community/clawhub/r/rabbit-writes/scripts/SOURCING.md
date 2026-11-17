# ste_lexicon.json v2 — sourcing notes

Everything in this folder is scratch, per project convention: nothing here is
tracked or wired into the skill. It exists so a human can review before any
of it is promoted to `skills/rabbit-writes/scripts/ste_lexicon.json`.

## What was done

1. Downloaded the official PDF: `ASD-STE100_ISSUE9.pdf` (3.3 MB, HTTP 200
   from asd-ste100.org).
2. Normalized it two ways with `pdftotext`:
   - `ste100-issue9.txt` — plain flow, via `rabbit-reads`'
     `scripts/extract_text.py` (also ran the concealed-text/injection scan
     that ships with it: one P2 finding, a false positive — the standard's
     own dictionary examples are written as imperative, all-caps commands,
     which is what an "instruction addressed to an agent" pattern matches
     on. Not a real injection).
   - `ste100-issue9-layout.txt` — `pdftotext -layout`, which keeps the
     dictionary's four-column table spatially aligned instead of flattening
     it column-by-column. This is the file the dictionary parser reads;
     plain-flow extraction interleaves table cells in an order that isn't
     row order and can't be recovered reliably.
3. Read Part 1 (Writing rules, sections 1–9, rules 1.1–9.4) directly and
   pulled exact rule text for every fact now cited by rule number in
   `ste_lexicon.json`.
4. Wrote `parse_dictionary.py` to walk the `-layout` text and reconstruct
   Part 2 (the alphabetical dictionary) into `{word, pos, approved,
   meaning_or_alternatives}` records. Output: `ste_dictionary_full.json`,
   2062 of the 2149 entries the standard's own introduction states it
   carries (875 approved, 1274 not approved). The parser is a best-effort
   table reconstruction over flattened PDF text, not a guaranteed-complete
   one — see its own file header and the `_limitations` note in
   `ste_dictionary_full.json` for what's known to be imperfect (word-wrap
   hyphenation across lines, multi-sense entries whose sub-senses can blur
   together). Every specific ruling cited in `ste_lexicon.json` was
   additionally spot-checked by grepping the source text directly, not
   just trusted from the parser's output.

## What changed from the previous version, and why

**`phrasal_verbs` was rewritten, not just corrected.** The previous version
shipped ~555 generic English phrasal-verb entries (`"zone out": "relax"`,
`"wedge in": "insert"`, `"trickle down": "spread gradually"`, and so on).
None of these strings exist anywhere in the Issue 9 PDF — checked directly
by grep, not inferred. Worse, the standard says outright that this shape of
data (a phrasal-verb lookup table) isn't how STE handles phrasal verbs at
all: Rule 9.3's own text reads *"You will not usually find phrasal verbs
listed as 'not approved' in the dictionary... Only a small number of
phrasal verbs (for example, 'put on' and 'come on') are approved in the
dictionary."* The rule is a productive-grammar constraint (don't let two
approved words combine into an unintended third meaning), not a banned-word
list. `phrasal_verbs` now carries the rule's own two worked examples (`put
out` → `extinguish`, `give off` → `release`) and its three named approved
exceptions (`PUT ON`, `COME ON`, `GO OFF`), each verified against the
dictionary body.

**`delete` was wrong in a specific, checkable way.** The previous version
called `delete` an approved "technical verb" under Rule 1.12 with no
tension noted. The dictionary itself lists `delete (v)` as *not* approved
(alternatives: `ERASE (v)`, `REMOVE (v)`). Rule 1.12 *does* list `delete`
by name, but in its "Computer processes and applications" technical-verb
category — and that same rule states the resolution order explicitly: use
an approved dictionary verb when one accurately covers the instruction, and
treat the technical verb as a fallback only when none does. Both facts are
now recorded, with the priority the rule itself gives.

**`run`, `execute`, `display`, `render`, `present`, `check`/`verify`/
`confirm`/`ensure` → `make sure that`, `acceptable` → `permitted`,
`however` → `but`, `therefore` → `thus`, `any` → delete/restructure** — all
matched the previous version's claims and are now cited with their exact
dictionary line, rather than asserted.

**`complete_adjective` was incomplete.** Previous version: `"completed"`
only. The dictionary's `complete (adj)` entry actually gives three separate
approved alternatives for three separate senses — `FULL (adj)`, `ALL
(adj)`, `COMPLETED (adj)` — and picking the wrong one changes the sentence.
All three are now recorded with which sense each covers.

**`since_as_conjunction`, `have_to`, `need_to`** were checked and are
correct in spirit but now cite the actual dictionary text: `SINCE (conj)`
is approved for its *time* sense and banned only for the causal sense
(`because`); `have to (v)` isn't approved and the dictionary's own note
says to use the imperative form, not a word swap; `need to` has no
dictionary entry at all (only bare `need (v)` does, → `NECESSARY (adj)`).

**Added, not present before:**
- `verb_forms_allowed` and `verb_construction_bans` — Rule 3.2's six
  allowed forms and Rule 3.4's two auxiliary-verb ban shapes, each with the
  rule's own examples. The old file had `approved_modals`/`banned_modals`
  but nothing about *why*, or about the perfect-tense/passive-auxiliary
  construction ban, which is the more common real-world violation.
- `technical_verb_categories` — Rule 1.12's full "Computer processes and
  applications" list (input/output, UI/application, system operations),
  which is the single most software-relevant paragraph in the entire
  standard and wasn't represented at all before.
- `punctuation_and_word_count` — the actual numeric limits (20 words/
  sentence procedural, 25 descriptive, 6 sentences/paragraph, no
  semicolon, hyphenated-group and parenthetical word-counting rules,
  contraction ban), each tied to its rule number. Previously there was no
  structured data at all for section 8 or the sentence-length caps in
  sections 5/6.
- `modal_notes` / `banned_modal_replacements` — the `COULD`-inside-`CAN`'s-
  own-paradigm nuance, and the fact that `might` has no dictionary entry at
  all (it's banned only by the "not in the dictionary" default, not by an
  explicit ruling — worth knowing if someone later asks "where does it say
  might is banned").

**Unchanged, not from the standard:** the `ai_slop` block. It was never
claimed as STE-sourced (its own `_comment` says so), so it carries over
as-is.

## What's still open

- `ste_dictionary_full.json` covers 2062 of 2149 stated entries (~96%).
  The gap is concentrated in multi-sense entries and hyphen-wrapped words;
  see its own `_limitations` field. Closing it further means hand-editing
  `parse_dictionary.py`'s continuation-line heuristics against specific
  failure cases, which wasn't done here — the ~96% that did extract
  cleanly is enough to ground every claim `ste_lexicon.json` actually
  makes, and every one of those claims was independently grepped against
  the source text rather than trusted from the parser alone.

## The bulk vocabulary promotion (ste_lexicon.json v4)

`ste_dictionary_full.json` and this file are no longer scratch. Both are
tracked, and the ~96% of the dictionary that extracts cleanly is now the
source for `ste_lexicon.json`'s `dictionary_vocabulary` block: a
word-to-approved-alternative mapping generated by `scripts/ste-research/`
(three stages — extract, corpus-evidence, merge — mirroring
`scripts/thesaurus-research/`'s shape) and checked into `ste_lexicon.json`
itself.

Extraction is anchored on the dictionary's own `ALTERNATIVE (pos)` marker,
never on "the first run of capital letters": the `meaning_or_alternatives`
field interleaves two PDF table columns word-for-word, and only the POS tag
reliably separates the ruling from the example text after it. That is 1,188
of the 1,283 not-approved entries (92.6%); the rest have a bare-phrase
alternative with no tag ("NOT EASY", "AT THE SAME TIME") and no reliable
delimiter, and are reported skipped rather than guessed at.

Corpus calibration matters more here than it did for the hand-picked
sections above: ASD-STE100 is an aerospace maintenance-manual standard, and
a word it bans for that register ("ability", "any", "run") is ordinary
software-README vocabulary. `docs/ste-research/candidates.json` carries the
evidence — every candidate's hit count against the 100-README corpus — and
a word appearing in 5 or more of the 100 READMEs is excluded as
corpus-common rather than shipped as a violation. Two calibration passes
were needed before the evidence was honest: the first used a plain `\b`
word boundary and measured "cross" as rare, when the shipped check
(`rwlib.ste.dictionary_vocab_regex`, hyphen-aware like `word_regex`) does
not match "cross" inside "cross-platform" at all; the first also counted
raw README text instead of the `apply_exemptions`-blanked copy scan.py
actually feeds every STE check, and counted a `mask=circle` image-crop URL
parameter as two ordinary-English hits. Both fixed by importing the real
regex and the real exemption pass into `02_corpus_evidence.py` rather than
approximating either. 719 words shipped after calibration, out of 1,090
extracted; 8 more were already covered by a hand-cited section above
(`run`, `insert`, and similar) and were excluded to avoid a document
scoring the same word twice under two different findings.

Regenerate with `python3 scripts/ste-research/01_extract_candidates.py &&
python3 scripts/ste-research/02_corpus_evidence.py && python3
scripts/ste-research/03_merge_accepted.py`, from the repo root. Rerunning
with no change to the dictionary or the corpus is idempotent: the merge
only bumps `ste_lexicon.json`'s version when the vocabulary content
actually differs from what is already there.
