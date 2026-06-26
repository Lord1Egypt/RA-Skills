## Description: <br>
Get snow conditions, forecasts, and ski reports for any mountain resort worldwide. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davemorin](https://clawhub.ai/user/davemorin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to retrieve current snow conditions, forecasts, and comparison reports for ski resorts through OpenSnow, with optional saved resort preferences for repeat lookups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill visits OpenSnow pages for requested resorts. <br>
Mitigation: Use it only when you are comfortable with the agent visiting OpenSnow for those resorts. <br>
Risk: The skill can save default and favorite mountains in memory/snow-preferences.md. <br>
Mitigation: Store only non-sensitive resort preferences, and edit or delete that file if preferences should not be retained. <br>
Risk: Snow conditions and forecasts can change throughout the day or be partially unavailable. <br>
Mitigation: Treat reports as current-condition guidance and verify critical trip decisions with OpenSnow or the resort. <br>


## Reference(s): <br>
- [Resort Slugs & SnowTick Codes](references/resorts.md) <br>
- [Snow Preferences Template](references/user-config-template.md) <br>
- [OpenSnow snow summary URL pattern](https://opensnow.com/location/{slug}/snow-summary) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown snow reports, comparison tables, and concise text guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read or create memory/snow-preferences.md for default and favorite resorts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
