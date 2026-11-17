## Description:

AI music generation via Suno API. Submit prompts, style tags, and lyrics to generate songs. Check generation status and download audio/cover art. Use when user asks to create music, generate songs, compose tracks, or produce audio content with AI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kennedydqz-del](https://clawhub.ai/user/kennedydqz-del)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to generate songs, extend or transform audio, check Suno generation status, and retrieve generated audio, cover art, lyrics, MIDI, and video outputs through a command-line client.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, lyrics, task IDs, media URLs, and generated media data may be sent to external Suno API services.

Mitigation: Review the skill before installing, avoid submitting sensitive content, and use only trusted HTTPS endpoints for SUNO_BASE_URL.

Risk: The CLI includes file-upload behavior that can send local audio files to an external upload host.

Mitigation: Use upload-file only for intentionally selected non-sensitive audio files and confirm the external upload destination is acceptable.

Risk: The skill forwards SUNO_API_KEY as a bearer credential to configured API endpoints.

Mitigation: Keep API keys scoped and private, and do not override SUNO_BASE_URL to an untrusted endpoint.

## Reference(s):

- [Suno API documentation](https://docs.sunoapi.org/cn/suno-api/)
- [ClawHub skill page](https://clawhub.ai/kennedydqz-del/skills/suno-music-skill)
- [Publisher profile](https://clawhub.ai/user/kennedydqz-del)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, API calls]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or retrieve external URLs for generated audio, cover art, lyrics, MIDI, and video assets.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
