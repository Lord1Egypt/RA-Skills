## Description:

Helps agents manage credentials and access for named external services using least privilege, secret redaction, connection verification, rate-limit awareness, and destructive-action guards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pmuhammadagus-byte](https://clawhub.ai/user/pmuhammadagus-byte)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill when an agent must set up, rotate, or verify credentials for a specific external service such as Vercel, Supabase, GitHub, cloud providers, databases, or collaboration tools. It is intended to help the agent request only necessary credentials, store them securely, verify access, and avoid leaking secrets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill guides an agent through handling credentials for external services.

Mitigation: Use OAuth or narrowly scoped tokens where possible, limit permissions to the specific project or repository, and avoid plaintext storage or chat-history retention.

Risk: Secrets could be exposed through output, logs, repository files, or ordinary memory.

Mitigation: Redact credential values, use a real secret store or protected environment variables, and scan planned outputs and commits for secrets before proceeding.

Risk: An agent could apply credentials to the wrong service, account, project, or destructive action.

Mitigation: Verify the service, capability, account, project, permission scope, and target before execution, and require approval for high-risk destructive operations.

Risk: Credential failures, service outages, and rate limits could be misdiagnosed as a need for new credentials.

Mitigation: Classify errors first, respect Retry-After and backoff behavior for rate limits, check service health, and request reauthentication only when authentication or permission checks fail.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/pmuhammadagus-byte/skills/universal-service-access)
- [Artifact README](artifact/README.md)
- [Artifact Skill Instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with redacted secrets and optional command or configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Credential values should be redacted, scoped to the requested service, and verified before success is reported.]

## Skill Version(s):

1.1.1 (source: evidence release, artifact frontmatter, artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
