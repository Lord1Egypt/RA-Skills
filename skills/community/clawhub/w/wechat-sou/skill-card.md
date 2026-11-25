## Description:

Search public WeChat articles and video content by keyword and return structured JSON results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[um-why](https://clawhub.ai/user/um-why)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can search publicly available WeChat articles or video content by keyword for topic discovery, competitor monitoring, and trend analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search keywords are sent to the third-party Guaikei service to retrieve public WeChat search data.

Mitigation: Avoid sensitive or confidential search terms and confirm the service is appropriate for your use.

Risk: Security inspection was partial, and scanner guidance notes undeclared tool scope.

Mitigation: Review the skill files and required runtime and network access before installation.

Risk: Timestamps use a fixed Beijing-time format that may differ from the reader's local time.

Mitigation: Account for Beijing time when interpreting result timestamps.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/um-why/skills/wechat-sou)
- [Guaikei service](https://www.guaikei.com)
- [Search options](references/options.md)
- [FAQ and environment setup](references/faq.md)
- [Output contract](references/contract.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [Structured JSON envelope containing article or video results, request details, and status information.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns up to the requested result limit; timestamps use Beijing time.]

## Skill Version(s):

1.1.3 (source: SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
