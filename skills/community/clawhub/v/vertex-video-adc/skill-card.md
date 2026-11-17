## Description:

Generate videos via Google Cloud Vertex AI predictLongRunning (Veo) using Application Default Credentials (ADC).

This skill is ready for commercial/non-commercial use.

## Publisher:

[neogeosnk](https://clawhub.ai/user/neogeosnk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation builders use this skill to generate text-to-video or image-to-video outputs through Google Cloud Vertex AI Veo using local Google Cloud credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, optional images, and API responses are sent to Google Cloud Vertex AI using the user's project credentials.

Mitigation: Install only when that data flow is acceptable for the project and account being used.

Risk: Raw response JSON can be written to predictable temporary files during operation.

Mitigation: Review or patch the script before use so raw response JSON is not left in shared temporary paths unless explicitly needed for debugging.

## Reference(s):

- [Google Cloud Vertex AI](https://cloud.google.com/vertex-ai)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [ClawHub skill page](https://clawhub.ai/neogeosnk/skills/vertex-video-adc)
- [Publisher profile](https://clawhub.ai/user/neogeosnk)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated videos are written as MP4 files when the Vertex AI response contains video bytes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
