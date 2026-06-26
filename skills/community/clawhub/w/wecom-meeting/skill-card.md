## Description: <br>
wecom-meeting helps an agent create, view, cancel, and list Enterprise WeChat scheduled meetings using the WeCom meeting API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[limawanyan](https://clawhub.ai/user/limawanyan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, administrators, and agents use this skill to manage Enterprise WeChat scheduled meetings for a configured organization, including creating meetings, retrieving meeting details, cancelling meetings, and listing a member's meetings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses company WeCom credentials and can create or cancel real meetings. <br>
Mitigation: Use a dedicated least-privilege WeCom app, protect ~/.wecom/config.json, and confirm meeting IDs, attendee lists, and meeting times before executing actions. <br>
Risk: Cancelling with force can remove a meeting without an interactive confirmation step. <br>
Mitigation: Avoid --force unless the user has intentionally confirmed the exact meeting ID and cancellation target. <br>
Risk: Diagnostic or command output can expose operational meeting or credential-adjacent information in shared terminals or CI logs. <br>
Mitigation: Do not run diagnostic API tests in shared terminals or CI logs, and review outputs before sharing them. <br>


## Reference(s): <br>
- [WeCom Meeting API Reference](references/api.md) <br>
- [WeCom Create Scheduled Meeting Documentation](https://developer.work.weixin.qq.com/document/path/99104) <br>
- [WeCom Cancel Scheduled Meeting Documentation](https://developer.work.weixin.qq.com/document/path/99048) <br>
- [WeCom Get Meeting Details Documentation](https://developer.work.weixin.qq.com/document/path/99049) <br>
- [WeCom Get Member Meeting ID List Documentation](https://developer.work.weixin.qq.com/document/path/99050) <br>
- [ClawHub Skill Page](https://clawhub.ai/limawanyan/wecom-meeting) <br>
- [Publisher Profile](https://clawhub.ai/user/limawanyan) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, and API result text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WeCom CorpID, Secret, and AgentID credentials configured for the target organization.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
