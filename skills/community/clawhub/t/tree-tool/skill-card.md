## Description:

Display directory structure as an indented tree. Use for visualizing folder hierarchies and project structure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect folder hierarchies and summarize project structure as an indented directory tree.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documented CLI options do not fully match the bundled script; the script supports a path argument and -d/--depth, while the documentation lists -L, -a, -h, and -I behavior.

Mitigation: Verify supported arguments before use and invoke the bundled script with its supported path and -d/--depth options.

Risk: Directory listings may expose hidden or sensitive filenames in the conversation.

Mitigation: Run the skill only on paths whose file and directory names are appropriate to disclose, or filter sensitive paths before sharing output.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text directory tree, with Markdown shell command examples in the skill documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recursive directory listing; bundled script defaults to depth 3]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
