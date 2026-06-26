## Description: <br>
Think-Plan guides agents through Chinese-language requirement discovery, critical planning, option comparison, and execution planning for complex tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[caoyachao](https://clawhub.ai/user/caoyachao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn ambiguous goals into clarified requirements, compare two or three executable plans, and proceed only after user confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved plans can retain sensitive project or business details in the workspace. <br>
Mitigation: Avoid including sensitive details when retention is unacceptable, or review and remove saved plan files after use. <br>
Risk: Execution coordination can expand the scope of work after a plan is selected. <br>
Mitigation: Confirm the selected plan, scope, and user approval before execution, and pause for user direction on major changes. <br>


## Reference(s): <br>
- [Question Framework](references/question-framework.md) <br>
- [Task Complexity Patterns](references/patterns.md) <br>
- [Think-Plan Workflow](references/workflow.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/caoyachao/think-plan) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, files] <br>
**Output Format:** [Markdown plan options, conversational guidance, and saved Markdown execution plans] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Confirmed plans may be saved under workspace/plans before optional execution coordination.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
