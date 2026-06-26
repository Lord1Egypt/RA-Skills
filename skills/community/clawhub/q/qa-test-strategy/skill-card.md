## Description: <br>
QA lead skill for test strategy, coverage planning, risk-based validation design, and cross-role quality governance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aiweline](https://clawhub.ai/user/aiweline) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, QA leads, and delivery teams use this skill to design layered validation plans, map change risks to appropriate unit, HTTP, E2E, WLS, and documentation checks, and define acceptance evidence before release. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may ask an agent to read local project guidance files while preparing a QA strategy. <br>
Mitigation: Run it only in the intended project workspace and review the resulting validation plan before sharing project-specific details. <br>
Risk: Runtime-sensitive WLS validation can affect shared development services if run against a default or shared instance. <br>
Mitigation: Use the skill's stated isolation rule: start a dedicated WLS test instance with a unique name and stop it after testing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aiweline/qa-test-strategy) <br>
- [Publisher profile](https://clawhub.ai/user/aiweline) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, shell commands] <br>
**Output Format:** [Markdown guidance with validation plans, risk-to-test mappings, evidence requirements, and gate definitions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include concrete runtime validation steps when WLS-sensitive changes require isolated testing.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
