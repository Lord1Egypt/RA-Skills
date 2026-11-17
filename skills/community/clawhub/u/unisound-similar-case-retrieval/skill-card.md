## Description:

Supports clinical research similar-case retrieval by comparing a de-identified anchor case against candidate case summaries and producing semantic rankings with explanatory rationale.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unisound-llm](https://clawhub.ai/user/unisound-llm)

### License/Terms of Use:

MIT-0

## Use Case:

Clinical researchers, educators, and developers use this skill to compare a de-identified anchor case with a prepared candidate set, review similarity reasoning, and identify cohort or subgroup analysis ideas. Outputs are for research, teaching, or methodology discussion and are not diagnostic or treatment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Case summaries are sent to a documented remote medical LLM endpoint.

Mitigation: Use only de-identified summaries unless the organization has approved that data flow for identifiable patient data.

Risk: The API key is accepted directly as a command-line argument.

Mitigation: Prefer a safer secret-handling method in deployment, such as an approved secret store or environment-mediated injection.

Risk: The generated similarity ranking and explanation may be mistaken for clinical guidance.

Mitigation: Use outputs for research, teaching, or methodology discussion only and keep human clinical review outside this skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unisound-llm/skills/unisound-similar-case-retrieval)
- [Hivoice medical LLM chat completions endpoint](https://maas-api.hivoice.cn/v1/chat/completions)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [JSON object with structured data and Markdown analysis text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes the anchor case, candidate count, top_k value, candidate IDs, and an AI-generated research disclaimer.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
