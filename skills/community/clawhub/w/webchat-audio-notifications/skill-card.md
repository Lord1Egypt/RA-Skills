## Description:

Add browser audio notifications to Moltbot/Clawdbot webchat with 5 intensity levels - from whisper to impossible-to-miss (only when tab is backgrounded).

This skill is ready for commercial/non-commercial use.

## Publisher:

[brokemac79](https://clawhub.ai/user/brokemac79)

### License/Terms of Use:

MIT

## Use Case:

Developers and webchat maintainers use this skill to add browser-side audio notifications, user settings, and configurable sound intensity to Moltbot/Clawdbot-style webchat interfaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill adds browser JavaScript to a webchat page.

Mitigation: Review the JavaScript before deployment and install it only in webchat environments where browser-side notification behavior is acceptable.

Risk: Uploaded custom sounds and notification preferences persist in browser localStorage.

Mitigation: Avoid storing sensitive audio files as custom sounds, and clear the custom sound or browser data when the data should be removed.

Risk: Browser autoplay and mobile restrictions can prevent audio from playing until a user gesture occurs.

Mitigation: Keep the enable or test-sound prompt visible during setup and test the target browsers, especially iOS Safari and mobile browsers.

Risk: Remote sound assets can add unnecessary availability and privacy exposure.

Mitigation: Prefer local or self-hosted sound assets, as recommended by the security guidance.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/brokemac79/skills/webchat-audio-notifications)
- [Integration Guide](docs/integration.md)
- [Easy Setup Guide](docs/EASY_SETUP.md)
- [Sound Files Attribution](client/sounds/SOUNDS.md)
- [Howler.js](https://howlerjs.com/)
- [Mixkit Sound Effects License](https://mixkit.co/license/#sfxFree)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JavaScript, HTML, JSON, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes browser-side JavaScript assets, a settings panel, example configuration, local/self-hosted sound assets, and integration guidance.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
