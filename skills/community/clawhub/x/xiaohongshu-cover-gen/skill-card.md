## Description:

Generates Xiaohongshu and RedNote cover images and content cards through a structured workflow for visual research, concepting, prompt writing, Lovart generation, and final review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[velmavalienteqejimu22-jpg](https://clawhub.ai/user/velmavalienteqejimu22-jpg)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content creators, marketers, and agent operators use this skill to turn Xiaohongshu or RedNote post copy, brand preferences, and optional source material into cover concepts, image-generation prompts, generated images, and text cards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can require Lovart login cookies, giving an agent access to a Lovart session.

Mitigation: Use a dedicated low-value Lovart account, keep cookies outside the project and source control, and refresh or revoke them when no longer needed.

Risk: The included image downloader disables TLS certificate verification for Lovart image downloads.

Mitigation: Avoid the TLS-disabled downloader when possible, replace it with a reviewed download path, and inspect shell scripts before execution.

Risk: Generated images, prompts, and visual concepts may be misleading, low quality, or poorly matched to the source post.

Mitigation: Review concepts, prompts, and generated images against the provided checklist before publication.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/velmavalienteqejimu22-jpg/skills/xiaohongshu-cover-gen)
- [Lovart Operation Guide](references/lovart-operation.md)
- [Prompt Checklist](references/prompt-checklist.md)
- [Research Platforms Guide](references/research-platforms.md)
- [Aesthetic Guide](references/aesthetic-guide.md)
- [Design Tokens Template](templates/design-tokens.md)
- [Iteration Log Template](templates/iteration-log.md)
- [Lovart](https://lovart.ai)
- [Dribbble](https://dribbble.com)
- [Xiaohongshu](https://xiaohongshu.com)
- [Pinterest](https://pinterest.com)
- [Pillow Documentation](https://pillow.readthedocs.io)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance, image-generation prompts, shell commands, Python/Pillow configuration, and generated PNG image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require Lovart session cookies for image generation and may produce 1080x1440 PNG text cards through the bundled Pillow script.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
