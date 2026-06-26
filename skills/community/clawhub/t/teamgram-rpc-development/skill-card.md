## Description: <br>
Complete guide for developing RPC services in Teamgram Server (v2.0.0). Use when creating new RPC methods, implementing business logic, or extending Teamgram functionality. Covers TL schema, DAO/Core/Server layers, error handling, performance optimization, security, testing, observability, and production best practices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhihang9978](https://clawhub.ai/user/zhihang9978) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill as reference material when creating or extending Teamgram RPC services across TL schema, Go service layers, data access, security, testing, observability, and production operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Production-style payment examples may be unsafe if copied directly into a real Teamgram service. <br>
Mitigation: Rewrite payment handling with verified provider callbacks, idempotency, and explicit error handling before applying it to production code. <br>
Risk: The tenant-isolation example may not provide robust isolation for real multi-tenant data. <br>
Mitigation: Replace it with scoped-query enforcement or database row-level security, and test isolation boundaries explicitly. <br>
Risk: Logging and audit examples may expose privacy or retention issues if adopted without review. <br>
Mitigation: Review log fields, audit retention, and access controls against the service's privacy and compliance requirements. <br>


## Reference(s): <br>
- [v1.1.0 - Error Handling and Logging](references/v1.1.0-error-handling.md) <br>
- [v1.2.0 - Performance and Caching](references/v1.2.0-performance.md) <br>
- [v1.3.0 - Security Best Practices](references/v1.3.0-security.md) <br>
- [v1.4.0 - Testing Strategy](references/v1.4.0-testing.md) <br>
- [v1.5.0 - Observability](references/v1.5.0-observability.md) <br>
- [v1.6.0 - Database Optimization](references/v1.6.0-database.md) <br>
- [v1.7.0 - Message Queue](references/v1.7.0-queue.md) <br>
- [v1.8.0 - Circuit Breaker and Rate Limiting](references/v1.8.0-circuit-breaker.md) <br>
- [v1.9.0 - Multi-Tenant](references/v1.9.0-multi-tenant.md) <br>
- [v2.0.0 - Final Summary](references/v2.0.0-final.md) <br>
- [TL Language Specification](https://core.telegram.org/mtproto/TL) <br>
- [gRPC Go Documentation](https://grpc.io/docs/languages/go/) <br>
- [Go Database Tutorial](https://golang.org/doc/tutorial/database-access) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline code and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only reference material; examples should be reviewed before use in production services.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
