## Description:

Automates a Xiaohongshu posting workflow from news or topic search through copywriting, text-cover generation, and MCP-based note publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shaohaojie1](https://clawhub.ai/user/shaohaojie1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and social media operators use this skill to draft Xiaohongshu note content, generate a 3:4 text cover image, and publish through a local xiaohongshu-mcp service after reviewing login and publishing readiness.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow relies on third-party Xiaohongshu login and publishing executables that can access the user's account session.

Mitigation: Verify the upstream source and release artifacts before use, and run the MCP service in a constrained environment where possible.

Risk: Stored session cookies may expose or prolong access to the Xiaohongshu account.

Mitigation: Protect the cookie storage location, delete temporary cookies after use, and avoid sharing the runtime environment.

Risk: Automated publishing can post incorrect, misleading, or unintended title, body, tags, or images.

Mitigation: Require the agent to show the exact title, body, tags, and image paths for explicit approval before any publish call.

## Reference(s):

- [Xiaohongshu content template](references/content-template.md)
- [xiaohongshu-mcp configuration](references/mcp-config.md)
- [xiaohongshu-mcp project](https://github.com/xpzouying/xiaohongshu-mcp)
- [ClawHub skill page](https://clawhub.ai/shaohaojie1/skills/xiaohongshu-mcp-publisher)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python helper scripts and JSON API payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate PNG cover files and make local HTTP API calls to a Xiaohongshu MCP service when helper scripts are run.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
