## Description:

Find Unreal Engine assets such as .uasset, .umap, .uby, and .udata files for maps, UI widgets, blueprints, audio, data tables, and references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vincentwilliam](https://clawhub.ai/user/vincentwilliam)

### License/Terms of Use:


## Use Case:

Developers and technical artists use this skill to locate Unreal Engine project assets and generate focused PowerShell searches for maps, blueprints, UI assets, audio files, data tables, and related references.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad recursive searches can surface local project data from Saved, logs, configs, or save-game folders.

Mitigation: Review proposed search paths before execution and exclude sensitive directories unless they are needed for the task.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vincentwilliam/skills/ue-asset-finder)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown text with PowerShell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results should include full path, file size, last modified date, and dependency or reference details when available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
