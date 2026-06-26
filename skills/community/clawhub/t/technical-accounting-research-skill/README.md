# Technical Accounting Research Skill

A Codex skill for technical accounting issue research and documentation under U.S. GAAP and SEC-focused reporting contexts.

## What It Does

- Forces clarification questions before analysis.
- Confirms output format (`memo`, `email`, or `q-and-a`) before drafting.
- Performs authoritative and interpretive accounting research (for example FASB, AICPA, SEC, and Big 4 sources).
- Requires the local FinResearchClaw repo/workflow as a wrapped research-and-drafting layer for substantive runs.
- Applies standards to the fact pattern and produces a deliverable, typically a DOCX memo.

## FinResearchClaw Dependency

This skill is designed to work with the local FinResearchClaw repo and should not be treated as fully operational until that repo is installed and runnable.

Required repo:
- `https://github.com/ChipmunkRPA/FinResearchClaw`

Expected local path by default:
- `~/.openclaw/workspace/AutoResearchClaw`

FinResearchClaw is used as a required wrapped execution layer for memo, email, and q-and-a workflows. It is intended to improve research depth and drafting quality, but final accounting conclusions must still be verified against authoritative and clearly labeled interpretive guidance.

## Requirements

- Python 3.11+
- Local clone/install of `FinResearchClaw`
- `python-docx` for DOCX memo generation

Install the supporting dependency if needed:

```bash
python -m pip install --user python-docx
```

## Recommended Local Setup

Install FinResearchClaw locally first:

```bash
git clone https://github.com/ChipmunkRPA/FinResearchClaw.git ~/.openclaw/workspace/AutoResearchClaw
cd ~/.openclaw/workspace/AutoResearchClaw
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

After that, this skill can wrap the local FinResearchClaw workflow during live technical-accounting tasks.

## Skill Layout

- `SKILL.md`: Core workflow and behavior rules.
- `agents/openai.yaml`: UI metadata for invocation.
- `references/`: Clarification checklist, source hierarchy, JSON schema, sample payload.
- `scripts/build_accounting_report_docx.py`: DOCX report generator.

## Generate a DOCX Report

```bash
python scripts/build_accounting_report_docx.py \
  --input-json references/example_report_input.json \
  --output-docx output/technical-accounting-report.docx \
  --format memo
```

Allowed formats: `memo`, `email`, `q-and-a`.

## Operational Notes

- The skill should verify that the local FinResearchClaw repo exists before relying on the wrapped workflow.
- If FinResearchClaw is missing or broken, fix that prerequisite before treating the skill as ready for substantive completion.
- FinResearchClaw does not replace ASC / SEC / AICPA source validation; it supports the research and drafting process.

## License

This project is licensed under the MIT License. See `LICENSE`.
