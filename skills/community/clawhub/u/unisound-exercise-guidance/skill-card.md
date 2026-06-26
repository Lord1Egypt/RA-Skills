## Description: <br>
Provides patient-facing post-surgery rehabilitation exercise guidance from existing exercise entries, formatted for structured display and Markdown guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unisound-llm](https://clawhub.ai/user/unisound-llm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Patients, care teams, or OpenClaw integrators use this skill to turn existing rehabilitation exercise details into structured instructions, precautions, and user-facing Markdown guidance. It is intended to display guidance from an existing plan and does not replace in-person clinical assessment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Medical-context inputs and extracted document content are sent to an external model API. <br>
Mitigation: Use only after privacy, retention, and compliance review; avoid patient identifiers or protected health information unless consent and secure handling are in place. <br>
Risk: The skill broadly processes documents and images before generating guidance. <br>
Mitigation: Run preprocessing in a sandboxed environment, install only the parsers needed for the chosen input types, and review extracted content before submission. <br>
Risk: Generated rehabilitation guidance may be inappropriate if the source plan is incomplete, outdated, or not patient-specific. <br>
Mitigation: Use the output as display guidance for an existing rehabilitation plan and have qualified clinical staff review care decisions and patient-specific changes. <br>


## Reference(s): <br>
- [CareKit instructions task view reference](https://github.com/carekit-apple/CareKit) <br>
- [ClawHub skill page](https://clawhub.ai/unisound-llm/unisound-exercise-guidance) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [UTF-8 JSON containing structured exercise fields and Markdown natural-language guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an appkey for the remote u1-insuremed model; optional preprocessing supports JSON, CSV, Excel, text, PDF, Word, and image inputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
