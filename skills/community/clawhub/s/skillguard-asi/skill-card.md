## Description:

Agent技能安全扫描器 — 上传Skill包自动检测安全漏洞（prompt注入/凭证泄露/代码执行/依赖审计等8维检测）。三平台首发，零依赖Python标准库。

This skill is ready for commercial/non-commercial use.

## Publisher:

[thebuddha5566](https://clawhub.ai/user/thebuddha5566)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use this skill to scan agent skill ZIP packages for OWASP ASI-aligned risks, credential exposure, dangerous code patterns, permission mismatches, dependency issues, network access, and memory-pollution indicators before installation or release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scanning untrusted ZIP files can exhaust disk or memory because the extractor does not enforce size limits.

Mitigation: Run scans in a sandbox or with resource limits, especially for third-party ZIP packages.

Risk: Scan results are advisory, and one permission cross-check can miss cases.

Mitigation: Review findings manually and use complementary security review before installing the scanned skill in sensitive or shared environments.

Risk: CLI output and generated reports are Chinese-language.

Mitigation: Route reports to reviewers who can assess Chinese-language security output or translate the report before acting on it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thebuddha5566/skills/skillguard-asi)
- [ClawHub publisher profile](https://clawhub.ai/user/thebuddha5566)

## Skill Output:

**Output Type(s):** [text, markdown, json, guidance]

**Output Format:** [CLI text plus JSON and Markdown security scan reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes severity-filtered findings and TRACE security scoring.]

## Skill Version(s):

1.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
