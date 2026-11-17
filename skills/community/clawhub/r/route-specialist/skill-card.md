## Description:

Classifies coding tasks by domain and routes them to specialist prompts with recommended models and structured routing metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stephenlthorn](https://clawhub.ai/user/stephenlthorn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to classify incoming coding tasks, select an appropriate domain specialist, and return prompt and model-routing metadata before implementation begins.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task text and file paths may be sent to the configured LLM endpoint during ambiguous classification.

Mitigation: Confirm the OpenClaw LLM endpoint and model routing are acceptable for proprietary code, client work, or other sensitive task context before installation.

Risk: Incorrect routing could select a specialist prompt or model that is not suitable for the task.

Mitigation: Review the returned domain, specialist, and model metadata before relying on the generated implementation path.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, JSON, Configuration, Guidance]

**Output Format:** [Structured JSON-style routing metadata with specialist prompt text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes the selected domain, specialist name, system prompt, recommended model, detected frameworks, project path, multi-hop flag, and hard-gate status.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
