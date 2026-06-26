## Description: <br>
Responsive Agent defines a two-layer OpenClaw pattern that keeps the main agent responsive by dispatching long, remote, state-changing, or uncertain work to subagents that use exec, yieldMs, timeouts, and result reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guytogay](https://clawhub.ai/user/guytogay) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to keep OpenClaw sessions responsive while long-running, remote, state-changing, or uncertain tasks execute in managed subagents. It provides decision rules for spawning, runtime selection, result delivery, error handling, cancellation, and memory updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Background delegation can reduce user visibility into long-running subagents. <br>
Mitigation: Review the skill before installing, monitor active background sessions, and use it only for user-approved tasks. <br>
Risk: Credentialed, destructive, or account-changing work may be delegated to subagents. <br>
Mitigation: Require clear confirmation before allowing subagents to perform credentialed, destructive, or account-changing operations. <br>
Risk: Cancelled or stalled subagents may continue running if lifecycle controls are not followed. <br>
Mitigation: Use the documented cancellation protocol, status checks for long-running work, runtime limits, and explicit completion or failure reporting. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions, Code] <br>
**Output Format:** [Markdown with decision tables, JSON-like tool-call examples, shell commands, and file-format examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes subagent labels, runtime/yieldMs/timeout recommendations, task log paths, and cancellation/error-reporting formats.] <br>

## Skill Version(s): <br>
1.8.1 (source: server release evidence; artifact frontmatter says 1.8.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
