## Description:

Build and maintain a reusable source-research system for discovering source pools, evaluating them, defining acquisition and filtering methods, recording rejection decisions, and producing high-quality source lists or notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[myvyang](https://clawhub.ai/user/myvyang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and agents use this skill to create reusable records for source pools, acquisition methods, filtering methods, high-quality source lists, captured information, rejection decisions, and automation notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create or update .source-research/ notes and templates in the current workspace.

Mitigation: Enable it only in workspaces where persistent source-curation records are wanted, and review generated Markdown artifacts before relying on them.

## Reference(s):

- [Source Research Skill](https://clawhub.ai/myvyang/skills/source-research)
- [Framework Reference](references/framework.md)
- [Artifact Reference](references/artifacts.md)
- [Storage Specification](references/storage.md)
- [Organization Research Notes](references/organization.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown files and concise agent guidance, with optional shell commands for initializing workspace storage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates disclosed source-research artifacts in the workspace, typically under .source-research/.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
