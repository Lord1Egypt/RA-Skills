## Description: <br>
A skill for retrieving Shenzhen local news and information, helping users quickly access various news updates from Shenzhen. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenefei](https://clawhub.ai/user/chenefei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Media professionals, business users, technology professionals, and Shenzhen residents use this skill to find current Shenzhen news, policy updates, business activity, technology developments, and local-life information. <br>

### Deployment Geography for Use: <br>
Global; content focus is Shenzhen, China. <br>

## Known Risks and Mitigations: <br>
Risk: News, policy, business, or financial information from web search and third-party sources may be stale, incomplete, or inaccurate. <br>
Mitigation: Verify important information against official sources before relying on it for decisions. <br>
Risk: Scheduled summaries can run repeatedly if HEARTBEAT.md is configured. <br>
Mitigation: Configure recurring HEARTBEAT.md tasks only when regular automatic Shenzhen news summaries are intended. <br>


## Reference(s): <br>
- [Shenzhen News Reference Sources](references/news-sources.md) <br>
- [Shenzhen Special Zone Daily](https://www.dutenews.com/) <br>
- [Shenzhen Business Daily](http://www.sznews.com/) <br>
- [Shenzhen TV](https://www.sztv.com.cn/) <br>
- [Shenzhen Science and Technology Innovation Commission](http://stic.sz.gov.cn/) <br>
- [Qianhai Administration](https://www.szqh.gov.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Configuration] <br>
**Output Format:** [Markdown news summaries with source links and optional HEARTBEAT.md scheduling snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses web search and third-party news sources; no code installation or credentials are requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
