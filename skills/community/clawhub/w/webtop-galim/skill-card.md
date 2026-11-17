## Description:

Check, monitor, and summarize student homework/tasks from Webtop (SmartSchool), Galim Pro, and Ofek.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shaike1](https://clawhub.ai/user/shaike1)

### License/Terms of Use:

MIT-0

## Use Case:

Parents or caregivers use this skill through an agent to retrieve, combine, and summarize student homework and task status from Webtop, Galim Pro, and Ofek. It can also support routine school-task updates and optional syncing of Galim due dates to Google Calendar.

### Deployment Geography for Use:

Israel

## Known Risks and Mitigations:

Risk: The skill handles local student portal credentials and child-related school task details.

Mitigation: Install only for intended school-account use, store env files and Google service-account files with restricted access, and avoid loading WEBTOP_GALIM_ENV from untrusted paths.

Risk: Calendar sync can copy homework titles, due dates, subjects, and child names into Google Calendar.

Mitigation: Run sync only against an intended calendar, review configured calendar and service-account access first, and use the dry-run mode before enabling writes.

Risk: The security evidence flags unsafe local configuration and external-script execution patterns that warrant review.

Mitigation: Review the external Webtop dependency and local wrapper behavior before running report commands in a trusted environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shaike1/skills/webtop-galim)
- [Environment credentials format](references/env-example.md)
- [Ofek students portal](https://students.myofek.cet.ac.il/he)
- [Galim Pro login](https://userdata.galim.org.il/login_idm?request_uri=https%3A%2F%2Fpro.galim.org.il%2F%3Flang%3Dhe)
- [Galim Pro tasks portal](https://lms.galim.org.il/personal?lang=he)
- [Google Calendar API endpoint used by sync](https://www.googleapis.com/calendar/v3)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Hebrew text or Markdown summaries, JSON task data, shell command guidance, and calendar sync result JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports report, expanded, ofek, galim, webtop, sync, and env-check command modes; report commands accept options such as --json, --days, --limit, --hide-overdue, and --due-within-days.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
