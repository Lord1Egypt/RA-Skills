## Description:

Window Truth helps agents compare local RTSP camera observations with Open-Meteo forecasts to detect rain and cloud-cover conflicts at a specific location.

This skill is ready for commercial/non-commercial use.

## Publisher:

[citriac](https://clawhub.ai/user/citriac)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and weather-observation practitioners use this skill to configure a local IP camera check, compare brightness and microphone RMS against remote forecast data, and flag cases where local conditions disagree with a weather app.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The included script accesses an RTSP camera stream and captures microphone audio to compute RMS.

Mitigation: Use only cameras the operator owns or is authorized to monitor, and review privacy expectations before running the script.

Risk: The default RTSP URL includes placeholder credentials and a private network address.

Mitigation: Replace the default RTSP URL with a dedicated least-privilege camera account supplied through environment variables.

Risk: Configured latitude and longitude are sent to Open-Meteo and local observations are appended to JSONL history.

Mitigation: Use coordinates appropriate for the deployment, understand the external API disclosure, and manage the local history file according to retention needs.

## Reference(s):

- [Window Truth - Local vs Remote Conflict Detection](references/conflict_detection.md)
- [Window Truth ClawHub skill page](https://clawhub.ai/citriac/skills/window-truth)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python code and shell-oriented configuration instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local JSONL observation history when the included twilight test script is run.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
