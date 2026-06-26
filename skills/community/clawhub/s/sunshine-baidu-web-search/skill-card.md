## Description: <br>
Provides real-time web retrieval through the Baidu Qianfan web search API for current information, fact checking, and Baidu search queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Sunshine-del-ux](https://clawhub.ai/user/Sunshine-del-ux) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run Baidu-backed web searches from an agent when a request needs current information, fact checking, or source-backed results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to Baidu Qianfan and may include sensitive user-provided terms. <br>
Mitigation: Use the skill only for clear web-search or current-information requests, and avoid submitting secrets or private data as search queries. <br>
Risk: The skill requires a Baidu API key for authenticated search requests. <br>
Mitigation: Configure BAIDU_API_KEY through trusted OpenClaw or ClawHub settings or a private local config, and do not share the key in chats, logs, screenshots, or generated output. <br>


## Reference(s): <br>
- [Baidu Qianfan API documentation](https://cloud.baidu.com/doc/qianfan-api/s/Wmbq4z7e5) <br>
- [LeiAIBot publisher website](https://leiaibot.com) <br>
- [ClawHub skill page](https://clawhub.ai/Sunshine-del-ux/sunshine-baidu-web-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [JSON search results with agent-authored text or markdown answers] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BAIDU_API_KEY and sends search terms to Baidu Qianfan.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
