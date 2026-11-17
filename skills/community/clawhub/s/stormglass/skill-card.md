## Description:

Fetches surf-relevant ocean conditions from Stormglass by spot name or coordinates, including current conditions and 1-3 day forecast windows with tides, gusts, and water temperature.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dgorissen](https://clawhub.ai/user/dgorissen)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to fetch machine-readable surf reports for beach or surf spot workflows. It supports cron-style pipelines and downstream summaries of waves, swell, wind, water temperature, and tide timing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Location queries may be sent to Stormglass and a geocoding provider.

Mitigation: Use direct coordinates when practical, avoid sending sensitive location strings, and cache results to reduce repeated external lookups.

Risk: Google geocoding API keys can be exposed in error logs.

Mitigation: Restrict the Google key in Google Cloud, avoid persistent stderr logging until URL redaction is fixed, and rotate the key if logs may contain key values.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dgorissen/skills/stormglass)
- [Project Homepage](https://github.com/dgorissen/stormglass-skill)
- [Stormglass API Documentation](https://docs.stormglass.io/#/)
- [Skill Reference](artifact/reference.md)
- [Skill Examples](artifact/examples.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [JSON or human-readable terminal text, with Markdown command examples in the skill documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires STORMGLASS_API_KEY for live Stormglass requests; GOOGLE_GEOCODING_API_KEY is optional for location geocoding; mock mode runs without API keys.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
