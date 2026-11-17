## Description:

Generates short music-video clips from melody audio, a photo, and a prompt using a local Node/Express app with Ollama scene descriptions and FFmpeg video rendering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gblockchainnetwork](https://clawhub.ai/user/gblockchainnetwork)

### License/Terms of Use:

ISC

## Use Case:

Developers and creators use this skill to run a local video-generation web app that accepts audio, an image, and a prompt, then returns scene text and an MP4 output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local web server exposes unauthenticated media processing.

Mitigation: Run it only in a trusted local environment until authentication, upload limits, and rate limiting are added.

Risk: Submitted audio, images, prompts, and generated MP4 outputs may contain sensitive content.

Mitigation: Treat inputs and outputs as sensitive local files and add safe cleanup or retention controls before broader deployment.

Risk: Long-running generation jobs and downloads may need stronger operational controls.

Mitigation: Add job timeouts, safe output cleanup, UUID validation on downloads, DOM-safe rendering, and patched or pinned dependencies before exposing the app.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gblockchainnetwork/skills/vibeclip)
- [Publisher profile](https://clawhub.ai/user/gblockchainnetwork)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Markdown and JSON responses with generated MP4 file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local Node.js, Ollama, and FFmpeg; generated audio, image, prompt, and MP4 outputs should be treated as sensitive local content.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
