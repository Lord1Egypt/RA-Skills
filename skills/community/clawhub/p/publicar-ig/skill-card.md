## Description:

Publishes photos, carousels, or reels to a user's Instagram for Business account through the user's connected Zapier MCP workflow, requiring a full preview and explicit confirmation before posting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[formula100k](https://clawhub.ai/user/formula100k)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use this skill to prepare and publish Instagram photos, carousels, and reels from local media or public media URLs. It is intended for Instagram for Business accounts connected through Zapier MCP and includes preview, caption, location, tagging, and confirmation steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local media may be uploaded to a public GitHub repository before publication.

Mitigation: Verify the repository owner and name before first use, avoid sensitive or private media, and only proceed when public hosting is acceptable.

Risk: The skill can publish content to Instagram through the user's connected account.

Mitigation: Require a full preview and an explicit confirmation tied to the displayed media and caption before any publish action.

Risk: Ambiguous account or repository scoping can result in publishing through the wrong connected target.

Mitigation: Confirm the Instagram account, stored page ID, and GitHub asset repository before publishing, especially on first use or when multiple accounts are connected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/formula100k/skills/publicar-ig)
- [ClawHub publisher profile](https://clawhub.ai/user/formula100k)
- [Zapier MCP configuration](https://mcp.zapier.com)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, Markdown]

**Output Format:** [Markdown guidance with inline shell commands and Zapier MCP action parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces preview text, media URL handling steps, Zapier MCP publish calls, and success or failure reports for Instagram posting.]

## Skill Version(s):

1.0.0 (source: release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
