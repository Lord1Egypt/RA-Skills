## Description:

Downloads video, audio, and music-card media from WeChat Official Account articles, using a user-verified visible Chrome session when WeChat blocks direct fetching.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ewanwu](https://clawhub.ai/user/ewanwu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to save media from WeChat Official Account articles they are authorized to access, especially when direct downloads are blocked by WeChat verification and a verified Chrome session is needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill attaches to a visible Chrome session that may be verified or logged in.

Mitigation: Use a dedicated browser profile for the task and close it when capture is complete.

Risk: The workflow saves page-derived URLs, text, HTML, JSON, and downloaded media locally.

Mitigation: Keep output in a private directory and review or delete temporary capture artifacts after use.

Risk: Untrusted direct media URLs may cause unwanted downloads or unexpected content retrieval.

Mitigation: Use only article and media URLs from sources you trust and are authorized to access.

## Reference(s):

- [WeChat Media Downloader README](references/github-readme-zh.md)
- [Reusable WeChat Media Workflow](references/reusable-workflow.md)
- [ClawHub Skill Page](https://clawhub.ai/ewanwu/skills/wechat-media-downloader-weixin)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated local media files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce downloaded media files, temporary HTML, text, JSON capture artifacts, and a download manifest in local directories.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
