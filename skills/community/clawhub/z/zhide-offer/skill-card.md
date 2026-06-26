## Description: <br>
职得Offer校园求职助手。调用职得Offer MCP接口查询校园招聘岗位和面试经验。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jack-yang-ai](https://clawhub.ai/user/jack-yang-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students and job seekers use this skill to search campus recruiting and internship roles, inspect job details, and retrieve interview experience writeups for preparation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Job and interview search queries are sent to the 职得Offer API. <br>
Mitigation: Use the skill only when the 职得Offer service is trusted with those queries. <br>
Risk: The skill requires a user-provided API key. <br>
Mitigation: Prefer ZHIDE_OFFER_KEY and keep any local config file private. <br>
Risk: Some trigger terms are broad and could invoke the skill when the user did not intend an external query. <br>
Mitigation: Confirm intent before running the scripts for broad job-search, offer, or interview-preparation requests. <br>


## Reference(s): <br>
- [职得Offer MCP API 文档](references/api.md) <br>
- [ClawHub skill page](https://clawhub.ai/jack-yang-ai/zhide-offer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and text results from local scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided ZHIDE_OFFER_KEY or private local config file for API access.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
