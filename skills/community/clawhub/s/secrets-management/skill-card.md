## Description:

Securely store, manage, rotate, and integrate secrets such as API keys, passwords, and certificates in CI/CD pipelines using Vault, AWS Secrets Manager, and native platform tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brandonwise](https://clawhub.ai/user/brandonwise)

### License/Terms of Use:


## Use Case:

Developers, DevOps engineers, and platform teams use this skill to choose and apply secrets-management patterns for CI/CD pipelines, Kubernetes deployments, cloud secret stores, secret rotation, and secret scanning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Copyable examples include local-only placeholders such as a Vault dev server, root token, and literal passwords.

Mitigation: Treat these as local placeholders only and replace them with hardened, environment-specific credentials and access controls before shared or production use.

Risk: Examples include mutable dependencies in CI/CD contexts, such as unpinned GitHub Actions or container image tags.

Mitigation: Pin actions and container images to reviewed immutable SHAs or digests before using them in CI, staging, or production.

Risk: Passing real secrets directly through command lines or pipeline variables can expose them in logs, shell history, or process metadata.

Mitigation: Prefer short-lived identity-based credentials, secret-store integrations, masking, and environment mechanisms that avoid exposing secret values.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash, YAML, HCL, and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes copyable examples that require review and hardening before use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
