## Description:

Adapt an existing agent skill so it works cleanly on Windows when the input is either a skill folder path or a zip file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iideas18](https://clawhub.ai/user/iideas18)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to convert agent skills distributed as folders or zip files so their instructions, paths, scripts, and packaging work cleanly on Windows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs an agent to edit or copy skill folders and may rebuild zip artifacts.

Mitigation: Review the generated Windows-ready folder or rebuilt zip before using it, especially when the original skill contains scripts.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/iideas18/skills/transfer-skill-to-windows)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with edited skill files and optional rebuilt zip artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce a sibling Windows-ready skill folder and, when the input is a zip file, a rebuilt Windows-ready zip.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
