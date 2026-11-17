## Description:

Audit all installed skills for quality, duplicates, structural issues, and best-practice compliance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bill492](https://clawhub.ai/user/bill492)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to audit installed OpenClaw skills for quality, duplicate functionality, structural gaps, stale files, and best-practice compliance before publishing or maintaining skill collections.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generated audit report may include local paths, skill names, and metadata about the user's setup.

Mitigation: Review .sub-agent-results/skill-audit-report.md before sharing it outside the local environment.

Risk: The audit reads local OpenClaw skill directories and summarizes discovered skill metadata.

Mitigation: Run it only in workspaces where local skill discovery is intended and where the resulting report can be handled appropriately.

## Reference(s):

- [Anthropic: Lessons from Building Claude Code Skills](https://x.com/trq212/status/2033949937936085378)
- [Ole Lehmann: Auto-improve Skills](https://x.com/itsolelehmann/status/2033919415771713715)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report with chat summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes audit results to .sub-agent-results/skill-audit-report.md.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
