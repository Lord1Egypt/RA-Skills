## Description: <br>
网页内容监控助手，用于抓取指定网页、检测内容或关键词变化，并输出变化结果。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xuyongliang-eccom](https://clawhub.ai/user/xuyongliang-eccom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and operators use this skill to monitor public web pages for content updates and keyword appearances or disappearances, such as competitor news, policy pages, and news updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches user-supplied web pages and stores monitored page content locally. <br>
Mitigation: Monitor public, non-sensitive pages and clear ~/.web_monitor/hashes.json when stored page contents are no longer needed. <br>
Risk: Separately obtained scheduler or alert scripts may introduce additional network, credential, or notification-channel risk. <br>
Mitigation: Review and scan any scheduler or alert script before running it, and keep notification credentials outside the skill artifact. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xuyongliang-eccom/web-content-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The included monitor script prints the URL, whether content changed, and keyword changes; it exits with status 1 when content changed and 0 otherwise.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
