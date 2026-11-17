## Description:

Track AI agent costs in real time, set budget limits, and detect runaway loops while routing OpenAI, Anthropic, and Google model traffic through the Reivo proxy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tazsat0512](https://clawhub.ai/user/tazsat0512)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use Reivo to monitor AI API spending, configure budget limits, receive cost and defense status, route provider requests through Reivo, and get optimization guidance for OpenAI, Anthropic, and Google model usage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill routes AI-provider traffic through Reivo and shares usage metadata with that service.

Mitigation: Install only when that routing and metadata sharing match the user's data-handling requirements.

Risk: Budget, routing mode, and Slack webhook changes are authenticated account-level settings changes.

Mitigation: Require the user to confirm exact values before running commands that change those settings.

Risk: Optional self-hosted guardrail installs can depend on external package versions.

Mitigation: Prefer pinned package versions when installing self-hosted guardrail components.

## Reference(s):

- [Reivo homepage](https://reivo.dev)
- [Reivo dashboard](https://app.reivo.dev)
- [Reivo ClawHub page](https://clawhub.ai/tazsat0512/skills/reivo)
- [reivo-guard open-source guardrail engine](https://github.com/tazsat0512/reivo-guard)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-style status reports, setup guidance, shell commands, and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires REIVO_API_KEY and may call Reivo dashboard or proxy APIs when the generated commands are run.]

## Skill Version(s):

0.4.4 (source: evidence.release.version and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
