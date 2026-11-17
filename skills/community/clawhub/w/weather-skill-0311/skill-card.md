## Description:

Looks up weather for a named city, including Chinese city names, using wttr.in live data or an offline sample mode.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuboon](https://clawhub.ai/user/yuboon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query current weather details for global city names, including Chinese city names, from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented install command uses a placeholder package name.

Mitigation: Verify the exact package identity and publisher profile before installing, and do not run the placeholder install command.

Risk: Live weather lookups use unencrypted HTTP.

Mitigation: Prefer offline mode for validation or use a version that performs live weather requests over HTTPS before relying on live data.

## Reference(s):

- [Weather Query Skill Homepage](https://example.com/weather-query-skill)
- [ClawHub Skill Page](https://clawhub.ai/yuboon/skills/weather-skill-0311)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON weather output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live mode returns weather fields such as temperature, humidity, condition, wind speed, and observation time; offline mode returns a fixed sample payload.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
