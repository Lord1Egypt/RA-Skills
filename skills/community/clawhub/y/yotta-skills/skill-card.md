## Description:

元阁 (YuanGe) recommends YottaMeta skill combinations for a task, inventories installed skills, and provides commands to install, update, and manage the skill family across supported agents and directories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yottameta](https://clawhub.ai/user/yottameta)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to choose combinations of YottaMeta skills for a task, inspect local skill installations, and manage installation or updates across agent directories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation examples use an unpinned package, which can change between runs.

Mitigation: Review the release and pin the installer version before execution; use --dry-run to inspect the planned skill and destination changes, and retain the package's exact-version pinning behavior.

Risk: The security evidence reports filesystem and network-exposure issues in adoption paths and installation guidance.

Mitigation: Review the target directories and network activity, and evaluate the installer in an isolated environment with only the filesystem access it needs.

Risk: The scan inspected only 15 of 58 components and reports difficult-to-interpret content and unresolved references.

Mitigation: Review the remaining components and resolve the flagged references before relying on the package in a production environment.

## Reference(s):

- [Orchestration guide](references/orchestration.md)
- [Installation flow](references/install-flow.md)
- [Hub guide](references/hub.md)
- [Provider protocol](references/provider-protocol.md)
- [Yotta Skills project repository](https://github.com/YottaMeta/yotta-skills)
- [Yotta Skills npm package](https://www.npmjs.com/package/@yottameta/yotta-skills)
- [ClawHub release page](https://clawhub.ai/yottameta/skills/yotta-skills)

## Skill Output:

**Output Type(s):** [Guidance, Text, Shell commands, Configuration]

**Output Format:** [Text or JSON reports and Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may install or update skills in a selected directory; routing and inventory can provide recommendations and local reports.]

## Skill Version(s):

0.30.16 (source: SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
