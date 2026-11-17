## Description:

Use when using ZeroToken MCP via OpenClaw for browser automation, trajectory recording and low-token replay, especially for recurring or scheduled browser tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amos144](https://clawhub.ai/user/amos144)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to guide agents through ZeroToken MCP setup, browser trajectory recording, reusable script generation, and low-token replay for recurring or scheduled browser tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser replay can affect accounts that post, purchase, or access sensitive data.

Mitigation: Review saved scripts and default variables before unattended execution, especially for privileged accounts.

Risk: Dependency installation and browser automation can expand local execution risk.

Mitigation: Install from trusted package sources, prefer pinned versions or an isolated environment, and avoid elevated privileges.

Risk: Scripts with unresolved variables or many fuzzy points may fail or behave unexpectedly during unattended replay.

Mitigation: Provide required runtime variables, audit sessions after replay, and use human review where the page requires judgment.

## Reference(s):

- [ZeroToken project homepage](https://github.com/AMOS144/zerotoken)
- [ClawHub skill page](https://clawhub.ai/amos144/skills/zerotoken)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides agents to call ZeroToken MCP browser, trajectory, script, and session tools; generated scripts and trajectories are handled by the MCP service.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
