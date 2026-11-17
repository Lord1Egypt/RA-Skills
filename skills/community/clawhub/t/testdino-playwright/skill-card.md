## Description:

Connect OpenClaw to TestDino for real-time Playwright CI intelligence. Ask about test failures, flaky tests, run history, and CI health in plain English.

This skill is ready for commercial/non-commercial use.

## Publisher:

[testdino-inc](https://clawhub.ai/user/testdino-inc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and QA engineers use this skill to query TestDino from OpenClaw for Playwright CI failures, flaky tests, run history, manual test cases, merge readiness, and recurring CI alerts or digests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on broad shell execution to call mcporter and TestDino tools.

Mitigation: Review exec approvals before use and limit approved commands to the required TestDino workflow.

Risk: The skill stores or reuses a TestDino personal access token in local configuration.

Mitigation: Use a narrowly scoped or read-only TestDino token where possible, avoid duplicating it across files, and protect token-bearing configuration files.

Risk: The setup flow installs npm packages and may use unpinned package versions.

Mitigation: Prefer pinned, reviewed package versions and verify packages before installing them globally.

Risk: Cron examples can include gateway tokens in shell commands.

Mitigation: Avoid pasting real gateway tokens into shell history and use safer secret-handling practices when configuring scheduled jobs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/testdino-inc/skills/testdino-playwright)
- [Publisher profile](https://clawhub.ai/user/testdino-inc)
- [OpenClaw documentation](https://openclaw.dev)
- [mcporter npm package](https://www.npmjs.com/package/mcporter)
- [testdino-mcp npm package](https://www.npmjs.com/package/testdino-mcp)
- [TestDino application](https://app.testdino.com)
- [TestDino documentation](https://docs.testdino.com)
- [README](artifact/README.md)
- [Failure alert example](artifact/examples/alert-setup.md)
- [Morning digest example](artifact/examples/morning-digest.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses should be concise and grounded in TestDino API responses.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
