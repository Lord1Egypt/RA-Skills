## Description:

Skill Tracker helps an agent record skill usage, calculate health scores, generate optimization proposals, and produce Markdown health reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alsoforever](https://clawhub.ai/user/alsoforever)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to monitor how local agent skills are used, score their health, and review generated improvement proposals and Markdown reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores usage records, timing, success or failure, satisfaction scores, and caller-supplied metadata under ~/.openclaw/data/gungun.

Mitigation: Review what metadata is passed into the logger, avoid sensitive values, and define retention and cleanup expectations before routine use.

Risk: The security evidence reports an unvalidated proposal file-write path that can escape the intended proposal folder.

Mitigation: Fix filename validation before using the proposal generator on shared or automation-heavy systems.

Risk: Optional cron automation can run health scoring, proposal generation, and report generation without interactive review.

Mitigation: Do not enable cron until storage location, retention, and generated proposal review practices are understood.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alsoforever/skills/xuanxuan)
- [README-opensource.md](README-opensource.md)
- [SKILL.md](SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON and JSONL data files, console summaries, shell commands, and Python integration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores local usage, health-score, and proposal files under ~/.openclaw/data/gungun and can be scheduled with cron.]

## Skill Version(s):

1.0.0 (source: server evidence release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
