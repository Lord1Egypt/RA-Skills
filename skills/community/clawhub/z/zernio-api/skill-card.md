## Description:

Zernio API is an API reference for building integrations that schedule posts across 14 social media platforms, covering authentication, endpoints, webhooks, and platform-specific features.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mikipalet](https://clawhub.ai/user/mikipalet)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build Zernio API integrations for creating profiles, connecting social accounts, scheduling or publishing posts, configuring webhooks, uploading media, managing queues, and reading analytics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples include live posting, retry, DELETE, queue, media download, and webhook configuration operations that can affect connected social accounts or transmit data.

Mitigation: Review generated commands before execution, use test profiles or sandbox accounts first, and require explicit confirmation before running calls that publish, delete, retry, change queues, download media, or configure webhooks.

Risk: The skill uses Zernio API keys, app passwords, bot tokens, and webhook secrets in examples.

Mitigation: Keep credentials server-side, load them from environment variables or a secret manager, avoid logging them, and rotate any secret that appears in chat, code, logs, or shared files.

Risk: Webhook configuration examples can send event payloads to user-controlled URLs.

Mitigation: Use HTTPS endpoints, verify Zernio webhook signatures, scope webhook events to what the integration needs, and test delivery before enabling production workflows.

Risk: API behavior depends on third-party social platform permissions, rate limits, media limits, and token health.

Mitigation: Handle rate limits and platform-specific errors, check account health before publishing, and validate media constraints for each target platform.

## Reference(s):

- [Zernio API documentation](https://docs.zernio.com)
- [Zernio API base URL](https://zernio.com/api/v1)
- [Zernio dashboard](https://zernio.com/dashboard)
- [Zernio API keys](https://zernio.com/dashboard/api-keys)
- [ClawHub release page](https://clawhub.ai/mikipalet/skills/zernio-api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline curl, TypeScript, Python, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance for Zernio API usage; examples may describe live API calls that affect connected accounts when executed.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
