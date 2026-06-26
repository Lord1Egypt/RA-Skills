## Description: <br>
Reddi Agent Evaluation helps test and benchmark LLM agents with behavioral testing, capability assessment, reliability metrics, regression testing, and production monitoring guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nissan](https://clawhub.ai/user/nissan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and quality engineers use this skill to design agent evaluations, including behavioral contracts, adversarial tests, statistical reliability checks, and regression test plans for LLM agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Evaluating real agents may expose confidential customer data, private prompts, or sensitive outputs to a configured LLM provider. <br>
Mitigation: Use only approved LLM providers for the relevant data class and avoid including sensitive data in evaluation inputs unless approval is explicit. <br>
Risk: Single-run tests can give misleading results for non-deterministic LLM agents. <br>
Mitigation: Run tests multiple times and use statistical measures such as distributions or confidence intervals before drawing reliability conclusions. <br>
Risk: Test data can leak into training data, prompts, or evaluation setup and inflate apparent performance. <br>
Mitigation: Separate evaluation data from training and prompt construction, and review evaluation workflows for data leakage before use. <br>


## Reference(s): <br>
- [ClawHub skill release page](https://clawhub.ai/nissan/reddi-agent-evaluation) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown prose, checklists, rubrics, and test plans] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference configured LLM API evaluation scoring when an agent evaluation workflow requires it.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
