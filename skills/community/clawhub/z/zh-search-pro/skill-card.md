## Description: <br>
Helps agents search Chinese-language content across Baidu, Bing China, WeChat, Zhihu, Toutiao, 360 Search, and other engines with advanced query syntax and time filters, without requiring an API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[careytian-ai](https://clawhub.ai/user/careytian-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to find Chinese-language market research, content ideas, academic material, public discussion, and SEO signals through common search engines from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms may be disclosed to the selected third-party search engine. <br>
Mitigation: Avoid sensitive, confidential, personal, or regulated data in search queries and choose engines appropriate for the user's data handling expectations. <br>
Risk: The broad search trigger can make the skill available for general search requests. <br>
Mitigation: Confirm the user wants a Chinese-focused search workflow before applying this skill to broad or ambiguous search requests. <br>
Risk: Some target search engines may present anti-abuse checks or unavailable results. <br>
Mitigation: Retry only within acceptable use limits, switch to another listed engine when needed, and treat missing results as a retrieval limitation. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/careytian-ai/zh-search-pro) <br>
- [Usage examples](artifact/examples/usage-examples.md) <br>
- [Changelog](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Code, Guidance] <br>
**Output Format:** [Markdown with web_fetch call examples and search URL patterns] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are intended to guide agent-issued web_fetch searches against third-party search engines.] <br>

## Skill Version(s): <br>
1.0.0 (source: CHANGELOG, metadata.json, config.json, and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
