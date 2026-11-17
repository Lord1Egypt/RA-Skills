## Description:

小花专用自我迭代技能，基于 self-improving-agent 增强，集成 OpenClaw 工作流、MEMORY.md、百度千帆、看想做找四部曲，并面向国内部署优化。

This skill is ready for commercial/non-commercial use.

## Publisher:

[aroooooy](https://clawhub.ai/user/aroooooy)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to capture corrections, command failures, workflow lessons, and reusable knowledge into local learning and memory files for future sessions. It is especially oriented toward OpenClaw workflows and China-friendly tooling patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory and behavior files can influence future agent sessions.

Mitigation: Require explicit review before writing to MEMORY.md, SOUL.md, AGENTS.md, or TOOLS.md, and keep learning entries project-scoped unless intentionally promoted.

Risk: Broad hook activation can inject reminders into every prompt or bootstrap event.

Mitigation: Prefer project-local hooks and scoped matchers; avoid empty matchers unless every-prompt activation is intentional.

Risk: Cross-session transcript access or message forwarding can expose user or project context.

Mitigation: Do not allow cross-session transcript access or message forwarding without clear user consent.

Risk: Installing the wrong package or version can alter agent behavior unexpectedly.

Mitigation: Verify the exact package name, publisher handle, and version before installation.

## Reference(s):

- [Hook Setup Guide](artifact/references/hooks-setup.md)
- [OpenClaw Integration](artifact/references/openclaw-integration.md)
- [Entry Examples](artifact/references/examples.md)
- [OpenClaw Documentation](https://docs.openclaw.ai)
- [ClawHub Skill Page](https://clawhub.ai/aroooooy/skills/xiaohua-self-improving)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, configuration examples, hooks, and templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes optional hook scripts and local-file learning templates; output is intended for agent context and workspace documentation.]

## Skill Version(s):

1.0.0 (source: release evidence and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
