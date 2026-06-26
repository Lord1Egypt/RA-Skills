## Description: <br>
Check accurate current time, date, and timezone information for any location worldwide using time.is. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1999AZZAR](https://clawhub.ai/user/1999AZZAR) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents and users can use this skill to check the current time, date, and timezone details for a city or country, especially when coordinating schedules across locations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Location lookup requests are sent to time.is. <br>
Mitigation: Avoid using sensitive private locations and disclose the external lookup source when that matters to the user. <br>
Risk: The skill depends on a live web page fetched with curl, so page changes or network failures can prevent a successful lookup. <br>
Mitigation: Report lookup errors clearly and verify critical scheduling information with another source when needed. <br>
Risk: The skill text includes an optional persona and tone preference unrelated to time accuracy. <br>
Mitigation: Treat the tone note as optional style guidance and follow the user's requested tone and higher-priority instructions. <br>


## Reference(s): <br>
- [time.is](https://time.is) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include the resolved location, current time, additional date or timezone details, and the source URL.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
