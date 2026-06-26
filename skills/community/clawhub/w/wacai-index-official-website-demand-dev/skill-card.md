## Description: <br>
Automates official website demand updates by writing requirements into a target project, backing up the demand file, updating a branch, committing and pushing selected changes, and sending a WeCom notification after a successful push. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shidengyun](https://clawhub.ai/user/shidengyun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to turn website product requirements into a demand document, selected code changes, a git commit, a remote branch push, and a post-push WeCom notification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify a specified repository, stage selected files, commit them, and push to a remote branch without a clear final approval step. <br>
Mitigation: Use a safe feature branch, inspect diffs and staged files before commit or push, and require human approval for repository changes in sensitive projects. <br>
Risk: The notification flow can send project path, branch, commit information, and change summaries to Enterprise WeChat. <br>
Mitigation: Disable notifications for sensitive repositories or tightly configure them so only approved metadata is sent. <br>
Risk: A default WeCom webhook URL is embedded in the artifact. <br>
Mitigation: Replace it with an approved webhook through configuration, rotate any exposed webhook, and avoid using the bundled default for production work. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shidengyun/wacai-index-official-website-demand-dev) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown requirements files, repository code changes, git command output, and notification text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates an hourly product demand backup when a prior demand file exists and sends a WeCom text notification after a successful push.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
