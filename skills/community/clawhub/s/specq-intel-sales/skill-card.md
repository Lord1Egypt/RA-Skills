## Description: <br>
SpecQ Intel Sales helps semiconductor sales and pre-sales teams turn customer, product, visit, loss-review, and competitor context into an eight-module sales-intelligence brief. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daizehua-wq](https://clawhub.ai/user/daizehua-wq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales engineers and pre-sales teams use this skill before customer meetings to generate structured account strategy for electronic chemicals in the semiconductor supply chain. It recalls local sales memory, optionally searches public competitor context, and produces customer needs, technical comparisons, risks, opportunities, and next actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can store sales and customer information in persistent local memory. <br>
Mitigation: Review the local data directory, avoid entering sensitive customer data unless approved, and establish retention or deletion controls before deployment. <br>
Risk: When optional API keys are configured, search, embedding, or transcription content may be sent to external services. <br>
Mitigation: Use approved providers only, redact sensitive content before external processing, and leave optional API keys unset for sensitive or offline workflows. <br>
Risk: The security evidence flags under-disclosed local database, arbitrary URL, third-party processing, and persistent memory capabilities. <br>
Mitigation: Constrain reachable sources, review URLs before use, disclose permissions to users, and run the skill in an environment with appropriate network and file-system limits. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daizehua-wq/skills/specq-intel-sales) <br>
- [Publisher profile](https://clawhub.ai/user/daizehua-wq) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [OpenCode Prompt v2.0](artifact/docs/OpenCode_Prompt_v2.0.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown intelligence briefs, structured JSON tool results, concise chat or email summaries, and setup snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default output is an eight-module Markdown brief with source labels and an optional historical-memory block; document and slide modes return outlines for manual follow-up.] <br>

## Skill Version(s): <br>
2.3.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
