## Description:

Covers launching vvvv gamma from the command line or programmatically -- normal startup, opening specific .vl patches, command-line arguments, package repositories, and key filesystem paths (install directory, user data, sketches, exports, packages).

This skill is ready for commercial/non-commercial use.

## Publisher:

[tebjan](https://clawhub.ai/user/tebjan)

### License/Terms of Use:

CC-BY-SA-4.0

## Use Case:

Developers and engineers use this skill to start vvvv gamma, open .vl patches, configure command-line launch arguments, manage package repositories, and locate vvvv gamma filesystem paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Launching vvvv.exe with user-selected .vl patches or local package repositories may load and run project code.

Mitigation: Use trusted patch and package paths, and review selected launch arguments and repositories before running vvvv gamma.

## Reference(s):

- [vvvv Command-Line Arguments Reference](cli-reference.md)
- [ClawHub skill page](https://clawhub.ai/tebjan/skills/vvvv-startup)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance is documentation-only and focused on user-selected vvvv gamma launch paths, patches, and package repositories.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
