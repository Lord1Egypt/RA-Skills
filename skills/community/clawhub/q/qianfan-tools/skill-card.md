## Description: <br>
Baidu Qianfan Tools integrates multiple Baidu Qianfan Platform APIs for search, hotword lookup, text generation, continuation, image generation, OCR, PPT generation, and academic search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yingyangdao](https://clawhub.ai/user/yingyangdao) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to call Baidu Qianfan services from an agent workflow for web search summaries, hot topics, text and image generation, OCR, PPT generation, and academic search. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User prompts, search queries, image URLs, and generated or extracted content are sent to Baidu Qianfan services for processing. <br>
Mitigation: Do not submit secrets, regulated data, private documents, or sensitive image URLs unless this external processing is approved for the intended use. <br>
Risk: The skill uses a Baidu API key and some API calls may consume quota or incur billing charges. <br>
Mitigation: Use a dedicated API key with quota or billing limits, keep configuration and environment values private, and enable only the Baidu APIs needed for the deployment. <br>


## Reference(s): <br>
- [Baidu Qianfan Console](https://console.bce.baidu.com/qianfan/) <br>
- [Baidu Qianfan API Documentation](https://cloud.baidu.com/doc/qianfan-api/s/3m9b5lqft) <br>
- [ClawHub Skill Page](https://clawhub.ai/yingyangdao/qianfan-tools) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, API Calls, Shell commands, Configuration] <br>
**Output Format:** [JSON results and command-line output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BAIDU_API_KEY; some Baidu Qianfan APIs require activation and may incur usage charges.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata, _meta.json, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
