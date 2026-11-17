## Description:

Xborder Ecom Check helps agents run a bilingual cross-border e-commerce compliance check covering customs, product safety, consumer protection, tax, advertising, and data privacy requirements for destination markets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wwumit](https://clawhub.ai/user/wwumit)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, compliance teams, and developers use this skill to preview and run a 12-item cross-border e-commerce compliance assessment. Scored runs send answers to compliancehub.cn and return a local compliance report; preview modes run offline.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scored checks send user compliance answers to compliancehub.cn.

Mitigation: Use offline preview modes for local review, and run scored checks only after confirming the user accepts transmission to compliancehub.cn.

Risk: The skill may store a local anonymous trial identifier or read an API key from the environment or user config.

Mitigation: Keep API keys outside the skill package, use restrictive file permissions, and remove the local trial or key file when access is no longer needed.

Risk: HTML reports are flagged by security evidence as unsafe until report fields are escaped.

Mitigation: Prefer text or JSON report output unless the cloud response source is trusted and the HTML output path has been reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wwumit/skills/xborder-ecom-check)
- [ComplianceHub account page](https://compliancehub.cn/account.html?skill=xborder-ecom-check)
- [ComplianceHub service endpoint](https://compliancehub.cn)
- [Artifact skill documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Text, JSON, or HTML compliance reports, with Markdown guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preview mode can run offline; scored runs submit answers to compliancehub.cn and may read COMPLIANCEHUB_API_KEY or a local key file.]

## Skill Version(s):

1.2.2 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
