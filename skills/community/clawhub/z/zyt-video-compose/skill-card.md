## Description:

Use Chanjing video synthesis APIs to create digital human videos from text or audio, with optional background upload, task polling, and explicit download when the user asks to save the result locally.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zuoyuting214](https://clawhub.ai/user/zuoyuting214)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and developers use this skill to create Chanjing digital human videos from text or uploaded audio, select public or customized digital human figures, poll generation tasks, and optionally download completed videos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Chanjing API secrets and cached access tokens are stored in local plaintext credential files.

Mitigation: Use owner-only permissions for ~/.chanjing/credentials.json or the configured credentials path, and prefer a dedicated low-privilege API key.

Risk: Local audio and background files may be uploaded to Chanjing for video processing.

Mitigation: Confirm user intent and data sensitivity before uploading local files, especially on shared or regulated systems.

## Reference(s):

- [Chanjing Open API](https://open-api.chanjing.cc)
- [Skill reference](artifact/reference.md)
- [Skill examples](artifact/examples.md)
- [ClawHub skill page](https://clawhub.ai/zuoyuting214/skills/zyt-video-compose)
- [Publisher profile](https://clawhub.ai/user/zuoyuting214)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text]

**Output Format:** [Markdown guidance with shell command snippets and API identifiers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce video task IDs, upload file IDs, video URLs, and local file paths when downloads are explicitly requested.]

## Skill Version(s):

0.4.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
