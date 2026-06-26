## Description: <br>
A metacognitive planning skill that helps an agent analyze tasks, review available skills, retrieve relevant memory, plan execution paths, and assess risks before acting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rfdiosuao](https://clawhub.ai/user/rfdiosuao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and users invoke this skill before complex, unfamiliar, or important tasks to structure task analysis, skill selection, memory lookup, step planning, risk assessment, and execution readiness. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad natural-language triggers may cause the planning flow to run when the user did not intend it. <br>
Mitigation: Invoke the skill deliberately with /thinking for complex tasks and cancel the planning mode when it is not needed. <br>
Risk: Plans may draw on memory, session history, and installed-skill context that should be reviewed before follow-on actions. <br>
Mitigation: Review the generated plan and risk assessment before allowing external actions or irreversible operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rfdiosuao/thinking-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown planning notes and execution guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill can consult agent memory, session history, and installed-skill context when planning.] <br>

## Skill Version(s): <br>
1.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
