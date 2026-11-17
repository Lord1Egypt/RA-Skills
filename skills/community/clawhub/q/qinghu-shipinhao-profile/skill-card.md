## Description:

查询微信视频号账号主页资料与统计信息，帮助用户了解账号画像和运营表现。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

运营人员及其他用户可查询微信视频号账号的主页资料和统计数据，用于账号画像与运营分析。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid profile lookups may incur Qinghu credit charges.

Mitigation: Check the current estimate and obtain user consent before paid calls.

Risk: Installation may change the local Node runtime, npm tools or PATH without a pinned qhkit version.

Mitigation: Prefer a separately reviewed, pinned qhkit installation and confirm installation or PATH changes first.

Risk: Credential setup may overwrite an existing international Qinghu/AutoAGC configuration.

Mitigation: Check the current site and credentials; ask before replacing any existing configuration.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/autoagc/skills/qinghu-shipinhao-profile)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu API keys](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Concise account-profile summary; optional exported data file for larger results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports the credits charged for paid lookups.]

## Skill Version(s):

0.1.2 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
