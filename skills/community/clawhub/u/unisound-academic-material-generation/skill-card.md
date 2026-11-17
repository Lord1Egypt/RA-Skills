## Description:

Generates structured academic material drafts for pharmaceutical medical-affairs work from a material type, topic, audience, key messages, evidence points, and references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unisound-llm](https://clawhub.ai/user/unisound-llm)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and pharmaceutical medical-affairs teams use this skill to create first-draft academic materials for clinical or scientific audiences. The output is intended for review by medical, compliance, and subject-matter experts before use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill conditionally runs preprocessing code from outside the reviewed package.

Mitigation: Install only after manual review of the skill and the runtime _shared/doc-preprocess location.

Risk: Submitted inputs are sent to the configured remote medical-model API.

Mitigation: Do not submit PHI, confidential strategy, or regulated data unless the organization has approved that API flow.

Risk: Document conversion and OCR for untrusted files can increase execution risk.

Mitigation: Run document preprocessing in a sandboxed environment and limit optional converters or OCR tools to trusted inputs.

Risk: Generated medical-affairs drafts may be mistaken for final reviewed materials.

Mitigation: Require medical, compliance, and subject-matter expert review before publication or operational use.

Risk: Long-lived API keys may be exposed when passed directly in shell commands.

Mitigation: Use approved secret handling and short-lived credentials where available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unisound-llm/skills/unisound-academic-material-generation)
- [Referenced Scientific Writing skill](https://agent-skills.md/skills/ovachiever/droid-tings/scientific-writing)
- [Configured remote medical-model API endpoint](https://maas-api.hivoice.cn/v1/chat/completions)

## Skill Output:

**Output Type(s):** [text, markdown, json]

**Output Format:** [UTF-8 JSON object with structured data and generated Markdown text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated medical-affairs content is a draft and requires expert review before use.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence; artifact _meta.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
