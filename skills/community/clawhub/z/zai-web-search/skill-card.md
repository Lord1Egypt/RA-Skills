## Description: <br>
Use ZHIPU AI's Web Search API to search the web, with optimization for Chinese content and support for four search engines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Tyduss](https://clawhub.ai/user/Tyduss) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to retrieve current web results through Z.AI, especially for Chinese-language queries, domain-filtered searches, and recency-filtered searches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and the API key are sent to the external Zhipu/Z.AI provider. <br>
Mitigation: Use a dedicated API key, store it outside screenshots and git, and avoid searching for secrets, private project data, or regulated personal information. <br>
Risk: Using this skill may incur paid API usage. <br>
Mitigation: Review Z.AI pricing and configure result count, engine, recency, and content size according to the user's cost tolerance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Tyduss/zai-web-search) <br>
- [Zhipu AI Open Platform](https://open.bigmodel.cn) <br>
- [Z.AI Web Search API documentation](https://open.bigmodel.cn/dev/api#web_search) <br>
- [Z.AI pricing](https://open.bigmodel.cn/pricing) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown, JSON, or compact plain text search results with URLs and snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search query is truncated to 70 characters by the CLI; result count, engine, intent recognition, recency, content size, and domain filter can be configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
