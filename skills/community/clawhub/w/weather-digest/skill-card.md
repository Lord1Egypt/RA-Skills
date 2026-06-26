## Description: <br>
Generate daily Weather Intelligence Digest using NOAA/NWS data with customizable locations and alert monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dannyboy1241](https://clawhub.ai/user/dannyboy1241) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, publishers, and automation builders use this skill to generate daily weather briefings for configured locations, including forecasts and active alert summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dependency or environment drift can affect repeatable installs. <br>
Mitigation: Install the skill in a virtual environment and pin or review the requests dependency before use. <br>
Risk: Configured locations may reveal sensitive audience or operational context. <br>
Mitigation: Keep config locations appropriate for the intended audience and avoid publishing private location sets. <br>
Risk: Generated HTML may be republished beyond its original trust boundary. <br>
Mitigation: HTML-escape or sanitize generated HTML before broad publication. <br>
Risk: Automation recipes can send digests to unintended paths, recipients, or notification channels. <br>
Mitigation: Review cron, LaunchAgent, heartbeat, and webhook paths and recipients before enabling automation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dannyboy1241/weather-digest) <br>
- [NOAA/NWS API](https://api.weather.gov) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, html, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, HTML, and JSON files with CLI usage and configuration guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3, pip, requests, a location configuration file, and network access to api.weather.gov.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
