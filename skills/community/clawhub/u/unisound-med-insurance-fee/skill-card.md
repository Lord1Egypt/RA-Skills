## Description:

医保理赔单据合规审核与医保费用核算规则应用；仅含 `scripts/run.py`，可独立拷贝部署。

This skill is ready for commercial/non-commercial use.

## Publisher:

[unisound-llm](https://clawhub.ai/user/unisound-llm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and healthcare operations teams use this skill to submit de-identified medical insurance questions to a configured medical LLM for claim compliance checks or fee calculations. Its output is model-assisted information and should not be treated as a formal clinical or reimbursement decision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send sensitive medical insurance questions to a configurable external HTTPS API endpoint.

Mitigation: Use only de-identified data unless external API processing has been approved by the organization.

Risk: The skill sends a bearer key when invoking the configured API.

Mitigation: Avoid passing production secrets on the command line, restrict use to vetted endpoints, and rotate any key that may have been sent to an untrusted endpoint.

Risk: The generated answer is model-assisted medical insurance guidance and may be incomplete or incorrect.

Mitigation: Review outputs under applicable clinical, reimbursement, and organizational workflows before using them for decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unisound-llm/skills/unisound-med-insurance-fee)
- [Default medical LLM chat completions endpoint](https://maas-api.hivoice.cn/v1/chat/completions)

## Skill Output:

**Output Type(s):** [text, JSON, files, guidance]

**Output Format:** [JSON by default, optional plain text answer, or NDJSON for batch output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write UTF-8 JSON or NDJSON output files when an output path is provided.]

## Skill Version(s):

1.0.2 (source: server release metadata, created 2026-07-16)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
