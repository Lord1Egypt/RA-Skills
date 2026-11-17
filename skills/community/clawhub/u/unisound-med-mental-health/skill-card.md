## Description:

Provides mental-health support responses and psychological health Q&A through task-specific prompts to a remote medical chat-completions model.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unisound-llm](https://clawhub.ai/user/unisound-llm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and integrators use this skill to route user-provided mental-health consultation or education prompts to a medical language model and receive structured responses. It supports direct questions, JSON, JSONL, plain text, stdin, dry-run parsing, and optional saved output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive patient or mental-health text can be sent to a configurable remote API with a bearer key.

Mitigation: Use only a trusted HTTPS endpoint, avoid overriding --api-url unless the destination is controlled, use a scoped key, and de-identify real patient or personal mental-health information before use.

Risk: The model output is supportive or educational assistance and may be mistaken for formal diagnosis or treatment advice.

Mitigation: Review outputs before clinical or operational use and direct crisis-risk cases to professional help and local emergency procedures.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unisound-llm/skills/unisound-med-mental-health)
- [Publisher profile](https://clawhub.ai/user/unisound-llm)
- [Default medical chat-completions endpoint](https://maas-api.hivoice.cn/v1/chat/completions)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON by default, plain text with --text-only, or NDJSON for batch output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write UTF-8 JSON or NDJSON to a file; dry-run mode emits parsed request data without calling the model.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact _meta.json lists 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
