## Description:

Runs as an OpenClaw cron workflow every 15 minutes to find meetings scheduled 15 minutes to 6 hours ahead, generate pre-meeting progress briefs, commit briefing artifacts to Gitea, update meeting status, and return email content for attendees.

This skill is ready for commercial/non-commercial use.

## Publisher:

[myd2002](https://clawhub.ai/user/myd2002)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to automate pre-meeting briefing workflows across managed Gitea repositories. It scans scheduled meeting metadata, prepares report parameters, stores brief records, updates meeting state, logs activity, and hands back email-ready HTML for delivery by a separate mail skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad automated Gitea access can expose meeting data or update repositories unexpectedly.

Mitigation: Install with a dedicated least-privilege Gitea bot token and restrict execution to explicit repositories.

Risk: HTTP Gitea configuration can expose tokens or meeting content in transit.

Mitigation: Use an HTTPS Gitea base URL before production use.

Risk: Automatic email sending can disclose sensitive meeting briefs to unintended recipients.

Mitigation: Avoid automatic sending for sensitive meetings and validate recipient lists before commit output is passed to the mail skill.

Risk: Commit mode accepts local HTML files and recipient lists that may be unsafe if supplied from an untrusted source.

Mitigation: Do not pass arbitrary local files or unvalidated recipient lists into commit.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON command output with Markdown and HTML briefing artifacts generated or referenced by the workflow]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scan output includes meeting records and report parameters; commit output includes status fields and email-ready recipient, subject, and HTML body values.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
