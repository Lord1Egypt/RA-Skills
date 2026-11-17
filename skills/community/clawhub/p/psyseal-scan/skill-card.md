## Description:

Offline, read-only scan of your AI agent (OpenClaw, Hermes Agent, nanobot, PicoClaw, ZeroClaw, NanoClaw or any agent folder): what loads on every message, what heartbeats and scheduled tasks cost, plaintext secrets, and planted or bloated memory. No network, no dependencies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyseal](https://clawhub.ai/user/psyseal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent owners use this skill to review local agent configuration, instructions, memory, and skills for per-message loading, scheduled task costs, plaintext secrets, and planted or bloated memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks the skill suspicious due to weaknesses in its claimed filesystem boundaries and unpinned npm commands; inspection was incomplete and the tool-misuse analyzer was degraded.

Mitigation: Follow the security guidance: avoid installation unless you trust the publisher and accept unpinned npm execution and the reported symlink boundary weaknesses. Treat scan results as partial; they cannot establish that unreported behavior is safe.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/psyseal/skills/psyseal-scan)
- [Project homepage](https://github.com/psyseal/psyseal-scan)

## Skill Output:

**Output Type(s):** [Analysis, Text, JSON]

**Output Format:** [Text or JSON scan report with findings and suggested fixes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only scan; findings identify secret type, file, and line without exposing secret values or quoting memory text.]

## Skill Version(s):

0.3.3 (source: frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
