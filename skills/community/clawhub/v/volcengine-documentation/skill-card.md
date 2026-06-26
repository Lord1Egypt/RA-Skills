## Description: <br>
火山引擎官方文档查询工具，支持文档检索和全文获取。涵盖火山引擎全部产品、开发者工具、服务支持、最佳实践，包括产品介绍、使用、计费、部署、故障排查、API、SDK、服务条款/协议等全流程。任何涉及火山引擎产品咨询、使用问题、文档查询的需求都优先调用本技能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[volc-sdk-team](https://clawhub.ai/user/volc-sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to search official Volcengine documentation and fetch full documentation pages when answering product, API, SDK, billing, deployment, troubleshooting, and service-support questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User queries and supplied documentation URLs are sent to Volcengine's documentation API. <br>
Mitigation: Avoid sending secrets, private architecture details, or sensitive customer data in questions or document URLs. <br>
Risk: The skill relies on network access to Volcengine documentation endpoints. <br>
Mitigation: Review returned documentation links and API responses before using the content for operational decisions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/volc-sdk-team/volcengine-documentation) <br>
- [Volcengine document search API](https://docs-api.cn-beijing.volces.com/api/v1/doc/search) <br>
- [Volcengine document fetch API](https://docs-api.cn-beijing.volces.com/api/v1/doc/fetch) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown answers with official documentation links and JSON returned by helper commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search and fetch operations return Volcengine documentation content; generated answers should cite clean official document URLs.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
