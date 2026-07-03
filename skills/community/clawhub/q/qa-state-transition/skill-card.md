## Description: <br>
Helps QA practitioners design state-transition tests that cover valid, invalid, boundary, and concurrent transitions for multi-state business objects or system lifecycles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kokxi](https://clawhub.ai/user/kokxi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, QA engineers, and testers use this skill to convert scenario trees, requirement decompositions, and optional risk assessments into state diagrams, transition lists, and test scenarios for lifecycle-heavy systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ambiguous requests involving the word state may not be about a business object or system lifecycle. <br>
Mitigation: Confirm the target object, lifecycle states, triggers, and expected transition rules before applying the workflow. <br>
Risk: Incomplete requirements or scenario-tree inputs can lead to missing guard conditions, invalid transitions, or concurrency cases. <br>
Mitigation: Review the generated state diagram and transition lists against product requirements, especially illegal transitions, boundary conditions, and concurrent actions. <br>


## Reference(s): <br>
- [ClawHub skill release: qa-state-transition](https://clawhub.ai/kokxi/skills/qa-state-transition) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown guidance with structured tables and test-case templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces state diagrams, valid and invalid transition lists, and state-transition test scenarios; no code execution.] <br>

## Skill Version(s): <br>
1.5.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
