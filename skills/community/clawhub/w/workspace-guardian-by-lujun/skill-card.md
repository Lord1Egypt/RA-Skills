## Description:

Workspace Guardian guides agents to place, name, organize, and clean workspace files consistently when users have not specified exact paths.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lujun2508](https://clawhub.ai/user/lujun2508)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to keep generated files in predictable project directories, apply naming conventions, and manage temporary or rejected outputs when no exact path is provided.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives broad default file-placement instructions that may conflict with a user's unstated preference.

Mitigation: Confirm the target project and destination before creating non-temporary files when the path is ambiguous.

Risk: The skill authorizes deletion or archiving when users reject, redo, or regenerate outputs without always requiring explicit deletion approval.

Mitigation: Ask before deleting or archiving any non-temporary output unless the user explicitly requested deletion.

Risk: Cleanup guidance for failed scripts and temporary files may remove material that is still useful for troubleshooting.

Mitigation: Retain or archive diagnostic files when they may help explain failures, and clean only clearly temporary files automatically.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lujun2508/skills/workspace-guardian-by-lujun)

## Skill Output:

**Output Type(s):** [Guidance, Configuration]

**Output Format:** [Markdown instructions and policy text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Applies default file placement, naming, and cleanup guidance for agent workspace activity.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
