## Description:

Provides agents with guidance for inspecting and editing UE5 Blueprint graphs, diagnosing compilation issues, and verifying behavior in PIE through the ue5-automation bridge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[miracle1814](https://clawhub.ai/user/miracle1814)

### License/Terms of Use:

MIT-0

## Use Case:

UE5 developers use the skill to guide an agent through reading or changing Blueprint graphs, resolving compile errors, and checking runtime behavior in PIE. It requires a supported Windows Unreal Engine setup with the separate ue5-automation bridge connected.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bridge runtime is distributed separately, so installing an unreviewed runtime could expose the local project or editor environment to unsafe behavior.

Mitigation: Review the downloaded runtime before installation, keep the bridge local, and protect its token.

Risk: Project asset deletions are not restored by ordinary undo.

Mitigation: Back up project assets before making changes.

Risk: The build-settings workaround changes files that concurrent builds may depend on.

Mitigation: Preserve and restore the original files, and avoid concurrent builds that depend on them.

## Reference(s):

- [Project homepage](https://github.com/miracle1814/ue5-automation)
- [Runtime v6.5.4 release](https://github.com/miracle1814/ue5-automation/releases/tag/v6.5.4)
- [Installation and connection guide](artifact/references/INSTALL-WINDOWS.md)
- [Security model and permissions](artifact/references/SECURITY.md)
- [Commands reference](artifact/references/COMMANDS.md)
- [Verification records and known limits](artifact/references/VERIFICATION.md)
- [Issue tracker](https://github.com/miracle1814/ue5-automation/issues)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, JSON, Shell commands, Configuration instructions]

**Output Format:** [Markdown operating guidance with JSON tool-call examples, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Windows 10/11 x64; requires the separate local UE5 bridge/MCP runtime. Engine support varies by version. The skill package contains instructions and references, not the runtime.]

## Skill Version(s):

6.5.11 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
