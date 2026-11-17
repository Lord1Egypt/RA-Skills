## Description:

YuanGe helps agent users choose and combine YottaMeta skills, inspect installed skills, and install or update selected packages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yottameta](https://clawhub.ai/user/yottameta)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use it to map a task to YottaMeta skill combinations, check what is installed, and manage installation across supported agent directories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The supplied partial scan reports serious execution, filesystem-scope, server-exposure, and unpinned installer risks.

Mitigation: Review the reported issues and the installation behavior independently before use; avoid installing until that review is complete.

## Reference(s):

- [Orchestration guide](references/orchestration.md)
- [Installation flow](references/install-flow.md)
- [Hub guide](references/hub.md)
- [Provider protocol](references/provider-protocol.md)
- [ClawHub release page](https://clawhub.ai/yottameta/skills/yotta-skills)
- [npm package](https://www.npmjs.com/package/@yottameta/yotta-skills)

## Skill Output:

**Output Type(s):** [Guidance, Text, Markdown, Shell commands, Configuration, JSON]

**Output Format:** [Concise recommendations and command examples; JSON when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include suggested skill combinations, order, rationale, inventory status, and installation or update commands.]

## Skill Version(s):

0.30.14 (source: SKILL.md frontmatter, package.json, ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
