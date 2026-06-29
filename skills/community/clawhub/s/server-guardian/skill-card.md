## Description: <br>
Server Guardian helps agents monitor OpenClaw server health, diagnose CPU, memory, disk, process, network, log, and crash signals, and propose or run recovery actions such as Gateway restarts, cache cleanup, log maintenance, OOM checks, and configuration guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[efgyuhhgy](https://clawhub.ai/user/efgyuhhgy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect OpenClaw server health, triage Gateway or bot outages, and apply recovery actions when resource, process, network, log, or OOM symptoms appear. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad operational control over an OpenClaw server, including automatic Gateway restarts and recovery flows. <br>
Mitigation: Run health checks first, review proposed recovery actions, and avoid automatic full recovery on production systems until the scripts are reviewed for the deployment. <br>
Risk: Recovery behavior includes log deletion and process termination paths that may remove diagnostic evidence or affect non-target processes. <br>
Mitigation: Require explicit approval for log deletion and non-OpenClaw process termination, or disable those actions before production use. <br>


## Reference(s): <br>
- [Server Guardian ClawHub Skill Page](https://clawhub.ai/efgyuhhgy/skills/server-guardian) <br>
- [Alarm Threshold Reference](references/thresholds.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Health-check usage is documented as limited to 40 invocations per 60 seconds.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
