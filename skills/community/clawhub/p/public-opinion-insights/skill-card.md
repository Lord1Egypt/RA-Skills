## Description: <br>
Calls the Midu public opinion insights API to return structured, dimension-specific public-opinion analysis for a specified event, topic, or subject. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bitallin](https://clawhub.ai/user/bitallin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to request concise public-opinion insights for a named event, topic, or subject across specific analysis dimensions such as media coverage, sentiment intensity, propagation, rumor status, and response recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and related content are sent to the Midu remote analysis service. <br>
Mitigation: Use the skill only with data approved for that service and transport, and avoid confidential content unless the service is explicitly authorized. <br>
Risk: The skill requires a MIDU_API_KEY secret and includes configuration guidance for storing it. <br>
Mitigation: Treat MIDU_API_KEY as a secret, avoid committing or sharing configuration files that contain it, and restrict local config file permissions. <br>
Risk: API key and user-text handling are under-disclosed in the release evidence. <br>
Mitigation: Review the service handling expectations before installation and deployment. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/bitallin/public-opinion-insights) <br>
- [Analysis Dimensions](references/analysis_dimension.md) <br>
- [Midu API Key Setup Guide](references/apikey-fetch.md) <br>
- [Midu API key endpoint](http://intra-znjs-yqt-agent-wx-beta.midu.cc/apiKey) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [JSON response containing structured public-opinion analysis, typically Markdown text in the result field] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and MIDU_API_KEY; sends the user prompt to the Midu remote analysis service and may take minutes for complex requests.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
