## Description: <br>
Runs a Trello-backed closed-loop delivery workflow for OpenClaw multi-agent execution, keeping cards moving through workflow lists with manager-only intake, local-first routing, reviewer-gated completion, and retry cycles until accepted or blocked. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeremiahdingal](https://clawhub.ai/user/jeremiahdingal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and delivery managers use this skill to coordinate OpenClaw work through Trello, creating or locating objective cards, moving them through scoped workflow states, routing execution, and recording reviewer decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, update, comment on, and move Trello cards using the user's Trello account. <br>
Mitigation: Use the least-privileged Trello token available, avoid sharing credentials in chat or logs, and require a clear summary and confirmation before Trello changes are made. <br>
Risk: Workflow state changes can mark work accepted, rejected, done, or blocked. <br>
Mitigation: Keep explicit reviewer ACCEPT as the gate for Done and review card descriptions and comments before relying on the recorded status. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jeremiahdingal/trello-orchestrator-runner) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown status summary with Trello card identifiers, URL, current list, routing mode, reviewer verdict, and next action.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TRELLO_API_KEY, TRELLO_TOKEN, and a workspace trello-workflow-map.json before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
