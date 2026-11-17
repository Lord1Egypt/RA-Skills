## Description:

Check USCIS case status by receipt number.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pkhanpara](https://clawhub.ai/user/pkhanpara)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to check a USCIS immigration case status from a receipt number and return the current case, date, and status fields.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an externally maintained Python package that is not pinned in the skill artifact.

Mitigation: Install and run it in an isolated environment and review the resolved package before operational use.

Risk: USCIS receipt numbers can be sensitive personal information.

Mitigation: Avoid unnecessary credentialed browser profiles, logs, or shared environments when checking case status.

Risk: The skill uses browser automation against the USCIS website, which may rate-limit frequent requests or hang when the site is slow.

Mitigation: Throttle requests to every few minutes and use command timeouts when scripting repeated checks.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Text, Guidance]

**Output Format:** [Markdown with inline bash commands and plain-text command output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, installs the uscis-case-status package, and expects a USCIS receipt number as input.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
