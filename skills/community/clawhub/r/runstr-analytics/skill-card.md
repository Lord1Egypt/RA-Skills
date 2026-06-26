## Description: <br>
Advanced RUNSTR fitness analytics with trend analysis, performance insights, training recommendations, and correlation tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[katla50](https://clawhub.ai/user/katla50) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and RUNSTR users use this skill to analyze workout history, habits, mood, and step data from encrypted Nostr backups. It generates trend analysis, performance insights, personal records, correlation summaries, coaching recommendations, and optional daily reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to a highly sensitive Nostr private key and the security evidence reports that handling is less safe than the documentation claims. <br>
Mitigation: Use only on a private, trusted machine; prefer a release that consistently avoids chat and command-line secret exposure; do not share RUNSTR_NSEC. <br>
Risk: Decrypted RUNSTR workout and journal data may be retained in a local cache. <br>
Mitigation: Use full-disk encryption, keep the machine single-user where possible, and delete ~/.cache/runstr-analytics when local retention is no longer needed. <br>
Risk: The optional daily cron setup can continue accessing cached data and RUNSTR_NSEC-dependent workflows on a schedule. <br>
Mitigation: Enable cron only when daily reports are needed, review installed crontab entries, and remove the job when automation is no longer required. <br>
Risk: The install metadata uses the latest nak package rather than a pinned release. <br>
Mitigation: Pin and review the nak dependency before use in sensitive or repeatable environments. <br>


## Reference(s): <br>
- [Runstr analytics ClawHub listing](https://clawhub.ai/katla50/runstr-analytics) <br>
- [nak command-line tool](https://github.com/fiatjaf/nak) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Text, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Terminal text, JSON exports, and Markdown reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create a local SQLite cache and text reports under ~/.cache/runstr-analytics; optional cron setup can generate daily reports.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
