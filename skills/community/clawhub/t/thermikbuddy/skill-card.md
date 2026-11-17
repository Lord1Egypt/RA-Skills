## Description:

ThermikBuddy helps agents fetch Central European soaring-weather forecasts and summarize thermal scores, climb rates, cloud base, alpine effects, and warnings for glider and paraglider flight planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[achimace](https://clawhub.ai/user/achimace)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to answer glider or paraglider weather-planning questions for configured German and Alpine regions or user-supplied coordinates. It returns planning guidance and should not replace official aviation weather briefings, local regulations, or pilot judgment.

### Deployment Geography for Use:

Germany and Central Europe

## Known Risks and Mitigations:

Risk: External weather services may be unavailable, incomplete, stale, or inconsistent with local conditions.

Mitigation: Confirm conditions with official aviation weather briefings and local weather sources before flight decisions.

Risk: The guidance is localized to German and Central-European soaring assumptions and may not transfer to all regions, terrain, or regulations.

Mitigation: Use the output as a planning aid for matching regions or explicit coordinates, and apply local regulations and pilot judgment.

## Reference(s):

- [Scoring-Parameter Referenz](references/scoring_params.md)
- [DHV Wetter](https://www.dhv.de/wetter/dhv-wetter/)
- [Open-Meteo Forecast API](https://api.open-meteo.com/v1/forecast)
- [SkySight](https://skysight.io)
- [TopMeteo](https://europe.topmeteo.eu/de/)
- [DWD Segelflug](https://www.dwd.de/DE/fachnutzer/luftfahrt/kg_segel/segel_node.html)
- [Soaringmeteo](https://soaringmeteo.org/v2)
- [aufwin.de](https://aufwin.de)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance derived from JSON forecast data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [German-language daily soaring forecast with 0-10 thermal scores, timing, weather warnings, and reference links.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
