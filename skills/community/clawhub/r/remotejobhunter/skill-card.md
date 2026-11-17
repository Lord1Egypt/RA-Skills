## Description:

Automates daily remote job search, matching, and email reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aliceyuruchan](https://clawhub.ai/user/aliceyuruchan)

### License/Terms of Use:

MIT-0

## Use Case:

Job seekers use this skill to search for remote roles, compare matches against their profile, verify that job links are still open, and receive job-search reports by console or email.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can help configure daily email reports and scheduled runs.

Mitigation: Confirm with the user before enabling scheduled execution or email delivery.

Risk: Email setup may involve SMTP credentials, and job-search profiles may contain personal data.

Mitigation: Avoid storing SMTP passwords in plain JSON when possible and treat profile, resume, email, and job-preference details as personal data.

Risk: Broad activation wording could start job-search or setup behavior when the user's intent is ambiguous.

Mitigation: Confirm intent before running searches, changing configuration, sending email, or setting up automation.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/aliceyuruchan/remotejobhunter)
- [ClawHub skill page](https://clawhub.ai/aliceyuruchan/skills/remotejobhunter)
- [Google App Passwords](https://myaccount.google.com/apppasswords)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce console job reports, email-report setup guidance, and user-specific configuration instructions.]

## Skill Version(s):

0.1.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
