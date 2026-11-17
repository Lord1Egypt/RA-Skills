## Description:

指导 agent 通过本地 szu-cli 安全查询和操作深圳大学校园事务，包括课程、成绩、学业进度、体育预约、图书馆和学术数据库检索。

This skill is ready for commercial/non-commercial use.

## Publisher:

[awesomehou](https://clawhub.ai/user/awesomehou)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to map Shenzhen University campus-service requests to szu-cli commands, parse JSON results, and apply privacy and confirmation boundaries for sensitive account data and state-changing campus actions.

### Deployment Geography for Use:

Global, for users with authorized Shenzhen University campus-system access.

## Known Risks and Mitigations:

Risk: The skill can surface private academic, ranking, account, and booking data through an authenticated campus session.

Mitigation: Return only the fields needed for the user's request, avoid credentials and session artifacts, and do not expose full records unless the user explicitly asks for them.

Risk: Sports reservations and cancellations can change campus-system state.

Mitigation: Use dry-run commands first, require explicit user confirmation and a unique target before any confirm command, and do not pay, cancel payments, or repeatedly submit actions.

Risk: The skill depends on a third-party local szu-cli package.

Mitigation: Install only from a trusted publisher, review or pin the szu-cli version before global installation, and avoid chained install-and-run commands when possible.

Risk: Academic database and notice downloads may involve access controls or publisher limits.

Mitigation: Use only supported CLI commands for user-specified single items, avoid bulk downloads, and do not construct hidden links or bypass authentication, CAPTCHA, WebVPN, rate limits, or download controls.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/awesomehou/skills/szu-campus)
- [README](README.md)
- [Campus Command Routing](references/commands.md)
- [Privacy and Safety](references/privacy-safety.md)
- [Structured Error Handling](references/errors.md)
- [Academic Databases](references/academic-databases.md)
- [Campus CLI Examples](references/examples.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands and JSON-output handling rules]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local szu-cli >= 0.2.0 and authenticated campus access for private queries.]

## Skill Version(s):

0.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
