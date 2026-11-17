## Description:

Helps agents run Xiaohongshu account operations, including account positioning, topic research, content drafting, publish preparation, comment handling, post-review, and reusable knowledge-base updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dongjie-oss](https://clawhub.ai/user/dongjie-oss)

### License/Terms of Use:

MIT-0

## Use Case:

External users, creators, and operators use this skill to guide Xiaohongshu account analysis, topic ideation, draft generation, publishing preparation, comment replies, and post-task review. It is especially oriented toward repeatable social-media operations that require platform-specific tone, browser workflow discipline, and local knowledge-base records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer may run remote installers and install global packages.

Mitigation: Review the installer before running it and avoid the one-click script unless the remote installers and packages are trusted.

Risk: Gateway tokens may be printed, shared, or left active in the local environment.

Mitigation: Rotate any exposed gateway token, confirm the gateway is bound locally, and verify the service can be removed.

Risk: Operational records may contain local account activity, drafts, comments, screenshots, or other sensitive work history.

Mitigation: Add real gitignore rules before using the knowledge base and keep records limited to reusable, non-sensitive summaries.

Risk: Publishing and reply workflows can affect a real Xiaohongshu account.

Mitigation: Use a dedicated account or profile when possible and require explicit user confirmation before any post or reply is sent.

## Reference(s):

- [Xiaohongshu Ops Skill on ClawHub](https://clawhub.ai/dongjie-oss/skills/xiaohongshu-ops-skill)
- [OpenClaw Browser Tool Documentation](https://docs.openclaw.ai/tools/browser)
- [XHS Account Analysis](references/xhs-account-analysis.md)
- [XHS Home Feed Analysis](references/xhs-home-feed-analysis.md)
- [XHS Topic Ideation](references/xhs-topic-ideation.md)
- [XHS Viral Copy Flow](references/xhs-viral-copy-flow.md)
- [XHS Publish Flows](references/xhs-publish-flows.md)
- [XHS Comment Ops](references/xhs-comment-ops.md)
- [XHS Runtime Rules](references/xhs-runtime-rules.md)
- [XHS Knowledge Base](references/xhs-knowledge-base.md)
- [XHS Eval Patterns](references/xhs-eval-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with structured templates, code snippets, shell commands, and optional local Markdown knowledge-base records.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can include Xiaohongshu titles, drafts, hashtags, reply text, account diagnostics, content-operation SOPs, publish checklists, browser-action guidance, and local review records.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
