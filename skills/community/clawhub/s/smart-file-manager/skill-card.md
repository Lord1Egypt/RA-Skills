## Description:

Smart File Manager helps agents organize user-provided and generated files into standardized workspace folders with naming, classification, move, initialization, verification, and cleanup scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[buptlihang](https://clawhub.ai/user/buptlihang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to keep user input files and generated outputs organized under predictable workspace folders by file type. It provides shell-script workflows for initializing folders, copying files into classified locations, checking structure, and cleaning a known nested-output issue.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can broadly reorganize workspace files and remove nested output directories without enough validation, confirmation, or recovery safeguards.

Mitigation: Use it only in a controlled workspace and add explicit confirmation, safe filename validation, no-clobber behavior, checked moves, and non-recursive cleanup before using it on important or shared files.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with inline bash commands and shell script outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a fixed /workspace directory layout for user_input_files and my_outputs.]

## Skill Version(s):

1.2.0 (source: server release metadata and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
