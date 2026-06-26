## Description: <br>
Offload date math to code -- get current date, days/weeks until goal dates, and month-end info. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elroyic](https://clawhub.ai/user/elroyic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use Time Anchor to answer date, deadline, scheduling, and timeline questions with deterministic local date calculations instead of mental date math. It supports current-date anchoring, days or weeks until target dates, upcoming weekday options with ambiguity metadata, and days remaining in the current month. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill has a broad trigger for date, deadline, scheduling, and 'when' phrasing. <br>
Mitigation: Use it for date-related questions and review whether invocation is appropriate before relying on its output. <br>
Risk: Editable configured target labels may expose sensitive private event names. <br>
Mitigation: Avoid storing confidential event names in the TARGETS list; use generic labels or user-provided context instead. <br>
Risk: The workflow allows web search when a named event date is unknown. <br>
Mitigation: Do not web-search confidential or internal events; ask the user for the date when the event is private or ambiguous. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/elroyic/time-anchor) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Plain text responses; weekday lookups include a trailing JSON ambiguity payload.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs a local Python helper and may use editable configured target dates.] <br>

## Skill Version(s): <br>
1.1.0 (source: clawhub.json and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
