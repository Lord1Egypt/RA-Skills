# The judgment doctor withholds

Load this when `doctor` emits SV401, SV101/SV103, SV301/SV303, SV501–SV508, or
SV201/SV202. Each section says what the tool established, what it refused to
decide, and how to decide it.

## SV401 — semantic overlap

**Tool established:** two descriptions share a high proportion of terms
(Jaccard ≥ `--min`, default 0.25).

**Tool refused:** whether they actually compete. It says so itself —
"a lexical filter, not a verdict", and **false negatives are more common than
false positives**. Skills worded differently can still compete for the same
request, and `overlap` will never show them to you.

**How to decide:** read the `description` fields, not the similarity score. For
each candidate pair produce:

- the competing names;
- **one concrete user request that could plausibly trigger both**;
- an action: merge, narrow the trigger boundaries, or add an explicit exclusion.

If you cannot write that concrete request, there is no overlap worth reporting.
Say the pair looks similar lexically but does not compete, and move on.

Because the filter misses reworded competitors, also scan the full description
list yourself when the library is small enough to read. `SV402 OVERLAP_CONFIRMED`
is listed under "Not assessed" precisely because this decision is yours.

## SV101 / SV103 — precedence conflicts

**Tool established:** two copies of the same `(namespace, name)` exist in one
`conflict_domain`, and which one wins.

**Tool refused:** whether the winner is the one the user wants.

**Precedence is `enterprise > personal > project > plugin`** — the
home-directory copy shadows the project copy, which is the opposite of most
people's intuition. That inversion is usually the whole finding:

- **SV101 `shadowed_newer`** (critical) — a *newer* copy is losing to an older
  effective one. Usually a real defect: the user edited the project copy and is
  still running the personal one.
- **SV103 `intentional_override`** (warning) — a higher-priority copy that looks
  deliberate. Confirm before touching it.
- **SV102 `redundant`** (info) — byte-identical hashes. Harmless; mention only
  as cleanup.

**Before recommending deletion, state which copy is currently effective and give
both absolute paths.** A user who deletes the wrong one loses their edits.

## SV301 / SV303 — split boundaries

**Tool established:** `tier2_core_tokens` exceeds `--split-threshold`
(default 6000), and for SV303 that the skill is also unused.

**Tool refused:** where to cut.

Judge from **`tier2_core_tokens`, never line count** — measured density varies
more than 4× within one library, so a line-based threshold can invert the answer.

The four buckets are not interchangeable:

| Field | Meaning |
|---|---|
| `tier1_tokens` | frontmatter — resident at every startup |
| `tier2_core_tokens` | SKILL.md body — loaded whenever the skill triggers |
| `tier2_refs_tokens` | reference `.md` — loaded on demand |
| `tier2_max_tokens` | core + refs — worst case when everything is read |

Only `.md` under `references/`/`docs/` or sibling to `SKILL.md` counts as tier 2.
`.md` elsewhere is classified as **data corpus** — bytes only, excluded from the
token buckets. If a skill's cost looks implausibly low, check whether its content
sits in a directory the scanner treats as corpus.

**Splitting lowers `core` but often raises `max`.** Any "it is cheaper now" claim
must name which number dropped. Give a specific boundary — which sections move to
`references/`, and what trigger condition sends the reader there — instead of
saying only "split this skill".

For SV303, resolve the "unused" half first (see below). Do not recommend
restructuring a skill you are about to recommend deleting.

## SV501–SV508 — security findings

**Tool established:** a line matched a heuristic rule.

**Tool refused:** whether it is dangerous. Its own caveat: *a match does not
prove malware, and no match does not prove safety.*

**Review every flagged line manually.** `cited=true` means the line *looks* like
a quoted example or defensive documentation — it changes reading order and
nothing else. It never suppresses a finding, never lowers severity, and is not a
safety verdict: a `For example,` prefix or one unbalanced quote is enough to fool
it. `max_severity` includes cited findings; `max_severity_uncited` exists only to
tell you what to read first.

Explain findings in plain language:

| Code | Rule | Plain meaning |
|---|---|---|
| SV501 | `adversarial_instruction` | tries to override prior instructions or hide actions |
| SV502 | `pipe_to_shell` | remote content piped straight into a shell |
| SV503 | `base64_exec` | encoded content executed directly |
| SV504 | `raw_ip_fetch` | download from an unverified numeric endpoint |
| SV505 | `hardcoded_secret` | credentials embedded in files |
| SV506 | `credential_env_read` | reads `.env`, AWS, SSH, or similar secrets |
| SV507 | `obfuscated_exec` | execution hidden behind obfuscation |
| SV508 | `password_archive` | archive that may evade inspection |

Include file paths, line numbers, and short snippets for anything serious. Never
tell a user a skill is safe — you can only report that these rules found nothing.

## SV201 / SV202 — dead or never selected?

**Tool established:** zero or few triggers, and that the skill is old enough to
judge. Skills under `--zombie-age` (default 14 days) are reported as **too new to
judge**, never as zombies — otherwise users delete what they installed yesterday.

That age comes from filesystem creation time, which is **unreliable on Linux** and
resets when a directory is copied or re-cloned. A skill the user has had for a year
can look like it arrived today. Treat the age gate as protection against false
zombie calls, not as evidence of when the skill was installed.

**Tool refused:** why the count is zero. Its own caveat: *zero triggers do not
prove uselessness; the skill may never have been selected.*

Rule out these first, in order:

1. **It never loaded** — check the loaded-vs-disk split and SV101/SV104.
2. **Budget pressure** — SV002 means descriptions may be truncated before the
   model ever sees this one.
3. **It lost to a competitor** — SV401 against a skill with real usage.
4. **Its description does not match how users actually phrase the request** —
   run `explain <name>` for the trigger funnel.

Only after all four are ruled out is inactivity evidence of low value. Then
recommend removal — and still require the user to confirm.

## Ordering your recommendations

1. Fix blocking visibility, budget, overlap, and precedence problems.
2. Review security findings.
3. Reduce expensive skill bodies and descriptions.
4. Remove only skills supported by real inactivity evidence and sufficient age.
5. Improve output quality only after confirming the effective copy is the one
   being selected.

When evaluating quality, build validation cases from real usage. Do not invent
expected outputs. Keep a holdout set and check for newly introduced failures
after each change.
