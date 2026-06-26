## Description: <br>
Checks outpatient medical records for hypertension cases that omit the maximum blood pressure value and returns either no defect or a defect finding with the reason. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unisound-llm](https://clawhub.ai/user/unisound-llm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Clinical quality-control teams and developers use this skill to screen outpatient medical-record text and supported document formats for a specific hypertension documentation rule. It is an assistive review tool and its findings should be checked by qualified medical staff. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Medical-record inputs may contain PHI or other identifiable data and are sent to the configured model service. <br>
Mitigation: Use only authorized, de-identified records and an approved HTTPS model endpoint before running the skill. <br>
Risk: The required app key could expose access to the model service if committed or shared. <br>
Mitigation: Keep the app key out of repositories and logs, and provide it only through approved secret-handling processes. <br>
Risk: Prepared input text can be persisted when the optional save-prepared mode is used. <br>
Mitigation: Avoid save-prepared when records may contain PHI or identifiable data; if used for debugging, store outputs only in an approved secured location. <br>
Risk: The quality-control result is an assistive model output and may be incomplete or incorrect. <br>
Mitigation: Require qualified medical review before using findings for clinical, compliance, or operational decisions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/unisound-llm/unisound-hypertension-missing-bp) <br>
- [HiVoice-compatible medical model endpoint](https://maas-api.hivoice.cn/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [text, files, guidance] <br>
**Output Format:** [UTF-8 text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns no-defect text or defect text with a reason; the CLI can also write the result to an output file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
