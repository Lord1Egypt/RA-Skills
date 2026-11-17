## Description:

Helps developers build a WeCom voice assistant for individual and group messages, calls, task follow-up, and call summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fyniujin](https://clawhub.ai/user/fyniujin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and enterprise teams use this skill to handle WeCom voice and text interactions, route calls, assign follow-up tasks, and produce call summaries and reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unauthenticated webhook requests can impersonate users and modify local workflow records.

Mitigation: Do not expose the webhook publicly until WeCom signature, token, and AES validation, replay protection, request size limits, and authorization checks are implemented; meanwhile keep it local or behind an authenticated reverse proxy.

Risk: Supervisor webhooks may send business data to untrusted destinations without verified TLS.

Mitigation: Disable supervisor webhooks until TLS verification is restored and destinations are allowlisted.

Risk: Local call records and ticket databases contain sensitive business information.

Mitigation: Restrict access to local ~/.wecom_voice data and ticket databases and review retention and access controls before deployment.

## Reference(s):

- [Step-by-step setup](references/step_by_step_setup.md)
- [WeCom bot API](references/wecom_bot_api.md)
- [ClawHub release](https://clawhub.ai/fyniujin/skills/wecom-voice-agent)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration instructions, Shell commands]

**Output Format:** [Text or Markdown with configuration and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include task confirmations, call summaries, and reports.]

## Skill Version(s):

2.9.0 (source: server release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
