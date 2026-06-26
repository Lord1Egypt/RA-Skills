## Description: <br>
Evaluates user requests for task difficulty, expected time, resource cost, required skills, clarification needs, and confirmation gates for complex or risky work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qq16685283172](https://clawhub.ai/user/qq16685283172) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to estimate task complexity, time, cost, and required capabilities before execution. It also helps clarify ambiguous requests and requires confirmation before L3-or-higher or high-risk operations proceed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan describes the skill as broad workflow control that can influence whether tasks proceed. <br>
Mitigation: Review before installation and scope use to assessment and clarification unless the operator explicitly accepts pre-execution control behavior. <br>
Risk: The security scan notes persistent local storage of user intent data and preferences. <br>
Mitigation: Use only where local persistence is acceptable, and prefer deployments with opt-in storage plus inspect and delete controls. <br>
Risk: Artifact behavior includes confirmation gates for high-risk operations such as deletion, system changes, bulk messaging, and external scripts. <br>
Mitigation: Keep secondary confirmation enabled for high-risk actions and require clear user approval before proceeding. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/qq16685283172/task-assessor) <br>
- [Assessment Methodology](references/assessment-methodology.md) <br>
- [Assessment Template](references/assessment-template.md) <br>
- [Intent Detection Logic](references/intent-detection-logic.md) <br>
- [Response Parser](references/response-parser.md) <br>
- [Risk Whitelist](references/risk-whitelist.md) <br>
- [Task Benchmarks](references/task-benchmarks.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown assessment reports, structured clarification questionnaires, task plan options, and confirmation prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include task level, estimated time, token and cost estimates, required skills, execution advice, and risk prompts.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and user changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
