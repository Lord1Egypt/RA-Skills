## Description: <br>
Generate, edit, and manage PowerPoint presentations via the SlideSpeak API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mve](https://clawhub.ai/user/mve) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to create presentations from text or uploaded documents, edit existing slides, list templates, and retrieve generated PowerPoint download URLs through SlideSpeak. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected files, prompts, and presentation content are sent to SlideSpeak. <br>
Mitigation: Use the skill only with content approved for SlideSpeak processing, and avoid confidential, regulated, or secret-bearing documents unless your organization authorizes that service. <br>
Risk: The skill requires a SlideSpeak API key. <br>
Mitigation: Store SLIDESPEAK_API_KEY in a secure environment variable or secret manager and avoid exposing it in prompts, logs, or shared files. <br>
Risk: Webhook subscriptions can send completion callbacks to a supplied URL. <br>
Mitigation: Register only webhook callback URLs that you control and trust. <br>


## Reference(s): <br>
- [SlideSpeak ClawHub release](https://clawhub.ai/mve/slidespeak) <br>
- [SlideSpeak publisher profile](https://clawhub.ai/user/mve) <br>
- [SlideSpeak homepage](https://slidespeak.co) <br>
- [SlideSpeak developer settings](https://app.slidespeak.co/settings/developer) <br>
- [SlideSpeak API Reference](references/API.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON responses, Presentation files, Configuration guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated presentations are retrieved through short-lived download URLs returned by the SlideSpeak API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
