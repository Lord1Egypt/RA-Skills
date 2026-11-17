## Description:

Helps agents use the a7w music-generation service to create songs and lyrics, work with reference audio and voices, and export or separate tracks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2253128](https://clawhub.ai/user/2253128)

### License/Terms of Use:

MIT

## Use Case:

Creators and developers use this skill to guide an agent through music and lyrics generation, audio editing, voice cloning, and export using their own a7w API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A stored API key may be sent to an unintended host if the service host is overridden.

Mitigation: Review the client before saving a real key; keep requests on api.a7w.cn and do not set A7W_HOST or --host unless the destination is trusted.

Risk: The client can call non-music a7w plugins and consume account credits.

Mitigation: Limit use to intended music endpoints and confirm costs before making paid calls.

Risk: Voice samples, lyrics, and reference audio may be shared with a third-party service without permission.

Mitigation: Upload only content for which the user has consent and appropriate rights.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/2253128/skills/sanjianke-music-generation-kit)
- [a7w API service](https://api.a7w.cn/)
- [Getting started and API key setup](references/getting-started.md)
- [Create music task API](references/api-create.md)
- [Voice cloning API](references/api-voice_clone.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with command examples and API response guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The external service may return generated media links and asynchronous task IDs.]

## Skill Version(s):

1.0.7 (source: ClawHub release; bundled SKILL.md lists 1.0.6)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
