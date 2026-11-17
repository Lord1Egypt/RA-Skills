## Description:

Builds or reuses a compact navigation index for large, multi-file, or layered skills so an agent can load only the sections needed instead of rereading the full source.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haoh51918-lgtm](https://clawhub.ai/user/haoh51918-lgtm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to create or reuse compact navigation indexes for large agent skills, especially when only a subset of a skill needs to be loaded for a task.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The companion script can write outside the intended index directory if given a crafted skill ID.

Mitigation: Use only simple skill IDs made of letters, numbers, dots, underscores, or hyphens, and do not pass user-supplied or path-like values such as ../name until validation is added.

Risk: The skill creates persistent .skill-index files in the workspace.

Mitigation: Install and use it only where persistent navigation files in the workspace root are acceptable, and review generated indexes before relying on them.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/haoh51918-lgtm/skills/skills-pager)
- [Initial Mapping](references/initial-mapping.md)
- [Lookup Patterns](references/lookup-patterns.md)
- [Pager Map Layout](references/map-layout.md)
- [Map Quality](references/map-quality.md)
- [Mapping Policy](references/mapping-policy.md)
- [Refresh Policy](references/refresh-policy.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional generated workspace index files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create persistent .skill-index/registry.json and .skill-index/skills/<skill-id>/index.md files in the workspace root.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
