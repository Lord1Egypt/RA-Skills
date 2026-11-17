## Description:

Think-Plan helps agents turn unclear or complex requests into clarified requirements, compared solution options, and executable plans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caoyachao](https://clawhub.ai/user/caoyachao)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and teams use Think-Plan to interrogate vague goals, compare two or three implementation approaches, and save confirmed execution plans before work begins.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated plans or critiques may be incorrect or misleading for broad, ambiguous, or high-stakes tasks.

Mitigation: Review generated plans before execution and require clarified scope, success criteria, constraints, and risks before committing to an approach.

Risk: The skill can save finalized plans into the workspace.

Mitigation: Confirm the selected plan and destination before allowing plan files to be written.

Risk: Complex workflows may involve subagent coordination after user confirmation.

Mitigation: Review the proposed agent responsibilities and execution boundaries before starting multi-agent work.

## Reference(s):

- [Question Framework](references/question-framework.md)
- [Task Complexity Patterns](references/patterns.md)
- [Workflow](references/workflow.md)
- [ClawHub Skill Page](https://clawhub.ai/caoyachao/skills/think-plan)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands]

**Output Format:** [Markdown conversation responses and saved Markdown plan files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save finalized plans under workspace/plans after user confirmation and may coordinate subagents for complex execution.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
