## Description:

Generate complete projects from a PRD and stack template, including directory structure, configuration, project documentation, git setup, and optional private GitHub push.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fortunto2](https://clawhub.ai/user/fortunto2)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to bootstrap new software projects from a PRD and selected stack, producing starter files, docs, build commands, git history, and project-specific agent guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create or modify local project files and store organization defaults in the user's home directory.

Mitigation: Review the proposed target path, stack, and organization defaults before confirming file creation.

Risk: The skill can initialize git, create a private GitHub repository using the user's gh authentication, and push generated files that may include PRD or internal content.

Mitigation: Confirm the repository name, private visibility, and included project content before allowing the GitHub push.

## Reference(s):

- [Scaffold Skill Page](https://clawhub.ai/fortunto2/skills/solo-scaffold)
- [Stack-Specific File Structures](artifact/references/stack-structures.md)

## Skill Output:

**Output Type(s):** [Files, Code, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Generated project files, Markdown documentation, configuration files, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local project directories, store organization defaults, initialize git, and push a private GitHub repository after user confirmation.]

## Skill Version(s):

1.5.1 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
