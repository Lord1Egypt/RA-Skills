## Description:

Fetches Yahoo Finance earnings calendar data for a single date and returns structured company earnings records, including ticker, earnings timing, and market capitalization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lhl09120](https://clawhub.ai/user/lhl09120)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to query Yahoo Finance earnings calendar entries for today or a specified date from a local Chrome-based workflow. It is useful when an agent needs JSON data for ticker symbols, BMO/AMC/TNS earnings timing, and numeric market capitalization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installed native host exposes an unauthenticated local socket that other local processes could use.

Mitigation: Install only in trusted local environments and prefer a version that uses a user-private socket path, validates local requests, authenticates callers, and limits request sizes.

Risk: The workflow requires installing a Chrome extension and local Native Messaging host.

Mitigation: Review the extension, native host, and install script before deployment; load the extension only under the intended browser profile and publisher release.

Risk: The Ubuntu installation guidance includes a deprecated apt-key sudo pipeline.

Mitigation: Use current distribution keyring practices for Chrome repository setup or install Chrome through an approved organizational package channel.

Risk: Yahoo Finance page structure changes can break parsing or produce incomplete earnings records.

Mitigation: Validate results against the Yahoo Finance earnings calendar after updates and review the documented DOM field assumptions when output changes unexpectedly.

## Reference(s):

- [Today Earnings ClawHub Release](https://clawhub.ai/lhl09120/skills/today-earnings)
- [Usage Guide](references/usage_guide.md)
- [Yahoo Finance Earnings Calendar Technical Reference](references/yahoo_earnings_calendar.md)
- [Skill Design](design.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration]

**Output Format:** [JSON array on stdout, with Markdown guidance and shell commands in the skill documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Each result contains code, earningType, and numeric marketCap; failures are reported on stderr with a non-zero exit code.]

## Skill Version(s):

4.3.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
