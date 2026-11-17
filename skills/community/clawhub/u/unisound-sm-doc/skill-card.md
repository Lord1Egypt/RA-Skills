## Description:

Extracts and structures requested fields from medical record text by sending a question or structured input to a remote medical LLM and returning constrained answers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unisound-llm](https://clawhub.ai/user/unisound-llm)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and workflow operators use this skill to submit medical-record questions or JSON/JSONL records for entity extraction and structured answers. Outputs are model-assisted information and are not a substitute for formal clinical decision-making.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive medical text and API credentials can be sent to a remote or operator-configured endpoint.

Mitigation: Use de-identified data, keep the API key scoped, pin the API URL to an approved HTTPS host, and prevent untrusted users or integrations from controlling the API URL, system prompt, or output path.

Risk: Model-assisted medical output may be mistaken for a formal diagnosis or treatment decision.

Mitigation: Use the output only as an assistive extraction result and require review under the operator's clinical and institutional process before acting on it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unisound-llm/skills/unisound-sm-doc)

## Skill Output:

**Output Type(s):** [text, JSON]

**Output Format:** [JSON object for a single record, NDJSON for batch runs, or plain answer text when text-only output is selected]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes status, question, answer, record index, metadata, model, input mode, and optional output file contents.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
