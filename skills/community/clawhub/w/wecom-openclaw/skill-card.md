## Description:

Integrates WeChat Work (Enterprise WeChat) with OpenClaw so agents can configure bidirectional messaging, verify and decrypt webhook payloads, and send asynchronous AI replies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[richagain](https://clawhub.ai/user/richagain)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to deploy and configure a Node.js adapter that receives WeChat Work messages, routes text to OpenClaw, and sends asynchronous replies through the WeChat Work API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The adapter handles sensitive enterprise chat content and credentials while bridging an internet-facing WeChat Work webhook to a local OpenClaw service.

Mitigation: Review before installing and use only in a controlled environment until webhook authentication, log handling, .env permissions, loopback binding, and dependency pinning meet deployment requirements.

Risk: Stale or replayed webhook requests could cause repeated or unauthorized processing if replay controls are absent.

Mitigation: Reject stale timestamps and duplicate message IDs before routing content to OpenClaw or sending WeChat Work replies.

Risk: AI replies could expose sensitive data from prompts, credentials, logs, or local context.

Mitigation: Apply response filtering, sanitize logs, restrict credential file permissions, and avoid logging full tokens or message content in production.

## Reference(s):

- [WeChat Work + OpenClaw Setup Guide](artifact/references/setup-guide.md)
- [Security Guide](artifact/references/security-guide.md)
- [WeChat Work Admin Console](https://work.weixin.qq.com)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands, environment configuration, and deployable JavaScript code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a local adapter deployment flow, .env template, and setup and security hardening guidance.]

## Skill Version(s):

1.0.0 (source: evidence.json release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
