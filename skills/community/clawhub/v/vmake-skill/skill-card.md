## Description:

Process images and videos with Vmake AI for watermark removal and quality restoration, using the remote task catalog to select supported operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wemayiiii](https://clawhub.ai/user/wemayiiii)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use the skill to remove watermarks or restore image and video quality through Vmake AI. Successful processing consumes quota on the configured Vmake account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner flags undisclosed Feishu and Telegram delivery features and concerns about remote notices.

Mitigation: Review the bundled delivery options and server-provided notices before use, and enable only an intended delivery channel.

Risk: The scanner reports incomplete analysis and unpinned dependencies.

Mitigation: Review the source and dependency versions before installation, and pin dependencies in the deployment environment.

Risk: Submitting media for processing consumes quota on the configured Vmake account.

Mitigation: Obtain authorization for the media upload and quota use before submitting a task.

## Reference(s):

- [Vmake API Key Documentation](https://vmake.ai/developers#api-key)
- [Errors and Polling Guide](docs/errors-and-polling.md)
- [IM Attachments Guide](docs/im-attachments.md)
- [Multi-platform Delivery Guide](docs/multi-platform.md)

## Skill Output:

**Output Type(s):** [Text, JSON, URLs, Image and video files, Guidance]

**Output Format:** [JSON task status and result URLs, with processed image or video media delivered when configured]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Task execution consumes Vmake account quota; available tasks and outputs depend on the remote catalog and selected operation.]

## Skill Version(s):

2.0.3 (source: server-resolved release metadata, skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
