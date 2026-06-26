## Description: <br>
Tavily quota-aware multi-key search router for reliable Tavily-backed web search across multiple API keys, automatic failover for invalid or rate-limited keys, official usage-based routing via Tavily's /usage endpoint, and status visibility for each key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fangtang0206](https://clawhub.ai/user/fangtang0206) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when they need quota-aware Tavily search across multiple user-provided API keys, automatic failover, and per-key usage visibility. It is useful when single-key search is not resilient enough or when quota must be balanced across keys. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads Tavily API keys from config/keys.json and uses them for outbound Tavily requests. <br>
Mitigation: Keep config/keys.json private, use only keys you control, and do not publish configured key files. <br>
Risk: Search queries and usage checks are sent to Tavily and may consume quota. <br>
Mitigation: Avoid sending secrets or sensitive internal text as queries, and review key status before high-volume use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fangtang0206/tavily-quota-router) <br>
- [Tavily Search API endpoint](https://api.tavily.com/search) <br>
- [Tavily Usage API endpoint](https://api.tavily.com/usage) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search and status commands may make Tavily API calls and consume quota.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
