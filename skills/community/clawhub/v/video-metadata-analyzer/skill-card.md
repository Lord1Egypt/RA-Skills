## Description:

Video Metadata Intelligence System extracts video frames and audio, analyzes visual and transcript signals, and synthesizes structured Bilibili publishing metadata including title, intro, tags, category, cover suggestions, and content declarations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyberkurry](https://clawhub.ai/user/cyberkurry)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and publishing workflow agents use this skill to convert a local video into Bilibili-ready publishing metadata. It is useful when an agent needs frame observations, audio transcription, and a structured metadata package for downstream publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API modes can send video frames, audio, transcripts, and generated metadata to external endpoints, which may expose sensitive media content.

Mitigation: Use local or agent-direct modes for private videos; when API modes are required, use only trusted HTTPS endpoints and review provider retention policies.

Risk: API keys can be exposed through command history, logs, or copied chat content.

Mitigation: Prefer environment variables or a secret manager over command-line keys, and rotate any key that may have been exposed.

Risk: The server security verdict is suspicious because sensitive media and credentials require careful handling.

Mitigation: Review the skill and its configured endpoints before deployment, and restrict use to approved media and approved providers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cyberkurry/skills/video-metadata-analyzer)
- [Full Technical Reference](artifact/references/REFERENCE.md)
- [Project homepage declared by artifact](https://github.com/CyberKurry/video-metadata-analyzer)
- [SkillHub listing declared by artifact](https://skillhub.cn/skills/video-metadata-analyzer)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [JSON files and Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces observations_visual.json, observations_audio.json, optional metadata.json, and optional extracted frames/audio in agent-direct mode.]

## Skill Version(s):

1.2.0 (source: server release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
