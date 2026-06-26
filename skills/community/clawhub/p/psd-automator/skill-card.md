## Description: <br>
Automate PSD text replacement on Mac and Windows with Photoshop, dry-run safety, style-lock checks, rollback, and local PSD index cache. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dhrxy](https://clawhub.ai/user/dhrxy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Designers, production artists, and workflow operators use this skill to run structured PSD edit tasks through local agents. It helps resolve PSD or PSB files by path or index hint, replace or place content in named layers, preserve style constraints, and export PNG or ZIP outputs for chat workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can index local PSD and PSB files, which may expose a broad inventory of local design assets. <br>
Mitigation: Use explicit narrow index roots, review or delete ~/.openclaw/psd-index.json when needed, and avoid indexing unrelated directories. <br>
Risk: Chat-driven tasks can modify PSD assets or export derived PNG and ZIP files. <br>
Mitigation: Run dry-run first, keep backups enabled, require human approval before real writes, and restrict which users or subagents can request edits. <br>
Risk: Ambiguous file hints could target the wrong design file if not resolved carefully. <br>
Mitigation: Prefer exact paths for write operations and require confirmation when multiple indexed candidates match a file hint. <br>
Risk: Photoshop automation runs local OS-specific scripts through AppleScript or PowerShell. <br>
Mitigation: Run only on intended macOS or Windows design agents with Photoshop installed and keep agent routing allowlists narrow. <br>


## Reference(s): <br>
- [Task Schema](artifact/references/task-schema.json) <br>
- [PSD Automator Error Codes](artifact/references/error-codes.md) <br>
- [OpenClaw Subagent Routing](artifact/references/openclaw-subagent-routing.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/dhrxy/psd-automator) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown or plain-text agent responses with JSON task payloads, shell commands, normalized execution results, and absolute file markers for generated PSD, PNG, or ZIP outputs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports dry-run previews, backup paths, audit log paths, standardized error codes, and optional DingTalk image or file markers.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
