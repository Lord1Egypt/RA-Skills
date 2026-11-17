## Description:

Checks the current public IP with ip38.com, compares it with a stored WeChat public-account IP value, and supports article publishing when the IP matches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[achievejia](https://clawhub.ai/user/achievejia)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators who publish WeChat public-account articles use this skill to check whether the current public IP matches a configured allowlist value before continuing with publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic WeChat article publication can occur when the stored IP matches, without a clearly documented confirmation step.

Mitigation: Require explicit user confirmation before publishing on real accounts and keep activation triggers narrow.

Risk: The IP lookup contacts ip38.com and can reveal public IP lookup metadata to that service.

Mitigation: Use the external lookup only when that disclosure is acceptable, or replace it with an approved IP lookup endpoint.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/achievejia/skills/wechat-ip-checker)
- [ip38.com IP Lookup Service](https://www.ip38.com/)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown or plain text status messages and instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use a browser-based public IP lookup and a dependent WeChat publishing skill.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
