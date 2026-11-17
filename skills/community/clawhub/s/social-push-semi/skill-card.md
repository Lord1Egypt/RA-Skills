## Description:

Prepares semi-automated Xiaohongshu publishing packages by generating captions, extracting or generating cover media, and stopping for human confirmation before final publish.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yugulugulu](https://clawhub.ai/user/yugulugulu)

### License/Terms of Use:


## Use Case:

Content creators, operators, and developers use this skill to prepare Xiaohongshu posts from videos, topics, keywords, or generated images. It creates reusable publishing assets and can prefill a draft page while retaining manual review before publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled vendor tools can automate actions on an authenticated Xiaohongshu account and may read account data.

Mitigation: Use only an account you are comfortable automating, keep final publish manual, and review generated title, content, tags, and media before submission.

Risk: Configurable network options can send API keys or media requests to unexpected destinations.

Mitigation: Use trusted --base-url and --api-key-env values only, and avoid untrusted media URLs.

Risk: The Chrome profile used for CDP automation stores an authenticated session.

Mitigation: Treat the profile as sensitive session storage and avoid sharing or reusing it outside the intended workflow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yugulugulu/skills/social-push-semi)
- [Xiaohongshu Creator Publish Page](https://creator.xiaohongshu.com/publish/publish)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Markdown drafts, JSON publish package, checklist Markdown, generated or extracted media files, and shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local workspace paths; CDP Chrome is required for draft prefill, ffmpeg is used when available for video cover extraction, and DOUBAO_API_KEY is required for Doubao image generation.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
