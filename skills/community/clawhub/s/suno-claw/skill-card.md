## Description:

Suno Claw is a multi-agent music-creation workflow that turns a user's song idea into Suno-compatible prompts, calls kie.ai/Suno services, and returns generated music with lyrics or instrumental guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jasonzhang-zzx](https://clawhub.ai/user/jasonzhang-zzx)

### License/Terms of Use:

MIT-0

## Use Case:

External users and music creators use this skill to develop songs or instrumental tracks from a short creative brief. The workflow gathers music context, drafts lyrics and style tags, packages Suno prompts, generates audio through kie.ai, and can retain liked outputs as local preference history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, lyrics, titles, style tags, and generated music requests are sent to kie.ai/Suno-related services.

Mitigation: Avoid submitting secrets, confidential lyrics, sensitive personal material, or content that should not leave the local environment.

Risk: The optional callback URL can expose generated content or task data if pointed at an untrusted endpoint.

Mitigation: Leave CALLBACK_URL empty unless the endpoint is controlled and trusted.

Risk: Liked-generation history and preference patterns are stored locally and may influence future generations.

Mitigation: Delete the skill's memory files when preference history should not be retained or reused.

## Reference(s):

- [Suno AI](https://suno.ai)
- [kie.ai API documentation](https://docs.kie.ai/)
- [kie.ai Suno API documentation](https://docs.kie.ai/suno-api/)
- [Suno Claw on ClawHub](https://clawhub.ai/jasonzhang-zzx/skills/suno-claw)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown status updates and structured generation results with JSON and shell command support]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns song titles, audio URLs, lyrics when applicable, concise style descriptions, Suno prompt data, and local preference-memory updates.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
