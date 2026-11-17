## Description:

Provides medical exam, specialty Q&A, literature reading comprehension, medical term explanation, and terminology synonym matching by sending caller-provided questions to the configured medical model.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unisound-llm](https://clawhub.ai/user/unisound-llm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and medical knowledge workflow owners use this skill to route caller-supplied medical questions into task-specific prompts for exams, specialty Q&A, literature comprehension, term explanations, and synonym matching. Outputs are model-assisted information and are not formal clinical decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Caller-provided medical questions are sent to the documented external medical model endpoint.

Mitigation: Confirm the endpoint is approved for the intended data before use and de-identify real patient information.

Risk: The required app key can grant access to the external model service.

Mitigation: Protect the --appkey value as a secret and avoid placing it in shared logs, command history, or committed files.

Risk: Saved outputs can contain the original question and metadata.

Mitigation: Choose --output paths carefully and apply the same access controls used for the input data.

Risk: Model-assisted medical answers may be unsuitable as final clinical decisions.

Mitigation: Route outputs through qualified review and applicable clinical or institutional processes before use in patient care.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unisound-llm/skills/unisound-med-knowledge-qa)
- [Publisher profile](https://clawhub.ai/user/unisound-llm)
- [Configured medical model API endpoint](https://maas-api.hivoice.cn/v1/chat/completions)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [JSON object or NDJSON by default, with optional plain text answer output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can include the original question, task, metadata, model, input mode, and generated answer; batch input produces one JSON object per line.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
