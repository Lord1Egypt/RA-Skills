## Description:

Counts ZenTao bugs for a specified start date and for the current day, including created, closed, activated, defect-introduction, unresolved, and pending-verification totals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hanweify](https://clawhub.ai/user/hanweify)

### License/Terms of Use:

MIT-0

## Use Case:

QA, engineering, and release teams with authorized ZenTao access use this skill to gather daily bug activity and version-date-range bug counts for release tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact ships default ZenTao credentials.

Mitigation: Replace embedded credentials with user-supplied secrets before use and rotate the exposed password if it may be real.

Risk: The default ZenTao URL uses plaintext HTTP.

Mitigation: Use an HTTPS ZenTao endpoint before running the script.

Risk: The skill accesses a ZenTao instance and retrieves bug data.

Mitigation: Install and run it only when authorized to access the target ZenTao environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hanweify/skills/zentao-bug-stats)

## Skill Output:

**Output Type(s):** [Shell commands, Text, Guidance]

**Output Format:** [Markdown guidance with command examples and terminal text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires authorized ZenTao connection details and credentials; reports aggregate bug counts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
