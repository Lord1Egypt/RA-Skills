---
name: python-pep-authoring
description: Draft, review, edit, or prepare Python Enhancement Proposals using the official python/peps repository rules. Use when working on PEP text, PEP metadata headers, PEP process/status decisions, reStructuredText PEP formatting, python/peps pull requests, or validation with check-peps.py, pre-commit, and local rendering.
---

# Python PEP Authoring

## Overview

Use this skill for Python Enhancement Proposal work that needs to follow the official `python/peps` repository, not generic Python code style. It covers PEP drafting, PEP review, metadata/header validation, reStructuredText formatting, repository checks, and contribution workflow.

The bundled references summarize the official `python/peps` repository at commit `63b05773e2b5e8355910df520e8cf319f70944be` from 2026-06-28. When working inside a current checkout of `github.com/python/peps`, prefer the checkout's local files over these summaries.

## Workflow

1. Classify the request:
   - New PEP draft or template creation.
   - Review of an existing PEP draft.
   - Change to an existing PEP.
   - Repository PR preparation, lint failure, or rendering issue.
2. Read the relevant reference before making detailed claims:
   - `references/process-and-policy.md` for PEP workflow, statuses, authorship, sponsors, review, and maintenance.
   - `references/header-and-rst-rules.md` for PEP 12 header order, metadata formats, PEP section template, and reST rules.
   - `references/repo-validation.md` for `python/peps` checkout commands, `check-peps.py`, pre-commit, spelling, and rendering.
3. If a live `python/peps` checkout is available, inspect local source files before editing:
   - `peps/pep-0001.rst`
   - `peps/pep-0012.rst`
   - `peps/pep-0012/pep-NNNN.rst`
   - `CONTRIBUTING.rst`
   - `README.rst`
   - `check-peps.py`
   - `.pre-commit-config.yaml`
4. For a new PEP, make sure the draft has one focused proposal, a champion, the correct PEP type, `Status: Draft`, a sponsor if required, a valid discussion plan, and the PEP 12 template structure.
5. For edits to existing PEPs, check the status first. Draft PEPs are open to discussion and proposed modification; Accepted, Final, Rejected, Withdrawn, and Superseded PEPs are mainly historical documents and should not receive major content changes without a process reason.
6. For reviews, report concrete issues first with file/line references when available. Separate process blockers, metadata/header defects, reST/rendering defects, and editorial/content concerns.
7. For repository work, run the narrowest meaningful validation command available. Prefer `python check-peps.py peps/pep-NNNN.rst` for a single PEP, then `make lint`, `make spellcheck`, and `make html` or `python build.py` when appropriate.

## New PEP Drafts

When asked to create or revise a new PEP:

- Use `peps/pep-0012/pep-NNNN.rst` as the source template if the official repo is present. Do not use rendered HTML as a template.
- Name the file `peps/pep-NNNN.rst` with zero padding. The `PEP:` header itself is not zero-padded.
- Use the next available PEP number not used by a published or in-PR PEP unless a PEP editor assigns a number.
- Include required headers in PEP 12 order and remove optional headers that do not apply.
- For Standards Track PEPs, include `Python-Version` when the feature targets a Python release; omit it for interoperability standards that initially live outside the stdlib.
- Add `Discussions-To: Pending` and `Post-History: Pending` only when the canonical thread does not exist yet; update them after the thread is created.
- Include the dual public domain / CC0-1.0-Universal copyright/license text.
- If the PEP has co-authors or sponsors with write access to `python/peps`, update `.github/CODEOWNERS`.

## Review Output

Use this structure for PEP reviews:

```markdown
Findings
- [P1] Missing sponsor for non-core authors - peps/pep-NNNN.rst:4
  Explain the official rule, why it blocks or weakens the PEP, and the smallest fix.

Open Questions
- Mention only questions that affect process, metadata, or content readiness.

Validation
- List commands run and whether rendering/linting passed.
```

Use priorities consistently:

- `P0`: would break rendering, validation, or repository acceptance outright.
- `P1`: process or metadata issue likely to block PEP editor approval.
- `P2`: clear PEP 1/PEP 12/repo-rule issue that should be fixed.
- `P3`: editorial polish, clarity, or optional improvement.

If there are no findings, say that directly and mention any validation not run.

## Source Links

- Official repository: https://github.com/python/peps
- PEP index: https://peps.python.org/
- PEP 1: https://peps.python.org/pep-0001/
- PEP 12: https://peps.python.org/pep-0012/
