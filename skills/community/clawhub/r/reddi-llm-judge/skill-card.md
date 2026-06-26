## Description: <br>
Build a cost-efficient LLM evaluation ensemble with sampling, tiebreakers, and deterministic validators. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nissan](https://clawhub.ai/user/nissan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to design LLM-as-judge evaluation workflows for comparing generative AI outputs across models, promotion gates, and shadow-testing pipelines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Evaluation workflows may send prompts, source text, candidate outputs, or ground truth to external judge providers. <br>
Mitigation: Use scoped API keys with spending limits, confirm provider data-handling settings, and avoid sending sensitive data unless the deployment has approved controls. <br>
Risk: Stored judge inputs, outputs, or rationales can expose sensitive evaluation data if logs are retained broadly. <br>
Mitigation: Redact sensitive logs, restrict access, and apply retention limits before using the workflow with confidential data. <br>
Risk: Judge model behavior can drift across provider model versions and affect evaluation consistency. <br>
Mitigation: Pin judge model versions, calibrate against manually reviewed samples, and use full judge coverage for promotion gates. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nissan/reddi-llm-judge) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown guidance with Python examples and evaluation configuration details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes external judge-provider considerations and local Ollama workflow guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
