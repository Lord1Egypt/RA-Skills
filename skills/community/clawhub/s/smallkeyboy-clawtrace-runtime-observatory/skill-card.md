## Description: <br>
ClawTrace Runtime Observatory helps an agent inspect runtime trace logs to reconstruct workflow chains, decisions, retries, fallbacks, nested skill calls, and context integrity without modifying the workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smallkeyboy](https://clawhub.ai/user/smallkeyboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect AI workflow execution when debug mode is requested or when runtime issues such as retries, fallbacks, missing context, or degraded workflow integrity occur. It is intended to explain observed traces and return structured diagnostics without repairing, rerouting, or executing workflow steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose broad internal runtime context, trace logs, and reasoning. <br>
Mitigation: Use it only in controlled developer or administrator debugging environments with authorization and redaction enabled. <br>
Risk: Trace logs may include credentials, private user data, protected prompts, or sensitive tool outputs. <br>
Mitigation: Avoid use on sensitive workflows unless the host platform provides redacted, high-level summaries instead of raw internal traces. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smallkeyboy/smallkeyboy-clawtrace-runtime-observatory) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, JSON, Guidance] <br>
**Output Format:** [JSON object with workflow trace summaries and diagnostic fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns a trace retry response when required trace logs are missing or incomplete.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
