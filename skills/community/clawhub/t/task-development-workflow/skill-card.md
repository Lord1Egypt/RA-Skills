## Description: <br>
TDD-first development workflow with structured planning, task tracking, and PR-based code review. Use when building software projects that require clarification phases, planning approval gates, Trello task management, test-driven development, Git branching policies, and PR feedback loops with reviewers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anikgnr](https://clawhub.ai/user/anikgnr) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to guide agents through software tasks that require clarification, planning approval, Trello-style tracking, TDD, branch discipline, pull requests, and review feedback loops. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may lead an agent to update task boards, create branches or repositories, push commits, open pull requests, and notify reviewers. <br>
Mitigation: Before use, specify the exact repository, task board, branch rules, reviewer, and accounts the agent may operate in. <br>
Risk: Strict planning, approval, TDD, and merge gates may block progress if the user has not authorized exceptions. <br>
Mitigation: State any allowed exceptions explicitly, especially for skipping tests or proceeding before approval. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/anikgnr/task-development-workflow) <br>
- [Workflow Details](references/workflow-details.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with task plans, PR descriptions, code changes, tests, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include task-board updates, branch and PR actions, reviewer notifications, and repository bootstrap steps when the agent has appropriate access.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
