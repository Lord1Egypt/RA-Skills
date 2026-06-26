## Description: <br>
Command-line weather checker tool with global city support, temperature, precipitation, and probability display with emoji formatting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luckisnow](https://clawhub.ai/user/luckisnow) <br>

### License/Terms of Use: <br>
MIT License <br>


## Use Case: <br>
Developers and command-line users use this skill to query weather forecasts for global cities, including temperature, precipitation, and precipitation probability in text or JSON formats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installation guidance may fetch code from a placeholder raw GitHub URL or create a system-wide command symlink. <br>
Mitigation: Install from the bundled reviewed weather_checker.py or a verified release, and prefer a user-level ~/.local/bin symlink unless system-wide installation is intentional. <br>
Risk: City and location queries are sent to Open-Meteo services. <br>
Mitigation: Avoid submitting sensitive or private location names, and disclose this network dependency to users. <br>


## Reference(s): <br>
- [ClawHub Weather Checker Release](https://clawhub.ai/luckisnow/weather-checker) <br>
- [Open-Meteo API](https://open-meteo.com/) <br>
- [Open-Meteo Geocoding API](https://geocoding-api.open-meteo.com/v1/search) <br>
- [Open-Meteo Forecast API](https://api.open-meteo.com/v1/forecast) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Plain text, simple one-line text, or JSON returned by a Python command-line tool] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses city, day offset, output format, and list-cities command-line options.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
