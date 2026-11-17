## Description:

Uses the Zhihu Open Platform through a CLI to search Zhihu and web content, retrieve hot lists, call Zhihu Direct Answer, and read the current user's own Zhihu creations, follows, and favorites.

This skill is ready for commercial/non-commercial use.

## Publisher:

[j3ffyang](https://clawhub.ai/user/j3ffyang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search Zhihu community content, web sources, and hot lists, or to work with their own account-scoped Zhihu content through the Zhihu Open Platform. It is suited for research, source discovery, and account-authorized content retrieval where original links and minimal necessary data access matter.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says the skill asks users to provide a full Zhihu Access Secret and stores it for future CLI use.

Mitigation: Use a secure host secret-entry path or out-of-band secret store when available, avoid echoing the secret in chat or logs, and revoke or rotate the Access Secret after testing.

Risk: The security evidence notes access to Zhihu Open Platform API quota and account-scoped public-range data.

Mitigation: Install only when this access is acceptable, authorize the minimum task needed, and monitor or stop calls when quota or frequency limits are reached.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/j3ffyang/skills/zhihu-for-opencode)
- [Zhihu Open Platform profile](https://developer.zhihu.com/profile)
- [CLI usage documentation](references/cli.md)
- [Zhihu Open Platform guide](references/open-platform.md)
- [HTTP API documentation](references/http-api.md)
- [User data API documentation](references/user-api.md)
- [OAuth application integration](references/oauth.md)
- [MCP integration documentation](references/mcp.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with source links, inline shell commands, and summarized CLI results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use account-scoped Zhihu API calls and return source URLs, excerpts, summaries, command output, or JSON-derived status.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
