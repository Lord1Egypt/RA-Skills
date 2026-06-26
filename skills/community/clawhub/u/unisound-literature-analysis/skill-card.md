## Description: <br>
Analyzes medical and pharmaceutical R&D literature by matching literature to research themes, structuring evidence, extracting key findings, summarizing evidence, and identifying research gaps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unisound-llm](https://clawhub.ai/user/unisound-llm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, pharmaceutical R&D teams, and medical affairs users use this skill to prepare structured evidence summaries from supplied literature records. It is intended for research literature organization and does not provide clinical diagnosis, treatment advice, or drug promotion conclusions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Supplied literature content may be sensitive and is sent to a remote medical model endpoint for semantic analysis. <br>
Mitigation: Install only where this remote processing is approved, and avoid confidential, unpublished, regulated, or personal medical data unless the API provider's retention and processing terms are acceptable. <br>
Risk: The artifact includes a shared preprocessing fallback that is under-disclosed in the public skill description. <br>
Mitigation: Review or remove the external _shared preprocessing fallback before production use. <br>
Risk: Generated medical literature summaries may be incomplete or misleading if treated as clinical or promotional conclusions. <br>
Mitigation: Use outputs for research literature organization only and require qualified review before relying on them for medical, regulatory, or product decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/unisound-llm/unisound-literature-analysis) <br>
- [Referenced Literature Review evidence synthesis skill](https://agent-skills.md/skills/ovachiever/droid-tings/literature-review) <br>
- [Configured hivoice medical model endpoint](https://maas-api.hivoice.cn/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Markdown, Text] <br>
**Output Format:** [UTF-8 JSON containing structured analysis data and Markdown natural-language summary text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an appkey bearer token and sends matched literature content to the configured medical model API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
