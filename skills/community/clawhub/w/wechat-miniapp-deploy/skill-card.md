## Description:

Deploy and manage WeChat Mini Programs using the official miniprogram-ci CLI, including code upload, version management, preview QR generation, review submission preparation, and CI/CD automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lm203688](https://clawhub.ai/user/lm203688)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill to guide agents through WeChat Mini Program deployment tasks, including first-time setup, versioned uploads, preview generation, privacy-compliance checks, review submission preparation, and multi-environment CI/CD deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents following this skill may handle WeChat Mini Program CI private keys, AppIDs, AppSecrets, and access tokens during deployment or review-submission workflows.

Mitigation: Use masked CI secrets, project-local pinned miniprogram-ci installs, restrictive temporary key files with cleanup traps, and avoid AppSecret-based review-submission commands in local or untrusted agent environments.

Risk: Deployment and audit-submission commands can affect live WeChat Mini Program release state if run against the wrong project, environment, or version.

Mitigation: Require human review of target AppID, environment, version, changelog, and generated preview QR before review submission or release promotion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lm203688/skills/wechat-miniapp-deploy)
- [WeChat Mini Program admin portal](https://mp.weixin.qq.com)
- [WeChat access token API endpoint](https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=$APPID&secret=$APPSECRET)
- [WeChat submit audit API endpoint](https://api.weixin.qq.com/wxa/submit_audit?access_token=$ACCESS_TOKEN)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Bash, JSON, YAML, and curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce deployment commands, CI configuration snippets, versioning guidance, privacy checklist guidance, and review-submission API examples.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
