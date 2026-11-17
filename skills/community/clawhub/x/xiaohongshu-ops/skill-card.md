## Description:

小红书相关操作，覆盖账号定位、选题研究、内容生产、发布执行与复盘修复的小红书全链路运营技能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiangyu-cas](https://clawhub.ai/user/xiangyu-cas)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, social media operators, and agent users use this skill to plan, draft, browse, publish-prep, reply to comments, and review Xiaohongshu operations through OpenClaw browser workflows. It supports reusable SOPs for account analysis, home-feed analysis, topic ideation, viral-copy drafting, publishing handoff, comment handling, and local knowledge-base capture.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide public Xiaohongshu posts and comment replies, where inaccurate, misleading, or poorly timed content could create reputational risk.

Mitigation: Review generated posts and replies before publication, use the skill's publish-before-confirmation stop point, and keep one-send-per-turn supervision for replies.

Risk: Browser workflows and local knowledge-base notes may expose or retain sensitive account context.

Mitigation: Use the OpenClaw browser profile intentionally, keep sensitive account details out of persistent notes when possible, and stop automation when account or browser state is uncertain.

Risk: Viral-copy workflows can overfit source content or assets and create copyright, plagiarism, or platform-policy issues.

Mitigation: Prefer style-only adaptation, avoid reusing source text or images, and review generated content for claims, privacy, and infringement risk.

Risk: Optional third-party skills or tools used for image generation may add unreviewed dependencies.

Mitigation: Verify any optional third-party skill, such as nano-banana-pro, before installing or using it in the workflow.

## Reference(s):

- [XHS runtime rules](references/xhs-runtime-rules.md)
- [XHS account analysis](references/xhs-account-analysis.md)
- [XHS home feed analysis](references/xhs-home-feed-analysis.md)
- [XHS topic ideation](references/xhs-topic-ideation.md)
- [XHS publish flows](references/xhs-publish-flows.md)
- [XHS comment ops](references/xhs-comment-ops.md)
- [XHS viral copy flow](references/xhs-viral-copy-flow.md)
- [XHS knowledge base](references/xhs-knowledge-base.md)
- [OpenClaw browser documentation](https://docs.openclaw.ai/tools/browser)
- [Xiaohongshu website](https://www.xiaohongshu.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown text with structured SOPs, analysis summaries, draft post copy, reply text, browser-action guidance, and local knowledge-base records.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include publish-ready drafts, comment replies, topic lists, risk notes, and knowledge-base markdown entries; public posting and replies should remain supervised.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
