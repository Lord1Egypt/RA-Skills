## Description:

Helps agents generate and edit video with Kling through RunAPI, using the CLI for one-off requests and SDKs for application integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runapi-ai](https://clawhub.ai/user/runapi-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and developers use this skill to generate or edit Kling videos through RunAPI, or integrate Kling video generation into applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API credentials could be exposed in project files.

Mitigation: Keep RunAPI keys in environment variables or approved CLI authentication, not project files.

Risk: Generation requests may incur charges and upload user-provided media.

Mitigation: Review request contents and pricing before submitting a paid task or uploading media.

Risk: Generated video downloads could be incomplete or have an unexpected file type.

Mitigation: Verify each requested download is non-empty and matches its expected MIME type before reporting completion.

Risk: Installing an unreviewed CLI may introduce third-party software risk.

Mitigation: Review the RunAPI CLI install source before installation.

## Reference(s):

- [RunAPI Kling model overview](https://runapi.ai/models/kling.md)
- [RunAPI Kling homepage](https://runapi.ai/models/kling)
- [Kuaishou provider overview](https://runapi.ai/providers/kuaishou.md)
- [RunAPI model catalog](https://runapi.ai/models.md)
- [Kling SDK integration](https://github.com/runapi-ai/kling-sdk)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Video files]

**Output Format:** [Markdown guidance, JSON task results, and downloaded video files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Checks requested video deliverables for non-empty content and expected MIME type.]

## Skill Version(s):

0.4.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
