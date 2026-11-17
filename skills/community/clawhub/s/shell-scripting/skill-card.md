## Description:

Write robust, portable shell scripts. Use when parsing arguments, handling errors properly, writing POSIX-compatible scripts, managing temp files, running commands in parallel, managing background processes, or adding --help to scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gitgoodordietrying](https://clawhub.ai/user/gitgoodordietrying)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to draft and improve shell scripts for automation, argument parsing, error handling, cleanup, portability, parallel execution, process management, and help text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead an agent to suggest insecure shell snippets.

Mitigation: Review generated shell code before use, especially snippets that handle filenames, source configuration files, download URLs, or remove files recursively.

Risk: Shell guidance can produce unintended command execution or deletion when copied into a script without local review.

Mitigation: Validate generated scripts with manual review and shell linting before running them against real files or systems.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gitgoodordietrying/skills/shell-scripting)
- [Publisher profile](https://clawhub.ai/user/gitgoodordietrying)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides examples and implementation guidance for shell scripts; it does not execute commands by itself.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
