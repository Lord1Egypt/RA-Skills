## Description:

Generate AI images and video, build TikTok slideshows, manage AI influencers, and schedule posts to TikTok / Instagram / YouTube / X through the Supapost MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[supapost-dev](https://clawhub.ai/user/supapost-dev)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, developers, and operators use this skill to guide agents through Supapost content generation, AI influencer workflows, and scheduled posting across connected social accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys and connected social accounts can grant content-management and posting access.

Mitigation: Use a narrowly scoped, revocable Supapost API key and avoid placing real tokens in project files, logs, prompts, or shared configuration.

Risk: The skill can guide agents to schedule posts, publish drafts, and change influencer or project state.

Mitigation: Require explicit user confirmation before scheduling, publishing drafts, deleting resources, or changing influencer and project records.

Risk: Package execution guidance can run unpinned dependencies during setup.

Mitigation: Review commands before execution, pin package versions where possible, and install only in environments approved for Supapost access.

## Reference(s):

- [Supapost OpenClaw developer page](https://supapost.so/developers/openclaw)
- [Supapost MCP documentation](https://supapost.so/developers/mcp)
- [Supapost MCP endpoint](https://mcp.supapost.so)
- [Supapost developer portal](https://developers.supapost.so)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration snippets, and tool-call instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Supapost API key and a connected Supapost MCP server for live tool use.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter says 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
