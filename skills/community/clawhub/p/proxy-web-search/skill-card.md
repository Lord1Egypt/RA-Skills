## Description:

Proxy Web Search performs web searches through an OpenClaw Manager Web Search Proxy configured with the WEB_SEARCH_PROXY_URL environment variable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whyhit2005](https://clawhub.ai/user/whyhit2005)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to retrieve current web search results through an approved OpenClaw Manager proxy, including optional engine selection, recency filtering, and result count control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to the configured OpenClaw Manager Web Search Proxy, which may expose sensitive prompts or proprietary terms to that proxy.

Mitigation: Install only with a trusted and approved proxy, prefer a trusted HTTPS WEB_SEARCH_PROXY_URL, and avoid sending secrets, credentials, private incident details, or proprietary terms unless the proxy is approved for that data.

Risk: The skill is unavailable when WEB_SEARCH_PROXY_URL is unset or points to an unavailable proxy.

Mitigation: Configure WEB_SEARCH_PROXY_URL before use and verify that the OpenClaw Manager Web Search Proxy is running and reachable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/whyhit2005/skills/proxy-web-search)
- [Publisher Profile](https://clawhub.ai/user/whyhit2005)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Guidance]

**Output Format:** [JSON search responses and Markdown usage guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and WEB_SEARCH_PROXY_URL; default engine is search_pro_quark with 25 results.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
