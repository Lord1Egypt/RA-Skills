## Description:

Teamgram Server architecture guide for building Telegram-compatible backends, covering service decomposition, data flow, deployment patterns, and development workflows based on teamgram/teamgram-server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhihang9978](https://clawhub.ai/user/zhihang9978)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to understand Teamgram Server topology, MTProto service responsibilities, data flows, deployment options, and service development patterns before designing or self-hosting a Telegram-compatible backend.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Copyable deployment examples include weak placeholder credentials and exposed internal service ports.

Mitigation: Replace all example credentials, use Kubernetes Secrets or an external secrets manager, remove public mappings for internal services, and apply network access controls before deployment.

Risk: Deployment snippets are architecture notes rather than production-ready manifests.

Mitigation: Pin container images by version or digest, use least-privileged database accounts, configure encrypted backups to owned storage, and complete security review before production use.

## Reference(s):

- [Teamgram Server Repository](https://github.com/teamgram/teamgram-server)
- [Architecture DeepWiki](https://deepwiki.com/teamgram/teamgram-server)
- [Deployment Guide](artifact/references/deployment.md)
- [Service Development Guide](artifact/references/service-development.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with architecture notes, command examples, Go snippets, YAML snippets, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only output; deployment examples require review before production use.]

## Skill Version(s):

1.0.1 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
