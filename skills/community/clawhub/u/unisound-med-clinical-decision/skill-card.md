## Description: <br>
Supports clinical decision and health management tasks including specialty treatment planning, primary care handling, general practice assistance, outcome analysis, condition review, and chronic disease management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unisound-llm](https://clawhub.ai/user/unisound-llm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and clinical workflow integrators use this skill to send medical questions to a configured medical language model and receive structured clinical assistance across selectable task modes. Outputs are intended to support review and workflow assistance, not to replace formal diagnosis or care decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Medical questions may be sent to a remote API without a documented consent, redaction, or minimization step. <br>
Mitigation: Use only de-identified inputs unless the publisher documents the processor, retention policy, consent flow, and privacy safeguards. <br>
Risk: Model output could be mistaken for a formal diagnosis or care decision. <br>
Mitigation: Require qualified clinical review and keep the output as assistance rather than authoritative medical advice. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/unisound-llm/unisound-med-clinical-decision) <br>
- [Publisher profile](https://clawhub.ai/user/unisound-llm) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON by default, optional plain text answer, and NDJSON for batch output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes task metadata, input provenance fields, model identifier, and the model answer; dry-run mode emits parsed input without calling the model.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
