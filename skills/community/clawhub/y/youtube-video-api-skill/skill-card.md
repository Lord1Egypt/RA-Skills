## Description: <br>
This skill helps users automatically extract channel-level and video detail data from a specific YouTube channel via BrowserAct API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ccmagia2-gif](https://clawhub.ai/user/ccmagia2-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and content operations teams use this skill to collect structured YouTube channel and video metrics for competitor tracking, creator research, reporting, and content strategy analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends the target YouTube channel URL and workflow parameters to BrowserAct. <br>
Mitigation: Use it only when BrowserAct is an acceptable third-party service for the data being processed. <br>
Risk: The skill requires a BrowserAct API key. <br>
Mitigation: Provide BROWSERACT_API_KEY through a secure environment or secret manager, use a dedicated or revocable key, and avoid pasting secrets into chat. <br>
Risk: Browser automation tasks can take several minutes or fail because of network or service conditions. <br>
Mitigation: Monitor the timestamped status logs, retry once for non-authorization failures, and stop on invalid or expired authorization. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ccmagia2-gif/youtube-video-api-skill) <br>
- [Publisher profile](https://clawhub.ai/user/ccmagia2-gif) <br>
- [BrowserAct integrations console](https://www.browseract.com/reception/integrations) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal status logs followed by structured YouTube channel and video data returned as text or JSON-like content from BrowserAct.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python and BROWSERACT_API_KEY; accepts a YouTube channel URL and optional video ordering mode: Latest, Popular, or Earliest.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
