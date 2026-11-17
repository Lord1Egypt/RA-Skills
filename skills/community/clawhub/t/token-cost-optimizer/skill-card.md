## Description:

Guides OpenClaw users through diagnosing token consumption and reducing API costs with context controls, model routing, workflow adjustments, cleanup checks, and monitoring practices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[taod7062-a11y](https://clawhub.ai/user/taod7062-a11y)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to investigate high token usage, rising API costs, long context windows, repeated agent calls, frequent scheduled tasks, and model routing choices. It provides a cost-reduction workflow covering diagnosis, analysis, optimization, and ongoing monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cleanup commands may delete workspace or memory files without safeguards.

Mitigation: List candidate files first, make backups, and require an explicit user decision before deleting files.

Risk: Suggested edits to openclaw.json or soul.md can persistently alter OpenClaw behavior.

Mitigation: Review and version configuration changes before applying them, then verify the resulting model routing and compaction behavior.

Risk: Broad activation guidance may cause the skill to be used for loosely related cost or optimization requests.

Mitigation: Confirm the user is working on OpenClaw token usage or API cost control before applying the workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/taod7062-a11y/skills/token-cost-optimizer)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May suggest persistent OpenClaw configuration and memory or workspace cleanup actions that require user review before execution.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
