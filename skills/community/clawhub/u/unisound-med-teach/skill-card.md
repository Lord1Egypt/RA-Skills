## Description: <br>
Generates clinical teaching case responses from question text or structured inputs using an internal medical LLM. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unisound-llm](https://clawhub.ai/user/unisound-llm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and clinical education teams use this skill to turn de-identified case prompts into structured teaching-case answers that emphasize learning objectives, differential considerations, and ethical boundaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Clinical prompts are sent to a model API and may contain sensitive patient information if users provide raw case text. <br>
Mitigation: Use only de-identified teaching cases and follow local patient-data handling procedures before running the skill. <br>
Risk: The app key is required for non-dry-run calls and could grant access to the medical model API. <br>
Mitigation: Store the app key outside shared files and command logs, rotate it if exposed, and restrict access to trusted operators. <br>
Risk: A custom API URL can redirect prompts and credentials to an unintended service. <br>
Mitigation: Verify any --api-url value before use and prefer the expected medical model endpoint for production workflows. <br>
Risk: Output files may include clinical text, metadata, and local input paths. <br>
Mitigation: Write outputs only to secure locations and apply the same retention and access controls used for clinical teaching data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/unisound-llm/unisound-med-teach) <br>
- [Publisher profile](https://clawhub.ai/user/unisound-llm) <br>
- [Default medical model API endpoint](https://maas-api.hivoice.cn/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files] <br>
**Output Format:** [Structured JSON by default, plain answer text with --text-only, or UTF-8 JSON/NDJSON files when --output is used.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes status, question, answer, record index, metadata, model, input mode, and input path when applicable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
