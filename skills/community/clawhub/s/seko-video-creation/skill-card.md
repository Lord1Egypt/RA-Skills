## Description:

All-in-one AI video creation that builds complete, consistent, production-ready long-form videos from simple text prompts using seko.sensetime.com.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sekoplatform](https://clawhub.ai/user/sekoplatform)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and developers use this skill to turn text prompts into video project plans and generated video assets through the Seko API. It supports planning, proposal updates, status polling, image downloads, and final video downloads for long-form videos, short plays, commercials, social media, education, and product demos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may ask the agent to store a real Seko API key in a local .env file, which can expose credentials if the workspace is shared, committed, or retained longer than intended.

Mitigation: Prefer setting SEKO_API_KEY only in the shell or a managed secret store; if a .env file is used, protect it from sharing or source control and delete it after use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sekoplatform/skills/seko-video-creation)
- [Seko API key page](https://seko.sensetime.com/explore)
- [Seko service endpoint](https://seko.sensetime.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls, files, guidance]

**Output Format:** [Markdown guidance with JSON API responses and generated media files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and SEKO_API_KEY; writes project plans, task queues, proposal JSON, proposal Markdown, downloaded images, and generated MP4 video files.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
