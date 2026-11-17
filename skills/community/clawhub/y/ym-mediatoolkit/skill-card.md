## Description:

自然语言媒体助手 - 视频压缩、MP4/MOV 封面提取、音频转换、字幕识别。

This skill is ready for commercial/non-commercial use.

## Publisher:

[370299455cx-web](https://clawhub.ai/user/370299455cx-web)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to turn natural-language or JSON requests into media-processing tasks such as video compression, thumbnail extraction, audio conversion, subtitle recognition, batch processing, and asynchronous job polling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The unauthenticated local HTTP API can process local files and remote URLs.

Mitigation: Run it only in a trusted local environment and do not expose the HTTP server to a network.

Risk: Changing the bind host to 0.0.0.0 can make the service reachable beyond localhost.

Mitigation: Use authentication, restricted CORS, and a controlled reverse proxy before any non-local deployment.

Risk: Accepting media_roots from untrusted callers can expand local file access.

Mitigation: Do not accept media_roots from untrusted callers and restrict configured media roots to approved directories.

Risk: Media processing and model dependencies can consume significant compute, memory, disk, and network resources.

Mitigation: Use pinned dependencies, trusted media sources, quota controls, and resource limits before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/370299455cx-web/skills/ym-mediatoolkit)
- [Publisher profile](https://clawhub.ai/user/370299455cx-web)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance, shell commands, JSON responses, and generated media or caption files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can include stable status/code/reply/hint fields, media file paths, caption JSON, pipeline manifests, and asynchronous job metadata.]

## Skill Version(s):

4.2.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
