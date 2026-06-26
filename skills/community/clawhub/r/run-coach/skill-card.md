## Description: <br>
Science-based running coach with HD visual training plans and Garmin sync for runners from 5K fitness to marathon. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ENAwareness](https://clawhub.ai/user/ENAwareness) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External runners use this skill through Telegram to log runs, request training plans, review trends, and optionally sync Garmin data for coaching feedback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The image feature may process untrusted or HTML-like text while generating Telegram images. <br>
Mitigation: Review generated content before sending images and avoid routing untrusted or HTML-like text through the image feature until escaping is fixed. <br>
Risk: The skill can store persistent fitness data and use Telegram bot access plus optional Garmin account access. <br>
Mitigation: Keep tokens and passwords out of logs and repositories, limit use to trusted accounts, and periodically review or delete MEMORY.md, garmin/.garth, and local Garmin activity files. <br>


## Reference(s): <br>
- [Run Coach on ClawHub](https://clawhub.ai/ENAwareness/run-coach) <br>
- [garminconnect releases](https://github.com/cyberjunky/python-garminconnect/releases) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command snippets and optional generated image delivery through Telegram.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Telegram bot credentials for image delivery; Garmin sync is optional and depends on user-provided Garmin credentials.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
