## Description:

Generate lip-sync video with Volcengine Lip Sync through RunAPI. Use when the user asks an agent to sync mouth movement in a source video to an audio track. Default to the RunAPI CLI for one-off generation; use SDKs only when integrating RunAPI into an app or backend.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runapi-ai](https://clawhub.ai/user/runapi-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to generate lip-sync video by synchronizing mouth movement in a source video to a supplied audio track through RunAPI. The skill supports one-off CLI generation and SDK-based integration for applications, backends, workers, libraries, and webhook pipelines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and relies on an unpinned third-party RunAPI CLI from a Homebrew tap.

Mitigation: Install only when the RunAPI tap and CLI are trusted, and review the installed CLI before using it in sensitive environments.

Risk: The workflow uses RunAPI authentication and uploads source video and audio media to the provider service.

Mitigation: Use appropriate RunAPI credentials and avoid submitting media unless the user is authorized to send it to the service.

Risk: A paid or asynchronous generation request may create a task before result verification is complete.

Mitigation: Submit exactly once, persist the task response, wait on the same task, and do not resubmit after service failure without user authorization.

## Reference(s):

- [Volcengine Lip Sync model overview](https://runapi.ai/models/volcengine-lip-sync.md)
- [Volcengine Lip Sync product page](https://runapi.ai/models/volcengine-lip-sync)
- [ByteDance provider overview](https://runapi.ai/providers/bytedance.md)
- [RunAPI model catalog](https://runapi.ai/models.md)
- [Volcengine Lip Sync SDK integration](https://github.com/runapi-ai/volcengine-lip-sync-sdk)
- [RunAPI publisher profile](https://clawhub.ai/user/runapi-ai)
- [ClawHub skill page](https://clawhub.ai/runapi-ai/skills/runapi-volcengine-lip-sync)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Code]

**Output Format:** [Markdown guidance with shell commands, JSON request and response handling, and SDK integration direction]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent instructions for discovering the current RunAPI contract, submitting one task, waiting for results, downloading video deliverables, and verifying MIME types.]

## Skill Version(s):

0.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
