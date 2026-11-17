## Description:

Generates video via the Loova Seedance 2.0 API from text prompts and optional image, video, or audio references, using LOOVA_API_KEY for authentication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hjianfeng](https://clawhub.ai/user/hjianfeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent to generate short videos from text prompts or supplied media references through Loova Seedance 2.0. The skill can configure duration, aspect ratio, model variant, function mode, URL references, and local media uploads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local paths passed with --files can upload any readable selected file to Loova's external API.

Mitigation: Run the skill in an isolated workspace, provide only intended media files, and require explicit user confirmation before any --files upload.

Risk: The skill requires an API key and sends generation requests to an external service.

Mitigation: Store LOOVA_API_KEY only in the environment or .env file, do not hardcode it, and avoid placing unrelated secrets or private documents in reachable paths.

Risk: Dependencies are specified with lower bounds and may resolve differently over time.

Mitigation: Pin Python dependencies when operating the skill in production or sensitive environments.

## Reference(s):

- [Loova Seedance 2.0 Video API Reference](artifact/reference.md)
- [Seedance 2.0 Video Generator Quick Start](artifact/QUICK_START.md)
- [Loova API Homepage](https://api.loova.ai/api)
- [ClawHub Skill Page](https://clawhub.ai/hjianfeng/skills/seedance-2-ai-video-generator)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with shell commands and final JSON returned by the video generation script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a Loova task result and video URL; generation can take up to 3 hours and requires LOOVA_API_KEY.]

## Skill Version(s):

1.0.13 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
