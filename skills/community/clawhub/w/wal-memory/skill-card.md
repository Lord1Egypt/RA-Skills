## Description: <br>
WAL Memory helps OpenClaw agents recover from session crashes, disconnects, provider outages, and context compaction by installing a local write-ahead state log, goals template, and cold boot recovery guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maikunari](https://clawhub.ai/user/maikunari) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to add local continuity for OpenClaw sessions by recording meaningful actions in STATE.log and maintaining a short GOALS.md recovery file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: STATE.log and GOALS.md can contain private project data because the recovery log is local plaintext. <br>
Mitigation: Add STATE.log to .gitignore, avoid logging secrets or sensitive payloads, and periodically review the recovery files before future sessions read them. <br>
Risk: Persistent recovery context can preserve stale or misleading session state. <br>
Mitigation: Review the latest STATE.log entries and keep GOALS.md current so resumed sessions start from accurate context. <br>


## Reference(s): <br>
- [WAL Memory release page](https://clawhub.ai/maikunari/wal-memory) <br>
- [GOALS template](assets/GOALS.template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and a JavaScript logging script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js; writes a local plaintext STATE.log with simple rotation at 5MB.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
