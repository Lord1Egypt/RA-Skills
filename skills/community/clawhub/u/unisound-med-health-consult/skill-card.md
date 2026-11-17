## Description:

Provides health consultation, physical exam interpretation, and medical department-routing guidance through task-specific prompts to a configured medical LLM.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unisound-llm](https://clawhub.ai/user/unisound-llm)

### License/Terms of Use:

MIT-0

## Use Case:

External users and integrators use this skill to submit health questions, physical exam interpretation requests, or triage-routing prompts to a medical LLM and receive explanatory answers or suggested registration departments. Outputs are model-assisted information and are not formal clinical decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive health questions and bearer credentials can be sent to the configured API endpoint.

Mitigation: Use only de-identified questions, avoid passing secrets through shell history where possible, and keep --api-url limited to trusted HTTPS endpoints.

Risk: Model-assisted medical guidance may be incomplete, misleading, or unsuitable for regulated patient care.

Mitigation: Treat outputs as informational support only and require appropriate clinical review before using them in real patient workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unisound-llm/skills/unisound-med-health-consult)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [JSON by default, with optional plain text answer output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports single-question, JSON, JSONL batch, text file, and stdin inputs; can write complete JSON or NDJSON results to a file.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
