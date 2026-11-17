## Description:

Tool Master helps an agent map Chinese task keywords to practical command-line and OpenClaw tools using a curated keyword-to-command table.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iamwangli](https://clawhub.ai/user/iamwangli)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to choose suitable shell, development, system, network, and OpenClaw commands from Chinese task keywords, then return command-oriented guidance or execute approved commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can steer an agent toward broad local commands and OpenClaw administrative operations with weak guardrails.

Mitigation: Require explicit user approval, command previews, and scope checks before deletion, file edits, network requests, session or configuration access, OpenClaw admin changes, service restarts, or backup restore operations.

Risk: Keyword-to-command matches can select an inappropriate or overly broad command for the user's actual intent.

Mitigation: Validate the selected command against the user request and prefer non-destructive inspection commands before any state-changing operation.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on matching user or task keywords against the bundled command map.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
