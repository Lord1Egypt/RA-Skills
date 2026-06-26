## Description: <br>
Smart Router Coding classifies coding prompts and recommends a cost-aware model tier for simple, standard, or architecture-heavy work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[certainlogicai](https://clawhub.ai/user/certainlogicai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to classify coding prompts and choose a cost-aware model tier before making an LLM call. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Model names, costs, and latency estimates can become stale. <br>
Mitigation: Treat routing results as advisory and review or update model metadata before relying on cost or latency claims. <br>
Risk: Keyword-based routing can misclassify unusual, ambiguous, or high-stakes coding prompts. <br>
Mitigation: Review recommendations for complex or security-sensitive work and override the suggested tier when deeper analysis is warranted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/certainlogicai/smart-router-coding) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [JSON recommendation with model tier, model name, estimated cost, latency, and reasoning.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Advisory local routing recommendation; no files, credentials, or network access are required.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
