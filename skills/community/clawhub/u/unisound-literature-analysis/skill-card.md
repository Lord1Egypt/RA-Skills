## Description:

Analyzes pharmaceutical R&D literature for medical affairs workflows by matching literature to a research topic, extracting key findings, summarizing evidence, and identifying research gaps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unisound-llm](https://clawhub.ai/user/unisound-llm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and medical affairs teams use this skill to turn structured or extracted literature inputs into topic-matched evidence summaries for pharmaceutical R&D analysis. It is intended for research reference and does not provide clinical diagnosis, individualized treatment guidance, or promotional drug conclusions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected literature fields and extracted document text are sent to the maas-api.hivoice.cn medical model service.

Mitigation: Use the skill only with content approved for that service, and avoid confidential, unpublished, regulated, or licensed material unless organizational policy permits it.

Risk: App keys may be exposed if passed directly on command lines or logs.

Mitigation: Prefer a secrets-managed invocation path and avoid including real app keys in shell history, logs, or shared examples.

Risk: Document and OCR preprocessing can process untrusted files and may execute external conversion tools.

Mitigation: Prefer JSON input when possible and run file preprocessing in a sandboxed environment for untrusted documents or images.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unisound-llm/skills/unisound-literature-analysis)
- [Publisher profile](https://clawhub.ai/user/unisound-llm)
- [Referenced Literature Review skill](https://agent-skills.md/skills/ovachiever/droid-tings/literature-review)
- [Medical model API endpoint](https://maas-api.hivoice.cn/v1/chat/completions)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown, Files]

**Output Format:** [UTF-8 JSON containing structured data and Markdown analysis text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write an output JSON file and, when requested, a prepared intermediate JSON file.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
