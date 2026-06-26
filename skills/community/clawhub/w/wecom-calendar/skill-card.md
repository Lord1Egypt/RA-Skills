## Description: <br>
Manage WeCom calendars and schedules by creating, querying, updating, and canceling events with support for repeats, reminders, attendees, and timezone settings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davinwang](https://clawhub.ai/user/davinwang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams with a configured WeCom app use this skill to let an agent manage organizational calendar events and shared calendars. It is suited for schedule creation, lookup, updates, cancellation, attendee handling, reminders, and recurring events. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify real organizational calendar data, including updates, cancellations, recurring events, and large attendee lists. <br>
Mitigation: Use a dedicated least-privilege WeCom app and require explicit review before update, cancel, recurring-event, or large-attendee operations. <br>
Risk: The skill depends on WeCom credentials that grant calendar API access. <br>
Mitigation: Keep WECOM_CORP_ID, WECOM_AGENT_ID, and WECOM_AGENT_SECRET out of source control and shared logs. <br>
Risk: Calendar API calls require correct WeCom permissions and trusted IP configuration. <br>
Mitigation: Confirm the app has only the required calendar permissions and that trusted IP settings are configured before deployment. <br>


## Reference(s): <br>
- [WeCom Schedule API documentation](https://developer.work.weixin.qq.com/document/path/93703) <br>
- [WeCom Calendar API documentation](https://developer.work.weixin.qq.com/document/path/93707) <br>
- [ClawHub skill page](https://clawhub.ai/davinwang/wecom-calendar) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Text] <br>
**Output Format:** [Command-line instructions and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WeCom app credentials and trusted IP configuration before use.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata; artifact docs and package.json show 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
