## Description:

Provides structured medical model assistance for specialty diagnosis and treatment, primary care handling, general practice support, outcomes analysis, condition analysis, and chronic disease management selected by --task.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unisound-llm](https://clawhub.ai/user/unisound-llm)

### License/Terms of Use:

MIT-0

## Use Case:

External integrators and clinical application developers use this skill to pass clinical questions into a medical LLM workflow for structured assistance across condition analysis, primary care, treatment planning, outcomes review, and chronic disease management. Outputs are auxiliary information and are not formal medical decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Clinical questions and bearer API keys can be sent to any configured API endpoint.

Mitigation: Pin --api-url to the intended trusted HTTPS endpoint, use endpoint-specific keys, and control who can invoke the script.

Risk: Clinical prompts may include identifiable patient information.

Mitigation: Do not send identifiable patient information unless the organization has approved the data flow, retention policy, and required de-identification process.

Risk: Model output may be mistaken for a formal diagnosis or treatment decision.

Mitigation: Treat answers as auxiliary information and require review through the applicable clinical workflow before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unisound-llm/skills/unisound-med-clinical-decision)
- [Publisher profile](https://clawhub.ai/user/unisound-llm)
- [Default OpenAI-compatible model endpoint](https://maas-api.hivoice.cn/v1/chat/completions)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [JSON by default, optional plain text answer with --text-only, and NDJSON for batched input]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write complete JSON or NDJSON results to --output; dry-run mode emits parsed input metadata without calling the model.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
