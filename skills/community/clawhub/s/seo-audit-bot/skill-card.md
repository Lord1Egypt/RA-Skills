## Description:

Perform a comprehensive SEO audit of any website. Analyzes technical SEO, on-page factors, content quality, performance, and generates an actionable report with scores and recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eyensama](https://clawhub.ai/user/eyensama)

### License/Terms of Use:

MIT-0

## Use Case:

External users, website owners, digital marketers, SEO agencies, and freelancers use this skill to audit website SEO health, compare competitors, and produce prioritized recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled audit behavior can fetch arbitrary URLs through curl without public-URL safeguards.

Mitigation: Use it only against public websites you intend to audit, avoid localhost and private or internal URLs, and restrict targets to public http/https URLs.

Risk: Fetched responses are stored in predictable temporary files.

Mitigation: Use private temporary files, clean them up after execution, and do not run the bundled script with elevated privileges.

Risk: Remote text displayed in audit output may be unsafe if copied directly into reports or terminals.

Mitigation: Escape remote text before displaying it and review generated findings before sharing or acting on them.

## Reference(s):

- [SEO Best Practices Reference](references/seo-best-practices.md)
- [SEO Audit Bot Demo Report](references/demo-report.md)
- [ClawHub Skill Page](https://clawhub.ai/eyensama/skills/seo-audit-bot)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with scores, findings, and prioritized recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include optional competitor comparisons and shell-command audit output.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
