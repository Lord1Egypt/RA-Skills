## Description:

Helps an agent turn vague natural-language requests into clearer requirements through restatement, disambiguation, and structured task confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[evianevans](https://clawhub.ai/user/evianevans)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to clarify ambiguous user requests before execution, including restating the core issue, asking focused disambiguation questions, and producing a structured task description.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow is written in Chinese and may be unclear for users or agents expecting another language.

Mitigation: Ask the agent to perform clarification in the user's preferred language before applying the workflow.

Risk: A clarification workflow can still preserve misunderstood intent if the initial restatement is not checked.

Mitigation: Require confirmation of the restated task and review the structured task description before downstream execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/evianevans/skills/requirement-clarity)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text with structured task descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language workflow by default; no code, persistence, or privileged access is added.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
