## Description: <br>
Zhipu Web Search lets agents run web searches through Zhipu AI's web_search API using curl, with configurable engine, result count, recency, and intent options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whyhit2005](https://clawhub.ai/user/whyhit2005) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to retrieve current web information through a Zhipu API key, including searches with selected engines, result counts, recency filters, and optional intent recognition. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to Zhipu/BigModel under the configured Zhipu account. <br>
Mitigation: Avoid secrets or confidential material in queries, use a revocable API key where possible, and rotate the key when the skill is no longer needed. <br>
Risk: The script requires a ZHIPU_API_KEY environment variable and uses it in an Authorization header. <br>
Mitigation: Store the API key in the runtime environment rather than in skill files, logs, prompts, or shared shell history. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/whyhit2005/zhipu-web-search) <br>
- [Zhipu web_search API endpoint](https://open.bigmodel.cn/api/paas/v4/web_search) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Configuration instructions, JSON] <br>
**Output Format:** [JSON responses from the Zhipu web_search API, with Markdown documentation and bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and the ZHIPU_API_KEY environment variable; defaults to search_pro_quark with 20 results.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
