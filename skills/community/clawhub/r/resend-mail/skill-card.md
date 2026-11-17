## Description:

Manage Resend email campaigns, contacts, audiences, domains, templates, transactional sends, and related email workflows via the Resend API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to manage Resend account resources from an agent, including inspecting email activity, maintaining contacts, audiences, domains, templates, webhooks, and API keys, and sending or scheduling emails with explicit confirmation for write actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to activate a third-party plugin with broad authority over the connected Resend account, and the evidence does not pin the plugin version or document exact permissions.

Mitigation: Review the ClawLink plugin and account permissions before installing, connect only a Resend account you are comfortable managing through ClawLink, and require a clear preview plus explicit approval for high-impact actions.

Risk: Email sends, contact changes, domain changes, webhook changes, deletes, and API key operations can have irreversible or high-impact effects.

Mitigation: Use read and describe steps before write actions, verify the target resource and intended effect, preview the operation, and execute only after explicit user confirmation.

Risk: The available Resend tool catalog may differ from examples in the skill text.

Mitigation: Treat the live catalog as authoritative by listing, searching, or describing Resend tools before choosing a tool or parameters.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hith3sh/skills/resend-mail)
- [Resend API Documentation](https://resend.com/docs/api-reference/introduction)
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=resend-mail)
- [ClawLink Docs](https://docs.claw-link.dev/openclaw)
- [ClawLink Verification](https://claw-link.dev/verify)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON tool parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide connection setup and issue Resend tool calls through ClawLink after live catalog checks, previews, and explicit confirmation for write actions.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
