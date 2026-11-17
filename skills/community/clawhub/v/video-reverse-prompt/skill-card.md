## Description:

Analyzes YouTube links, direct MP4 URLs, or local MP4 files with NanoPhoto.AI to produce reverse prompts, shot-by-shot breakdowns, and AI-ready visual descriptions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nanophotohq](https://clawhub.ai/user/nanophotohq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to turn authorized video inputs into structured shot analysis, reverse prompts, storyboard-style breakdowns, and AI-ready visual descriptions through the NanoPhoto.AI API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected videos, video URLs, and generated analysis are sent to NanoPhoto.AI for processing.

Mitigation: Use only content the user is authorized to upload or process, and avoid private, regulated, or third-party content unless authorization is clear.

Risk: Passing the NanoPhoto.AI API key directly as a command argument can expose it through shell history or process metadata.

Mitigation: Configure the credential with platform skill settings or the NANOPHOTO_API_KEY environment variable instead of passing it with --api-key.

## Reference(s):

- [Video Reverse Prompt API Reference](references/api.md)
- [NanoPhoto.AI](https://nanophoto.ai)
- [NanoPhoto.AI API Key Settings](https://nanophoto.ai/settings/apikeys)
- [ClawHub Skill Page](https://clawhub.ai/nanophotohq/skills/video-reverse-prompt)
- [ClawHub Publisher Profile](https://clawhub.ai/user/nanophotohq)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Streaming text response, typically Markdown with shot breakdowns and prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires NANOPHOTO_API_KEY and supports YouTube URLs, direct MP4 URLs, and local MP4 files up to 30 MB.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
