## Description:

Complete guide for developing RPC services in Teamgram Server (v2.0.0). Use when creating new RPC methods, implementing business logic, or extending Teamgram functionality. Covers TL schema, DAO/Core/Server layers, error handling, performance optimization, security, testing, observability, and production best practices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhihang9978](https://clawhub.ai/user/zhihang9978)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create or extend Teamgram RPC services, from TL schema design through Go service layers, testing, observability, and production hardening.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Payment and authorization examples could be copied into production without complete trust and identity checks.

Mitigation: Require authenticated identity checks, verified payment callbacks, transaction handling, and idempotency before using those patterns.

Risk: Secret-loading and Vault examples could expose secrets or allow unsafe path handling if copied directly.

Mitigation: Validate secret endpoints and paths, block path traversal, and apply strict secret redaction.

Risk: Logging examples could disclose sensitive user, payment, token, or secret data.

Mitigation: Redact sensitive fields before logging and review log schemas before deployment.

## Reference(s):

- [v1.1.0 - Error Handling and Logging](references/v1.1.0-error-handling.md)
- [v1.2.0 - Performance and Caching](references/v1.2.0-performance.md)
- [v1.3.0 - Security Best Practices](references/v1.3.0-security.md)
- [v1.4.0 - Testing Strategy](references/v1.4.0-testing.md)
- [v1.5.0 - Observability](references/v1.5.0-observability.md)
- [v1.6.0 - Database Optimization](references/v1.6.0-database.md)
- [v1.7.0 - Message Queue](references/v1.7.0-queue.md)
- [v1.8.0 - Circuit Breaker and Rate Limiting](references/v1.8.0-circuit-breaker.md)
- [v1.9.0 - Multi-Tenant Design](references/v1.9.0-multi-tenant.md)
- [v2.0.0 - Final Summary](references/v2.0.0-final.md)
- [TL Language Spec](https://core.telegram.org/mtproto/TL)
- [gRPC Go Documentation](https://grpc.io/docs/languages/go/)
- [Go Database/SQL Tutorial](https://golang.org/doc/tutorial/database-access)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with code blocks and command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance; examples require review before production use.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
