## Description: <br>
Generates VeADK-Go agent code from user requirements and converts Enio agent code to VeADK-Go agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[helloldm](https://clawhub.ai/user/helloldm) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to create VeADK-Go agent implementations from functional requirements or to migrate existing Enio agent code into VeADK-Go patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated agent code may be incorrect, unsafe to run as-is, or overwrite existing work if the output path is reused. <br>
Mitigation: Review generated files before execution and confirm the target output path does not overwrite important work. <br>
Risk: Generated examples may include model API keys, web search, callbacks, or cloud knowledge-base configuration that changes runtime behavior or exposes sensitive data if copied without review. <br>
Mitigation: Avoid hardcoding secrets and deliberately choose whether to enable web search, callbacks, model API keys, or cloud knowledge-base creation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/helloldm/veadk-go-skills) <br>
- [Agent definition methods](common/agent.md) <br>
- [Tool definition methods](common/tools.md) <br>
- [Callback definition methods](common/callback.md) <br>
- [Knowledge base usage](common/knowledgebase.md) <br>
- [Enio to VeADK-Go conversion rules](converter/enio_rule.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Go code and file output instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Expected generated code artifact is agent_name/agent.py.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
