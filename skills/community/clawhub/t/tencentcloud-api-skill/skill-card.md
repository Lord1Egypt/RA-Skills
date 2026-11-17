## Description:

Helps agents use Tencent Cloud's tccli to discover Cloud API documentation and query, create, modify, or delete Tencent Cloud resources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tencent-adm](https://clawhub.ai/user/tencent-adm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to manage Tencent Cloud resources and automate Cloud API operations through tccli after checking Tencent Cloud API documentation and credential state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Commands can create, modify, or delete Tencent Cloud resources and may affect production services or cost.

Mitigation: Review every create, modify, or delete tccli command and confirm the target region, resource IDs, parameters, permissions, and cost impact before execution.

Risk: Credential handling can expose Tencent Cloud secrets if local credential files or configuration output are printed.

Mitigation: Use browser-based tccli auth login, prefer least-privilege CAM credentials, and avoid commands that display local credential material.

Risk: High-volume API calls can hit Tencent Cloud rate limits or unintentionally amplify operational changes.

Mitigation: Run bulk operations serially or with deliberate delays, and handle RequestLimitExceeded responses before retrying.

## Reference(s):

- [TCCLI installation guide](references/install.md)
- [TCCLI authentication guide](references/auth.md)
- [Tencent Cloud API reference workflow](references/refs.md)
- [Tencent Cloud API services index](https://cloudcache.tencentcs.com/capi/refs/services.md)
- [TencentCloud CLI source installation reference](https://github.com/TencentCloud/tencentcloud-cli.git)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON response interpretation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose tccli API calls that return JSON from Tencent Cloud; destructive create, modify, or delete operations require user confirmation.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
