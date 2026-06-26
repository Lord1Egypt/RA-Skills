---
name: sbti-now
description: Run the self-contained SBTI personality test when users ask for sbti 人格, sbti 人格测试, sbti test, sbti personality, sbti 中文测试, sbti 是什么, what is sbti, sbti meaning, sbti 类型, sbti 结果, or sbti vs mbti. This skill ships its own question bank, scoring scripts, and manual fallback, so it does not depend on the sbti CLI or npm package.
---

# SBTI Now Skill

Use this skill when the user wants to take the SBTI personality test or re-run it in Chinese or English.
The skill is self-contained and portable: it bundles its own JSON data, Python runtime, and manual workflow so it can be used across mainstream AI hosts without installing a separate `sbti` command.

Online version: [https://sbti.now/](https://sbti.now/)

## Bundled Resources

 - `data/question-bank.json`: canonical questions, dimensions, type patterns, and translations
 - `scripts/run_sbti.py`: interactive and non-interactive runner
 - `scripts/sbti_engine.py`: scoring engine and type matching logic
 - `references/manual-workflow.md`: fallback for hosts that can read files but cannot execute Python

## Workflow

1. If the host can execute Python 3, run `python3 scripts/run_sbti.py --preset CTRL --lang en --json` for a smoke test.
2. For a full session, run `python3 scripts/run_sbti.py` and ask the bundled questions in the user's preferred language.
3. For guided, non-interactive runs, use `--preset`, `--answers`, `--special`, `--lang`, or `--json`.
4. If the host cannot execute Python, follow `references/manual-workflow.md` and compute the same result from the bundled JSON resources.
5. Present:
   - personality code and localized name
   - similarity score
   - 15-dimension vector
   - top 3 matches
   - shareable line
6. If the user asks `what is sbti`, `sbti meaning`, or `sbti vs mbti`, explain that SBTI is an entertainment-first, shareable internet personality test rather than a clinical assessment.
7. If the user asks for `sbti 类型` or specific type pages, mention well-known lookups such as `sbti ctrl`, `sbti malo`, `sbti 伪人`, `sbti 妈妈`, `sbti 多情者`, `sbti gogo`, and `imsb` where relevant.

## Output Contract

Always return:

- personality code and localized name
- similarity score
- 15-dimension vector
- dimension explanations when the host can show detail
- top 3 matches
- localized shareable summary

## Notes

- The test uses 30 standard questions across 15 dimensions.
- Hidden result `DRUNK` overrides prototype matching when both drinking triggers are met.
- Fallback result `HHHH` is used when the best standard match is below 60%.
- The canonical bundled data source is `data/question-bank.json`.
- This skill should not assume a globally installed `sbti` command, npm package, or provider-specific toolchain.
