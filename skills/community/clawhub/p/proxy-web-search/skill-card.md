## Description: <br>
Proxy Web Search lets an agent perform web searches through a user-configured OpenClaw Manager Web Search Proxy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whyhit2005](https://clawhub.ai/user/whyhit2005) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve current web information, choose supported search engines, and apply result count, recency, or domain filters through an OpenClaw Manager proxy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to the configured OpenClaw Manager proxy and may be forwarded to search providers. <br>
Mitigation: Use only a trusted WEB_SEARCH_PROXY_URL and avoid submitting secrets, private personal data, or sensitive internal prompts as search queries. <br>
Risk: The skill depends on an external proxy and curl being available at runtime. <br>
Mitigation: Confirm curl is installed and WEB_SEARCH_PROXY_URL points to a reachable, intended OpenClaw Manager Web Search Proxy before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/whyhit2005/proxy-web-search) <br>
- [Publisher profile](https://clawhub.ai/user/whyhit2005) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [JSON search responses and Markdown usage guidance with bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, WEB_SEARCH_PROXY_URL, and a reachable OpenClaw Manager Web Search Proxy.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
