## Description:

Tracks shipments with 17Track batch APIs, updates shipment status, sends customer email notifications, and alerts on delivery exceptions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cjboy007](https://clawhub.ai/user/cjboy007)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to automate ecommerce shipment monitoring, customer delivery notifications, and exception alerting across supported carriers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local alert file writes and customer-facing HTML email content may be unsafe when built from untrusted shipment or customer data.

Mitigation: Review and fix alert filename path handling and HTML escaping before installation; use dry-run until the behavior is verified.

Risk: The scheduler can use 17Track API and SMTP credentials while writing local state on a recurring schedule.

Mitigation: Use dedicated least-privileged credentials and run scheduled jobs under an unprivileged account with limited writable paths.

## Reference(s):

- [17Track API](https://api.17track.net/)
- [ClawHub Skill Page](https://clawhub.ai/cjboy007/skills/ssa-logistics-tracker)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands plus JSON configuration and status data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May trigger 17Track API calls, local state file updates, customer email notifications, and Discord or email alerts when configured.]

## Skill Version(s):

1.0.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
