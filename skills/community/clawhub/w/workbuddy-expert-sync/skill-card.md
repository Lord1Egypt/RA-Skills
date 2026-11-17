## Description:

Make locally created WorkBuddy experts and expert teams visible across all WorkBuddy accounts on the same machine, and automatically sync them to future accounts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangjiaocheng](https://clawhub.ai/user/wangjiaocheng)

### License/Terms of Use:

MIT-0

## Use Case:

WorkBuddy users and support agents use this skill to diagnose missing local experts after account switching and mirror local expert registries across accounts on the same Windows device. It also helps deploy and verify recurring local synchronization for future accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The recurring scheduled task can repeatedly overwrite all local WorkBuddy account expert registries with the mirrored marketplace list.

Mitigation: Use it only when ongoing local automation is desired, confirm affected accounts first, keep an independent backup of experts.json files, and remove WorkBuddy_SyncMyExperts plus the deployed script if recurring mirroring is no longer wanted.

Risk: The skill syncs registry files on the current device only and does not migrate expert package directories.

Mitigation: Before syncing, verify that the expected expert package folders already exist in the local WorkBuddy marketplace on that machine.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wangjiaocheng/skills/workbuddy-expert-sync)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with PowerShell commands, diagnostic summaries, backup locations, verification results, and removal guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write WorkBuddy experts.json registry files, deploy a local PowerShell sync script, and register a recurring Windows scheduled task when the user proceeds.]

## Skill Version(s):

1.0.0 (source: release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
