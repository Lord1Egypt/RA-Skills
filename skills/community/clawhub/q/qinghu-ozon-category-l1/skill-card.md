## Description:

按语言和名称关键词查询 Ozon 公共一级类目及其类目 ID。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Ozon sellers and analysts use this skill to look up public top-level category names and IDs by language and optional name keyword.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation may change local Node tooling, PATH or shell profile settings through unpinned dependencies.

Mitigation: Review setup steps and use a preinstalled, pinned qhkit version in an isolated environment.

Risk: Configuring qhkit may persist an access token on the machine.

Mitigation: Review credential storage and use a scoped token or environment-based configuration where appropriate.

Risk: Category lookups can incur qhkit charges.

Mitigation: Confirm the estimated cost and obtain user approval before paid calls.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-ozon-category-l1)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Concise category results in Markdown or a tabular file for larger result sets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Category names and IDs are filtered by requested language and optional name keyword; paid calls report credits used.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
