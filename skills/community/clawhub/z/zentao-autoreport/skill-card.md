## Description:

帮助用户根据当天工作描述匹配禅道任务，确认后通过 ZenTao API 记录工时并更新剩余工时。

This skill is ready for commercial/non-commercial use.

## Publisher:

[crecendow](https://clawhub.ai/user/crecendow)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and teams using ZenTao use this skill to turn plain-language daily work summaries into matched task selections and confirmed work-hour records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses ZenTao credentials and active sessions that can read tasks and modify work-hour records.

Mitigation: Install only for accounts and ZenTao workspaces where that access is acceptable, and review the skill before deployment.

Risk: Login credentials and zentaosid session values may be exposed through local configuration files or logs.

Mitigation: Store credentials in a protected secret store or chmod 600 configuration file, stop logging zentaosid values, and rotate any credentials or sessions that may already have appeared in logs.

Risk: Using a non-HTTPS ZenTao endpoint could expose credentials or session data in transit.

Mitigation: Require HTTPS for ZENTAO_URL before using the skill.

Risk: The shell fallback may pass form values through curl in a less defensive way.

Mitigation: Prefer the Python scripts or update the shell fallback to use curl --form-string before relying on it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/crecendow/skills/zentao-autoreport)
- [ZenTao example server URL](https://zentao.example.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown text with task match summaries, confirmation prompts, shell command execution guidance, and success or failure status.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call local Python or shell scripts that read ZenTao configuration, authenticate to ZenTao, list tasks, and submit work-hour records after confirmation.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
