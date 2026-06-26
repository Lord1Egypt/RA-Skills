## Description: <br>
Stop your AI from making the same mistake twice with pre-action gates that block repeat hallucinations, retry loops, and known-bad tool calls before they reach the model. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[igorganapolsky](https://clawhub.ai/user/igorganapolsky) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use ThumbGate to create persistent tool-call gates that block repeated agent mistakes, destructive commands, incorrect paths, and other known-bad actions before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent tool-call gates can block intended agent actions if configured too broadly or installed in projects where this behavior is not expected. <br>
Mitigation: Install ThumbGate only in projects where persistent agent tool-call blocking is desired, and review generated .thumbgate/ files and hooks after initialization. <br>
Risk: Feedback, lessons, shared databases, or exports may include secrets or private business details if users enter sensitive information. <br>
Mitigation: Avoid putting secrets or private business details into feedback, lessons, shared databases, or exports. <br>
Risk: The skill depends on the external thumbgate CLI and generated project hooks to enforce behavior. <br>
Mitigation: Review the thumbgate npm package or repository before use and verify generated hook behavior in a controlled project. <br>


## Reference(s): <br>
- [ClawHub ThumbGate page](https://clawhub.ai/igorganapolsky/thumbgate) <br>
- [ThumbGate homepage](https://thumbgate-production.up.railway.app) <br>
- [ThumbGate dashboard](https://thumbgate-production.up.railway.app/dashboard) <br>
- [Skill-provided ThumbGate repository link](https://github.com/IgorGanapolsky/ThumbGate) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces guidance for installing and using the thumbgate CLI, configuring agent PreToolUse hooks, managing gates and feedback, and opening the dashboard.] <br>

## Skill Version(s): <br>
1.5.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
