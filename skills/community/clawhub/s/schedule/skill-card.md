## Description: <br>
Program recurring or one-time tasks. User defines what to do, skill handles when. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users use this skill to create, store, review, and cancel one-time or recurring scheduled tasks while keeping the task action, timing, timezone, and required permissions explicit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved scheduled tasks can run later using permissions the user has granted. <br>
Mitigation: Review each job's action, timing, timezone, required skills, and expiration before saving it. <br>
Risk: Task text or local history could contain sensitive information. <br>
Mitigation: Avoid putting secrets in scheduled task text and periodically review or delete ~/schedule/jobs.json and history logs that are no longer needed. <br>
Risk: Ambiguous dates, timezones, daylight saving changes, or indefinite recurrence can cause jobs to run at an unexpected time. <br>
Mitigation: Confirm exact date, time, timezone, recurrence, and review or end date before creating the job. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/schedule) <br>
- [Job Storage Format](jobs.md) <br>
- [Cron Patterns Reference](patterns.md) <br>
- [Scheduling Traps](traps.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, shell commands, guidance] <br>
**Output Format:** [Markdown confirmations with JSON job configuration and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists job definitions, preferences, and execution history under ~/schedule/.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
