## Description:

End-to-end Xiaohongshu operations including positioning, topic research, content production, publish execution, and post-incident recovery. Reusable across verticals with templates and a concrete 陪你看剧 case preset.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mjscjj](https://clawhub.ai/user/mjscjj)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, agencies, and social media operators use this skill to plan Xiaohongshu topics, draft platform-native posts, prepare publishing workflows, review comments, and generate reply guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled OpenClaw setup guide includes broad installer and gateway-administration steps that can expose credentials or persistent access.

Mitigation: Review setup commands before use, avoid blindly pasting curl-to-bash installers, do not print or share gateway tokens, and verify device identities before approving them.

Risk: Persistent browser and gateway access may be inappropriate for some Xiaohongshu accounts.

Mitigation: Use a dedicated account or environment when possible, confirm whether persistent access is acceptable, and monitor approved devices and gateway status.

Risk: Automated publishing or replies can create unintended public content or platform-rate issues.

Mitigation: Keep the documented publish-before-confirmation checkpoint, require user confirmation before replies, send one reply per turn by default, and stop when platform warnings or send failures appear.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mjscjj/skills/xiaohongshu-ops-lobster)
- [XHS Runtime Rules](references/xhs-runtime-rules.md)
- [XHS Publish Flows](references/xhs-publish-flows.md)
- [XHS Comment Ops](references/xhs-comment-ops.md)
- [XHS Viral Copy Flow](references/xhs-viral-copy-flow.md)
- [XHS Evaluation Patterns](references/xhs-eval-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with structured lists, draft copy, prompts, and inline code or shell blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include browser-operation steps, account-positioning templates, post drafts, comment replies, image prompts, and publish-confirmation checkpoints.]

## Skill Version(s):

1.0.0 (source: server release metadata and PUBLISH.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
