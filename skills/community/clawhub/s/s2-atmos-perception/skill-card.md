## Description: <br>
S2-SP-OS Atmos Radar. Real-time meteorological and space weather (NOAA) perception organ for AI Agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SpaceSQ](https://clawhub.ai/user/SpaceSQ) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agent operators use this skill to fetch weather, air quality, and NOAA space-weather signals for a user-provided location and return environmental insights or a human-readable report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Location input is sent to external weather and geocoding services. <br>
Mitigation: Ask for explicit user consent and prefer coarse city-level locations when possible. <br>
Risk: Weather, air-quality, or space-weather service failures can return default or incomplete values. <br>
Mitigation: Treat results as advisory, disclose uncertainty when data appears defaulted, and avoid automatic device actions. <br>
Risk: The included Python file appears to contain a markdown code fence that may prevent direct execution. <br>
Mitigation: Verify the file runs before deployment and remove the fence if needed. <br>


## Reference(s): <br>
- [S2 Atmos Perception on ClawHub](https://clawhub.ai/SpaceSQ/s2-atmos-perception) <br>
- [Open-Meteo Geocoding API endpoint](https://geocoding-api.open-meteo.com/v1/search) <br>
- [Open-Meteo Forecast API endpoint](https://api.open-meteo.com/v1/forecast) <br>
- [Open-Meteo Air Quality API endpoint](https://air-quality-api.open-meteo.com/v1/air-quality) <br>
- [NOAA SWPC NOAA Scales data](https://services.swpc.noaa.gov/products/noaa-scales.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown instructions with shell commands; runtime output is JSON in agent mode or Markdown-like text in human mode.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and a user-provided location; calls external weather and space-weather services.] <br>

## Skill Version(s): <br>
1.0.9 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
