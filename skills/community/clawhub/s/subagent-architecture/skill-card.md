## Description:

Advanced patterns for specialized subagent orchestration with production-ready reference implementations. Security isolation, phased implementation, peer collaboration, and cost-aware spawning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[donovanpankratz-del](https://clawhub.ai/user/donovanpankratz-del)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to design, spawn, review, and score specialized subagents for security isolation, research synthesis, phased implementation, peer validation, and cost-aware orchestration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security verdict is suspicious because its security-isolation helper and orchestration guidance may overstate controls that the shipped code does not enforce.

Mitigation: Review and harden the JavaScript libraries before production use, and rely on runtime-enforced tool, filesystem, network, output-size, and cost limits for actual isolation.

Risk: Optional peer-review and external-agent workflows can involve Discord webhooks or peer endpoints when users configure them.

Mitigation: Keep these integrations opt-in, supply credentials manually, and sanitize review packages before sending data to external peers.

Risk: The artifact includes runnable JavaScript reference libraries and examples.

Mitigation: Treat the libraries as reference code, inspect them before copying into a workspace, and avoid executing examples against sensitive data without review.

Risk: The security evidence specifically calls out an optional failure-tracer hook as needing review before scoring sensitive outputs.

Mitigation: Review, disable, or remove the hook before using quality scoring with sensitive subagent output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/donovanpankratz-del/skills/subagent-architecture)
- [Main skill documentation](artifact/SKILL.md)
- [Security proxy pattern](artifact/templates/security-proxy.md)
- [Researcher specialist pattern](artifact/templates/researcher-specialist.md)
- [Phased implementation pattern](artifact/templates/phased-implementation.md)
- [Peer review specialist pattern](artifact/templates/peer-review-specialist.md)
- [Proxy recovery pattern](artifact/templates/proxy-recovery.md)
- [Release changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript reference code, shell command examples, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes optional JavaScript reference libraries and templates that are not auto-executed on install.]

## Skill Version(s):

2.3.5 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
