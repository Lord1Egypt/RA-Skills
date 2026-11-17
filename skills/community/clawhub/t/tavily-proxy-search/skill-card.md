## Description:

Searches the web through a self-hosted TavilyProxyManager instance using Bearer master-key authentication while preserving familiar tavily-search parameters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ugvfpdcuwfnh](https://clawhub.ai/user/ugvfpdcuwfnh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run Tavily-style web searches, gather sources, and return compact result summaries through an already deployed TavilyProxyManager endpoint.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and returned content pass through the configured TavilyProxyManager endpoint, so an untrusted proxy operator could observe or alter traffic.

Mitigation: Use a trusted local loopback proxy or an HTTPS endpoint with a valid certificate, and avoid sending sensitive queries through untrusted proxy infrastructure.

Risk: The default proxy URL uses plaintext HTTP on localhost; remote plaintext use could expose the Bearer master key.

Mitigation: Keep the default limited to loopback, prefer HTTPS for remote endpoints, and rotate the master key if it may have crossed remote plaintext HTTP.

## Reference(s):

- [TavilyProxyManager](https://github.com/xuncv/TavilyProxyManager)
- [ClawHub Skill Page](https://clawhub.ai/ugvfpdcuwfnh/skills/tavily-proxy-search)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON or Markdown search results, with setup and troubleshooting guidance in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Raw JSON includes query, optional answer, and title/url/content results; the brave-style JSON format uses title/url/snippet results.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
