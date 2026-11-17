## Description:

Enhanced Tavily search with intelligent intent recognition, source preferences, critical source validation, and offline report generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fundou1081](https://clawhub.ai/user/fundou1081)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use this skill to run Tavily-backed web searches with intent recognition, preferred-source routing, critical-source checks, and optional Markdown report export.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tavily credentials are required and may be exposed to this integration.

Mitigation: Use dedicated Tavily keys with appropriate limits and rotate or revoke them if the skill is no longer trusted.

Risk: Changing TAVILY_BASE_URL can route searches and credentials to a non-default endpoint.

Mitigation: Leave TAVILY_BASE_URL unset unless the replacement endpoint is controlled and trusted.

Risk: Report export can persist sensitive query and result data locally.

Mitigation: Disable report export for sensitive searches unless local persistence under the OpenClaw workspace is acceptable.

## Reference(s):

- [Tavily API endpoint](https://api.tavily.com)
- [ClawHub skill page](https://clawhub.ai/fundou1081/skills/tavily-web-seeker)
- [Publisher profile](https://clawhub.ai/user/fundou1081)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON search responses, Markdown reports, and concise agent guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Tavily API key configuration; optional report export writes Markdown files under the OpenClaw workspace.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
