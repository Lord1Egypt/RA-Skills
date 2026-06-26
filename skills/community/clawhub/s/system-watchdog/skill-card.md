## Description: <br>
System resource monitoring. Detects actionable anomalies (memory pressure, runaway processes, disk pressure) and reports only when something needs attention. Optimized for few, high-signal alerts. Works on both Linux and macOS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BrennerSpear](https://clawhub.ai/user/BrennerSpear) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to run a local Linux or macOS resource check and receive a concise report only when memory pressure, runaway processes, sustained CPU burn, or disk pressure need attention. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The persisted state can include full process command lines, which may expose secrets, tokens, or private paths. <br>
Mitigation: Keep the state file in a protected location, avoid putting secrets in process command-line arguments, and use SYSTEM_WATCHDOG_STATE to place state in an access-controlled path when needed. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [JSON stdout from the watchdog script and concise Markdown or text reporting when anomalies are present] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists lightweight local state between runs to compare swap and process memory growth.] <br>

## Skill Version(s): <br>
2.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
