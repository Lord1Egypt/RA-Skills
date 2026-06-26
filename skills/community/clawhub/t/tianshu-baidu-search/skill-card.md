## Description: <br>
Search the web using Baidu AI Search Engine (BDSE) for live information, documentation, and research topics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangshengli0421](https://clawhub.ai/user/wangshengli0421) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run live Baidu web searches for current information, documentation, and research topics when a Baidu AI Search API key is available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to Baidu through the Baidu AI Search API. <br>
Mitigation: Avoid placing secrets or sensitive private data in search queries and review Baidu's applicable terms before use. <br>
Risk: The skill requires a Baidu API key that may carry quota, billing, or account-access impact if exposed. <br>
Mitigation: Use a dedicated or revocable API key, keep it in environment configuration, and monitor usage. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wangshengli0421/tianshu-baidu-search) <br>
- [Baidu AI Search API Key Console](https://console.bce.baidu.com/ai-search/qianfan/ais/console/apiKey) <br>
- [Baidu AI Search Web Search Endpoint](https://qianfan.baidubce.com/v2/ai_search/web_search) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration instructions] <br>
**Output Format:** [JSON search result references from a Node.js command-line script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BAIDU_API_KEY and accepts query, count, and freshness parameters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
