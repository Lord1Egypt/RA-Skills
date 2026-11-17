## Description:

Zoho Social via MCP with action catalog, least-privilege profiles, portal/brand/channel helpers, media upload, and verified draft/schedule workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sprintcx](https://clawhub.ai/user/sprintcx)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to operate Zoho Social through an MCP endpoint, including resolving portals, brands, and channels, inspecting drafts and schedules, uploading media, and validating, scheduling, or publishing posts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide credentialed Zoho Social publishing, scheduling, deletion, and media upload workflows.

Mitigation: Use the smallest Zoho profile that fits the task, keep social-admin and deleteSocialSchedule disabled unless specifically needed, and require explicit confirmation before publish, schedule, or delete actions.

Risk: The MCP endpoint URL is a credential-bearing secret.

Mitigation: Treat the endpoint as a password and avoid printing, committing, logging, or copying it into chats, tickets, prompts, or repositories.

Risk: The shipped package is missing the advertised references/actions.jsonl catalog file, so catalog lookup helpers can fail until that file is restored.

Mitigation: Review before installing and restore or verify the action catalog before relying on lookup helper results.

Risk: The skill includes GitHub issue, pull request, and merge workflow guidance.

Mitigation: Require explicit confirmation before creating issues, opening pull requests, merging changes, or including any sanitized operational evidence.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sprintcx/skills/zoho-social-mcp)
- [Zoho Social MCP](https://mcp.zoho.eu)
- [Action Profiles](references/ACTION_PROFILES.md)
- [Catalog Format](references/CATALOG_FORMAT.md)
- [Common Workflows](references/COMMON_WORKFLOWS.md)
- [Multi-account Profiles](references/MULTI_ACCOUNT.md)
- [Profiles and Task Recipes](references/profiles.json)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide credentialed MCP calls and local helper scripts; users should review write actions before execution.]

## Skill Version(s):

1.0.2 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
