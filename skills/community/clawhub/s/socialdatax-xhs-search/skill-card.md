## Description: <br>
用于小红书数据分析、小红书笔记搜索、关键词检索、内容调研、竞品分析和趋势研究。覆盖 Xiaohongshu / XHS / RedNote note search，来自 SocialDataX 社媒数据助手。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[devinchen2014](https://clawhub.ai/user/devinchen2014) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search Xiaohongshu / XHS / RedNote notes for topic discovery, content planning, competitor research, market observation, and trend scanning through SocialDataX. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a third-party SocialDataX service and npm package. <br>
Mitigation: Confirm the user trusts the SocialDataX service and the socialdatax-skills npm package before installation or use. <br>
Risk: The skill requires a SOCIALDATAX_API_KEY for data calls. <br>
Mitigation: Provide only the intended API key through the SOCIALDATAX_API_KEY environment variable and avoid exposing it in prompts, logs, or shared output. <br>
Risk: Returned note URLs can include xsec_token-bearing links that may be private or sensitive. <br>
Mitigation: Avoid publicly sharing returned note URLs when those token-bearing links should remain private. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/devinchen2014/skills/socialdatax-xhs-search) <br>
- [SocialDataX homepage](https://socialdatax.com/?from=clawhub) <br>
- [Publisher profile](https://clawhub.ai/user/devinchen2014) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands, MCP tool guidance, and summarized search findings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search output may include note URLs with xsec_token query parameters that should be preserved exactly when traceability is needed.] <br>

## Skill Version(s): <br>
0.1.9 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
