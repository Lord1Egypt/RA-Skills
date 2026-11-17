## Description:

Provides current system time, detailed time information, time differences, multiple time formats, and timezone-aware time conversion through MCP tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qzy05231](https://clawhub.ai/user/qzy05231)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to retrieve current time, inspect detailed date/time fields, convert across timezones, and calculate elapsed time between two timestamps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tool responses and descriptions include Chinese-language text that may not fit every workflow.

Mitigation: Install only where Chinese-language tool text is acceptable, or review and localize the user-facing strings before deployment.

Risk: Dependency versions are not pinned and no lockfile is included in the artifact.

Mitigation: For stronger supply-chain control, pin dependency versions and use a lockfile before production deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qzy05231/skills/system-time)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text]

**Output Format:** [Plain text returned by MCP tool calls, including ISO dates, date-only strings, time-only strings, Unix timestamps, and Chinese-language detailed time labels.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports optional IANA timezone input for current-time output and ISO 8601 or Unix timestamp input for time-difference calculations.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
