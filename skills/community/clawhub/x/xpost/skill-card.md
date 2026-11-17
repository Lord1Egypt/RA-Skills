## Description:

Post to social media through xpost — draft, schedule, edit and check delivery across X, Instagram, LinkedIn, Facebook, TikTok, YouTube, Threads, Bluesky and Pinterest, with their brand rules enforced server-side and their approval where the project asks for it.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vladkorzinin](https://clawhub.ai/user/vladkorzinin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to create, schedule, edit, delete, take down, and review social posts across connected xpost accounts while respecting project guardrails and approval flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish, bulk post, edit, delete, or take down public social content through connected accounts.

Mitigation: Require clear confirmation of destination, timing, and content before publishing, bulk posting, editing, deleting, or taking down live posts.

Risk: The CLI/API fallback can use unpinned npx commands or API keys in sensitive environments.

Mitigation: Prefer the authenticated MCP connector; when CLI use is necessary, avoid bare unpinned npx commands in sensitive environments and handle XPOST_API_KEY according to local secrets policy.

Risk: Connected social accounts and uploaded media may expose sensitive brand or account content.

Mitigation: Install only when the publisher and xpost service are trusted with the connected social accounts and media provided by the user.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vladkorzinin/skills/xpost)
- [xpost MCP server](https://xpost.to/api/mcp)
- [xpost API base URL](https://xpost.to)
- [xpost OpenAPI specification](https://xpost.to/api/v1/openapi.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance]

**Output Format:** [Markdown guidance with inline shell commands, tool names, API routes, and JSON response details.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May initiate posting, scheduling, editing, deletion, take-down, media upload, delivery receipt, retry, and metrics workflows through the connected xpost MCP server, CLI, or API.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
