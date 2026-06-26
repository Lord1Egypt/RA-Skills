## Description: <br>
Fetches Indonesian prayer schedules for city or regency locations from api.myquran.com, including today's schedule, a specific date, a full month, or location ID search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[banghasan](https://clawhub.ai/user/banghasan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to find Indonesian city or regency IDs and retrieve prayer times for today, a selected date, or a one-month period. <br>

### Deployment Geography for Use: <br>
Global; schedule data is focused on cities and regencies in Indonesia. <br>

## Known Risks and Mitigations: <br>
Risk: Using the skill sends the requested location and date or month to api.myquran.com. <br>
Mitigation: Review requests before execution and avoid sending sensitive or unnecessary location details. <br>
Risk: The artifact does not include a strict manifest declaring the network domain it uses. <br>
Mitigation: Run it in an environment that only permits the disclosed api.myquran.com network access. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/banghasan/sholat) <br>
- [api.myquran.com v3 API base](https://api.myquran.com/v3) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and plain-text schedule output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No API key is required; output may include imsak, subuh, terbit, dhuha, dzuhur, ashar, maghrib, and isya times when returned by the API.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
