## Description: <br>
Builds command-ready sessions_spawn payload JSON from explicit CLI profile arguments without executing spawn. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nextaltair](https://clawhub.ai/user/nextaltair) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to generate reviewable sessions_spawn JSON from explicit CLI arguments while keeping actual subagent execution separate. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated payloads are appended to a local build log, so task text or parameters may persist sensitive details. <br>
Mitigation: Avoid putting secrets or sensitive internal details in task text or spawn parameters unless local logging is acceptable. <br>
Risk: The generated sessions_spawn payload may contain incorrect or unintended subagent parameters if CLI arguments are wrong. <br>
Mitigation: Review the generated payload before using it to spawn a subagent. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nextaltair/subagent-spawn-command-builder) <br>
- [README.md](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON payload with command-line usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Does not execute sessions_spawn; generated payloads may be logged locally by the builder script.] <br>

## Skill Version(s): <br>
0.1.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
