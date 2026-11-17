## Description:

Connects OpenClaw agents with n8n workflows through webhook triggers, result callbacks, token validation, and observability hooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuyonghao-123](https://clawhub.ai/user/yuyonghao-123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this skill to let n8n workflows trigger OpenClaw agent actions and receive execution results for follow-on workflow steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Webhook callbacks can send execution results and the configured token to caller-supplied callback URLs.

Mitigation: Restrict callback URLs to trusted n8n endpoints and avoid forwarding authentication tokens to callback targets.

Risk: The artifact documents and implements a default webhook token.

Mitigation: Replace the default token with a strong unique secret stored in the environment before enabling the webhook server.

Risk: The n8n client can access workflows, executions, and credentials when configured with an API key.

Mitigation: Use least-privilege n8n API credentials and review permissions before enabling workflow deletion or credential access.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yuyonghao-123/skills/yuyonghao-n8n-integration)
- [n8n Documentation](https://docs.n8n.io/)
- [n8n Webhook Node](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.webhook/)
- [n8n HTTP Request Node](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.httprequest/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript and shell command examples plus JSON workflow configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include webhook endpoint settings, authentication token guidance, callback configuration, and n8n workflow JSON examples.]

## Skill Version(s):

0.1.1 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
