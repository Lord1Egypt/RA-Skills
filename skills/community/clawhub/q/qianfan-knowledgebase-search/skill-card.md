## Description: <br>
Search knowledge from Qianfan Knowledgebase. Use this when you need to retrieve information from user's private knowledge bases on Baidu Qianfan platform. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hannatao](https://clawhub.ai/user/hannatao) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users use this skill to query private Baidu Qianfan knowledge bases from an agent workflow and retrieve structured chunks with scores and metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and selected knowledge-base IDs are sent to Baidu Qianfan using the configured API key. <br>
Mitigation: Use the skill only for intended Qianfan searches, avoid placing unnecessary secrets in queries, and configure an appropriately scoped BAIDU_API_KEY. <br>


## Reference(s): <br>
- [Qianfan KnowledgeBase Search on ClawHub](https://clawhub.ai/hannatao/qianfan-knowledgebase-search) <br>
- [Baidu Qianfan Knowledgebase Search API endpoint](https://qianfan.baidubce.com/v2/knowledgebases/search) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Shell commands, Configuration instructions] <br>
**Output Format:** [JSON response printed to stdout with setup and invocation guidance in Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, BAIDU_API_KEY, and either request-supplied knowledgebase IDs or QIANFAN_KNOWLEDGEBASE_IDS.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
