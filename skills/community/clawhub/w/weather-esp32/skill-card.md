## Description: <br>
Get weather data from your personal ESP32+BMP280 sensor. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[manisaigaddam](https://clawhub.ai/user/manisaigaddam) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to have an agent read and explain live temperature, pressure, altitude, and health data from their own ESP32+BMP280 sensor. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may contact the wrong ESP32 IP address or Cloudflare Tunnel URL if the configured endpoint is stale or incorrect. <br>
Mitigation: Before first use, replace or verify the configured endpoint and confirm it points to the intended ESP32 sensor. <br>
Risk: The sensor provides local readings, not full weather forecasts or complete umbrella-decision data. <br>
Mitigation: Use the skill for ESP32 sensor readings and only rely on forecast-style advice when the device actually provides the needed data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/manisaigaddam/weather-esp32) <br>
- [Publisher profile](https://clawhub.ai/user/manisaigaddam) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown conversation responses with HTTP request instructions and parsed sensor readings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include live sensor values for temperature, pressure, altitude, ESP32 health status, and troubleshooting guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
