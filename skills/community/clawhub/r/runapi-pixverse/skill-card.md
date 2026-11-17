## Description:

Create, edit, transition, and extend PixVerse V6 videos through RunAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runapi-ai](https://clawhub.ai/user/runapi-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide agents through PixVerse video generation, editing, transition, and extension tasks with RunAPI. It covers contract discovery, authenticated job submission, result waiting, media download verification, and SDK-oriented integration when building applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PixVerse requests use network access and may submit billable RunAPI jobs.

Mitigation: Authenticate first, review request JSON and paid generation parameters before submission, submit once, and require user authorization before any replacement paid request.

Risk: Prompts and media inputs selected by the user may be uploaded to RunAPI/PixVerse.

Mitigation: Review intended media files and request fields before submission, and use local file paths only for media that should be sent.

Risk: A completed task may still lack the requested media deliverables or return unexpected file types.

Mitigation: Download every requested media URL and verify each file is non-empty and matches the expected video MIME family before reporting completion.

Risk: Authentication can involve API keys or interactive browser login.

Mitigation: Prefer RUNAPI_API_KEY or saved CLI authentication, and ask the user before using browser login.

## Reference(s):

- [RunAPI PixVerse model overview, pricing, and rate limits](https://runapi.ai/models/pixverse.md)
- [RunAPI PixVerse homepage](https://runapi.ai/models/pixverse)
- [RunAPI PixVerse provider overview](https://runapi.ai/providers/pixverse.md)
- [RunAPI model catalog](https://runapi.ai/models.md)
- [RunAPI PixVerse SDK](https://github.com/runapi-ai/pixverse-sdk)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration, code]

**Output Format:** [Markdown guidance with shell commands, JSON request guidance, and optional SDK integration code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce task and result JSON handling guidance; generated video media is produced by RunAPI/PixVerse and verified by the agent workflow.]

## Skill Version(s):

0.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
