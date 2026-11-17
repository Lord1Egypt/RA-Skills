## Description:

Assists pharmaceutical R&D teams with drug target screening by ranking candidate targets using target-disease association, evidence strength, druggability, and safety-risk signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unisound-llm](https://clawhub.ai/user/unisound-llm)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and pharmaceutical R&D teams use this skill to submit a disease or indication with candidate targets, then receive a ranked screening output with basis, target-level rationale, and risk notes. It is intended for research support and does not provide clinical diagnosis, treatment advice, or drug efficacy conclusions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends target-screening inputs to a remote medical model service, which may expose sensitive research data.

Mitigation: Use only with approval for the API key and endpoint terms; avoid confidential, regulated, or proprietary R&D inputs unless retention and access terms are acceptable.

Risk: Untrusted Office, PDF, or image inputs can expand the parsing surface through optional conversion and OCR tools.

Mitigation: Prefer JSON or trusted spreadsheet inputs, and avoid untrusted Office, PDF, and image files.

Risk: A fallback preprocessing path can execute Python code outside the packaged skill if the local parser fails.

Mitigation: Remove or pin the external shared preprocessing fallback before production use.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/unisound-llm/skills/unisound-target-screening)
- [Open Targets Database reference skill](https://agent-skills.md/skills/x-cmd/skill/opentargets-database)
- [Remote medical model endpoint](https://maas-api.hivoice.cn/v1/chat/completions)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [UTF-8 JSON containing structured ranked targets and Markdown natural-language analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an appkey for the remote medical model service; JSON-only inputs do not require optional document parsing dependencies.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
