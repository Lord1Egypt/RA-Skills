## Description:

Creates Xiaohongshu note content, render-ready Markdown, themed image cards, and optional Xiaohongshu publishing commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[limoxt](https://clawhub.ai/user/limoxt)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, marketers, and agents use this skill to draft Xiaohongshu-style notes, turn note material into 1080x1440 image cards across multiple themes and pagination modes, and optionally publish the result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional publishing requires access to a Xiaohongshu session cookie.

Mitigation: Keep the cookie in a local .env file, do not commit or share it, and prefer a dedicated account.

Risk: Publishing can affect a live social account.

Mitigation: Use dry-run and private posting first; only publish publicly after reviewing generated content and images.

Risk: API publishing mode can send content and credentials to a service endpoint.

Mitigation: Avoid API mode unless the API service is your own trusted local service.

Risk: Rendering Markdown from untrusted sources may expose the local rendering environment to unsafe content.

Mitigation: Render only trusted Markdown or use sandboxing and sanitization for untrusted input.

## Reference(s):

- [XHS Image Gen ClawHub Skill Page](https://clawhub.ai/limoxt/skills/xhs-image-gen)
- [Parameter Reference](artifact/references/params.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown, shell commands, configuration snippets, and PNG image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional publishing requires a Xiaohongshu session cookie; generated cards default to 1080x1440 PNG output.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
