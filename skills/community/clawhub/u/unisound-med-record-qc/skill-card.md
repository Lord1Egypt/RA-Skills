## Description: <br>
Extracts structured medical-record entities and supports chart, clinical-pathway, and imaging-report quality control through a standalone Python script. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unisound-llm](https://clawhub.ai/user/unisound-llm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Clinical and healthcare developers use this skill to pass de-identified medical records or report prompts to an approved medical LLM for entity extraction and quality-control review. Authorized operators can select chart quality control, clinical-pathway quality control, imaging-report text quality control, or structured medical-record extraction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Medical inputs or saved outputs may contain patient information. <br>
Mitigation: Use only approved, de-identified data and avoid shared terminals or CI logs for sensitive cases. <br>
Risk: The script requires an app key and a configured medical LLM endpoint. <br>
Mitigation: Verify endpoint authorization and handle the app key as a secret before use. <br>
Risk: Model answers may be mistaken for clinical decisions. <br>
Mitigation: Treat outputs as reference-only quality-control assistance and require review under local clinical procedures. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/unisound-llm/unisound-med-record-qc) <br>
- [Default OpenAI-compatible medical LLM endpoint](https://maas-api.hivoice.cn/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files, API Calls] <br>
**Output Format:** [JSON or NDJSON by default; plain text when --text-only is used; optional UTF-8 output file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include task metadata, the original question, selected model, input mode, and model answer; --output stores the full response.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
