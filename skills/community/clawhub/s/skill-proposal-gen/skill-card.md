## Description:

Generates and manages structured proposal drafts for performance, cultural tourism, meeting, and exhibition projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zimuge-doudou](https://clawhub.ai/user/zimuge-doudou)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators can use this skill to create, update, list, export, and generate structured project proposal drafts. It is aimed at routine business workflows, automation tasks, and proposal data handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe project-name handling could allow proposal JSON or Markdown files to be read from or overwritten outside the intended proposal folder.

Mitigation: Run the skill only in a constrained environment until project names are validated to reject path separators, parent-directory traversal, and absolute paths.

Risk: The skill creates local proposal JSON and Markdown files.

Mitigation: Review the target working directory and generated files before using the outputs in business workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zimuge-doudou/skills/skill-proposal-gen)
- [Publisher profile](https://clawhub.ai/user/zimuge-doudou)

## Skill Output:

**Output Type(s):** [text, markdown, configuration]

**Output Format:** [CLI text, JSON proposal records, and Markdown proposal documents]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local proposal JSON and Markdown files under its proposals directory.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
