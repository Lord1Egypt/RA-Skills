## Description:

将操作视频自动转换为图文并茂的 Word 操作指南文档，支持智能截图、语音转录、LLM 内容提炼和流程图生成。

This skill is ready for commercial/non-commercial use.

## Publisher:

[siyou315](https://clawhub.ai/user/siyou315)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operations teams, and content authors use this skill to turn software operation, system demonstration, training, or product walkthrough videos into illustrated Word procedure guides with screenshots, transcripts, refined steps, and a flow overview.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Normal use can send XIAPING_TOKEN to a third-party licensing endpoint.

Mitigation: Use environment variables instead of command-line API keys, review the endpoint under your policy, and avoid shared or sensitive tokens.

Risk: Dependency installation can install unpinned packages automatically.

Mitigation: Review and pin dependencies, then install them manually in an isolated environment.

Risk: Video-derived audio, screenshots, or transcripts may be processed externally depending on the configured path.

Mitigation: Avoid confidential videos unless the external services and mirror are acceptable under your policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/siyou315/skills/video-to-doc)
- [视频转文档操作指南](references/guide.md)

## Skill Output:

**Output Type(s):** [Files, Text, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell commands; generated artifacts include DOCX, JSON, audio, and image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local screenshots, audio transcripts, frame-analysis JSON, and Word documents from the supplied video.]

## Skill Version(s):

1.0.0 (source: evidence release, SKILL.md frontmatter, skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
