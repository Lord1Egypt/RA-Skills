## Description:

RelayAPI helps agents post to 22 social and messaging platforms and manage accounts, workspaces, media, scheduling, analytics, inbox activity, and webhooks through a unified API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zanhk](https://clawhub.ai/user/zanhk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to prepare and execute RelayAPI API calls for cross-platform social publishing, account management, analytics, inbox responses, and webhook workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish posts, delete content, send messages, moderate comments, disconnect accounts, and create or change webhooks.

Mitigation: Require explicit confirmation of the exact account, workspace, target platforms, content, and action before any write action.

Risk: A RelayAPI API key grants access to connected social accounts and workspaces.

Mitigation: Store RELAYAPI_API_KEY in a secret manager, never paste it into chat, and use the skill only with RelayAPI accounts the user trusts.

Risk: Immediate publishing is asynchronous and can later become partial or failed.

Mitigation: Check post status after creation or configure webhooks for publication results before treating a post as complete.

## Reference(s):

- [RelayAPI ClawHub Skill](https://clawhub.ai/zanhk/skills/relayapi)
- [RelayAPI Homepage](https://relayapi.dev)
- [RelayAPI API Docs](https://api.relayapi.dev/docs)
- [RelayAPI OpenAPI Spec](https://api.relayapi.dev/openapi.json)

## Skill Output:

**Output Type(s):** [Shell commands, JSON payloads, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands, JSON examples, and API guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires RELAYAPI_API_KEY and curl; generated API calls may perform reads, writes, publishing, moderation, messaging, account changes, and webhook changes.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
