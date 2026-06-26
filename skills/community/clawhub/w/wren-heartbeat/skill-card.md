## Description: <br>
Unified heartbeat system for OpenClaw agents that runs parallel health checks, data collectors, and state monitors in one command and returns a single actionable summary optimized for LLM consumption. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wrentheai](https://clawhub.ai/user/wrentheai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to configure recurring OpenClaw heartbeat checks, collect status from external sources, monitor workspace or system state, and produce a concise action-needed or all-clear result. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configured heartbeat entries can run arbitrary shell commands on a recurring schedule. <br>
Mitigation: Install only after reviewing every heartbeat.yaml command, keep collectors read-only, avoid inline secrets, use least-privilege API keys, and restrict destinations. <br>
Risk: Heartbeat results can write files into the workspace and may prompt later agent actions. <br>
Mitigation: Use controlled output and cache paths, review summaries before acting, and require human confirmation before any action that posts content, deletes data, changes accounts, spends money, or modifies important files. <br>


## Reference(s): <br>
- [Config Reference](references/config.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/wrentheai/wren-heartbeat) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown or JSON summaries with stdout status text and process exit codes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a summary file by default and returns exit code 0 for all clear, 1 for errors, or 2 for action needed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
