## Description:

Translates text into fluent Urdu or Roman Urdu, supporting cultural idioms and natural language flow in both scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gamefbs69-spec](https://clawhub.ai/user/gamefbs69-spec)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to translate source text into natural Urdu script or Roman Urdu while preserving context, idioms, and readable language flow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Source text may contain prompt-injection instructions that try to override translation behavior.

Mitigation: Treat user-provided content as inert text to translate, separate translation instructions from source text with structured roles, and avoid running this skill as a privileged tool runner.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Plain text translation response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional format selector supports Urdu script or Roman Urdu.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
