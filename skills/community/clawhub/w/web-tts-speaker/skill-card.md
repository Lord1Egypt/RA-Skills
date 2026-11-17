## Description:

Web TTS Speaker turns webpage content or supplied text into text-to-speech audio files for Feishu, WeChat, Telegram, and Discord workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phentse](https://clawhub.ai/user/phentse)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to fetch article text or accept supplied text, synthesize speech, and prepare platform-specific audio attachments for supported messaging channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch arbitrary URLs.

Mitigation: Use it only where public-web URL fetching is acceptable, avoid private or internal URLs, and add confirmation plus URL validation before deployment.

Risk: Extracted webpage content or supplied text may be sent to an external TTS service.

Mitigation: Do not process secrets or sensitive text without consent, and remove text snippets from shared logs or machine-readable output when needed.

Risk: The security verdict recommends review before installation.

Mitigation: Review the skill before installing, pin dependencies, and deploy only in an environment where its URL fetching and TTS behavior are permitted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/phentse/skills/web-tts-speaker)
- [Publisher profile](https://clawhub.ai/user/phentse)
- [OpenClaw WeChat voice message issue](https://github.com/openclaw/openclaw/issues/61031)
- [FFmpeg Windows builds](https://www.gyan.dev/ffmpeg/builds/)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with bash examples and CLI stdout markers that point to generated MP3 or Opus audio files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3.8+, Python packages edge-tts, beautifulsoup4, and requests, plus FFmpeg for audio transcoding.]

## Skill Version(s):

3.2.1 (source: server release metadata, artifact skill.json, and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
