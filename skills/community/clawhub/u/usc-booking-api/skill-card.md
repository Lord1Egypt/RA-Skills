## Description:

Scans configured Urban Sports Club venues, lists classes with booking links, and can book, cancel, or list bookings using local USC credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[niklaspriddat](https://clawhub.ai/user/niklaspriddat)

### License/Terms of Use:


## Use Case:

Developers and personal automation users use this skill to scan configured Urban Sports Club venues by date and venue, then produce class listings or intentionally perform booking, cancellation, and booking-list actions through the CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses local USC account credentials and packaged credential files can accidentally include real account secrets.

Mitigation: Keep real credentials out of packaged source control, protect the credentials file, and prefer a secret manager or protected local path.

Risk: Booking and cancellation commands can modify a user's Urban Sports Club account.

Mitigation: Only run booking or cancellation commands with an explicitly reviewed class ID and confirm the account and target class before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/niklaspriddat/skills/usc-booking-api)
- [Urban Sports Club venue URL pattern](https://urbansportsclub.com/de/venues/20818)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration]

**Output Format:** [CLI text or JSON arrays with Urban Sports Club class and booking details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May perform authenticated booking or cancellation actions when invoked with explicit class IDs.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
