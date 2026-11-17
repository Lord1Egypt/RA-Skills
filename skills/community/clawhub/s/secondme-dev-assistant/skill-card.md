## Description:

Helps developers build and maintain SecondMe platform integrations, including third-party app setup, OAuth, MCP integration, API usage, scaffolding guidance, review submission, and release maintenance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daihaochen-mv](https://clawhub.ai/user/daihaochen-mv)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and platform engineers use this skill to plan, configure, and maintain SecondMe third-party apps and integrations. It supports OAuth credential handling, MCP-compatible integration design, open API usage, app scaffolding briefs, review submission, and release maintenance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run unpinned self-update tooling automatically during pre-flight checks.

Mitigation: Require explicit user approval before update commands and pin the update source or version before installation.

Risk: The skill stores SecondMe credentials and local telemetry state under the user's home directory.

Mitigation: Use a secret store or strict file permissions, avoid printing secrets, and review persisted files before deployment.

Risk: OAuth state mismatch handling can be relaxed for trusted WebView scenarios, which can weaken CSRF protection.

Mitigation: Fail closed on OAuth state mismatches unless the app explicitly targets a trusted WebView and documents the CSRF tradeoff.

Risk: Telemetry behavior writes local usage events when enabled.

Mitigation: Keep telemetry consent explicit, allow opt-out, and verify that logs do not include code, file paths, credentials, or personal information.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/daihaochen-mv/skills/secondme-dev-assistant)
- [App Bootstrap](references/app-bootstrap.md)
- [Requirements And Scaffold Plan](references/requirements-scaffold.md)
- [Implementation Guidance And SecondMe Standards](references/implementation-guidance.md)
- [Open APIs For Third-Party Developers](references/open-apis.md)
- [MCP And Integration Implementation Guidance](references/mcp-integration.md)
- [Control Plane Operations](references/control-plane.md)
- [Release And Maintenance](references/release-maintenance.md)
- [Feedback Preference Flow](references/feedback-prompt.md)
- [SecondMe Develop](https://develop.second.me)
- [SecondMe API Reference](https://develop-docs.second.me/zh/docs/api-reference/secondme)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, API calls]

**Output Format:** [Markdown guidance with inline code, command snippets, JSON payloads, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May inspect local code, draft implementation briefs, and perform authenticated SecondMe control-plane actions when the user confirms write operations.]

## Skill Version(s):

2.1.0 (source: server release evidence and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
