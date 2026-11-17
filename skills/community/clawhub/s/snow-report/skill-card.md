## Description:

Get snow conditions, forecasts, and ski reports for any mountain resort worldwide.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davemorin](https://clawhub.ai/user/davemorin)

### License/Terms of Use:


## Use Case:

External users use this skill to get current snow conditions, forecasts, and ski reports for named resorts, SnowTick codes, favorites, and resort comparisons.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation phrases for snow or mountain weather questions may trigger browser lookups when the user did not intend a ski report.

Mitigation: Confirm the target resort or use the user's configured default before opening OpenSnow pages for ambiguous requests.

Risk: The skill can retain a user's home mountain and favorite resorts in memory/snow-preferences.md.

Mitigation: Tell users where preferences are stored and review or delete memory/snow-preferences.md when they do not want resort preferences retained.

Risk: OpenSnow data changes throughout the day and some forecast windows may be paywalled or unavailable.

Mitigation: Present visible data with timestamps when available and avoid treating long-range or inaccessible forecast fields as definitive.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/davemorin/skills/snow-report)
- [OpenSnow snow summary URL pattern](https://opensnow.com/location/{slug}/snow-summary)
- [Resort Slugs & SnowTick Codes](references/resorts.md)
- [Snow Preferences Template](references/user-config-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown snow reports, ticker summaries, comparison tables, powder alerts, and preference prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May summarize live OpenSnow browser data and may create or read memory/snow-preferences.md for user resort preferences.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
