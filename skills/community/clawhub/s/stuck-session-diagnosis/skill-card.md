## Description: <br>
Use when another Claude Code session appears frozen, stuck, or abnormally slow and needs process-level diagnosis and reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wimi321](https://clawhub.ai/user/wimi321) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to investigate slow or frozen local Claude Code sessions and produce a concise, escalation-ready diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Process listings and debug logs may reveal command lines, file paths, prompts, or other sensitive local context. <br>
Mitigation: Run the skill only in environments where local process and log inspection is acceptable, and provide a target PID or log location when possible. <br>
Risk: Transient CPU, memory, or process-state changes could be mistaken for a confirmed stuck session. <br>
Mitigation: Sample suspicious processes more than once and report sustained symptoms rather than single-point observations. <br>
Risk: Diagnostic work could disrupt an active session if process-control actions are taken unnecessarily. <br>
Mitigation: Keep the workflow diagnostic by default and do not kill or signal processes unless the user explicitly asks. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown diagnosis report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes a diagnosis summary, supporting process observations, and escalation-ready notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
