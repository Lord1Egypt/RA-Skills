## Description: <br>
Automated transcript trimming, LLM memory extraction, and session hygiene for OpenClaw gateways. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[halfdeadcat](https://clawhub.ai/user/halfdeadcat) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators who run OpenClaw gateways use Session Janitor to trim oversized transcripts, archive and prune stale session data, and optionally extract structured memories from trimmed content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Background cleanup can mutate or archive OpenClaw session transcripts. <br>
Mitigation: Back up session directories and review generated config.json before installing cron jobs or watcher services. <br>
Risk: Generated configuration may contain gateway tokens and session paths. <br>
Mitigation: Protect config.json as sensitive local data and avoid sharing it in logs, tickets, or repositories. <br>
Risk: LLM extraction, mem CLI storage, Slack alerts, watchdog restart, and scene file paths may process or publish transcript-derived information. <br>
Mitigation: Disable these options unless the operator explicitly wants transcript-derived data processed, stored, or sent outside the session files. <br>


## Reference(s): <br>
- [Session Janitor on ClawHub](https://clawhub.ai/halfdeadcat/session-janitor) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [Architecture and Trimming Deep Dive](artifact/ARCHITECTURE.md) <br>
- [Example Configuration](artifact/config.example.json) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown instructions with shell commands and JSON configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and jq; optional mem CLI, fswatch, or inotify-tools enable additional runtime behavior.] <br>

## Skill Version(s): <br>
1.6.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
