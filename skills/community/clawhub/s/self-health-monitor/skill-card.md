## Description: <br>
Monitors an agent's own PCEC execution, memory usage, sub-agent activity, response quality, and skill health. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xaiohuangningde](https://clawhub.ai/user/xaiohuangningde) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to have an agent periodically summarize its own operational health, including scheduled PCEC activity, memory state, sub-agent activity, tool reliability, response latency, error rate, and loadable skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to run proactively in the background. <br>
Mitigation: Enable scheduling only with explicit operator approval and set alert suppression or rate limits before deployment. <br>
Risk: The skill asks the agent to inspect internal memory, state, sub-agent activity, and response quality. <br>
Mitigation: Restrict checks to read-only access, named memory paths, or metadata-only inspection unless broader access is explicitly approved. <br>
Risk: The artifact describes immediate self-repair when problems are found. <br>
Mitigation: Require manual approval before the agent changes memory, skills, sub-agents, configuration, or other persistent state. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xaiohuangningde/self-health-monitor) <br>
- [Artifact skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown status report and abnormal-state alerts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No user input is required; the artifact describes a scheduled self-check cadence and threshold-based alerts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
