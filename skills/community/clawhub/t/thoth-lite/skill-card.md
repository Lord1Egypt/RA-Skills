## Description:

Thoth Lite -- Auto-Documentation. Point Thoth at a file or folder and get a clean README instantly. Free tier.

This skill is ready for commercial/non-commercial use.

## Publisher:

[occupythemilkyway](https://clawhub.ai/user/occupythemilkyway)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to scan a file or project folder and generate a concise README from the discovered source files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill copies raw project file contents into the agent context, which may expose secrets or private configuration if a broad path is selected.

Mitigation: Use a narrow PROJECT_PATH and avoid directories that may contain secrets, credentials, or private configuration.

Risk: The install step uses an unpinned Python package with system-package override flags.

Mitigation: Install dependencies in a virtual environment and pin package versions before running the skill.

## Reference(s):

- [Thoth Lite ClawHub page](https://clawhub.ai/occupythemilkyway/skills/thoth-lite)
- [Thoth Lite homepage](https://clawhub.ai/occupythemilkyway/thoth-lite)
- [OccupyTheMilkyWay publisher profile](https://clawhub.ai/user/occupythemilkyway)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates README guidance from up to 20 discovered files, reading the first 3000 characters from each file.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
