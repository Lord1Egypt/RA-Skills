## Description:

Manage Typeform forms, responses, themes, workspaces, and webhooks via the Typeform API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to manage Typeform survey workflows from chat, including forms, responses, themes, workspaces, settings, and webhooks through a connected Typeform account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access Typeform forms and responses that may contain personal data.

Mitigation: Install only if the Typeform account connection is appropriate, handle response data according to privacy requirements, and revoke the connection when it is no longer needed.

Risk: Write actions can create, update, archive, or delete Typeform resources, including irreversible deletion of forms or responses.

Mitigation: Use preview and explicit user confirmation before destructive or state-changing actions.

Risk: Webhook registration and workspace operations may have account, permission, plan, or public HTTPS endpoint requirements.

Mitigation: Verify the live Typeform tool catalog, account permissions, plan limits, and webhook URL requirements before execution.

## Reference(s):

- [Typeform Developer Documentation](https://www.typeform.com/developers/)
- [Typeform API Reference](https://www.typeform.com/developers/get-started)
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=typeform-surveys)
- [ClawLink Docs](https://docs.claw-link.dev/openclaw)
- [ClawLink Verification](https://claw-link.dev/verify)
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/skills/typeform-surveys)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls, text]

**Output Format:** [Markdown with inline bash commands and JSON tool parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses ClawLink-hosted Typeform OAuth connections and live tool discovery before execution.]

## Skill Version(s):

1.0.5 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
