## Description:

Talkies provides a self-hosted, OpenAI-compatible service for speech recognition, live audio transcription, and text-to-speech.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Talkies with a self-hosted speech service to transcribe audio, generate subtitles, stream live speech recognition, and synthesize speech through OpenAI-compatible endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples invoke local shell tools and handle caller-selected files, despite the declared permission note that the skill itself does not access the local filesystem.

Mitigation: Review commands and approve only the specific local inputs and outputs needed for the task.

Risk: Audio, text, and voice samples sent through the skill are processed by the configured Talkies service; URL inputs are fetched by that server.

Mitigation: Use a service you trust and review the specific files, URLs, and voice samples before sending them.

Risk: Server-side staged files may be shared among callers, and deployments may be reachable without authentication.

Mitigation: Enable authentication, restrict network access, and manage staged files as admin-only on shared instances.

Risk: Container image references may not identify a fixed, verified release.

Mitigation: Deploy a verified container image at a fixed version.

Risk: Voice cloning can reproduce a real person's voice without their knowledge.

Mitigation: Use voice samples only with the speaker's explicit authorization and consent.

## Reference(s):

- [Setup guide](references/setup.md)
- [Streaming ASR documentation](https://github.com/psyb0t/docker-talkies/blob/main/docs/streaming.md)
- [Talkies project documentation](https://github.com/psyb0t/docker-talkies)
- [Talkies on ClawHub](https://clawhub.ai/psyb0t/skills/talkies)

## Skill Output:

**Output Type(s):** [Transcription text, Audio files, Subtitle files, API calls, Shell commands, Configuration instructions]

**Output Format:** [Text, audio, JSON, SRT/VTT, and Markdown guidance with shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output and model availability depend on the selected speech model and service configuration.]

## Skill Version(s):

1.3.19 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
