## Description:

一个提供高级筛选功能和详细房源信息的Airbnb搜索桌面扩展，适用于旅行规划和房源研究。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cainingnk](https://clawhub.ai/user/cainingnk)

### License/Terms of Use:

MIT-0

## Use Case:

Travel planners, researchers, and external users use this skill to search Airbnb listings with filters, pagination, and listing detail lookup, then review the returned listing data and direct links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores the Xiaobenyang API key in a local plaintext .env file.

Mitigation: Use only in trusted environments, limit key scope where possible, and document how users can rotate and delete the stored key.

Risk: Search parameters and the API key are sent to a third-party Xiaobenyang API.

Mitigation: Use the skill only when users trust Xiaobenyang with their Airbnb search parameters and credentials.

Risk: The Airbnb tools expose an ignoreRobotsText option.

Mitigation: Keep ignoreRobotsText disabled unless a reviewer has confirmed the request complies with applicable site rules and policy.

Risk: The package contains mismatched gaokao configuration remnants.

Mitigation: Remove stale school-exam configuration and naming before broad distribution to reduce user confusion and review ambiguity.

Risk: Dependencies are declared with minimum versions instead of pinned versions.

Mitigation: Pin dependencies for reproducible installation before broad distribution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cainingnk/skills/xby-airbnb-search)
- [Xiaobenyang API Key Page](https://xiaobenyang.com)
- [Xiaobenyang MCP API Endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls]

**Output Format:** [Markdown summary of JSON API results with direct Airbnb listing links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Xiaobenyang API key; search results may include pagination cursors and raw listing data.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
