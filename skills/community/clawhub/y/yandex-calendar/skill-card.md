## Description:

Manage Yandex Calendar through CalDAV using vdirsyncer and khal to view, add, sync, and search calendar events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gbroccoli](https://clawhub.ai/user/gbroccoli)

### License/Terms of Use:


## Use Case:

Developers and personal-assistant agent users use this skill to operate a Yandex Calendar from a trusted local environment where khal and vdirsyncer are already configured. The skill helps agents list today's, weekly, or monthly events, create new events, sync calendars, and search for events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent to run user-derived shell commands that create or sync remote calendar events.

Mitigation: Use only in a trusted local environment, confirm event details before creating or syncing, and invoke command arguments literally or with robust escaping.

Risk: Calendar sync can modify remote state or fail when vdirsyncer is unavailable or misconfigured.

Mitigation: Keep khal and vdirsyncer configured before use, review sync errors, and fall back to read-only khal commands when sync is unavailable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gbroccoli/skills/yandex-calendar)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Assumes local CalDAV tooling is configured; calendar changes should be confirmed before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
