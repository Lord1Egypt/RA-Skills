# Shipping Checklist

Follow this checklist before merging any feature PR to `main`. Both humans and agents (including Claude Code) must complete all steps.

---

## 1. Code Quality
- [ ] All tests pass (`pytest`)
- [ ] No regressions in existing functionality

## 2. Update Manifest
- [ ] `critic-status.yaml` updated (add/change status for shipped feature)
- [ ] Version string bumped in `critic-status.yaml`
- [ ] Version string bumped in `reference-implementation/pyproject.toml`

## 3. Documentation Sweep
Run `python tools/validate-docs.py` to find stale references, then fix:

- [ ] `CHANGELOG.md` — add entry for this release
- [ ] `README.md` — version badge in header
- [ ] `README.md` — "What I can do today" section accurate
- [ ] `README.md` — critic count in depth table footnote
- [ ] `README.md` — architecture diagram labels (shipped vs roadmap)
- [ ] `README.md` — "What's coming" section (remove shipped items)
- [ ] `SPEC.md` — status matrix / implementation checklist updated
- [ ] `SPEC.md` — shipped critic counts in prose
- [ ] `docs/getting-started/FOR_BEGINNERS.md` — critic counts and cost estimates
- [ ] `docs/configuration/CONFIG_REFERENCE.md` — critic status markers
- [ ] `docs/getting-started/TUTORIAL.md` — critic descriptions and status markers
- [ ] `docs/architecture/IMPLEMENTATION.md` — critic status markers and depth profiles
- [ ] `SKILL.md` — critic counts in depth descriptions

**⚠️ Note on Cross-Consistency:** Cross-Consistency is a shipped critic but requires the `--relationships` flag. When updating counts, use language like: "6 shipped critics (including Cross-Consistency, activated with `--relationships`)".

## 4. Validation
- [ ] `python tools/validate-docs.py` passes (exit 0)
- [ ] `tools/boundary-scan.sh` passes (exit 0)

## 5. Commit & Ship
- [ ] Commit message includes: what shipped, critic N of 9, known limitations
- [ ] Tag release if version bump warrants it

---

## Why This Exists

PR #8 (Tester critic) shipped with 10+ doc files still claiming "4 critics." The Cross-Consistency critic shipped at some point with zero doc updates. This checklist + `validate-docs.py` + CI enforcement exists to prevent that from happening again.
