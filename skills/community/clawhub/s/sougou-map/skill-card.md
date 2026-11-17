## Description:

Sougou Map helps agents explain the May 2022 Sogou Maps shutdown and guide migration of legacy references, APIs, and coordinate data to Amap, Baidu Maps, or Tencent Maps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangifonly](https://clawhub.ai/user/zhangifonly)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to answer legacy Sogou Maps questions, explain the service shutdown, and plan migration of APIs, provider choices, and coordinate conversions for Chinese map platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Current third-party map API details may differ from the static migration guidance.

Mitigation: Verify provider documentation, API keys, request parameters, and quotas before implementation.

Risk: Legacy Sogou coordinate data may shift if migrated without coordinate-system conversion.

Mitigation: Use official provider coordinate-conversion interfaces and validate sample locations before bulk migration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhangifonly/skills/sougou-map)
- [Publisher profile](https://clawhub.ai/user/zhangifonly)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown guidance with migration notes and comparison tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No code execution; verify current third-party map API details against provider documentation before implementation.]

## Skill Version(s):

1.1.0 (source: evidence release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
