## Description: <br>
Manages QQBot reminders through real OpenClaw cron jobs with explicit per-user timezone settings for reminders, alarms, timed notifications, recurring reminders, lookup, cancellation, and timezone setup or changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zykkk-power](https://clawhub.ai/user/zykkk-power) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External QQBot users and operators use this skill to create, list, cancel, and manage timezone-aware reminders backed by OpenClaw cron jobs. It is intended for reminder workflows where delivery should be scheduled as real cron jobs rather than promised only in chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can manage real OpenClaw cron jobs, including listing the global cron inventory and deleting jobs by raw job ID. <br>
Mitigation: Review the script before deployment and run it with a restricted OpenClaw account or isolated environment when multiple QQ users or unrelated cron jobs share the same system. <br>
Risk: Timezone guidance is inconsistent, which can affect time-sensitive reminders. <br>
Mitigation: Resolve the timezone documentation conflict and require explicit IANA timezone confirmation before creating reminders. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zykkk-power/qqbot-remind-absolute) <br>
- [references.txt](references.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Short text replies with inline shell commands and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit per-target IANA timezone setup before first reminder creation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
