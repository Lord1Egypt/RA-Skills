## Description:

Fetches a specific web page URL through a configured OpenClaw Manager proxy and returns parsed Markdown or plain text with optional metadata, image, and link summary controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whyhit2005](https://clawhub.ai/user/whyhit2005)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to fetch a known web page by URL and convert its content into Markdown or plain text for reading, summarization, or extraction workflows. It is for direct URL fetching, not keyword web search.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Secret-bearing, internal, regulated, or credential-token URLs could expose sensitive page content to the configured proxy.

Mitigation: Use only an approved and trusted OpenClaw Manager Web Fetch Proxy, and avoid those URLs unless the proxy is approved for that data.

Risk: The shell wrapper is a convenience interface with weak validation for options such as timeout and return format.

Mitigation: Use normal trusted option values, review commands before execution, and prefer direct proxy calls or stronger wrappers for automation.

Risk: Fetched web content is untrusted and may contain instructions or misleading text that should not automatically control agent behavior.

Mitigation: Treat fetched content as data, review it before acting on it, and keep agent/system instructions separate from page content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/whyhit2005/skills/proxy-web-fetch)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [JSON response containing parsed page content in Markdown or plain text, page metadata, and optional image or link summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and WEB_FETCH_PROXY_URL; supports timeout, cache, image retention, GFM, image summary, and link summary options.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
