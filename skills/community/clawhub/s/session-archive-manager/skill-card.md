## Description: <br>
Manages OpenClaw session files by trimming large sessions, generating summaries, archiving old sessions, and freeing disk space. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[delgyd](https://clawhub.ai/user/delgyd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to reduce session storage growth by trimming oversized JSONL session files, writing summaries, compressing archives, and optionally scheduling recurring archival. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automated trimming, archiving, and cleanup can rewrite, move, compress, or delete OpenClaw session and log files. <br>
Mitigation: Run the scripts manually first, confirm configured paths and retention thresholds, and keep independent backups before enabling automated cleanup. <br>
Risk: The cron setup can make archival behavior persistent and recurring. <br>
Mitigation: Enable cron only when recurring archival is required, inspect the installed crontab entry, and review archive logs after scheduled runs. <br>
Risk: Generated summaries may contain sensitive commands, file paths, or credential-like text copied from session history. <br>
Mitigation: Review summary JSON files before sharing or retaining them broadly, and store them with the same access controls as the original sessions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/delgyd/session-archive-manager) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with bash commands and JSON summary files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create compressed archives, trimmed session files, cron entries, and summary JSON under OpenClaw session directories.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
