## Description:

Reward and motivation system for AI agents. Dopamine-like wanting, not just doing. Part of the AI Brain series.

This skill is ready for commercial/non-commercial use.

## Publisher:

[impkind](https://clawhub.ai/user/impkind)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to add persistent reward, drive, seeking, and anticipation state to OpenClaw agents, including scripts for logging rewards, reading drive state, processing reward signals, and generating a local dashboard.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent motivation state can influence future OpenClaw sessions through generated auto-loaded context.

Mitigation: Install only when persistent motivation behavior is intended, review VTA_STATE.md, and delete or disable generated state if it should not be retained or auto-loaded.

Risk: Optional cron setup can run recurring agent jobs that process local transcripts and update memory files.

Mitigation: Avoid --with-cron unless recurring transcript processing is acceptable; prefer manual runs for tighter control.

Risk: Generated files can contain conversation-derived state and local memory summaries.

Mitigation: Treat VTA_STATE.md, reward-signals.jsonl, reward-log.jsonl, brain-events.jsonl, and brain-dashboard.html as sensitive local files and remove them when no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/impkind/skills/vta-memory)
- [README](artifact/README.md)
- [Encode reward signals prompt](artifact/prompts/encode-rewards.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown instructions, shell commands, JSON/JSONL state files, and an HTML dashboard]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Bash plus jq, awk, and bc on Linux or macOS; optional cron setup creates recurring OpenClaw jobs.]

## Skill Version(s):

1.2.0 (source: OpenClaw metadata and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
