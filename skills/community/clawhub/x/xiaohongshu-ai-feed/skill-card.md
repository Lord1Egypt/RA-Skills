## Description: <br>
AI小红书信息源 scans AI-related Xiaohongshu posts, ranks them by engagement, clusters topics, and generates local HTML daily reports with cover images, metrics, and subscription support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redfox-data](https://clawhub.ai/user/redfox-data) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External content operators, Xiaohongshu creators, and industry analysts use this skill to fetch trending AI posts, review engagement metrics, and generate daily or historical reports for content and market research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a RedFox API key for normal operation. <br>
Mitigation: Verify the key source, scope, validity period, and revocation path before use; provide it through the REDFOX_API_KEY environment variable and avoid hardcoding or logging it. <br>
Risk: Subscription mode creates a persistent daily scheduled task and may store the API key on disk on macOS. <br>
Mitigation: Prefer one-off runs unless daily automation is needed; avoid --subscribe unless you accept the persistence behavior, and rotate the API key if subscription mode was previously enabled. <br>
Risk: Normal runs create local HTML reports and may open them automatically in a browser. <br>
Mitigation: Use --no-open when browser launch is not desired and review the generated files in ~/Downloads/QoderReports before sharing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/redfox-data/xiaohongshu-ai-feed) <br>
- [RedFox API key settings](https://redfox.hk/settings/api-keys?source=skillhub) <br>
- [RedFoxHub](https://redfox.hk) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [Terminal text plus local HTML report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REDFOX_API_KEY; default reports are saved under ~/Downloads/QoderReports and can be opened in a browser.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
