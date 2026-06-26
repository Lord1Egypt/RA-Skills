## Description: <br>
TESP enforces the Task Execution Signal Protocol for non-instant work so execution stays visible, staged, versioned, and auditable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wewehg](https://clawhub.ai/user/wewehg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agent coordinators use TESP to keep long or multi-agent work visible through fast acknowledgement, staged progress updates, task boards, blocker escalation, and handoffs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The protocol includes hardcoded local task-board paths that may not match the user's workspace. <br>
Mitigation: Replace those paths with approved workspace locations before using the queue, archive, or handoff conventions. <br>
Risk: Queue, archive, and handoff notes can expose sensitive task or client details if used without filtering. <br>
Mitigation: Avoid placing secrets, credentials, or sensitive client information in progress notes and task-board files. <br>
Risk: The skill names preferred model providers for governance tasks that may not match organizational policy. <br>
Mitigation: Follow the organization's approved model-provider policy instead of treating GLM or MiniMax as mandatory. <br>
Risk: Applying the protocol to instant work can add unnecessary process overhead. <br>
Mitigation: Use TESP for non-instant, multi-step, asynchronous, or cross-agent work where status visibility matters. <br>


## Reference(s): <br>
- [TESP Protocol Reference](references/protocol.md) <br>
- [TESP Templates](references/templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown and plain-text progress updates, task-board tables, handoff notes, and audit checklists.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses visible protocol versions, numeric progress stages, active/archive task-board separation, and concise blocker escalation.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
