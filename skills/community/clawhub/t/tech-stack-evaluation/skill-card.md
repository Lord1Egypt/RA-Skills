## Description: <br>
Evaluates whether a project's current tech stack is appropriate for its goals and recommends alternatives when maintainability, performance, or feature expansion is blocked. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adelvillar1](https://clawhub.ai/user/adelvillar1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering leads use this skill to assess whether an existing project stack matches project goals, diagnose maintainability, performance, feature, team, and deployment blockers, and compare refactor, modernization, or rewrite options with effort, payoff, and risk. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Suggested commands inspect local project filenames and source metrics, which can reveal project structure in the agent conversation. <br>
Mitigation: Run the skill only in the repository intended for assessment and review command output before sharing it outside the project team. <br>
Risk: Stack recommendations can be misleading if based on incomplete evidence or if team and deployment constraints are skipped. <br>
Mitigation: Use the skill's checklist to tie each recommendation to observed maintainability, performance, feature, team, and deployment evidence before acting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/adelvillar1/tech-stack-evaluation) <br>
- [Publisher profile](https://clawhub.ai/user/adelvillar1) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown with assessment tables, recommendation options, and inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only recommendations grounded in local codebase assessment evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
