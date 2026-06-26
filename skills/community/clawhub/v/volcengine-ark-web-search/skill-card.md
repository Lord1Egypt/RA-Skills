## Description: <br>
Use when you need fresh web results through Volcengine ARK Responses API, especially for today's news, recent updates, fact checks, topic monitoring, or Chinese-language search workflows powered by ARK_API_KEY. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[henry-insomniac](https://clawhub.ai/user/henry-insomniac) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and agents use this skill to route current public web research through Volcengine ARK, then summarize results with explicit dates and source links. It is useful for recent news, fact checks, topic monitoring, and Chinese-language search workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search prompts are sent to Volcengine ARK using the user's API key. <br>
Mitigation: Avoid sending secrets, private documents, or regulated personal data unless that use is approved for the user's Volcengine account and policies. <br>
Risk: Overriding ARK_BASE_URL can send API requests to a different destination. <br>
Mitigation: Keep the default ARK endpoint unless the alternate base URL is trusted. <br>
Risk: Current web results can be thin, conflicting, or change over time. <br>
Mitigation: Preserve uncertainty, include source links when available, and use explicit dates for recent or relative-time claims. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/henry-insomniac/volcengine-ark-web-search) <br>
- [Volcengine Responses API documentation](https://www.volcengine.com/docs/82379/1783703?lang=zh) <br>
- [Volcengine Responses streaming article](https://developer.volcengine.com/articles/7563963410168569894) <br>
- [Volcengine web search article](https://developer.volcengine.com/articles/7565184101091639338) <br>
- [Volcengine web search API reference](https://www.volcengine.com/docs/82379/1958524?lang=zh) <br>
- [ARK Responses API Notes](references/ark-responses-api.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown summaries by default, with optional JSON or raw API responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and ARK_API_KEY; default output includes a title, summary, and sources when available.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
