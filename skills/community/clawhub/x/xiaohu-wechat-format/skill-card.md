## Description:

Formats Markdown or rough notes into WeChat Official Account compatible inline-style HTML with theme previews, image handling, optional cover generation, and draft publishing workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lingmafuture](https://clawhub.ai/user/lingmafuture)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and developers use this skill to convert articles into WeChat-ready HTML, compare themes, prepare images and covers, and optionally publish drafts or manage comment replies after explicit confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses WeChat credentials and may call external WeChat and AI APIs.

Mitigation: Keep config.json, tokens, and API keys private; use preview or dry-run modes before granting external access.

Risk: Draft publishing, permanent media upload, and comment auto-reply can create live external writes.

Mitigation: Require explicit user confirmation before running publishing or reply workflows, and review the target article, cover, and reply scope first.

Risk: Automated comment replies can process reader comments through external AI services and post public responses.

Mitigation: Use comment_reply.py only after reviewing the scope; prefer dry-run first and avoid high-risk advice in generated replies.

Risk: Imported Markdown, HTML, and external image URLs may be untrusted or incompatible with WeChat upload requirements.

Mitigation: Avoid untrusted sources, preview generated output locally, and use Pillow-backed image normalization for WebP or unsupported image formats before upload.

Risk: Republishing imported WeChat articles can create rights or attribution issues.

Mitigation: Treat imported articles as drafts or previews unless the user confirms they have rights to publish.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lingmafuture/skills/xiaohu-wechat-format)
- [Publisher profile](https://clawhub.ai/user/lingmafuture)
- [WeChat API access token endpoint](https://api.weixin.qq.com/cgi-bin/token)
- [OpenRouter API base](https://openrouter.ai/api/v1)

## Skill Output:

**Output Type(s):** [Markdown, HTML, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands plus generated HTML previews, gallery pages, cover image files, and optional WeChat draft uploads.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [External writes and automated replies require explicit user confirmation; draft publishing requires WeChat credentials and IP whitelist configuration.]

## Skill Version(s):

1.0.0 (source: release evidence and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
