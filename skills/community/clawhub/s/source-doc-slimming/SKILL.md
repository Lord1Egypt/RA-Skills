---
name: source-doc-slimming
description: "Slim down an oversized \"always-read\" source document — a single source of truth, a registry, a config, a published skill/README, or a rule document — without deleting any content. Use when a file that must be read under time pressure has grown so large that its load-bearing parts get skimmed past, when a review or incident concludes that something important was missed because of file volume, when a document accretes a new section after every incident, or when someone sets a size target for a file and you need to check whether that target is arithmetically reachable. Moves long narrative, chronology and incident history into a companion file, leaves an operating spine plus pointers inline, adds a shape guard so the file cannot silently re-inflate, and proves the move was lossless by replaying the original text line-by-line against the companion. Do not use for ordinary editing or for trimming prose that is genuinely dead."
description_zh: "把过大的「必读」源文件瘦身——叙事外置 + 留脊柱 + 守形状 + 逐行零丢失证明"
description_en: "Slim an oversized always-read source doc without losing content"
disable: false
agent_created: true
version: "1.0.0"
---

# Source-document slimming

Split an over-large "always-read" file into an operating spine plus a companion reference, and **prove nothing
was lost**. The problem this solves is not disk space: it is that a file read under time pressure gets skimmed
*by topic*, so a load-bearing caveat goes unread while every automated check stays green.

## When to use

- A source-of-truth / registry / config / rule document has grown large enough that readers skim it.
- A post-mortem concludes something was missed **because of volume** ("因体量挑读").
- A document accretes one new section per incident and shows no sign of stopping.
- A size target has been proposed for such a file ("get it under N KB") — verify it before working to it.

Do **not** use this for ordinary prose editing, for dead text, or when nothing is under time pressure.

## Steps

### 1. Reconnaissance — three read-only measurements, before proposing anything

```bash
python scripts/slim.py breakdown <file>          # section sizes in UTF-8 bytes
python scripts/slim.py coupling <root> "<regex>" # who references the parts you intend to move
```

Then answer explicitly, in writing:

- **What does code actually read?** Grep the readers (validators, tests, loaders) for the exact keys/sections you
  plan to move. Count hits per key. **Zero hits on a key is the licence to move it.**
- **What is the arithmetic floor?** Sum the blocks that readers depend on. If that sum already exceeds the
  proposed target, **the target is impossible — say so with the number** instead of under-delivering.
- **Is the coupling zero?** If nothing automated references the parts being moved, the change cannot break a
  pipeline. If something does, stop and sequence it differently.

### 2. Run the keep/move test on every block

The test is **"is it still binding?"**, not **"does it look historical?"**

| Keep in the file | Move to the companion |
|---|---|
| Operative values and rule definitions | Chronology / append-only version history |
| Any record carrying a **currently binding condition** (a gate to be re-checked, a split governing the next action) | Resolution narratives, incident write-ups, superseded values |
| The decision procedure: lookup tables, step lists, the detection formulas | Corollaries, worked examples, the "why this rule exists" |

A record that *looks* chronological but states a live precondition stays. Moving it recreates the incident.

### 3. Move the text **verbatim**, then write the spine

Move whole blocks byte-for-byte into the companion. Do not paraphrase while moving. Then write the inline
spine by hand — a digest, not a copy:

- the step list / lookup table / detection formulas a reader needs to act;
- the short list of things a green check does **not** tell you;
- a pointer line naming the companion.

Then declare the direction explicitly, in both files:

> The table above is a **digest**, re-derived from `companion.md`, which is **authoritative**. If the two ever
> diverge, the companion wins and this digest is regenerated from it.

Without that sentence the split itself violates the "one writable copy" rule it is meant to uphold.

### 4. Give future appends a single write path

If the companion is now where new history goes, add one small helper that appends **and** updates the pointer's
count in the source (e.g. `changelog_ref` / `changelog_count`). Otherwise the next dated script will append back
into the source and quietly undo the work.

### 5. Add a shape guard, and wire it into the existing gate

Guard **shape**, not just size:

- FAIL if a moved-away key reappears in the source;
- FAIL if the serialization round-trip drifts (a reformat buries a three-line change in a three-thousand-line diff);
- FAIL if a required operative field is missing;
- FAIL if the pointer count disagrees with the companion;
- WARN / FAIL at byte thresholds **derived from the measured floor**, not from a round number.

Register it as a step in whatever gate the project already runs, so it is not "only mentioned in prose".

### 6. Prove it losslessly

```bash
python scripts/slim.py verify <pre_migration_copy> <companion_file> \
    --start "## 12. Section Heading" --end "## Next Heading"
```

Repeat per moved section. Exits non-zero if any non-empty line of the original did not land in the companion.

Then assert the retained side too: every operative field byte-identical to the pre-migration copy, and the
source's remaining key set correct.

### 7. Merging two divergent copies of one document

A document published in several forms (`SKILL.md` + `README.md` + `README_zh.md`) has usually drifted. Merge
before externalising, and merge deliberately:

- **Normalise aliases first.** A release written `v1.5` in one file and `v1.5.x` in another is **one** row. Without
  an alias table the merge reproduces the very duplicate you set out to remove.
- **Fix the language; never pick "the longest".** Byte-longest silently mixes languages row by row, because CJK
  runs ~1.4 bytes/char and therefore always wins. Decide the companion's language, prefer that source's wording,
  and use the others only to fill gaps.
- **Reuse the other language's wording verbatim** for rows that will still be shown in that language. Never
  re-translate a line that is already published elsewhere.
- **Log every superseded paraphrase** to a durable place rather than dropping it silently.
- **Mark holes; never invent.** An entry with an empty summary gets `*(not recorded in any source file)*`; a
  version range with no rows keeps the gap. Two entries that plausibly describe one release but **cannot be
  proven to** stay separate with a note — a wrong merge is unrecoverable, a visible duplicate is not.
- **Declare the direction** exactly as in step 3: companion authoritative, every other copy an abridged digest.

## Pitfalls

- **`len(str)` is characters, not bytes.** Chinese-dense text runs ~1.4 bytes/char. Mixing the two produces
  self-contradictory percentages (a section reported as both 46% and 17.5% of the same file). Always
  `len(s.encode('utf-8'))`.
- **Anchors must be taken from the file, not from memory.** Read the exact line back with `repr()` before
  building a search-and-replace anchor — invisible indentation differences (6 spaces vs 7) silently produce
  zero matches. Assert `text.count(anchor) == 1` and **abort the whole batch** on mismatch.
- **A backup helper must tolerate a file that does not exist yet**, or creating a new companion file crashes on
  `shutil.copy2`. Guard with `os.path.exists`.
- **Never leave `.bak` files inside a published / archived directory.** They get packaged or mirrored and then
  report as drift. Park them in the project's scratch dir.
- **Same file, multiple edits: serialise them.** Either one edit per turn, or one script doing
  read → all replacements → single write. Parallel edits to one file silently drop all but the last.
- **Never `| head` / `| tail` / `| sed`** in this environment's shell; the tools are missing and the pipeline
  still exits 0, so failures are invisible. Do output shaping in Python via `subprocess(capture_output=True)`.
- **Do not move the last operative copy of a live condition.** If a block states a precondition that still
  applies, its *long-form rationale* moves but the **condition stays**.
- **Splitting is not the same as hitting a size target.** If the floor is above the target, report the
  arithmetic and propose a revised target rather than gutting the source.
- **Your verification script is code, and it has bugs too.** Three false alarms in a single session, each
  reported FAIL on a file that was correct:
  a `\b` boundary after a numbered heading also matches its children (`### 7.7` matched `### 7.7.1`) — anchor
  headings with a trailing space or end-of-line; counting a **substring** matches twice inside one line
  (`|------` occurs twice in `|---------|------|-------------|`) — compare whole stripped lines, never substrings;
  a section slice that runs to end-of-string absorbs the trailing separator *and* the next section's blurb,
  inflating the measured size — slice between explicit boundaries; and the one that misleads hardest, a
  **wrong expectation set** — a comparator that assumed the shipped package excluded `X` and included `Y`
  reported FAIL on a byte-perfect package, because both assumptions were backwards. Derive the expected set
  from the **authoritative side** (the remote's own file list), never from what you believe you shipped.
- **Put assertions before the write, or split the run.** An assertion after the write leaves the file modified
  *and* raises a traceback, so no one can tell whether the write was good. Write-then-verify is fine only if the
  verify step is a separate, re-runnable script.
- **Re-derive any anchor that failed once.** A paragraph containing an internal newline will never match a
  hand-typed single-line anchor. Slice it out with `text.index(start)` → `text.index(end_marker)` instead of
  reconstructing it from what the text looked like when printed.
- **`%` and `{}` are hostile in generated text.** Escape `%` as `%%` in `%`-format strings, and prefer
  `.replace()` over `.format()` when the content legitimately contains braces.
- **Never infer what a platform sidecar means from local cross-comparison.** A sidecar that disagrees with its
  local source of truth reads like a stale "last publish" record, and comparing it across many sibling projects
  appears to confirm that — but that is still local-only evidence, and in this project it was **wrong**. One
  read-only query against the authority settled it in seconds and reversed the conclusion: the sidecar was a
  snapshot frozen months earlier, not a publish record at all. If a remote exists, query the remote; do not
  adjudicate a platform's semantics from the files it left on disk.
- **A sidecar sitting next to a project directory may be published with it.** Do not assume bookkeeping files
  are excluded — read the published artifact's own file list. A stale sidecar that was not even valid JSON rode
  into a public package this way, while a different file (the one everyone expected to be dropped) was the one
  actually excluded.
- **Do not repair a defect found in a platform-generated artifact when the repair destroys the evidence.**
  Hand-fixing the symptom makes the next check pass for the wrong reason. Record the observation, leave the
  artifact untouched, and re-check after the next natural regeneration.

## Verification

- [ ] `breakdown` run both before and after; before/after byte counts stated.
- [ ] The arithmetic floor computed and stated; target checked against it.
- [ ] `coupling` run for every moved block; zero runtime coupling, or the coupling named and sequenced.
- [ ] `verify` run per moved section; all lines hit, zero misses.
- [ ] Retained operative fields byte-identical to the pre-migration copy.
- [ ] Digest-vs-authoritative direction declared in **both** files.
- [ ] Single append path exists for new history, and it updates the pointer count.
- [ ] Shape guard added and wired into the project's gate.
- [ ] No secret / private data moved into a file that is published or shared.
- [ ] If the document exists in more than one copy, they were merged with alias normalisation and **one declared language**.
- [ ] Every superseded paraphrase logged; empty entries marked, not invented; unprovable-duplicate pairs left separate with a note.
- [ ] The verification script itself was re-checked for the false-alarm classes above **before** trusting any FAIL it reported.
- [ ] Platform-generated sidecar files left untouched; any defect in them recorded for a post-regeneration check.
- [ ] Any comparator's expected include/exclude set was read off the **authoritative** side, not assumed.
- [ ] The published/shared artifact's own file list was inspected, so no local sidecar rode along.
