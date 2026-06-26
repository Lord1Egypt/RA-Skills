## Description: <br>
Screens pharma drug-development candidate targets by ranking disease-target associations using evidence strength, druggability, and safety risk. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unisound-llm](https://clawhub.ai/user/unisound-llm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Pharma R&D teams use this skill to screen and prioritize candidate drug targets for a disease or indication from a supplied target list. It produces ranked structured results and a Markdown analysis for evidence review, not clinical diagnosis or treatment guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Potentially sensitive disease, target, mechanism, evidence, druggability, safety-risk, and reference data may be sent to an external LLM endpoint. <br>
Mitigation: Install only if your organization approves this data transfer and avoid confidential or regulated data unless that use is explicitly approved. <br>
Risk: DOC, XLS, PDF, and image inputs can invoke broad local document parsers or converters without strong containment guidance. <br>
Mitigation: Prefer trusted JSON or CSV inputs; use document and image parsing only in a contained environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/unisound-llm/unisound-target-screening) <br>
- [Open Targets Database skill reference](https://agent-skills.md/skills/x-cmd/skill/opentargets-database) <br>
- [HiVoice medical LLM chat completions endpoint](https://maas-api.hivoice.cn/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Markdown, Text] <br>
**Output Format:** [UTF-8 JSON containing structured ranked targets and Markdown natural-language analysis] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an appkey for the documented external medical LLM endpoint; JSON-only input requires no optional parser packages.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
