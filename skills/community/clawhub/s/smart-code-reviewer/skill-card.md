## Description:

A code review assistant that analyzes code, provides review comments, suggests performance improvements, detects possible security issues, and generates detailed review reports across multiple programming languages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryan-wuxl](https://clawhub.ai/user/ryan-wuxl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review individual files or project directories, identify code quality issues, performance concerns, and potential security vulnerabilities, and produce a Markdown review report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact references a Node review script that is not included in the submitted files.

Mitigation: Inspect the actual installed script before running it, especially on private or proprietary code.

Risk: The documentation is Chinese-only, which may make review harder for teams that do not read Chinese.

Mitigation: Translate or review the instructions with a Chinese-reading reviewer before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ryan-wuxl/skills/smart-code-reviewer)
- [Skill-declared homepage](https://github.com/openclaw/code-review-assistant)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown review reports with issue summaries, severity levels, and remediation suggestions; shell commands are shown for invoking the reviewer.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The documented Node review script is referenced by the artifact but is not included in the submitted files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
