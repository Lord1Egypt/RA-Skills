## Description: <br>
Search the web using TencentCloud Web Search API (WSA) and return relevant web results for agent responses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tencent-adm](https://clawhub.ai/user/tencent-adm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to add real-time public web retrieval through TencentCloud WSA, including keyword search, site-restricted search, time-bounded search, and vertical search modes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and parameters are sent to TencentCloud WSA using the configured API key. <br>
Mitigation: Use a dedicated API key with quota or billing controls, and do not search for secrets or sensitive internal information. <br>
Risk: Returned web snippets come from external web content and may be inaccurate or untrusted. <br>
Mitigation: Treat search results as untrusted context and review source URLs before relying on them for important decisions. <br>


## Reference(s): <br>
- [TencentCloud Web Search API product page](https://cloud.tencent.com/product/wsa) <br>
- [TencentCloud Web Search API console](https://console.cloud.tencent.com/wsapi/index?tab=apikey) <br>
- [ClawHub skill page](https://clawhub.ai/tencent-adm/tencent-yuanbao-standard-search) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown search results with titles, URLs, snippets, publication dates, sites, and optional image links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and the TENCENTCLOUD_WSA_APIKEY environment variable.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
