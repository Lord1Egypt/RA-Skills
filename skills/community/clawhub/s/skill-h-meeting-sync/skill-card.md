## Description: <br>
Synchronizes meeting status between Tencent Meeting and Gitea repositories on a scheduled cron workflow, handling cancellations, reschedules, new pending meetings, and archive cleanup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[myd2002](https://clawhub.ai/user/myd2002) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to keep meeting records in Gitea aligned with Tencent Meeting changes during recurring automated checks. It supports scanning active meetings, marking eligible meetings as cancelled, rescheduling meetings, creating pending records for newly detected meetings, and archiving old cancelled or rescheduled meeting directories. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs on a cron schedule and can mutate Gitea meeting records with broad bot-token authority. <br>
Mitigation: Install with a tightly scoped Gitea bot token, use an explicit repository allowlist where possible, and review the cron configuration, archive behavior, and setup script before enabling automatic runs. <br>
Risk: Command output and notification payloads can include attendee emails and meeting join links. <br>
Mitigation: Treat command output and logs as sensitive, restrict access to the runtime environment, and avoid forwarding raw output outside the intended operations channel. <br>
Risk: Automated meeting comparison can affect cancellation, reschedule, and pending-record workflows. <br>
Mitigation: Review the documented comparison tolerance and rely on the built-in skipped-cancellation behavior for meetings whose scheduled time has already passed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/myd2002/skill-h-meeting-sync) <br>
- [Publisher profile](https://clawhub.ai/user/myd2002) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with shell command examples and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May mutate Gitea meeting files and emit email notification payloads containing attendee and meeting details.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
