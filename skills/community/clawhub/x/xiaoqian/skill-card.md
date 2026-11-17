## Description:

Automatically queries Jiangsu Maritime Safety Administration platform meeting information for a requested date range and exports structured meeting data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tokido-25](https://clawhub.ai/user/tokido-25)

### License/Terms of Use:

MIT-0

## Use Case:

Authorized users with access to the Jiangsu Maritime Safety Administration integrated platform can use this skill to automate meeting lookup by date or date range and export meeting fields such as time, location, attendees, and organizer.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The release exposes reusable government-portal credentials.

Mitigation: Treat the embedded password as compromised, rotate it before use, and provide credentials only through a protected secret source such as environment variables.

Risk: Meeting exports and JSON backups may contain sensitive operational data.

Mitigation: Run the skill only on authorized accounts and remove exported JSON backups or make backup creation explicit opt-in with restricted file permissions.

Risk: The automation accesses the portal over HTTP and depends on browser driver downloads.

Mitigation: Use HTTPS where available, preinstall or pin ChromeDriver and dependencies, and review the execution environment before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tokido-25/skills/xiaoqian)
- [Publisher profile](https://clawhub.ai/user/tokido-25)
- [Jiangsu MSA portal login](http://gchportal.js-msa.gov.cn/cas/login)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration, Text]

**Output Format:** [Excel workbook, JSON backup, and console/log text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Exports meeting records with date, start time, title, location, attendees, organizer, and optional row metadata.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
