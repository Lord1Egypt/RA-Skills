## Description:

Safely manage your AI skill collection with trust scoring, security vetting, delayed auto-updates, and pending periods for new skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liefqin](https://clawhub.ai/user/liefqin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill library maintainers use this skill to track installed skills, queue new additions, check for updates, and apply trust-based delays before changes are made.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The advertised safety gate may not provide effective security review before skills are added or updated.

Mitigation: Manually review and independently vet each skill before installation or update; use dry-run or manual workflows first.

Risk: Recommended scheduled automation can change installed skills without timely human review.

Mitigation: Avoid running this skill from cron or as root until approval controls and update verification are confirmed.

Risk: Trust scores may be mistaken for real security results.

Mitigation: Treat trust scores as advisory only until vetting output, update verification, and approval controls are fixed.

## Reference(s):

- [Skill Guardian release page](https://clawhub.ai/liefqin/skills/skill-guardian)
- [Registry format](references/registry-format.md)
- [Trust ratings](references/trust-ratings.md)
- [Cron setup guide](references/cron-setup.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes command-line workflows for adding, listing, updating, and scheduling skill registry checks.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
