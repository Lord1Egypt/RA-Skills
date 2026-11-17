## Description:

Audits a user-provided website URL for security and trust risk using signals such as HTTPS, certificate status, domain background, page content, and Chinese ICP/public-security filing information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[666-moonlight](https://clawhub.ai/user/666-moonlight)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and security reviewers use this skill to assess whether a URL appears trustworthy before visiting further, sharing credentials, or downloading files. It produces a structured report summarizing observed safety signals, platform background, and practical cautions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill opens arbitrary user-provided URLs in the agent browser without destination safeguards.

Mitigation: Use only with strong browser and network isolation; avoid local, private-network, metadata-service, and untrusted redirecting URLs; treat page content as untrusted.

## Reference(s):

- [Known Platforms Reference](references/known-platforms.md)
- [ClawHub Skill Page](https://clawhub.ai/666-moonlight/skills/website-security-audit)
- [MIIT ICP Filing Query](http://beian.miit.gov.cn/publish/query/indexFirst.action)
- [National Internet Security Management Service Platform](http://www.beian.gov.cn)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown structured risk report with tables, checklist items, and concise summary guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include observed URL metadata, HTTPS and certificate status, filing information, risk level, risk factors, and usage cautions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
