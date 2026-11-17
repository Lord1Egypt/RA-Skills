## Description:

Automates Wacai official website demand-change work by saving a supplied demand brief, preparing the target Git branch, guiding code changes, running checks, committing, pushing, and sending a WeCom notification after a successful push.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shidengyun](https://clawhub.ai/user/shidengyun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site maintainers use this skill to turn a pasted official-website change request plus an explicit project path and branch into a prepared demand file, code-change workflow, commit, push, and post-push notification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repository metadata and summary content may be sent to a hardcoded external WeCom webhook.

Mitigation: Remove the hardcoded webhook, load the webhook from a trusted secret source, and require explicit confirmation before sending notifications.

Risk: The workflow can commit and push repository changes automatically.

Mitigation: Require review of staged changes and explicit confirmation before git push, and keep the project path and target branch explicit for each run.

Risk: Demand or summary file handling could affect files outside the intended target repository.

Mitigation: Restrict demand and summary file paths to the target repository and reject paths that resolve outside that boundary.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shidengyun/skills/wacai-index-official-website-demand-change)
- [Publisher profile](https://clawhub.ai/user/shidengyun)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown status updates with shell commands and generated or modified project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write or back up demand files, modify code, commit and push Git changes, and send a WeCom notification when the workflow succeeds.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
