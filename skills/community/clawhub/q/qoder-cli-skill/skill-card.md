## Description:

Delegates coding tasks to Qoder CLI in non-interactive Print mode for feature development, code review, refactoring, and file-exploration workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lfeng](https://clawhub.ai/user/lfeng)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to delegate coding tasks to Qoder CLI from automated or shared sessions while keeping Qoder in non-interactive Print mode.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends bypassing permission checks with Qoder yolo mode.

Mitigation: Use project-scoped Qoder permissions and avoid yolo mode unless a trusted reviewer has approved the task and workspace.

Risk: The skill shows unpinned npx MCP server commands, which can install or execute changing external packages.

Mitigation: Pin MCP package versions and review MCP server registrations before use.

Risk: The skill describes broadly inherited Qoder access tokens and persistent Qoder state.

Mitigation: Keep Qoder tokens out of globally inherited shell startup files and audit Qoder agents, memory files, settings, MCP registrations, and background jobs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lfeng/skills/qoder-cli-skill)
- [Publisher profile](https://clawhub.ai/user/lfeng)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires qodercli to be installed; Qoder TUI mode is not supported in automated sessions.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
