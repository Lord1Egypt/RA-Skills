## Description:

Automatically analyze and enhance content-short SKILL.md files by analyzing skill directory structure, adding usage examples, script documentation, common use cases, and best practices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[834948655](https://clawhub.ai/user/834948655)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to inspect short or incomplete SKILL.md files, generate documentation recommendations, and optionally append examples, script references, best practices, and common use cases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The enhancement script can overwrite a target SKILL.md file.

Mitigation: Run with --dry-run first, review the proposed content, and apply changes only to skills you control under version control.

Risk: Generated documentation may contain generic placeholders or inaccurate examples.

Mitigation: Review generated sections before committing and test any commands or examples that are added.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/834948655/skills/skill-doc-enhancer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance and JSON reports, with optional SKILL.md file edits]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can run in dry-run mode to preview documentation changes before writing files.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
