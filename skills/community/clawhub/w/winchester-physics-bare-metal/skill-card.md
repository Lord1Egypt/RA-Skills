## Description:

Configures a local, unsandboxed LLM setup optimized for Ryzen 9 5900XT and Radeon RX 6600XT workstations for theoretical physics research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zedwiater](https://clawhub.ai/user/zedwiater)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and researchers with high-RAM local workstations use this skill to configure a Gemma-based agent environment tuned for theoretical physics exploration and balanced CPU/GPU use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release enables a broadly capable unsandboxed local agent with elevated access.

Mitigation: Use only in an isolated trusted environment, review allowed tools before use, and disable elevation by default unless explicitly required.

Risk: Discord access is broad enough to expose the agent outside the intended operator scope.

Mitigation: Restrict Discord access to explicit trusted IDs and disable wildcard access, name matching, bot access, and Discord configuration writes unless needed.

Risk: Conversation-derived memory, shell environment inheritance, and unredacted logging may retain or expose sensitive information.

Mitigation: Scope or disable memory, disable shell environment inheritance, and enable sensitive-data redaction before using the configuration with private data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zedwiater/skills/winchester-physics-bare-metal)
- [Publisher Profile](https://clawhub.ai/user/zedwiater)
- [Release Skill Definition](artifact/SKILL.md)
- [Release Configuration](artifact/config.json)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with configuration references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
