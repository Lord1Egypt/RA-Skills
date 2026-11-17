## Description:

Fixes two critical @tencent-weixin/openclaw-weixin@2.4.1 issues on OpenClaw 2026.5.4+: a waitForWeixinRuntime timeout caused by runtime module isolation and rejected manual Content-Length headers in undici 8.2.0.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnsonxuan](https://clawhub.ai/user/johnsonxuan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators maintaining OpenClaw Weixin integrations use this skill to patch a local @tencent-weixin/openclaw-weixin@2.4.1 installation so Weixin channels can start, receive messages, send replies, and upload files on OpenClaw 2026.5.4+.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer persistently edits an installed OpenClaw Weixin messaging plugin.

Mitigation: Review install.sh before execution, keep separate copies of original plugin files, and run it only against the stated @tencent-weixin/openclaw-weixin@2.4.1 target.

Risk: Validation and rollback safeguards are limited for local plugin patching.

Mitigation: Verify the patched plugin manually after installation and use the generated .bak files or a clean plugin reinstall to recover if behavior is unexpected.

## Reference(s):

- [OpenClaw Issue 78376](https://github.com/openclaw/openclaw/issues/78376)
- [OpenClaw Weixin Fix Report](https://github.com/user-attachments/files/27447892/openclaw-weixin-fix-report.md)
- [@tencent-weixin/openclaw-weixin npm Package](https://www.npmjs.com/package/@tencent-weixin/openclaw-weixin)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown with shell commands and patch guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local plugin patch instructions and an installer script that edits installed OpenClaw Weixin plugin files.]

## Skill Version(s):

2.4.2 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
