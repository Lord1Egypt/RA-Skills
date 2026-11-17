## Description:

Use this skill when the user wants to analyze or explore a codebase using Repomix, including remote repositories, local repositories, repository structure, file and token counts, and code patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kongyo2](https://clawhub.ai/user/kongyo2)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to pack repositories with Repomix and analyze the generated output for structure, metrics, important files, and implementation patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs the agent to run npx repomix@latest, which can download and execute mutable third-party code.

Mitigation: Pin Repomix to a reviewed version and ask the user before first execution or network access.

Risk: Repository packing reads local or remote repository contents and writes generated output files that may be large or sensitive.

Mitigation: Validate repository and path inputs, keep remote outputs in /tmp, and limit cleanup to known generated files.

## Reference(s):

- [Repomix](https://github.com/yamadashy/repomix)
- [Repomix Explorer on ClawHub](https://clawhub.ai/kongyo2/skills/repomix-explorer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and repository analysis summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create Repomix output files such as XML, Markdown, JSON, or plain text for analysis.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
