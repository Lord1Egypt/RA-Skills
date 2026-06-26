## Description: <br>
连接智合AI法律大模型平台进行法律研究。本技能应在用户需要进行法律问题研究、查找法律法规、检索类似案例、或获取法律研究报告时使用。需要智合AI平台会员账号。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cat-xierluo](https://clawhub.ai/user/cat-xierluo) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and legal professionals use this skill to submit Chinese legal research questions to the Zhihe AI legal research platform, check asynchronous task status, retrieve analysis, and archive generated reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles Zhihe account phone numbers, OTP login, bearer tokens, legal questions, research history, downloaded reports, and local archives. <br>
Mitigation: Use it only for matters appropriate for the Zhihe service and local storage model; clear credentials with the logout or clear commands and remove archived reports when they are no longer needed. <br>
Risk: Token export and legacy token migration can expose authentication material if command output or old configuration files are shared. <br>
Mitigation: Avoid token export except for explicit administrative needs, keep configuration files private, and rotate or clear tokens after troubleshooting. <br>
Risk: Legal research output and reports may be incomplete, delayed, expired, or unsuitable as final legal advice. <br>
Mitigation: Review results with qualified legal judgment, check task status before relying on output, and refresh expired report links through the documented report flow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cat-xierluo/zhihe-legal-research) <br>
- [Publisher profile](https://clawhub.ai/user/cat-xierluo) <br>
- [Project homepage from ClawHub metadata](https://github.com/cat-xierluo/legal-skills) <br>
- [API reference](references/api-reference.md) <br>
- [Interaction examples](references/interaction-examples.md) <br>
- [Zhihe AI legal platform](https://www.zhiexa.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with bash command invocations, JSON API responses, legal research text, report links, and archived Markdown or DOCX files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses asynchronous task IDs; completed results can be archived locally and report links may expire.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
