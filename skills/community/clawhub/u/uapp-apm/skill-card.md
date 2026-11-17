## Description:

查询友盟应用性能监控（U-APM）数据，包括崩溃、ANR、卡顿、启动、网络、原生页面、H5 页面和分钟级实时监控指标。

This skill is ready for commercial/non-commercial use.

## Publisher:

[squall0925](https://clawhub.ai/user/squall0925)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to query read-only Umeng U-APM crash, stability, startup, network, and page performance data through umeng-cli.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs telemetry that can include appkeys.

Mitigation: Allow telemetry only when that reporting is explicitly accepted, and avoid sending appkeys unless the receiving process is approved.

Risk: The skill offers mutable installation methods, including a curl-to-shell installer.

Mitigation: Use a pinned, inspectable CLI installation method and review the installed CLI before use.

Risk: Logging in grants the CLI access to the user's Umeng account context.

Mitigation: Use an account with the minimum required permissions and treat saved CLI credentials as sensitive.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/squall0925/skills/uapp-apm)
- [Umeng CLI project homepage](https://github.com/umeng/umeng-cli)
- [Umeng API credentials documentation](https://devs.umeng.com/api/credentials)
- [Umeng console](https://www.umeng.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides read-only API calls and interpretation of JSON API responses.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
