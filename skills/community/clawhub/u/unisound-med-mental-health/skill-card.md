## Description: <br>
Provides mental-health support responses and mental-health knowledge Q&A through task-specific prompts for counseling and education. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unisound-llm](https://clawhub.ai/user/unisound-llm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and integrators use this command-line skill to send mental-health support or mental-health knowledge questions to a configured medical LLM and receive structured answers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mental-health prompts and saved outputs may contain sensitive personal or patient data. <br>
Mitigation: De-identify real patient data before use, avoid secrets in prompts, and protect terminal logs and --output files. <br>
Risk: Questions are sent to the configured remote medical LLM endpoint. <br>
Mitigation: Use this skill only when that data flow is acceptable for the deployment environment and keep the required app key protected. <br>
Risk: Model-assisted mental-health responses can be incomplete or inappropriate for crisis or clinical decision needs. <br>
Mitigation: Review outputs before relying on them and route crisis, diagnosis, or treatment decisions to qualified professionals. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/unisound-llm/unisound-med-mental-health) <br>
- [Configured medical LLM API endpoint](https://maas-api.hivoice.cn/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [Structured JSON by default, answer text with --text-only, or NDJSON for batch output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write complete results to --output; --dry-run emits parsed input without calling the model.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
