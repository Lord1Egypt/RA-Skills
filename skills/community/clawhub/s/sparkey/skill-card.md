## Description:

Provides time-limited, self-revoking SSH access for AI agents using certificate TTL, user expiry, forced command restrictions, and scheduled automated cleanup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sanjeevneo](https://clawhub.ai/user/sanjeevneo)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use Sparkey to grant AI agents temporary, auditable SSH access for remote diagnostics or remediation while limiting session duration, command scope, and leftover access artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill provisions temporary SSH access and can perform root-level account, key, SSH configuration, timer, and log operations.

Mitigation: Install only on hosts where the operator authorizes root-level SSH access tooling, use dry-run or review steps before execution, and keep an independent recovery path available.

Risk: The CA private key is a persistent operator-side credential that can sign future session certificates if compromised.

Mitigation: Keep the CA private key on a secured operator host, restrict permissions, rotate it on a defined schedule, and consider an offline CA or HSM for high-security environments.

Risk: Broader command profiles increase access scope, and the full profile removes command restrictions.

Mitigation: Prefer the default diagnostic profile, escalate to remediation only when necessary, and avoid the full profile unless a human operator explicitly accepts unrestricted shell access.

Risk: Server security guidance identifies command-restriction and revocation weaknesses that need review before important use.

Mitigation: Review and fix the remediation dispatcher and revoke-access.sh --user validation before using the skill on important hosts, then run audit.sh to check for orphaned accounts, keys, support shells, cleanup scripts, and timers.

Risk: Authorized_keys-only mode relies on server-side expiry and local cleanup rather than CA-backed cryptographic certificate expiry.

Mitigation: Prefer CA-backed sessions when feasible, verify OpenSSH expiry support before using authorized_keys-only mode, and pair expiry-time with immutable authorized_keys and scheduled cleanup.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sanjeevneo/skills/sparkey)
- [Skill definition](SKILL.md)
- [README](README.md)
- [Agent Skills open standard](https://github.com/anthropics/skills/blob/main/spec/agent-skills-spec.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose root-level SSH access commands, temporary key and certificate workflows, cleanup commands, and audit steps.]

## Skill Version(s):

1.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
