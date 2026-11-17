## Description:

Searches videos within a specified WeChat Channels creator account by keyword using Qinghu AI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content analysts use this skill to find videos matching a keyword within a specified WeChat Channels account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing qhkit or changing local configuration can persist beyond the search task.

Mitigation: Install qhkit yourself in a controlled environment; avoid persistent shell-profile changes unless desired.

Risk: Search calls consume paid Qinghu credits or may target the wrong account.

Mitigation: Confirm the target account and estimated cost with the user before paid calls.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-shipinhao-account-search)
- [Qinghu qhkit package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu API keys](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Concise search summary with video results and optional table file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports credits used when paid calls are made.]

## Skill Version(s):

0.1.2 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
