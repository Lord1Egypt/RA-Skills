## Description: <br>
微信搜索 provides Node.js CLI tools for real-time WeChat article and video searches by keyword, returning JSON results and saved logs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[um-why](https://clawhub.ai/user/um-why) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, marketers, and content analysts use this skill to query WeChat article and video search results by keyword for content planning, trend monitoring, competitor analysis, and source discovery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms are sent to an external provider service. <br>
Mitigation: Use the skill only for non-sensitive searches unless the provider terms and data handling are acceptable for the deployment. <br>
Risk: Full search outputs are saved locally as result logs. <br>
Mitigation: Treat logs as potentially sensitive, restrict access to the skill workspace, and remove logs when they are no longer needed. <br>
Risk: Documentation and evidence should reflect the supported article and video behavior. <br>
Mitigation: Use the article and video CLI commands and schemas unless additional content-type support is separately verified. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/um-why/skills/wechat-search-sou) <br>
- [Publisher profile](https://clawhub.ai/user/um-why) <br>
- [GUAIKEI API and token site](https://www.guaikei.com) <br>
- [Complete CLI options](references/options.md) <br>
- [Article search input schema](assets/article_cli_req.schema.json) <br>
- [Article search output schema](assets/article_cli_resp.schema.json) <br>
- [Video search input schema](assets/video_cli_req.schema.json) <br>
- [Video search output schema](assets/video_cli_resp.schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, JSON, files, guidance] <br>
**Output Format:** [JSON printed to stdout with saved result logs, plus concise command guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and GUAIKEI_API_TOKEN; writes article and video result JSON under logs/.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence, package.json, scripts/config/constants.js) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
