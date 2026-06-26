## Description: <br>
联网搜索, 网页搜索, 实时联网, 一键配置。让 OpenClaw 用 Tavily 实现实时搜索（含免费额度）。One-step install + guided key setup. Guide: github.com/plabzzxx/openclaw-tavily-search <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[plabzzxx](https://clawhub.ai/user/plabzzxx) <br>

### License/Terms of Use: <br>


## Use Case: <br>
OpenClaw users and developers use this skill to add Tavily-backed real-time web search, page extraction, site crawling, and URL mapping to agent workflows. It is intended for guided local setup with a Tavily API key and concise command outputs for downstream agent use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries, URLs, extracted pages, crawls, and maps are sent to Tavily. <br>
Mitigation: Do not send secrets, private prompts, internal URLs, or sensitive sites through search, extract, crawl, or map unless Tavily is intended to receive them. <br>
Risk: The Tavily API key can be exposed if pasted into chat or committed to source control. <br>
Mitigation: Store the API key locally in an environment variable or ~/.openclaw/.env, avoid committing .env files, and prefer manual local editing for setup. <br>
Risk: Making Tavily the default fallback for web lookups can route more agent queries to an external service than expected. <br>
Mitigation: Review the optional memory preference before enabling Tavily as the default fallback for web lookup tasks. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/plabzzxx/tavily-one-step-search) <br>
- [Publisher profile](https://clawhub.ai/user/plabzzxx) <br>
- [Project guide](https://github.com/plabzzxx/openclaw-tavily-search) <br>
- [Tavily](https://tavily.com) <br>
- [Tavily API endpoint](https://api.tavily.com) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown, JSON, and Brave-like JSON emitted by a Node CLI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports search, extract, crawl, and map commands with domain, time, depth, proxy, timeout, retry, and output-format controls.] <br>

## Skill Version(s): <br>
1.0.3 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
