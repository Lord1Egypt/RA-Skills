## Description: <br>
ThermikBuddy helps an agent fetch soaring-weather forecasts and summarize thermal conditions, scores, daily timing, cloud-base estimates, alpine wind effects, and warnings for glider and paraglider pilots. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[achimace](https://clawhub.ai/user/achimace) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to evaluate soaring, thermal, cross-country, gliding, and paragliding weather conditions for predefined regions or custom coordinates. It runs bundled Python forecast scripts, then formats the resulting weather and scoring data into a pilot-facing assessment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs bundled Python forecast code and makes outbound weather requests. <br>
Mitigation: Review the selected region or coordinates before execution and install only if outbound weather requests are acceptable. <br>
Risk: Custom coordinates can reveal precise location information. <br>
Mitigation: Use predefined regions or coarse coordinates when exact private locations are unnecessary. <br>
Risk: Package metadata is inconsistent across server release evidence and artifact files. <br>
Mitigation: Confirm that version 1.0.3 is the intended release before publishing or deploying the card. <br>


## Reference(s): <br>
- [Scoring Parameter Reference](artifact/references/scoring_params.md) <br>
- [ThermikBuddy ClawHub Page](https://clawhub.ai/achimace/thermikbuddy) <br>
- [DHV Weather](https://www.dhv.de/wetter/dhv-wetter/) <br>
- [DWD Soaring Weather](https://www.dwd.de/DE/fachnutzer/luftfahrt/kg_segel/segel_node.html) <br>
- [Open-Meteo Forecast API](https://api.open-meteo.com/v1/forecast) <br>
- [SkySight](https://skysight.io) <br>
- [TopMeteo Europe](https://europe.topmeteo.eu/de/) <br>
- [Soaringmeteo](https://soaringmeteo.org/v2) <br>
- [aufwin.de](https://aufwin.de) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown summary with command-driven JSON forecast data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The agent may invoke local Python scripts that return JSON on stdout and logs or errors on stderr.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence; artifact frontmatter says 2.0.0 and artifact metadata/origin say 1.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
