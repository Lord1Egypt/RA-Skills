## Description: <br>
Converts natural-language relative day expressions into the soonest future calendar date in ISO format for accurate scheduling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jtheodas](https://clawhub.ai/user/jtheodas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents, developers, and scheduling workflows use this skill before creating calendar events or stating specific future dates that depend on expressions such as "next Friday", "this Wed", or "tomorrow". <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Important calendar events may be scheduled incorrectly if the reference time or timezone differs from the user's intent. <br>
Mitigation: Confirm the returned date manually for important events and provide a reference time or IANA timezone when timezone matters. <br>
Risk: The local helper depends on python-dateutil for parsing weekday expressions. <br>
Mitigation: Ensure python-dateutil is available in the runtime before relying on the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jtheodas/relative-date-resolver) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance] <br>
**Output Format:** [ISO date string (YYYY-MM-DD)] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns the soonest future matching date; invalid or ambiguous expressions may raise a clear error or use a reasonable future match.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
