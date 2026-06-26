## Description: <br>
Reviews prescription-audit, medical safety procedure, and medical ethics or legal questions through a command-line medical Q&A workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unisound-llm](https://clawhub.ai/user/unisound-llm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and clinical workflow integrators use this skill to submit prescription review, medical safety, and medical ethics questions by CLI and receive structured JSON or answer text from a configured medical model. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Medical question text is sent to the configured model API. <br>
Mitigation: Use de-identified inputs for testing and avoid identifiable patient information unless organizational policy permits that use. <br>
Risk: Model answers can be incomplete or inappropriate for clinical decisions. <br>
Mitigation: Treat outputs as assistive information and require qualified review before relying on them for diagnosis, treatment, or formal policy decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/unisound-llm/unisound-med-rx-safety-ethics) <br>
- [Default medical model API endpoint](https://maas-api.hivoice.cn/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files] <br>
**Output Format:** [Structured JSON by default, optional plain answer text, and NDJSON for batch output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write UTF-8 JSON or NDJSON to --output; dry-run returns parsed input without calling the model.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
