## Description:

Truth Check guides an agent to verify generated technical content, statistics, references, code examples, and external-operation results for hallucinations or inaccuracies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jack123255829](https://clawhub.ai/user/jack123255829)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to prompt verification after generating technical content, numbers, references, code examples, or results from external actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages running generated code for verification without built-in limits or approval steps.

Mitigation: Review generated code first and run it only in an isolated, disposable environment with no secrets and explicit approval for external side effects.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jack123255829/skills/truth-check)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Text]

**Output Format:** [Markdown text with verification checklists and confidence labels]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses VERIFIED, LIKELY, and UNCERTAIN labels to summarize confidence.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
