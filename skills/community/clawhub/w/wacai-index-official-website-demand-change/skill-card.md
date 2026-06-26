## Description: <br>
Automates the Wacai official website demand-change workflow by preparing the target branch, writing and backing up productdemand.md, supporting code changes and checks, committing and pushing changes, and sending an Enterprise WeChat notification after a successful push. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shidengyun](https://clawhub.ai/user/shidengyun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill to turn a pasted website-change demand, project path, and target branch into an executed repository workflow: branch preflight, demand-file update, implementation guidance, checks, git commit, push, and post-push notification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish repository changes by committing all pending changes and pushing to the selected branch. <br>
Mitigation: Run it only on an intended safe feature branch and require a human diff review before the commit-and-push step. <br>
Risk: The skill can send repository metadata and change summaries to Enterprise WeChat through a bundled webhook. <br>
Mitigation: Replace or remove the bundled webhook key and confirm that notification recipients are approved for the project details being sent. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command invocations and generated repository changes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write files, create git commits, push to the selected branch, and send an Enterprise WeChat notification.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
