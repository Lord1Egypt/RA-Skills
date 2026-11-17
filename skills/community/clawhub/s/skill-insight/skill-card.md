## Description:

Understand what your AI agent's skills are actually being used for with usage reports, success and failure tracking, and unused-skill recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yingy4](https://clawhub.ai/user/yingy4)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to record, scan, report on, and analyze local skill usage so they can identify active skills, failures, and unused installed skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The session scanner reads recent conversation history and tool-call data more broadly than users may expect.

Mitigation: Review the skill before installing when sessions may contain secrets, private prompts, credentials, or sensitive tool arguments; prefer manual recording or narrowly scoped structured logs.

Risk: The cron setup can create recurring local scans and logs.

Mitigation: Only add the cron entry after confirming what local files and logs it creates and how to remove or disable them later.

## Reference(s):

- [ClawHub Skill Insight page](https://clawhub.ai/yingy4/skills/skill-insight)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown or terminal text with optional JSON report output and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports English and Chinese report output; writes local JSON usage and registry files when recording or scanning.]

## Skill Version(s):

1.0.8 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
