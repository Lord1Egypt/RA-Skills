## Description:

Guides AI agents to reduce verbose command output using vx-managed filters, compact modes, and focused GitHub and CI queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loonghao](https://clawhub.ai/user/loonghao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to guide AI agents through builds, tests, linting, and GitHub or CI work while keeping command output concise.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Posting issue or PR updates without authorization or exposing sensitive internal details.

Mitigation: Require explicit authorization before posting and omit internal IDs, paths, hostnames, and other sensitive details.

Risk: Aggressive output filtering can omit details needed to diagnose failed commands.

Mitigation: Retain full logs when troubleshooting and inspect them if filtered summaries are insufficient.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/loonghao/skills/vx-agent-workflow)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Markdown with inline shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Focused output filters and token-savings suggestions]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
