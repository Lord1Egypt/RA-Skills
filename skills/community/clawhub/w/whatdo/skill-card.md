## Description: <br>
What Should We Do? helps an agent suggest personalized activities, entertainment, and group plans using context such as weather, local options, preferences, history, calendars, and group profiles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ScotTFO](https://clawhub.ai/user/ScotTFO) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to get activity ideas, date-night plans, stay-home entertainment, and group-planning suggestions that account for personal preferences and current context. It can also help turn accepted plans into calendar events, reminders, invitations, and RSVP tracking when the user approves those actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can remember personal preferences, activity history, group profiles, and contact details. <br>
Mitigation: Review stored data in data/whatdo/preferences.json and data/whatdo/history.json periodically, delete stale or sensitive entries, and only store contact details that are needed for planning. <br>
Risk: Calendar, reminder, and messaging actions may affect schedules or send information to other people. <br>
Mitigation: Before acting, require the agent to show the exact calendar event, recipients, invite or reminder text, and any data it will store or send. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ScotTFO/whatdo) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown responses with optional shell command snippets and JSON preference or history examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update data/whatdo/preferences.json and data/whatdo/history.json when the agent has file access.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
