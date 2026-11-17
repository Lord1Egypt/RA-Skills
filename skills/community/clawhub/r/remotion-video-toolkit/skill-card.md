## Description:

Complete toolkit for programmatic video creation with Remotion and React, covering animations, timing, rendering, captions, 3D, charts, text effects, transitions, and media handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shreefentsar](https://clawhub.ai/user/shreefentsar)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to write Remotion code, build video generation pipelines, and create data-driven templates for personalized videos, social media clips, dynamic ads, captions, visualizations, and server-side rendering workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public rendering endpoints can allow unauthorized video rendering and unexpected compute or cloud cost.

Mitigation: Add authentication, authorization, render quotas, concurrency limits, timeouts, and cost monitoring before exposing a rendering API.

Risk: URL-fetch and remote media examples can expose internal-network access or oversized request risks when copied into production services.

Mitigation: Use URL allowlists, restricted egress, request and output size limits, and explicit input schemas for all user-provided media or data URLs.

Risk: Scaffolding and package installation examples may be unsafe in sensitive environments without dependency controls.

Mitigation: Pin package versions, use lockfiles, and avoid running scaffolding commands in sensitive environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shreefentsar/skills/remotion-video-toolkit)
- [Remotion Tailwind documentation](https://www.remotion.dev/docs/tailwind)
- [Remotion Whisper.cpp documentation](https://remotion.dev/docs/install-whisper-cpp)
- [Remotion Whisper Web documentation](https://remotion.dev/docs/whisper-web)
- [Remotion OpenAI Whisper captions documentation](https://remotion.dev/docs/openai-whisper/openai-whisper-api-to-captions)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with TypeScript, TSX, JSON, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Remotion implementation guidance, reusable snippets, rendering commands, deployment patterns, and media handling recommendations.]

## Skill Version(s):

1.4.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
