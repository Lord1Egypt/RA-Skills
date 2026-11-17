## Description:

Internal reasoning from <think> blocks leaks into the final user-facing reply instead of being stripped.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mvogt99](https://clawhub.ai/user/mvogt99)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to diagnose replies that expose hidden reasoning tags or planning preambles, then apply prompt or output-handling changes that keep internal reasoning out of the user-facing response.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompt or output-handling changes based on this guidance could over-trim valid answer content.

Mitigation: Test changes against raw and final model outputs, and limit redaction to recognized reasoning tags or clear planning preambles.

Risk: The skill describes leakage symptoms but does not automatically verify provider-specific reasoning channel behavior.

Mitigation: Use provider-supported reasoning channels where available and inspect raw outputs in a test harness before deploying changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mvogt99/skills/think-block-leakage)
- [Publisher profile](https://clawhub.ai/user/mvogt99)

## Skill Output:

**Output Type(s):** [Guidance, Markdown]

**Output Format:** [Markdown guidance with troubleshooting bullets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No code execution, tool calls, or privileged data access described.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
