## Description:

Timezone Helper converts times between zones, provides world clock answers, plans meetings across regions, and explains DST using built-in city-to-IANA mapping data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobewin](https://clawhub.ai/user/tobewin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to answer time zone conversion, current-time, DST, and meeting-planning questions without network calls or API keys.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Time-zone and DST rules can change, and precise current-time answers depend on the system clock.

Mitigation: Treat outputs as convenience guidance; confirm the current date, DST status, and authoritative time-zone rules for high-stakes scheduling.

## Reference(s):

- [City to IANA Timezone Mapping](references/cities.md)
- [ClawHub Skill Page](https://clawhub.ai/tobewin/skills/timezone-helper)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-formatted time zone conversions, world clock summaries, meeting planner options, and DST explanations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fully offline; current-time answers depend on the system clock and DST-sensitive results should be checked for high-stakes scheduling.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
