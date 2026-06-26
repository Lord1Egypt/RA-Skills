## Description: <br>
ZhiPu Search calls the Zhipu Web Search API with multiple search engines and returns structured search results suitable for agent processing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hulinying](https://clawhub.ai/user/hulinying) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to run web searches through the Zhipu/BigModel service and receive JSON results with titles, URLs, descriptions, site names, and publication dates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to the external Zhipu/BigModel API. <br>
Mitigation: Avoid putting secrets, personal data, or confidential business information into search queries. <br>
Risk: The skill requires a Zhipu API key and can also read it from config.json. <br>
Mitigation: Prefer ZHIPU_API_KEY, keep config.json private when used, and never output API-key values. <br>
Risk: Returned web results may be incomplete, stale, or misleading. <br>
Mitigation: Review important results before using them in decisions or downstream agent actions. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/hulinying/zhipu-ai-search) <br>
- [Publisher profile](https://clawhub.ai/user/hulinying) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Shell commands, Configuration] <br>
**Output Format:** [JSON search result object emitted by a Node.js command-line script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a ZHIPU_API_KEY environment variable or a private config.json file.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, _meta.json, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
