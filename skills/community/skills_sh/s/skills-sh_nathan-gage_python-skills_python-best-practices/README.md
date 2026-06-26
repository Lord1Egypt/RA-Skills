# Python Best Practices

A structured skill for writing and reviewing Python. Rules are derived from real PR review patterns, organized by impact and applicability, and formatted for agent consumption.

**Python version baseline:** 3.11+ (some rules call out higher-version features inline — e.g., `warnings.deprecated()` is 3.13+).

## Structure

```
python-best-practices/
├── SKILL.md                # Entrypoint loaded into agent context (quick reference)
├── README.md               # This file
├── metadata.json           # Version, abstract, references, Python version floor
├── AGENTS.md               # (generated) Compiled document with every rule expanded
├── test-cases.json         # (generated) LLM eval data extracted from rule examples
├── rules/                  # Individual rule files (one rule per file)
│   ├── _sections.md        # Section metadata
│   ├── _template.md        # Template for new rules
│   └── {prefix}-{name}.md  # Rule files; `prefix` matches a section in `_sections.md`
└── src/                    # Build, validate, extract-tests scripts
```

## Sections

| # | Section | Typical Impact | Prefix |
|---|---|---|---|
| 1 | Data Modeling | HIGH | `data-` |
| 2 | Error Handling | MEDIUM-HIGH | `error-` |
| 3 | Type Safety | MEDIUM-HIGH | `types-` |
| 4 | API Design | MEDIUM | `api-` |
| 5 | Code Simplification | LOW-MEDIUM | `simplify-` |
| 6 | Performance | LOW-MEDIUM | `perf-` |
| 7 | Naming | LOW-MEDIUM | `naming-` |
| 8 | Imports & Structure | LOW | `imports-` |

Section impact is the typical case; individual rules range one level above or below — always check the rule frontmatter. Applicability (e.g., Pydantic-only) is tagged on the rule, not the section.

## Impact Levels

- `CRITICAL` — prevents a real bug class (data corruption, swallowed cancellations, insecure defaults)
- `HIGH` — meaningful correctness or maintainability win
- `MEDIUM-HIGH` — noticeable improvement worth enforcing
- `MEDIUM` — good practice; clarity or drift prevention
- `LOW-MEDIUM` — marginal; new code preferred
- `LOW` — style; opportunistic only

Reserve `CRITICAL` for bug classes you'd block a PR on. If more than a handful of rules are `CRITICAL`, the signal is lost.

## Authoring Workflow

1. Copy `rules/_template.md` to `rules/{prefix}-{name}.md`
2. Choose the prefix from `_sections.md`
3. Fill in frontmatter (`title`, `impact`, `impactDescription`, `tags`, `references`)
4. Write a short explanation + Incorrect/Correct pair + optional note
5. Run `src/validate.py` → fix → `src/build.py` → `src/extract_tests.py`

Keep rule bodies short — target 20–40 lines. One Incorrect block, one Correct block, optional one-paragraph note. Avoid enumerated "use X when / use Y when" taxonomies; let the example carry the point.

## Scripts

```bash
python src/build.py            # compile rules into AGENTS.md
python src/validate.py         # lint frontmatter, references, example structure
python src/extract_tests.py    # generate test-cases.json for LLM evals
```

Typical loop: `validate.py` → fix → `build.py` → `extract_tests.py` before commit. `AGENTS.md` and `test-cases.json` are generated outputs — don't hand-edit.

## Rule File Format

```markdown
---
title: Rule Title Here
impact: MEDIUM
impactDescription: brief phrase on the payoff
tags: tag1, tag2
references: https://docs.python.org/3/library/...
---

## Rule Title Here

Brief explanation — one or two sentences. Observational, not prescriptive.

**Incorrect:**

```python
# Bad example
```

**Correct:**

```python
# Good example
```

Optional one-paragraph note on edge cases or version notes.
```

### When `references` is required

`references` is required when the rule depends on:

- A specific Python version (3.10 union isinstance, 3.11 `assert_never`, 3.13 `warnings.deprecated`)
- Standard-library behavior with versioned semantics (`assert` under `-O`, `cached_property` thread safety)
- Third-party library behavior (Pydantic, mypy, ruff)
- A PEP

Pure judgment-call rules (naming preferences, taste) may omit `references`.

### Tagging applicability

Rules that only apply within a specific ecosystem (e.g., Pydantic) carry an `applicability:{name}` tag in `tags` and call it out in the body.

## Tone

Rules are observational, not prescriptive. Describe the pattern and the cost; show the fix. Don't moralize about what an agent "is tempted to do" — the reader already has the code in front of them.

Rule bodies should leave judgment to the reader. A rule that applies everywhere in a codebase without exception is rare; most need a reader who knows their context.

## Acknowledgments

Rule material draws from PR-review patterns in the Pydantic AI codebase, Vercel's `react-best-practices` and `composition-patterns` skills (structural inspiration and tone), and the `clanker-discipline` skill.
