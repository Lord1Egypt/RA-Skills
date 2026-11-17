## Description:

查询域名 SSL 证书过期时间。用法：说「查 xxx.cn 证书」或「SSL 证书 xxx.com」即可。

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunny-lobster-api](https://clawhub.ai/user/sunny-lobster-api)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to check SSL certificate expiry for a single domain from a natural-language request, or to run batch checks from a local domains file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Batch checks may use a local domains file that includes unintended or unreviewed hosts.

Mitigation: Review or control the domains file before running batch checks.

Risk: JSON output may be unsafe to trust in automation because evidence flags an escaping issue.

Mitigation: Treat JSON output as informational until JSON escaping is fixed and validated.

Risk: SSL status depends on local openssl behavior, network access, and platform date parsing.

Mitigation: Confirm openssl is available and manually review failed, urgent, or automation-triggering results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sunny-lobster-api/skills/ssl-monitor)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional text or JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires openssl; batch mode reads a local domain list and supports warning and critical day thresholds.]

## Skill Version(s):

1.2.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
