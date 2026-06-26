## Description: <br>
Reward and motivation system for AI agents. Dopamine-like wanting, not just doing. Part of the AI Brain series. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ImpKind](https://clawhub.ai/user/ImpKind) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to add a persistent motivation and reward-state layer to OpenClaw-style agents, including drive tracking, reward logging, anticipation, and session state summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent motivation and memory files may contain sensitive or unwanted conversation-derived content. <br>
Mitigation: Install only when persistent agent-wide motivation state is desired, and review or delete ~/.openclaw/workspace/memory/*, ~/.openclaw/workspace/VTA_STATE.md, and ~/.openclaw/workspace/brain-dashboard.html when needed. <br>
Risk: Auto-injected motivation state can shape future agent behavior. <br>
Mitigation: Inspect the generated VTA_STATE.md before relying on it in sessions, and remove or edit it if the behavior influence is unwanted. <br>
Risk: The optional --with-cron install path can run recurring transcript and reward processing. <br>
Mitigation: Avoid --with-cron unless recurring processing is acceptable, and review any created OpenClaw cron jobs after installation. <br>


## Reference(s): <br>
- [Vta Memory on ClawHub](https://clawhub.ai/ImpKind/vta-memory) <br>
- [README.md](README.md) <br>
- [VTA: Encode Reward Signals](prompts/encode-rewards.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance, shell command output, JSON/JSONL state files, and an HTML dashboard] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes persistent motivation state under ~/.openclaw/workspace and can optionally register recurring OpenClaw cron jobs.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release and OpenClaw metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
