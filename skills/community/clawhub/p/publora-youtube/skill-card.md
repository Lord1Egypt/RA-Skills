## Description:

Upload and publish video content to YouTube using the Publora API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sergebulaev](https://clawhub.ai/user/sergebulaev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and publishing teams use this skill to prepare Publora API requests for uploading or scheduling YouTube videos with channel, privacy, metadata, and media upload settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Publora API key can authorize publishing actions if exposed or reused outside the intended workflow.

Mitigation: Keep the key out of prompts, logs, and committed source, and inject it only through an approved secret or environment mechanism when executing generated code.

Risk: Generated API requests can publish or schedule video content to the wrong YouTube channel, privacy setting, time, or media file.

Mitigation: Review the channel ID, privacy setting, scheduled time, title, description, and video file before running any upload or scheduling request.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sergebulaev/skills/publora-youtube)
- [Publora API base URL](https://api.publora.com/api/v1)
- [Publora create-post endpoint](https://api.publora.com/api/v1/create-post)
- [Publora get-upload-url endpoint](https://api.publora.com/api/v1/get-upload-url)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript and Python API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Publora API request guidance for YouTube video upload and scheduling workflows.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
