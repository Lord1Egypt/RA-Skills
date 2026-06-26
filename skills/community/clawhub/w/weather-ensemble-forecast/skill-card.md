## Description: <br>
Multi-model ensemble weather forecasts comparing GFS, ECMWF, JMA, GEM, ICON, ARPEGE, GraphCast and more, with high temperature predictions from up to 9 independent weather models and agreement analysis for 16 global cities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Lucasnocodo](https://clawhub.ai/user/Lucasnocodo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, weather enthusiasts, event planners, researchers, travelers, and prediction market traders use this skill to compare model-by-model high-temperature forecasts and forecast agreement for supported cities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: City and date forecast queries, and any configured WEATHER_ENSEMBLE_API_KEY, are sent off-device to the Weather Ensemble API or to a custom WEATHER_ENSEMBLE_HOST. <br>
Mitigation: Install only when that data sharing is acceptable, and set WEATHER_ENSEMBLE_HOST only to a trusted service. <br>
Risk: Weather model outputs can disagree, and forecast uncertainty may be higher when the ensemble standard deviation is large. <br>
Mitigation: Use the per-model predictions and standard deviation as decision support, and cross-check high-impact decisions against an official forecast source. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Lucasnocodo/weather-ensemble-forecast) <br>
- [Weather Ensemble API forecast endpoint](https://polymarket-scanner.fly.dev/forecast/{city}) <br>
- [Weather Ensemble API cities endpoint](https://polymarket-scanner.fly.dev/cities) <br>
- [Weather Ensemble API key endpoint](https://polymarket-scanner.fly.dev/keys/free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown-facing command guidance and JSON-formatted shell command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and jq; accepts a city key and optional YYYY-MM-DD date; can use WEATHER_ENSEMBLE_API_KEY and WEATHER_ENSEMBLE_HOST.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
