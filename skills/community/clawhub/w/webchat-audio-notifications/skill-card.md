## Description: <br>
Add browser audio notifications to Moltbot/Clawdbot webchat with 5 intensity levels - from whisper to impossible-to-miss (only when tab is backgrounded). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brokemac79](https://clawhub.ai/user/brokemac79) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and webchat operators use this skill to add configurable browser audio alerts to Moltbot or Clawdbot-style webchat deployments. It is intended for chat events where users should hear a notification only when the tab is backgrounded. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audio notifications may be enabled, too loud, or too frequent for a deployment's user expectations. <br>
Mitigation: Review the default enabled setting, selected intensity level, volume, and cooldown before deployment, and expose controls so users can disable or lower notifications. <br>
Risk: Custom sound and preference data stored in localStorage can persist on the browser profile. <br>
Mitigation: Document local storage behavior for users, provide a reset or removal path for custom sounds, and avoid storing sensitive audio files on shared browser profiles. <br>
Risk: A settings panel served from an untrusted or user-editable path could present unsafe or misleading controls. <br>
Mitigation: Serve the bundled settings panel from a trusted local path and review related Content Security Policy settings during integration. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/brokemac79/webchat-audio-notifications) <br>
- [Integration Guide](artifact/docs/integration.md) <br>
- [Easy Setup Guide](artifact/docs/EASY_SETUP.md) <br>
- [Sound Files Attribution](artifact/client/sounds/SOUNDS.md) <br>
- [Howler.js](https://howlerjs.com/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, configuration, shell commands, markdown] <br>
**Output Format:** [Markdown with JavaScript, HTML, JSON, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces browser integration guidance and client-side configuration for webchat audio notifications.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata; artifact SKILL.md lists 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
