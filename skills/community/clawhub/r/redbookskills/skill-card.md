## Description: <br>
Automates Xiaohongshu (XHS) browser workflows for publishing image or video posts, checking login state, searching content, commenting, and retrieving account-facing content data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Viv888-AI](https://clawhub.ai/user/Viv888-AI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content operators and developers use this skill to prepare confirmed Xiaohongshu posts, run browser-based publishing commands, inspect login state, search notes, post comments, and retrieve content or notification data from a logged-in account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill controls a logged-in Xiaohongshu browser session and can take real account actions. <br>
Mitigation: Use a dedicated or test account and Chrome profile, and review the account state before running publish, comment, notification, or analytics commands. <br>
Risk: Publishing and commenting workflows can post public content from the account. <br>
Mitigation: Require manual confirmation of the final title, body, media, and comment text, and prefer preview mode before allowing an automated post. <br>
Risk: Remote Chrome DevTools Protocol access can expose browser control to an untrusted host. <br>
Mitigation: Keep CDP bound to localhost unless the remote host is fully controlled and network access is restricted. <br>
Risk: Notification capture and content analytics can expose account or audience data. <br>
Mitigation: Limit use to accounts intended for automation and avoid exporting or sharing data that is not needed for the task. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Viv888-AI/redbookskills) <br>
- [Publisher profile](https://clawhub.ai/user/Viv888-AI) <br>
- [Xiaohongshu](https://www.xiaohongshu.com) <br>
- [Xiaohongshu creator publishing page](https://creator.xiaohongshu.com/publish/publish) <br>
- [Claude Code integration guide](docs/claude-code-integration.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text with shell commands and structured command results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include success or failure status, publishing details, search result fields, notification data, analytics fields, or exported CSV paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
