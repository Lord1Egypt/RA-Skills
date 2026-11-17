## Description:

All-in-one AI skill via Router9 API for speech recognition, text-to-speech, image description, OCR, image generation, and file storage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shushuo-dev](https://clawhub.ai/user/shushuo-dev)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use Router9 to call cloud AI services for audio transcription, speech generation, image understanding, OCR, image generation, and hosted file storage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected text, audio, images, and files may be sent to Router9-managed services.

Mitigation: Use the skill only for data that is approved for external processing, and avoid sending secrets or regulated data.

Risk: File upload and download commands can read from and write to local paths selected by the agent or user.

Mitigation: Review file paths before transfer and provide an explicit safe output path for downloads.

Risk: Remote delete operations do not add a confirmation step in the bundled CLI.

Mitigation: Verify file IDs before deletion and restrict use to storage entries intended for removal.

## Reference(s):

- [Router9 Homepage](https://router9.com)
- [Router9 API Keys](https://router9.com/settings/api-keys)
- [ClawHub Router9 Skill](https://clawhub.ai/shushuo-dev/skills/router9)

## Skill Output:

**Output Type(s):** [text, JSON, files, shell commands, configuration]

**Output Format:** [JSON stdout responses plus generated local files for audio, images, uploads, downloads, and storage operations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and ROUTER9_API_KEY; uploads are documented with a 50 MB maximum file size.]

## Skill Version(s):

1.0.2 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
