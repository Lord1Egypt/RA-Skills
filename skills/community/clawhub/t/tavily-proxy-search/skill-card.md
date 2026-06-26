## Description: <br>
Search the web through a self-hosted TavilyProxyManager instance using Bearer master-key authentication while preserving the familiar tavily-search parameter style. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ugvfpdcuwfnh](https://clawhub.ai/user/ugvfpdcuwfnh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run Tavily-style web search, source gathering, quick research, and result summaries through a trusted self-hosted TavilyProxyManager endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends search queries and a Bearer master key to the configured TavilyProxyManager endpoint. <br>
Mitigation: Use only a proxy endpoint you operate or trust, prefer localhost or HTTPS for TAVILY_PROXY_URL, and use the least-privileged key available. <br>
Risk: An incorrect or untrusted proxy URL can expose credentials or return unexpected results. <br>
Mitigation: Verify TAVILY_PROXY_URL before use and avoid untrusted proxy hosts. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ugvfpdcuwfnh/tavily-proxy-search) <br>
- [Publisher profile](https://clawhub.ai/user/ugvfpdcuwfnh) <br>
- [TavilyProxyManager project](https://github.com/xuncv/TavilyProxyManager) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [JSON or Markdown search results with optional answer text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Result count is capped by the script and the proxy endpoint must return JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
