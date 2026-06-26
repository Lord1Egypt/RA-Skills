## Description: <br>
A Git repository monitoring skill that supports GitHub, GitLab, Gitee, and other Git platforms, with repository update checks, pulls, and change summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1yihui](https://clawhub.ai/user/1yihui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams use this skill to monitor selected Git repositories, check for code updates, pull changes, and receive concise change summaries in chat or Feishu. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for recurring repository pulls and automatic use of shared Feishu credentials without enough scoping or user control. <br>
Mitigation: Use it only for repositories and chats that are intentionally monitored, keep Feishu credentials scoped to the intended bot and chat, and review behavior before enabling recurring checks. <br>
Risk: The reviewed package references helper.js, but that runtime implementation was not present in the artifact evidence. <br>
Mitigation: Verify the actual runtime files before installation or deployment, especially any code that pulls repositories or sends Feishu messages. <br>


## Reference(s): <br>
- [YiHui GIT MONITOR on ClawHub](https://clawhub.ai/1yihui/yihui-git-monitor) <br>
- [Feishu Open Platform](https://open.feishu.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce repository change summaries and setup guidance for Git monitoring and Feishu notifications.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
