# Interaction & Verification (self-contained)

Templates and details for skill-debloater's Steps 3 and 4. On Hermes, use `clarify` for interaction.

---

## 1. ALIVE interaction: clarify template

For the `review` bucket output by triage.py, ask the user **in one batch**, not one item at a time.
Principle: default to keeping everything, only delete what the user explicitly checks.

### Standard template

```
clarify title: Skill Debloating — Confirm Deletions (default: keep all)

The following N items have accumulated across versions and are suspected deletable. Tell me which ones can be deleted; I'll keep the rest:

1) references/upgrade-recipe.md
   Basis: orphan (not referenced in the body) + a v1→v2 migration guide, now at v2.2.0
   Suggestion: deletable

2) references/v2.1.8-sla-cases.md
   Basis: old-version-tag v2.1.8 < current 2.2.0 (but still referenced in the body)
   Suggestion: your call — deletable if you no longer need to reference old-version metrics, otherwise keep

3) changelog.md section v2.1.0~v2.1.6
   Basis: empty-shell, content is already "(omitted, see git)"
   Suggestion: deletable (full content is in git history)

Example reply: "delete 1 and 3, keep 2" / "delete all" / "keep everything for now"
```

### Interaction discipline

- User doesn't explicitly say delete → keep.
- User says "use your judgment" → still only delete the safest items marked `suggestion: deletable` with `orphan`+`empty-shell`, keep the rest and explain why.
- Any file still referenced in the body, even with an old version number, needs an extra warning before deletion: "deleting this will break a reference, the body needs to be updated too."

---

## 2. Lossless reorganization: no interaction needed, but log it

The WHAT/WHERE/HOW reorganization executes automatically, but list it in the final summary so the user can trace it:

```
Automatic reorganization this run (no information lost, reversible):
- Pushed down: <body section> → references/<file>.md (WHAT=Background)
- Externalized: <deterministic step> → scripts/<file>.py (HOW, body now just says "run it")
- Merged: <fully duplicate/equivalent section A+B> → 1 section (verbatim-equivalent dedup only; rewriting shorter is "lossy compression," see §2.5)
```

---

## 2.5 Lossy compression: automatic only when verified, otherwise ask via before/after

Rewriting verbose prose shorter ≠ lossless reorganization — it's lossy and irreversible, default to asking the user. **Only auto-compress when all four hard conditions are met**, missing any one escalates to asking the user:

1. Load-bearing information (conditions/causality/constraints/order/numbers) — none lost in the compressed version;
2. The compressed version introduces no new interpretation, no added ambiguity;
3. Doesn't touch the "keep verbatim" list (numbers/thresholds, API/field/parameter names, "don't do X" prohibitions, boundary and exception rules);
4. Contains no subtext or domain-private meaning the model might miss.

**Don't write "95% confidence"** — models don't have calibrated confidence, they'll convince themselves the bar is met; use four checkable hard conditions instead of "high confidence."

If any condition is uncertain, use this template to ask the user:

```
Compression confirmation (want to check before/after in case of lost info/ambiguity):

Original (N characters):
  <original text>
Compressed (M characters):
  <compressed text>

Question: does this compression lose any detail you care about, or read differently than intended?
Example reply: "fine" / "keep sentence 2 as-is" / "don't compress any of it"
```

Cases where all four conditions are clear and compression happens automatically should also be logged in the final summary, so the user can trace it later and roll back from the Step 4 snapshot if needed.

---

## 3. Three-way verification template (Step 4, don't skip)

The only reliable quality assurance. For 3–5 real tasks:

```
Verification: <skill name>

| Task | No skill | Original skill | Debloated | Verdict |
|------|---------|-----------|--------|------|
| Task 1 | Fail | Pass | Pass | OK |
| Task 2 | Fail | Pass | Fail | Rollback: add <X> back into the body |

Verdict:
- Does the debloated version match or beat the original on every task? Yes/No
- If no, content rolled back: ____
- Token change: ____ → ____ (down __%)
```

Rollback rule: if the debloated version does worse than the original on any task, add the content that caused the failure back into the body's Core section, retest, until it's no worse than the original.

---

## 4. Final delivery summary template

```
## skill-debloater result: <skill name>

- tokens: <before> → <after> (down __%), body line count: <before> → <after>
- automatic reorganization: pushed down N sections / externalized M scripts / merged K places
- user-confirmed deletions: <list what the user checked to delete>; kept: <list what the user decided to keep>
- frontmatter fixes: <e.g. name changed to match folder / description completed>
- verification: <X/Y tasks ≥ original>, rollback: <yes/no>
```
