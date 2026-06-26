## Description: <br>
A Chinese-language orchestration helper that decomposes complex tasks into 3-6 independent, executable sub-skill structures and returns structured retry or error responses when inputs are incomplete or unsuitable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smallkeyboy](https://clawhub.ai/user/smallkeyboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and orchestrator agents use this skill to turn a structured task brief, prior analysis, and critic insight into independent sub-skill definitions with names, descriptions, input examples, and output examples. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated sub-skill plans may be used by downstream agents before a human or orchestrator checks whether the structure is appropriate. <br>
Mitigation: Review the proposed sub-skill plan before orchestration or execution. <br>
Risk: The skill designs structures but does not enforce safe execution of the generated sub-skills. <br>
Mitigation: Apply normal safety, security, and policy checks to any downstream skill that is created or run from the plan. <br>


## Reference(s): <br>
- [Decomposition Patterns](references/decomposition-patterns.md) <br>
- [Independence Check](references/independence-check.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Guidance] <br>
**Output Format:** [JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns success, need_retry, or error objects with proposed sub-skill structures and reasoning.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
