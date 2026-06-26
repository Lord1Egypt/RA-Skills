## Description: <br>
CLI for Yandex Tracker (bash + curl). Queues, issues, comments, worklogs, attachments, YQL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bkamuz](https://clawhub.ai/user/bkamuz) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operations teams use this skill to manage Yandex Tracker queues, issues, comments, worklogs, attachments, projects, sprints, checklists, and YQL searches from an agent-driven shell workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The CLI can directly update, delete, transition, upload to, export from, or otherwise change live Yandex Tracker data. <br>
Mitigation: Use a least-privilege Yandex Tracker token and require explicit human confirmation before delete, transition, update, upload, or export commands. <br>
Risk: The TOKEN credential and optional ~/.yandex-tracker-env file are sensitive and could expose organization access if logged or shared. <br>
Mitigation: Prefer environment variables, keep tokens out of logs and shared configuration, and restrict any credential file permissions. <br>
Risk: Attachment path protection is not fully robust, especially around sensitive paths or symlinked directories. <br>
Mitigation: Set a dedicated YANDEX_TRACKER_ATTACHMENTS_DIR, avoid symlinks in that directory, and do not upload from or download to sensitive paths. <br>


## Reference(s): <br>
- [Yandex Tracker](https://tracker.yandex.ru/) <br>
- [Yandex Tracker API v2](https://api.tracker.yandex.net/v2) <br>
- [Yandex Tracker API v3](https://api.tracker.yandex.net/v3) <br>
- [ClawHub skill page](https://clawhub.ai/bkamuz/yandex-tracker-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, JSON, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON responses from the Yandex Tracker API] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, TOKEN, and ORG_ID; attachment operations should use a dedicated YANDEX_TRACKER_ATTACHMENTS_DIR.] <br>

## Skill Version(s): <br>
1.2.8 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
