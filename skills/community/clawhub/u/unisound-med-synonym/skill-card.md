## Description:

Matches medical terms to equivalent or closest standardized synonyms from caller-provided questions using a configured medical LLM.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unisound-llm](https://clawhub.ai/user/unisound-llm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and medical workflow integrators use this skill to submit medical terminology questions and receive synonym-matching answers with brief rationale. It supports direct questions, JSON or JSONL records, stdin, and batch selection for integration into evaluation or operational pipelines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Medical questions and the bearer API key can be sent to a caller-supplied API URL.

Mitigation: Use only trusted HTTPS endpoints, avoid untrusted --api-url values, and treat the app key as sensitive.

Risk: Medical prompts may contain real patient identifiers or sensitive clinical details.

Mitigation: De-identify patient data before use and follow applicable institutional review and handling procedures.

Risk: Model output is assistive and may be unsuitable as a formal clinical decision.

Mitigation: Have qualified personnel review outputs before clinical or operational reliance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unisound-llm/skills/unisound-med-synonym)
- [Unisound-LLM publisher profile](https://clawhub.ai/user/unisound-llm)
- [Default medical LLM API endpoint](https://maas-api.hivoice.cn/v1/chat/completions)

## Skill Output:

**Output Type(s):** [text, JSON, files]

**Output Format:** [JSON by default; plain text with --text-only; NDJSON for batch output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write results to a configured output path; dry-run returns parsed input without a model answer.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
