## Description:

Detect prompt injection, jailbreak, role-hijack, and system extraction attempts using layered pattern, semantic, evasion, and penalty scoring defenses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[georges91560](https://clawhub.ai/user/georges91560)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill as a security gate for autonomous agents to screen user inputs and tool outputs for prompt injection, jailbreak, system extraction, and credential exfiltration attempts before normal agent execution proceeds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is intended to serve as a high-trust security gateway and can affect agent-wide input, tool-output, and blocking behavior.

Mitigation: Install only after review, prefer a pinned ClawHub package or reviewed commit, and enforce blocking through host-managed policy.

Risk: The optional install script performs mutable remote installation and may attempt Python dependency installation with --break-system-packages.

Mitigation: Prefer ClawHub or manual installation from reviewed files, review install.sh before use, and avoid --break-system-packages in managed environments.

Risk: Persistent audit logging and optional external alerts may expose sensitive event metadata if configured too broadly.

Mitigation: Disable raw prompt logging and external alerts unless explicitly needed, set retention for audit logs, and restrict alert destinations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/georges91560/skills/security-sentinel-skill)
- [Publisher Profile](https://clawhub.ai/user/georges91560)
- [Security Policy and Transparency](artifact/SECURITY.md)
- [Configuration Guide](artifact/CONFIGURATION.md)
- [Blacklist Patterns](artifact/blacklist-patterns.md)
- [Semantic Scoring](artifact/semantic-scoring.md)
- [Multilingual Evasion](artifact/multilingual-evasion.md)
- [Advanced Threats 2026](artifact/advanced-threats-2026.md)
- [Memory Persistence Attacks](artifact/memory-persistence-attacks.md)
- [Credential Exfiltration Defense](artifact/credential-exfiltration-defense.md)
- [Advanced Jailbreak Techniques](artifact/advanced-jailbreak-techniques.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON-like security decision objects, Python and shell snippets, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce BLOCKED or ALLOWED decisions, audit log guidance, alert guidance, threshold configuration, and detection pattern updates.]

## Skill Version(s):

2.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
