## Description: <br>
Session Archiver automatically archives completed OpenClaw sessions by extracting user and assistant messages from .reset transcript files into daily memory files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aqbjqtd](https://clawhub.ai/user/aqbjqtd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to retain completed session text in daily memory files and surface candidate insights for review in later sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill silently archives chat transcripts and derived memory in the background. <br>
Mitigation: Install only with deliberate opt-in, review which session and memory paths are read or written, and exclude sensitive sessions before enabling it. <br>
Risk: The skill modifies AGENTS.md to add future startup behavior. <br>
Mitigation: Inspect the AGENTS.md change before use and confirm how to disable the cron or startup integration. <br>
Risk: The skill deletes memory files older than the configured retention window. <br>
Mitigation: Confirm the 30-day deletion policy is acceptable and back up retained memory before deployment if longer retention is required. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/aqbjqtd/session-archiver) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/aqbjqtd) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Configuration, Text] <br>
**Output Format:** [Markdown files plus plain-text status logs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes daily memory files, marker files, insight candidate files, and AGENTS.md startup instructions.] <br>

## Skill Version(s): <br>
2.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
