## Description: <br>
This skill helps university students find available classrooms for self-study, group discussion, exam prep, or meetings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jjmorant12](https://clawhub.ai/user/jjmorant12) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, especially university students, use this skill to choose campus study spaces by time, group size, location, and preferences such as quietness, outlets, or group-work suitability. The skill ranks usable rooms, explains tradeoffs, and flags schedule conflicts, room restrictions, and recent feedback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recommendations may be based on bundled sample classroom, schedule, and feedback data rather than the school's live room system. <br>
Mitigation: Verify room availability with the school's official classroom system, posted notices, or on-site checks before relying on a recommendation. <br>
Risk: The included demo login and admin controls are not suitable as real application security. <br>
Mitigation: Do not deploy the demo page as a production application without replacing it with server-side authentication and authorization. <br>


## Reference(s): <br>
- [StudySeat Buddy ClawHub page](https://clawhub.ai/jjmorant12/studyseat-buddy) <br>
- [Classroom data](references/classroom_data.md) <br>
- [Schedule data](references/schedule_data.md) <br>
- [Feedback data](references/feedback_data.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, text] <br>
**Output Format:** [Markdown response with ranked recommendations, rationale, avoided-room notes, and cautions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses bundled sample campus data unless replaced with official school classroom, schedule, and feedback sources.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
