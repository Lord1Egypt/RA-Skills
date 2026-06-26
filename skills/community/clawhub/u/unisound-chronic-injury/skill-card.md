## Description: <br>
Reviews insurance-claim imaging or examination report text for a specified body part and asks an internal medical model to classify the injury status using the caller's required categories and output format. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unisound-llm](https://clawhub.ai/user/unisound-llm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Insurance claim reviewers and workflow agents use this skill to classify whether a specified body part shows chronic injury, acute injury, no injury, or no mention based on supplied medical report text. It is intended as an auxiliary review aid, not a forensic determination or final claim decision. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided medical report text is sent to the configured hivoice.cn/internal medical model endpoint. <br>
Mitigation: Use the skill only when the publisher and endpoint are trusted and organizational policy permits the processing. <br>
Risk: Inputs may contain names, ID numbers, imaging numbers, or other protected medical details. <br>
Mitigation: Redact sensitive identifiers before execution; the artifact states redaction is the caller's responsibility. <br>
Risk: The output is an auxiliary medical-claims classification and may be mistaken for a final claims or forensic decision. <br>
Mitigation: Require qualified human review before using the result in claim decisions. <br>
Risk: Using --output writes results locally. <br>
Mitigation: Use --output only when a local result file is intentionally required and handled under the appropriate data controls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/unisound-llm/unisound-chronic-injury) <br>
- [Publisher profile](https://clawhub.ai/user/unisound-llm) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, files] <br>
**Output Format:** [JSON result by default, plain model answer text with --text-only, or UTF-8 JSON/NDJSON file when --output is used.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes skill name, status, record index, metadata passthrough, input question, model name, input mode, optional input path, and the model-generated answer.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
