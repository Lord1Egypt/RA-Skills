## Description:

Provides Chinese lunar calendar utilities for BaZi, solar-lunar calendar conversion, Huangli, daily fortune, solar terms, and Wu Xing analysis through the XiaoBenYang API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cainingnk](https://clawhub.ai/user/cainingnk)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve Chinese lunar calendar, almanac, BaZi, Wu Xing, solar-term, and daily fortune results. The skill routes user-supplied dates and birth times to XiaoBenYang API tools and formats the returned data for the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores the XiaoBenYang API key in a local .env file in plaintext.

Mitigation: Use a throwaway or low-privilege API key, keep .env out of shared workspaces and source control, and rotate or remove the key when access is no longer needed.

Risk: The skill sends user-provided calendar and birth date/time information to the third-party XiaoBenYang API.

Mitigation: Avoid entering sensitive personal birth data and inform users that requests are sent to mcp.xiaobenyang.com.

Risk: The security verdict is suspicious because the skill presents as a calendar tool while requiring credential storage and third-party API transfer.

Mitigation: Review the skill and its network behavior before deployment, and install it only if the API key and data-sharing requirements are acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cainingnk/skills/xby-lunar-calendar)
- [XiaoBenYang API key portal](https://xiaobenyang.com)
- [XiaoBenYang MCP API endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Configuration, Guidance]

**Output Format:** [Markdown summaries derived from JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an XBY_APIKEY value before API-backed tools can return results.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
