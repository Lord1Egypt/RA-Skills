## Description: <br>
Routes incoming tasks into six thinking scenarios, selects the highest-priority reasoning tools, and verifies whether the resulting conclusion is explainable, example-backed, and free of obvious gaps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wukaifeng704-cell](https://clawhub.ai/user/wukaifeng704-cell) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill as a task-routing layer for decision-making, learning, writing, prioritization, crisis response, and brainstorming. It helps an agent choose structured thinking methods such as first principles, inversion, SMART goals, quadrant prioritization, and SCQA before presenting conclusions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes under-scoped handoffs to external workflow or memory systems. <br>
Mitigation: Only enable Memory_Bus or layout/render integrations after confirming what data is sent, where it is stored, and how it can be inspected or deleted. <br>
Risk: The crisis-mode workflow includes an approval-bypass instruction. <br>
Mitigation: Keep confirmations in place for external actions, publishing, file or account changes, and irreversible steps. <br>
Risk: As a thinking-framework skill, its output can influence decisions without independently proving correctness. <br>
Mitigation: Use it as a reasoning aid and review conclusions before acting on them. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/wukaifeng704-cell/scenario-first-thinking) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/wukaifeng704-cell) <br>
- [Six Scenario Routing](artifact/references/six-scenario-routing.md) <br>
- [SCQA Writing Template](artifact/references/scqa-template.md) <br>
- [Eight Tool Handbook](artifact/references/tool-handbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or plain text reasoning guidance with prioritized steps and checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce task classifications, tool sequences, reasoning checks, SCQA outlines, prioritized task lists, and action recommendations.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
