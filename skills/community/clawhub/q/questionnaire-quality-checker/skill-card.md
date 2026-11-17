## Description:

Screens psychology questionnaire CSV data for missingness, invalid or out-of-range values, within-scale straightlining, and extreme response patterns, then summarizes respondent-level flags for review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yunyue619](https://clawhub.ai/user/yunyue619)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, analysts, and agents use this skill to run transparent quality checks on Likert-scale questionnaire CSV files and produce a concise report of respondents that need manual review. It is intended to support review decisions, not to automatically exclude samples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Respondent flags may be misused as automatic exclusion decisions.

Mitigation: Treat flags as review prompts, apply study-specific exclusion rules, and document thresholds, counts, and overlapping criteria before making final decisions.

Risk: Local CSV, JSON config, and report paths could be pointed at unintended files.

Mitigation: Run the checker only on intended project-scoped input files and review any output path before execution.

Risk: Incorrect scale items, ranges, or thresholds can produce misleading quality flags.

Mitigation: Review the JSON configuration before running, use separate legal ranges for each scale, and confirm configured columns exist in the CSV.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yunyue619/skills/questionnaire-quality-checker)
- [Skill definition](artifact/SKILL.md)
- [Example configuration](artifact/examples/config.example.json)
- [Example JSON report](artifact/examples/demo_report.json)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown report with optional JSON report file and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write a local JSON report when the --output path is supplied.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
