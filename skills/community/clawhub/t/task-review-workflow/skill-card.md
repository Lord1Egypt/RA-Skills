## Description: <br>
Standard PR review and merge workflow for task-driven development, used when reviewing a programmer agent PR linked to a task, deciding merge versus change request, handling post-merge actions, and sending a clear outcome handoff. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anikgnr](https://clawhub.ai/user/anikgnr) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to guide agent-assisted pull request review, local validation, merge decisions, Trello follow-up, branch cleanup, and final handoff for task-linked work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can lead an agent to participate in pull request review, merge decisions, Trello updates, and branch deletion. <br>
Mitigation: Limit GitHub and Trello permissions to the intended repositories and projects, use protected branches, and require human approval for merges when appropriate. <br>
Risk: Local PR validation may expose sensitive workspace data or environment variables to test, lint, or build commands. <br>
Mitigation: Run validation in an isolated workspace without sensitive environment variables. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown guidance with review outcomes and optional local validation commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces review decisions such as merged, CR sent, or waiting for fixes.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
