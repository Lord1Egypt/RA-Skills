## Description:

Generates WorkBuddy open-platform skill, connector, expert, expert team, and Buddy app asset bundles with field-level validation, packaging, and submission guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangjiaocheng](https://clawhub.ai/user/wangjiaocheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and platform builders use this skill to create WorkBuddy-compliant asset packages for skills, connectors, experts, expert teams, and Buddy apps. It is most useful when teams need structured templates, field-level specification checks, packaging steps, and submission guidance for ClawHub or WorkBuddy releases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled OAuth callback templates are not ready for production deployment as-is.

Mitigation: Before production use, add strict token-endpoint allowlisting, HTTPS enforcement, HTML escaping, session-bound one-time state, PKCE where supported, durable encrypted token storage, and a stable configured state secret.

Risk: Generated asset packages may include incomplete or unsafe implementation choices if accepted without review.

Mitigation: Treat generated assets as drafts, run an independent secret and security scan, and review the package before installation, submission, or deployment.

Risk: File writes, overwrites, or generated behavior with financial or account authority can have high impact.

Mitigation: Require explicit confirmation before file writes, overwrites, and any high-impact financial or account-authority behavior.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wangjiaocheng/skills/wb-open-builder)
- [WorkBuddy Open Platform Documentation](https://open.workbuddy.cn/docs)
- [Asset Generation Catalog](references/wb-open-builder-catalog.md)
- [Asset Requirements](references/wb-open-builder-requirements.md)
- [Asset Exemplars](references/wb-open-builder-exemplars.md)
- [Template Inventory](templates/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with generated files, JSON configuration templates, code templates, validation commands, and packaging guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated assets should be treated as drafts and reviewed before deployment.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
