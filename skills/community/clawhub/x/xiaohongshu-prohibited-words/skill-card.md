## Description:

本技能用本地违禁词库扫描小红书文案，输出分级命中结果并支持词库维护。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bonniegeng-max](https://clawhub.ai/user/bonniegeng-max)

### License/Terms of Use:

MIT

## Use Case:

面向创作小红书内容的用户与代理，在发布前对标题、正文和标签运行离线违禁词检查，并维护用于检查的词库。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan does not establish the host runtime's actual environment or file-read permission limits.

Mitigation: Review the host's permission settings and restrict environment and filesystem access to what the workflow needs.

Risk: An offline word list can miss changed or context-dependent platform rules, and this check does not cover every publication requirement.

Mitigation: Treat the results as a text-only check, maintain entries using verifiable evidence, and separately check requirements such as title length and AI disclosure.

## Reference(s):

- [Prohibited word list](references/prohibited-words.md)
- [Word list section configuration](references/sections.json)
- [ClawHub skill release](https://clawhub.ai/bonniegeng-max/skills/xiaohongshu-prohibited-words)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands]

**Output Format:** [Plain-text scan findings and command-line usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports word matches by severity and a pass, revise, or error result; exit codes distinguish these outcomes.]

## Skill Version(s):

1.0.6 (source: SKILL.md frontmatter; ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
