## Description:

Self-reflection, self-criticism, self-learning, and self-organizing memory help an agent evaluate its work, catch mistakes, and carry correction patterns forward across sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mifashion](https://clawhub.ai/user/mifashion)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add local correction tracking, self-reflection, and reusable preference memory to an agent workflow. It is most relevant when agents should learn from explicit feedback, failed operations, repeated lessons, and workspace-specific behavior patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent free-form memory can influence future agent behavior in ways the user may not expect.

Mitigation: Review and approve what the skill writes to memory and workspace steering files, and use the documented audit, export, and forget flows to keep stored context visible.

Risk: User corrections or workspace notes may accidentally include sensitive, third-party, access, financial, medical, or location information.

Mitigation: Follow the security boundary guidance: avoid storing sensitive or third-party data, keep entries source-tagged, and remove stored items when requested.

Risk: The optional companion install can add additional behavior beyond the core memory skill.

Mitigation: Do not enable the companion install unless the user explicitly agrees and the source and version can be verified.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mifashion/skills/self-dyxc)
- [Declared homepage](https://www.sztv.com.cn/ysz/zx/zw/80706997.shtml)
- [Skill definition](artifact/SKILL.md)
- [Setup guide](artifact/setup.md)
- [Security boundaries](artifact/boundaries.md)
- [Learning mechanics](artifact/learning.md)
- [Memory operations](artifact/operations.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command snippets and configuration templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates local memory files under ~/self-improving/ and may propose workspace steering edits.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 1.2.16)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
