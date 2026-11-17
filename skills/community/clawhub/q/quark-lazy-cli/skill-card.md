## Description:

Quark Lazy Cli helps agents and advanced Python users maintain QAS-backed Quark cloud-drive TV and anime subscriptions by checking tasks, finding replacement resources, and updating or repairing missing episodes after user authorization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jesustoachild](https://clawhub.ai/user/jesustoachild)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agent operators use this skill to maintain QAS-backed Quark cloud-drive media subscriptions, inspect subscription status, plan scheduled checks, and run authorized update or repair workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles powerful QAS and LLM credentials.

Mitigation: Use only trusted local or HTTPS QAS endpoints, rotate and limit tokens, and avoid exposing tokens in examples, logs, reports, or scheduled tasks.

Risk: Sample automation includes unsafe transport or shell environment sourcing patterns.

Mitigation: Review scripts before use and remove shell sourcing of .env from sample run scripts before adapting them for local automation.

Risk: The artifact includes an unrelated Claude permission file.

Mitigation: Remove .claude/settings.local.json unless that local Claude permission is intentionally required.

## Reference(s):

- [OpenClaw Scheduled Tasks](references/OpenClaw定时任务.md)
- [Daily Reporting](references/每日汇报.md)
- [Environment Variables](references/环境变量.md)
- [Subscription Time Estimation](references/订阅时间估算.md)
- [Advisor Mode](references/顾问模式.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce operational recommendations for QAS subscription checks and updates; update commands require explicit user authorization.]

## Skill Version(s):

0.1.22 (source: pyproject.toml and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
