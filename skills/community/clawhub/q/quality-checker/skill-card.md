## Description:

Quality Checker evaluates Markdown chapter drafts for word count, paragraph length, dialogue ratio, punctuation issues, repeated wording, and produces a scored quality report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuzhihui886](https://clawhub.ai/user/yuzhihui886)

### License/Terms of Use:

MIT-0

## Use Case:

Writers, editors, and publishing workflow developers use this skill to check chapter drafts before release and identify measurable writing-quality issues such as insufficient length, overly long paragraphs, abnormal dialogue ratio, punctuation overuse, and repeated words.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned Python dependencies may resolve to different package versions over time.

Mitigation: Install in an isolated virtual environment and pin reviewed versions of rich and PyYAML before production use.

Risk: The tool reads chapter and configuration paths and can write a report path supplied by the user.

Mitigation: Run it only on intended local files and review input, config, and output paths before execution.

Risk: The command-line interface and generated report text are Chinese-language only.

Mitigation: Use it in workflows where Chinese output is expected, or add localization before relying on it with non-Chinese-speaking reviewers.

## Reference(s):

- [Quality Checker ClawHub page](https://clawhub.ai/yuzhihui886/skills/quality-checker)
- [Quality Checker source skill definition](artifact/SKILL.md)
- [Quality Checker default configuration](artifact/configs/quality_config.yml)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Terminal report with optional Markdown report file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include a 0-100 quality score, metrics, issue list, and repeated-word details when present.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
