## Description: <br>
Provides medical exam, specialty Q&A, literature comprehension, terminology explanation, and synonym-matching answers by sending caller-provided questions to a configurable medical language model. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unisound-llm](https://clawhub.ai/user/unisound-llm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and integrators use this skill to route medical knowledge questions into task-specific prompts for exams, specialty Q&A, literature comprehension, terminology explanations, and synonym matching. The output is model-assisted information and is not a formal clinical decision. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Questions are sent to the configured medical model API, which can expose sensitive health or patient-identifying information. <br>
Mitigation: Use the skill only with trusted, approved model endpoints and do not include patient-identifying, confidential, or regulated health data unless the workflow is authorized. <br>
Risk: Medical answers may be mistaken for formal diagnosis or treatment decisions. <br>
Mitigation: Treat outputs as model-assisted information and require qualified review before clinical or operational use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/unisound-llm/unisound-med-knowledge-qa) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, files] <br>
**Output Format:** [JSON or plain text; batch output may be NDJSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write full UTF-8 JSON results to a file and can emit answer text only when requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
