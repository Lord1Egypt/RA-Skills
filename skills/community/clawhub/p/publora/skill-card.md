## Description:

Publora API helps agents schedule, publish, draft, bulk-schedule, manage workspace users, configure webhooks, and retrieve LinkedIn analytics across supported social media platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sergebulaev](https://clawhub.ai/user/sergebulaev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, social media operators, and workspace administrators use this skill to have an agent work with the Publora API for drafting, scheduling, publishing, deleting, monitoring posts, configuring webhooks, and managing workspace users across connected social accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables broad public-posting, deletion, webhook, reaction, API-key, and workspace-management actions.

Mitigation: Require explicit user approval before publishing, bulk scheduling, deleting posts or reactions, creating webhooks, generating API keys, or acting on behalf of workspace users.

Risk: A Publora API key can authorize actions on real connected social accounts.

Mitigation: Use only a Publora API key the user intends the agent to use, keep workspace keys server-side, and prefer per-user API keys for client-facing scenarios.

Risk: Draft versus immediate-publish behavior may be unclear before a request is sent.

Mitigation: Confirm whether the user wants a draft, scheduled post, or immediate publication before calling posting endpoints for real accounts.

## Reference(s):

- [ClawHub Publora Skill](https://clawhub.ai/sergebulaev/skills/publora)
- [Publora](https://publora.com)
- [Publora Pricing](https://publora.com/pricing)
- [Publora API Docs](https://github.com/publora/publora-api-docs)
- [Publora API Base URL](https://api.publora.com/api/v1)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline JavaScript, Python, and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes REST endpoint guidance, request examples, platform constraints, authentication notes, and operational cautions.]

## Skill Version(s):

1.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
