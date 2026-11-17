## Description:

Provides an MCP-style Bilibili API skill for video search, user lookup, user content retrieval, danmaku retrieval, collections, and related content analysis workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alinklab](https://clawhub.ai/user/alinklab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operators use this skill to route Bilibili search, user, video, danmaku, dynamic, submission, and collection queries through the XiaoBenYang API and return structured results for content management or analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores XBY_APIKEY in a local plaintext .env file, which can expose billing, quota, or private-data access if the project directory is shared, synced, committed, or has broad file permissions.

Mitigation: Provide XBY_APIKEY through a secure environment or secret manager where possible, ensure .env is ignored by version control, avoid shared or synced project directories, restrict file access, and rotate the key if exposure is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alinklab/skills/xby-bilibili)
- [XiaoBenYang API key portal](https://xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, JSON, API calls, configuration guidance]

**Output Format:** [Structured Python dictionaries with success, raw, and message fields, typically summarized to the user as text or Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires XBY_APIKEY before API calls; output content depends on upstream XiaoBenYang and Bilibili API responses.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
