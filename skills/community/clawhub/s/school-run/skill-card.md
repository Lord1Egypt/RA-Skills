## Description: <br>
Manages the School Run Schedule Google Sheet. Use when reading or updating the school run drop-off schedule for Damian and Zachary (date, responsible person, marks). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cbasah](https://clawhub.ai/user/cbasah) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Household or caregiver users use this skill to read and update a specific school drop-off schedule in Google Sheets, including dates, the responsible person, and remarks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and update a live school-run schedule in Google Sheets. <br>
Mitigation: Keep the Google service account least-privileged, check current data before changes, dry-run write operations where possible, and require clear confirmation before updating the live sheet. <br>
Risk: The commands depend on the configured gws CLI, spreadsheet ID, sheet tab name, and credential path. <br>
Mitigation: Verify the spreadsheet, sheet tab, gws CLI installation, and service-account credential path before use. <br>


## Reference(s): <br>
- [School Run ClawHub Release](https://clawhub.ai/cbasah/school-run) <br>
- [cbasah Publisher Profile](https://clawhub.ai/user/cbasah) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Google Workspace CLI command templates for reading and updating a Google Sheet.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
