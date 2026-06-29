## Description: <br>
Window Truth helps an agent compare local RTSP camera observations with Open-Meteo forecasts to detect rain and cloud-cover conflicts near a specific window. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[citriac](https://clawhub.ai/user/citriac) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, weather-monitoring hobbyists, and local automation users use this skill to test whether a nearby IP camera's photo and audio observations better answer immediate rain and cloud-cover questions than a remote forecast. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill accesses an RTSP camera stream that may include audio and sensitive views near a user's home or building. <br>
Mitigation: Configure the RTSP URL deliberately, avoid embedded camera credentials where possible, and run the skill only in environments where camera video and audio access is appropriate. <br>
Risk: The skill sends configured latitude and longitude to a weather API and stores local observation records. <br>
Mitigation: Use only intended coordinates, review or rotate the local data/twilight_predictions.jsonl log, and avoid sharing logs when location or observation history is sensitive. <br>
Risk: Local camera signals can be affected by IR night mode, audio noise, camera placement, and calibration choices. <br>
Mitigation: Review conflict output before acting on it, calibrate thresholds for the local camera, and treat generated weather judgments as observational guidance rather than authoritative forecasts. <br>


## Reference(s): <br>
- [Window Truth on ClawHub](https://clawhub.ai/citriac/window-truth) <br>
- [Window Truth Source](https://github.com/citriac/window-truth) <br>
- [Local vs Remote Conflict Detection](references/conflict_detection.md) <br>
- [Open-Meteo Forecast API](https://api.open-meteo.com/v1/forecast) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Console text, JSONL observation records, and Markdown guidance with configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an RTSP camera URL, ffmpeg, Python with requests, and latitude/longitude configuration for weather lookups.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
