## Description:

Repeatedly output a string (or 'y' by default) for automated scripts, batch confirmation, and pipeline input generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this skill to generate repeated responses for scripts, prompt confirmation flows, pipeline tests, and other stdin-driven automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic confirmations can approve installer, setup, or deletion prompts without human review.

Mitigation: Use only with fully understood, trusted, non-destructive commands, and review the receiving command before piping automatic responses into it.

Risk: Unbounded repeated output can hang or flood a pipeline if the receiving process does not terminate.

Mitigation: Use external timeouts or process controls when bounded output is required, and stop the process promptly when the downstream command is complete.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell command examples and text stream output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled command-line behavior emits repeated text until the downstream pipe closes or the process is stopped.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
