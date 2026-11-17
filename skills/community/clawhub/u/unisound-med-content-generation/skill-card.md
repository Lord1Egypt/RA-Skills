## Description:

Generates medical education content, clinical-document summaries, terminology explanations, teaching cases, and draft clinical note text through selectable task modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unisound-llm](https://clawhub.ai/user/unisound-llm)

### License/Terms of Use:

MIT-0

## Use Case:

Healthcare content teams, educators, and integrators use this skill to turn a supplied medical question or document excerpt into auxiliary explanatory, educational, summarization, or draft documentation output. Use only de-identified medical content and human review because outputs are not clinical decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive medical text may be sent to a configurable remote API.

Mitigation: Use only de-identified medical content and verify that the configured endpoint is a trusted HTTPS service approved for the workflow.

Risk: Bearer app keys may be exposed to untrusted custom endpoints or command-line handling.

Mitigation: Treat app keys as sensitive, avoid production keys with custom endpoints, and keep keys out of logs, shell history, and shared scripts.

Risk: Generated medical content may be inaccurate or unsuitable for clinical use.

Mitigation: Require qualified human review and follow institutional procedures before using outputs in education, documentation, or patient-facing material.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unisound-llm/skills/unisound-med-content-generation)
- [Publisher profile](https://clawhub.ai/user/unisound-llm)
- [Default API endpoint](https://maas-api.hivoice.cn/v1/chat/completions)

## Skill Output:

**Output Type(s):** [text, JSON, files]

**Output Format:** [JSON by default, plain text with --text-only, and NDJSON for batch output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can save full JSON or NDJSON to --output; dry-run returns parsed input without calling the model.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
