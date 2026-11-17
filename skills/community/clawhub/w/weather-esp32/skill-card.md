## Description:

Get weather data from your personal ESP32+BMP280 sensor.

This skill is ready for commercial/non-commercial use.

## Publisher:

[manisaigaddam](https://clawhub.ai/user/manisaigaddam)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to query a personal ESP32+BMP280 weather sensor for live local temperature, pressure, altitude, and device health, then receive concise weather status, comfort advice, and troubleshooting guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill saves and contacts a user-configured ESP32 network endpoint.

Mitigation: Verify the endpoint belongs to the user's ESP32 device before use and avoid arbitrary URLs.

Risk: The skill remembers the ESP32 address but does not describe a clear deletion control.

Mitigation: Review the host agent's memory or profile controls before deployment so users can inspect or remove the stored endpoint.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Natural-language responses with sensor readings, device health status, and brief advice or troubleshooting messages.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include temperature, pressure, altitude, uptime, readings served, and reachability guidance based on the configured ESP32 endpoint.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata, created 2026-02-09)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
