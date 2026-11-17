## Description:

Helps agents scaffold and validate Stardew Valley Content Patcher or SMAPI mod projects, including JSON content packs, NPC, dialogue, event data, and C# SMAPI project files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yizege](https://clawhub.ai/user/yizege)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and mod authors use this skill to create Stardew Valley mod project structures, draft Content Patcher JSON, add NPC, event, dialogue, and schedule data, and prepare SMAPI C# projects for local builds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The project generator can write outside the intended folder.

Mitigation: Run it only in a controlled workspace, avoid overwriting existing folders, and confirm generated paths before building or moving files.

Risk: Untrusted mod names or author names can be embedded into generated build and source files.

Mitigation: Use simple identifier-style names from trusted input only, then inspect generated .csproj and .cs files before running dotnet build.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yizege/skills/stardewvalley-modding)
- [Quick reference](references/quickref.md)
- [Stardew Valley modding wiki](https://stardewvalleywiki.com/Modding:Index)
- [SMAPI](https://smapi.io/)
- [Content Patcher](https://smapi.io/mods/1915)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with generated JSON, C# project files, shell commands, and configuration templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Helper scripts may create Stardew Valley Content Patcher or SMAPI project files when run by the agent.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
