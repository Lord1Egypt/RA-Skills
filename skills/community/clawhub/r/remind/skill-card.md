## Description: <br>
Auto-learns when and how to bring things back to your human's attention and adapts timing and style to their preferences. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use Remind to help an assistant identify known commitments, choose appropriate lead times, and bring reminders back at the right moment while adapting to feedback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Inferred reminders can capture sensitive commitments or preferences without an explicit request. <br>
Mitigation: Prefer explicit reminder requests for sensitive commitments, review learned reminder preferences, and clear inferred reminders that should not be retained. <br>
Risk: Adaptive timing can produce reminders that are too early, too frequent, or unnecessary. <br>
Mitigation: Use user feedback such as 'too early', 'I knew already', or 'forgot' to adjust or skip categories after repeated signals. <br>


## Reference(s): <br>
- [Timing Defaults](timing.md) <br>
- [Reminder Triggers](triggers.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance, Configuration] <br>
**Output Format:** [Plain text reminders and learned preference entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reminder timing and style adapt based on explicit requests, implicit signals, and user feedback.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
