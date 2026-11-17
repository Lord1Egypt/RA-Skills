## Description:

Runs RenameRegex (RR.exe) as a preview-first Windows PowerShell workflow for regex-based bulk file and directory renaming.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nextaltair](https://clawhub.ai/user/nextaltair)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill when they need an agent to prepare safe RR.exe preview and apply commands for scoped regex bulk renaming on Windows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bulk regex renaming can change unintended files when the root folder, pattern, or replacement is too broad.

Mitigation: Choose a narrow root folder, run the pretend preview first, and review the preview output before approving apply.

Risk: The skill depends on an external RR.exe binary that is not bundled or validated by the artifact.

Mitigation: Verify the RR.exe binary separately and install the skill only when RR.exe is already intended for the workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nextaltair/skills/rr-renamer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline PowerShell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preview-first workflow; apply actions require explicit user approval.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
