## Description:

Create, edit, and automate presentations with programmatic tools, visual consistency, and project-based learning of user style preferences.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Employees, external users, and developers use this skill to create, edit, and validate presentation decks across PowerPoint, Google Slides, reveal.js, Slidev, and Marp workflows while preserving project style preferences.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may create local files under ~/slides and user-selected project paths.

Mitigation: Review generated file paths before execution and keep project, style, and template files in expected workspace locations.

Risk: Google Slides workflows may require service account credential files.

Mitigation: Keep credential files private, do not commit creds.json, and grant only the scopes needed for the presentation task.

Risk: Presentation tooling may rely on third-party packages or global npm installs.

Mitigation: Prefer pinned package versions, project-local dependencies, and locked environments before using the skill in shared or production workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/slides)
- [Programmatic slide tools](tools.md)
- [Visual design rules](design.md)
- [Deck structures by type](formats.md)
- [Memory setup](memory-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with code and shell command blocks; generated presentation artifacts may include PPTX, PDF, HTML, or Google Slides content.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local project, style, memory, template, version, and presentation files under ~/slides and user-selected project paths.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
