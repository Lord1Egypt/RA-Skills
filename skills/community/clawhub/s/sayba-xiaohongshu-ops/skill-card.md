## Description:

End-to-end Xiaohongshu operations including positioning, topic research, content production, publish execution, comment handling, viral-copy workflows, and post-incident recovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[saybanet](https://clawhub.ai/user/saybanet)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, operators, and agent users can use this skill to plan Xiaohongshu account positioning, generate post drafts, prepare publishing flows, manage comment replies, and recover from browser automation failures. It is especially suited to repeatable content operations where human confirmation is expected before publishing or replying.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup guidance includes a remote install script and non-interactive risk acceptance.

Mitigation: Review the setup before execution, prefer pinned and verified OpenClaw installation steps, and avoid piping remote scripts directly to a shell.

Risk: Gateway startup and terminal output may expose local tokens or account-control access.

Mitigation: Keep the gateway local and optional, avoid sharing terminal output that contains tokens, and rotate or clear device tokens when pairing state changes.

Risk: Publishing and replying workflows can act on a Xiaohongshu account.

Mitigation: Use a test account first, stop at publish-confirmation checkpoints, require human confirmation before publishing or replying, and keep default reply cadence to one send per turn.

Risk: Viral-copy workflows may create content too close to a source note.

Mitigation: Use structure-level or style-only adaptation, avoid reusing original text or images, and regenerate assets when the result is too similar.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/saybanet/skills/sayba-xiaohongshu-ops)
- [XHS Runtime Rules](references/xhs-runtime-rules.md)
- [XHS Publish Flows](references/xhs-publish-flows.md)
- [XHS Comment Ops](references/xhs-comment-ops.md)
- [XHS Viral Copy Flow](references/xhs-viral-copy-flow.md)
- [XHS Evaluate Patterns](references/xhs-eval-patterns.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with structured sections, short post copy, hashtags, image prompts, and occasional bash or JavaScript snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include account-positioning variables, content drafts, reply text, risk notes, browser-operation checkpoints, and publish-confirmation status.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
