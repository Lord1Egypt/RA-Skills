## Description:

Adds bidirectional voice workflows for agents, including speech-to-text transcription, Edge TTS speech synthesis, generated MP3 output, and optional local or tunneled access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[patrickgeek](https://clawhub.ai/user/patrickgeek)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to add voice input and spoken responses to assistant workflows. It is suited for local voice interaction, generated voice reply links, and integrations that can consume transcription text or MP3 output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated audio can be exposed through unauthenticated local or tunneled HTTP endpoints.

Mitigation: Keep the service bound to localhost by default, add authentication before external exposure, and avoid public tunnels for private audio.

Risk: Generated MP3 files may contain sensitive conversation content and remain on disk.

Mitigation: Store output in a controlled directory, delete old files routinely, and treat generated audio as sensitive data until removed.

Risk: The documentation describes integrations and helper scripts that are not all present in the artifact.

Mitigation: Verify shipped scripts and required integrations before relying on documented workflows in production.

Risk: Setup guidance includes downloading or installing third-party executables and tunnel clients.

Mitigation: Install dependencies from trusted sources, verify downloads where possible, and review network tools before enabling remote access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/patrickgeek/skills/voice-chat-bridge)
- [Edge TTS](https://github.com/rany2/edge-tts)
- [hear macOS speech recognition](https://github.com/sveinbjornt/hear)
- [Cloudflare Tunnel documentation](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/)

## Skill Output:

**Output Type(s):** [Text, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash, JSON, and Python examples; scripts output transcription text, generated MP3 files, file paths, and URLs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated MP3 files are retained locally until cleanup and may be served through a local HTTP endpoint or public tunnel when configured.]

## Skill Version(s):

1.1.0 (source: evidence.release.version and artifact/SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
