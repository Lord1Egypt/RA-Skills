## Description:

Complete ZEDEDA edge management API client for 473 endpoints across edge node, application, cluster, storage, network, Kubernetes, diagnostics, and user management domains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krisclarkdev](https://clawhub.ai/user/krisclarkdev)

### License/Terms of Use:

MIT

## Use Case:

Developers and infrastructure operators use this skill to inspect and manage ZEDEDA edge infrastructure, applications, Kubernetes resources, storage, networks, diagnostics, jobs, and users through an agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A ZEDEDA token used with this skill can read and change edge infrastructure.

Mitigation: Install only when the publisher and intended operations are trusted, and use the least-privileged ZEDEDA token possible.

Risk: A custom ZEDEDA_BASE_URL can send the token and request payloads to a non-default endpoint.

Mitigation: Leave ZEDEDA_BASE_URL unset unless it points to a trusted HTTPS ZEDEDA endpoint.

Risk: Session-token lookup methods and routine URL logging may expose sensitive values.

Mitigation: Avoid session-token lookup methods until logging redaction is fixed, and set ZEDEDA_LOG_LEVEL to WARNING or ERROR for normal use.

## Reference(s):

- [ClawHub ZEDEDA skill page](https://clawhub.ai/krisclarkdev/skills/zededa)
- [ZEDEDA API endpoint](https://zedcontrol.zededa.net/api)
- [Keybase author verification](https://keybase.io/krisclarkdev)

## Skill Output:

**Output Type(s):** [text, json, code, shell commands, configuration, guidance]

**Output Format:** [JSON API responses and Markdown guidance with inline shell or Python snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ZEDEDA_API_TOKEN; supports optional ZEDEDA_BASE_URL and ZEDEDA_LOG_LEVEL settings.]

## Skill Version(s):

1.0.6 (source: server release metadata; artifact frontmatter version is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
