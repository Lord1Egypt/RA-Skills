## Description:

Xhs Skills automates Xiaohongshu login, publishing, search and discovery, social interaction, and content operations through agent-routed commands and a browser bridge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zengfan-ai](https://clawhub.ai/user/zengfan-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to automate Xiaohongshu account workflows including login checks, content publishing, content discovery, commenting, likes, favorites, and multi-step content operations. It is intended for use with the user's own logged-in browser session and should be operated with explicit confirmation for publishing and social actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill and Chrome extension can broadly control a logged-in Xiaohongshu browser session.

Mitigation: Install only in trusted environments and use an account whose browser session you are comfortable delegating to the agent.

Risk: Sensitive login and browser data handling is under-disclosed.

Mitigation: Authenticate the bridge before use, remove or tightly limit generic JavaScript evaluation and cookie access, and avoid sending QR login data to third-party services by default.

Risk: Automated publishing or social actions can affect a real account.

Mitigation: Require explicit user confirmation before publishing, commenting, liking, or favoriting content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zengfan-ai/skills/xhs-skills)
- [Publisher profile](https://clawhub.ai/user/zengfan-ai)
- [Project homepage from ClawHub metadata](https://github.com/xpzouying/xiaohongshu-skills)
- [uv documentation](https://docs.astral.sh/uv/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON CLI result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CLI operations return JSON; analysis workflows may produce Markdown tables.]

## Skill Version(s):

1.0.0 (source: server release metadata and root SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
