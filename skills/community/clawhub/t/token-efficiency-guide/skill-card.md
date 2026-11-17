## Description:

A documentation-only agent skill that guides OpenClaw operators through manual configuration, session, cron, and workspace changes for reducing Claude subscription token consumption.

This skill is ready for commercial/non-commercial use.

## Publisher:

[globalcaos](https://clawhub.ai/user/globalcaos)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill as a reference when diagnosing high Claude subscription usage and choosing manual changes to model selection, cron scheduling, session management, cache retention, and workspace file size.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Manual configuration changes can affect model selection, operating cost, and answer quality.

Mitigation: Review openclaw.json and AGENTS.md edits before applying them, and keep changes scoped to the documented settings.

Risk: Manual crontab entries can schedule recurring local work.

Mitigation: Inspect each crontab command, frequency, and model choice before enabling it.

Risk: The session archiver moves old session files when run with --apply.

Mitigation: Run it without --apply first, review the listed files, and confirm the archive location before scheduling or applying it.

## Reference(s):

- [GUIDE.md](artifact/GUIDE.md)
- [ClawHub skill page](https://clawhub.ai/globalcaos/skills/token-efficiency-guide)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only; no runtime tool calls, network access, writes, or credential access by the skill itself.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
