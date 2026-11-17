## Description:

Queries weather for cities worldwide, including Chinese city names, using wttr.in with an offline demo mode.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuboon](https://clawhub.ai/user/yuboon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to look up weather for a named city and return temperature, humidity, conditions, wind, and observation time. The offline mode supports demonstrations and tests without network access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Online weather requests send city queries to wttr.in over plaintext HTTP, which can expose or alter queries and results on untrusted networks.

Mitigation: Use offline mode for demonstrations and tests, or prefer a release that uses HTTPS before relying on online results.

Risk: Weather output depends on an external service and may return errors or unexpected data.

Mitigation: Check the returned JSON for an error field and review results before using them in downstream decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuboon/skills/weather-skill-yub)
- [Publisher profile](https://clawhub.ai/user/yuboon)
- [Project homepage](https://example.com/weather-query-skill)
- [wttr.in weather service](http://wttr.in)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [JSON weather data and Markdown command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Online mode queries wttr.in; offline mode returns a bundled sample response.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
