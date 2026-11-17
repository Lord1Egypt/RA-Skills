## Description:

wxgzh-mcp helps agents manage WeChat Official Account drafts, including image uploads, draft creation, listing, deletion, and publishing after AppID, AppSecret, and IP allowlist configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[279458179](https://clawhub.ai/user/279458179)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators managing WeChat Official Account content use this MCP skill to create article drafts, upload cover and inline images, inspect drafts, and submit eligible drafts for publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live WeChat account credentials and access tokens can be exposed or misused.

Mitigation: Use a dedicated least-privilege WeChat account, keep AppID and AppSecret out of shared transcripts, avoid the token tool unless needed, and do not print tokens into logs.

Risk: Media upload tools can read and upload local files reachable by the server process.

Mitigation: Run the skill in an isolated environment with a restricted upload directory and only mount approved media paths.

Risk: Draft deletion and publishing operations can affect live account content.

Mitigation: Require explicit human confirmation before deleting drafts or submitting drafts for publishing.

Risk: Unpinned Python dependencies can change behavior between installs.

Mitigation: Pin and review dependencies before deployment.

## Reference(s):

- [WeChat Official Accounts Platform](https://mp.weixin.qq.com)
- [WeChat Official Account API Endpoint](https://api.weixin.qq.com/cgi-bin)
- [ClawHub skill page](https://clawhub.ai/279458179/skills/wxgzh-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, shell commands, API calls]

**Output Format:** [JSON tool results with Markdown setup and usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns WeChat access tokens, media identifiers, draft metadata, publish status, and operational messages.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and artifact/src/__init__.py)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
