## Description: <br>
Monitors agent token usage and model cost from OpenClaw session logs or Hermes logs and state.db, compares current spend with prior snapshots or thresholds, and can generate or send alert reports when cost growth exceeds configured limits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to track OpenClaw or Hermes token spend, identify cost spikes, and configure threshold-based cost alerts for agent runtimes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local OpenClaw or Hermes usage logs and Hermes state.db to summarize token spend. <br>
Mitigation: Install and run it only in environments where that local usage data may be read for cost reporting. <br>
Risk: The skill writes local cost reports and snapshot state on disk. <br>
Mitigation: Review or configure the state and reports directories when local persistence matters. <br>
Risk: The skill can send alert reports to an OpenClaw channel or target when configured. <br>
Mitigation: Use --send-openclaw only with an intended channel and target, and use dry-run behavior before enabling delivery where appropriate. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/harrylabsj/token-cost-guard) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Chinese Markdown cost reports with optional JSON summaries and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local report and snapshot state files; sends OpenClaw alerts only when explicitly configured.] <br>

## Skill Version(s): <br>
0.2.4 (source: evidence.release.version, artifact skill.json, clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
