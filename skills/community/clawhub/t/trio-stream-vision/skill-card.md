## Description: <br>
Analyze YouTube livestreams, RTSP camera feeds, Twitch streams, and HLS streams using natural-language questions, event detection, and periodic summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drandrewlaw](https://clawhub.ai/user/drandrewlaw) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
External users and developers use this skill to ask natural-language questions about authorized live video streams, start event monitors, and receive periodic summaries without building their own vision pipeline. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected livestream or camera content can be sent to Trio for analysis, including footage from private spaces or bystanders. <br>
Mitigation: Use only streams the user owns or is authorized to monitor, avoid private spaces and bystanders without consent, and disclose that selected stream content is sent to Trio. <br>
Risk: Continuous monitoring can run longer or trigger more often than intended, increasing privacy exposure and usage cost. <br>
Mitigation: Test conditions with check-once first, set finite monitor_duration_seconds and max_triggers values, and inform users about per-minute costs before starting live-monitor or live-digest jobs. <br>
Risk: Exposure of TRIO_API_KEY could allow unauthorized API use. <br>
Mitigation: Store the key in an environment variable or secret manager, never print it in user-visible output or logs, and rotate the key if exposure is suspected. <br>
Risk: Security-guard and social-posting use cases could normalize overly broad surveillance or public sharing of observations. <br>
Mitigation: Treat those examples as risky marketing notes, not safe defaults; require explicit authorization and consent before monitoring or sharing stream-derived observations. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/drandrewlaw/trio-stream-vision) <br>
- [Trio API Reference](https://docs.machinefi.com/api-reference/) <br>
- [Trio Console](https://console.machinefi.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash curl commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TRIO_API_KEY plus curl and python3; responses may include triggered status, explanations, job IDs, job status, and optional frame data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
