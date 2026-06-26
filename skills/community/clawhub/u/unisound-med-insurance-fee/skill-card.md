## Description: <br>
Applies medical insurance claim compliance review and medical insurance fee calculation rules through a configurable LLM-backed command-line wrapper. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unisound-llm](https://clawhub.ai/user/unisound-llm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and healthcare insurance workflow integrators use this skill to submit medical-insurance questions or claim records for fee calculation and claim compliance review through a configured model endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Medical-insurance questions or claim records may contain patient identifiers or sensitive claim details. <br>
Mitigation: Remove patient identifiers and sensitive claim details unless the organization has approved sending that data to the documented or configured model endpoint. <br>
Risk: API keys may be exposed when passed directly in shell commands. <br>
Mitigation: Use safer secret handling appropriate to the deployment environment instead of embedding keys in command history or shared scripts. <br>
Risk: Saved outputs may contain the original question, metadata, and model-generated answer. <br>
Mitigation: Store outputs only in approved locations and apply the same handling controls used for the underlying insurance or medical data. <br>
Risk: Model output is assistive and may be unsuitable as a final medical or claims decision. <br>
Mitigation: Route outputs through the organization's clinical, compliance, or claims-review process before operational use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/unisound-llm/unisound-med-insurance-fee) <br>
- [Publisher profile](https://clawhub.ai/user/unisound-llm) <br>
- [Configured model API endpoint](https://maas-api.hivoice.cn/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON by default, plain text when text-only output is requested, and NDJSON for batch output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include task metadata, input metadata, model name, question text, and generated answer; dry-run mode returns parsed input without calling the model.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
