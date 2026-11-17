---
name: skill-debloater
description: Diagnoses and slims down bloated, flaky Agent Skills into a lean, stable version. Use when a skill's body has grown too long, burns too many tokens, or has accumulated stale files across versions and behaves inconsistently. The method makes a four-axis decision for every piece of content: WHAT is its nature, WHERE should it live, HOW should it be expressed (prose vs. script), and ALIVE — is it still in use. The first three axes are handled automatically by scripts and the model via lossless reorganization (push down / externalize / merge); the fourth axis, deletion, depends on history only the user knows, so it must be confirmed with the user item by item — default to keep, never auto-delete. Trigger this when the user asks to debloat, slim down, clean up old versions, or when a skill is too long/verbose or flaky.
---

# Skill Debloating (Four-Axis Method)

Refactor a skill that's both bloated (too many tokens) and flaky (inconsistent) into a lean, stable version.

This skill is **self-contained** and **platform-agnostic** (works generically across Hermes / openclaw / Claude, etc.): all methodology lives in `references/`, no external knowledge required.

## Platform conventions (cross-platform, read first)

Replace these placeholders below with what applies to your platform:

- `<SKILL_DIR>` — the install directory of this skill. Hermes: `~/.hermes/skills/skill-debloater`; Claude: `~/.claude/skills/skill-debloater`; substitute the equivalent path for openclaw etc.
- **RUN** — the platform's "execute code / command" tool (Hermes: `execute_code` or `terminal`; use the equivalent tool on other platforms).
- **ASK** — the platform's "ask the user / clarify" tool (Hermes: `clarify`; use the equivalent user-interaction mechanism on other platforms).

## Core model: run every piece of content through four axes

| Axis | Question | Who answers | Action |
|----|------|--------|------|
| WHAT  | What is this piece's nature? (Core / Background / Example / Template / Redundant) | Automatic | — |
| WHERE | Which layer should it live in? (body / references / scripts) | Automatic | Lossless reorganization |
| HOW   | Prose or script? (deterministic logic should be externalized into a script) | Automatic | Lossless reorganization |
| ALIVE | Is it still in use? (stale version leftovers / orphans / empty shells) | **User** | **Lossy deletion** |

**Iron rule**: if the first three axes don't lose information and are reversible → do them automatically. The fourth axis destroys information, is irreversible, and only the user knows whether it's still alive → **must ASK for confirmation, default to keep, never auto-delete**.

> Note: pushing content down under WHERE is reversible for **information**, but not neutral for **behavior** — under progressive disclosure, the model may fail to read layer 3 exactly when it should. Misjudging a Core Rule as Background and pushing it down is a textbook way to cause "works sometimes, fails other times." So content near the Core/Background boundary **defaults to staying in the body**, even if that means staying a bit heavier; every file that gets pushed down must leave a trigger condition in the body for "when to read it" (see the "Files" list) so the model can reliably pull it back. Three-way verification (Step 4) is a backstop, not a substitute.

> There's a third category of operation: **compression/rewriting** (rewriting verbose prose to be shorter). Unlike push-down/externalize, it doesn't preserve content verbatim — it can lose detail, introduce ambiguity, and the original isn't recoverable. Default to **asking the user**; only auto-compress when losslessness can be **verified**. "Verified" doesn't rely on the model self-reporting confidence (models don't have calibrated confidence — telling it "only proceed at 95% confidence" just gets rationalized away) — it relies on **all four hard conditions** being met: ① no loss of load-bearing information (conditions/causality/constraints/order/numbers); ② no new interpretations introduced, no added ambiguity; ③ doesn't touch the "keep verbatim" list; ④ contains no subtext or domain-specific meaning the model might miss. **If any condition is uncertain → treat it as unverified → show the user a before/after: "any information lost? any ambiguity?"** The original is backstopped by the Step 4 snapshot; details and templates are in `references/interaction-and-verify.md`.

>
> In one line: operations are sorted into three tiers by reversibility — **lossless reorganization (automatic) < lossy compression (automatic only when verified, otherwise ask) < lossy deletion (must ask, item by item)**.

For the full methodology (five-category definitions, four-axis derivation, root causes of instability) see `references/methodology.md`.

## When to trigger

A skill's body has grown too long / burns too many tokens / behaves inconsistently / has accumulated a pile of stale version files, and the user asks to debloat, slim down, or clean up.

## Execution flow

### Step 1: Health check (quantify current state)

Use **RUN**:

```bash
python3 <SKILL_DIR>/scripts/audit_skill.py "<path to target skill>"
```

Output: estimated body token count, line count, frontmatter compliance (name ≤ 64 chars & matches folder name, description ≤ 1024 chars with no `<` `>`), and a list of layer-3 files. Flags items over threshold (body should ideally be < 5000 tokens / < 500 lines).

### Step 2: Four-axis signal collection (two scripts, both read-only)

**ALIVE axis** — run `triage.py` to find orphans, stale version numbers, empty shells, and version mismatches:

```bash
python3 <SKILL_DIR>/scripts/triage.py "<path to target skill>"
```

Outputs a `keep` bucket (referenced + current version, kept automatically) and a `review` bucket (suspected deletable, each with `signals` + `suggestion`) → feeds into Step 3's interaction.

**HOW axis (AIP)** — the core of AIP is **compiling prose that describes a deterministic process into a script/pseudocode**. Run `scan_how.py`:

```bash
python3 <SKILL_DIR>/scripts/scan_how.py "<path to target skill>"
```

It gives two kinds of signal:

1. **Already written as code, but in the wrong layer** (strong signal, judged automatically by the script): a code block of ≥ 8 lines in the body means the code lives in layer 2 instead of scripts/ (layer 3) — it "should have been externalized but wasn't," which both dilutes attention and gets reloaded into context every time. Externalize it into a script and leave only "run it" in the body.
2. **Should be code, but is still prose** (AIP's main battleground; the script only gives weak hints): a paragraph of plain prose describes a deterministic process (sorting/calculation/formatting/a fixed multi-step procedure) but hasn't been written as code. The script flags deterministic keywords when it spots them, but **the judgment call is yours, from reading the body** (the same pass as WHAT/WHERE) — **zero code blocks does not mean HOW is healthy**.

Both kinds get externalized into scripts: it saves tokens + makes execution deterministic (fixes flakiness). Only externalize deterministic steps — **steps needing judgment or interaction stay as prose**. This is lossless reorganization, done automatically.

**WHAT / WHERE axes** — you (the agent) read the body and, per the five categories (see `references/methodology.md`), push background/examples/templates down into references. Lossless reorganization, done automatically — but WHERE has one discipline: **content whose boundary is uncertain (could be Core, could be Background) defaults to staying in the body**; only push down content you're confident is background, examples (keep one per concept), or templates. Every file pushed down needs a "when to read it" sentence left in the body.

> The three automatic axes (WHAT/WHERE/HOW) only **reorganize information, never destroy it**, so they run automatically. Only ALIVE deletes information, which is left to Step 3 to ask the user. WHERE's information is reversible but its behavior isn't neutral (see the iron rule above) — pushing content to the wrong layer can hurt stability on its own, backstopped by Step 4 verification.

### Step 3: ALIVE interaction (the only human-in-the-loop gate)

For the `review` bucket, use **ASK** to ask the user in one batch, defaulting to keep everything:

```
ASK: The following files are suspected deletable. Please check which ones to delete (default: keep all):

[ ] references/upgrade-recipe.md
      Basis: not referenced by SKILL.md + a v1→v2 migration guide, now at v2.2.0
      Suggestion: deletable
[ ] references/v2.1.8-sla-cases.md
      Basis: filename has stale version tag v2.1.8 < current 2.2.0 (but still referenced in the body)
      Suggestion: your call — deletable if you no longer need to reference old-version metrics
[ ] changelog section v2.1.0~v2.1.6
      Basis: content is already an empty shell ("(omitted, see git)")
      Suggestion: deletable
```

**Only what the user explicitly checks gets deleted.** If the user doesn't respond, says "keep it all," or hesitates → keep everything.

### Step 4: Execute + verify

1. **Snapshot before deleting anything**: before any deletion, use **RUN** to back up the entire target skill directory (`cp -r "<path to target skill>" "<path to target skill>.bak"`; if under git, `git stash` or a commit works too). Reason: deletion is irreversible, and even with user confirmation there should be a rollback path. Don't delete anything without a usable backup.
2. Execute the lossless reorganization (push-down/externalize/merge) + the deletions the user confirmed.
3. **Three-way verification**: take 3–5 real tasks and compare `original skill` / `debloated skill` / `no skill`. If the debloated version does worse on any task → **add the content that caused the failure back into the body**. It's best to ask the user for "cases that previously misfired or that you care about most" as test tasks (only the user knows which cases are flaky — same logic as ALIVE). Templates in `references/interaction-and-verify.md`.
4. Give the user a before/after summary: token counts, what was pushed down/externalized, what the user deleted, verification results, and the backup location (the `.bak` path, which can be deleted by the user once everything checks out).

## Hard rules

- **Never auto-delete any information.** Deletion can only happen via Step 3's ASK, checked by the user.
- **Always snapshot before deleting** (Step 4, item 1). Don't perform any deletion without a backup to fall back on.
- Lossless reorganization (push-down/externalize) can be done automatically — no information is lost, and it's reversible. But WHERE's push-down is not behavior-neutral: content with an uncertain boundary stays in the body, and pushing to the wrong layer is backstopped by Step 4 verification.
- Compression/rewriting is a **lossy, irreversible** operation, handled separately from lossless reorganization: (a) the "keep verbatim" list — numbers/thresholds, API/field/parameter names, explicit "don't do X" prohibitions, boundary and exception rules — **never compress these**; (b) other prose can only be auto-compressed when all four hard conditions are met (see the core model); if any is uncertain, show the user a before/after and default to not compressing.
- Don't chase a fixed compression ratio; stop once it's good enough — don't sacrifice correctness for a number.

## Files

- `references/methodology.md` — the self-contained four-axis methodology: five-category definitions, why the four axes are split this way, four root causes of instability, sources
- `references/interaction-and-verify.md` — ASK interaction templates + compression before/after confirmation template + three-way verification template + bucket-judgment details
- `scripts/audit_skill.py` — health check: token / frontmatter / file listing
- `scripts/triage.py` — ALIVE axis: buckets orphans/stale versions/empty shells (read-only)
- `scripts/scan_how.py` — HOW axis (AIP): scans the body for large code blocks and flags what should be externalized into a script (read-only)
