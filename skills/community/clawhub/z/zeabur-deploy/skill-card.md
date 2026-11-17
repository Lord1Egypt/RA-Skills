## Description:

Prepare, deploy, diagnose, and verify applications on Zeabur, including existing-server reuse, scoped service updates, private databases, HTTPS readiness, and deployment runbooks. Use when Zeabur is requested or already selected for a deployment; does not publish mobile apps or choose a new hosting provider.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theosunny](https://clawhub.ai/user/theosunny)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan, deploy, update, diagnose, and verify applications on Zeabur while reusing authorized resources and documenting deployment and rollback evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A deployment could target the wrong account, project, service, or exceed the approved budget.

Mitigation: Confirm the target account and live resource IDs and review capacity and budget before deployment or resource creation.

Risk: Uploaded files, configuration, or diagnostic logs could expose private data or secrets.

Mitigation: Review and narrow the upload context, keep raw configuration and logs in private storage, and share only redacted results.

Risk: An unreviewed migration or incompatible rollback could disrupt production data or service availability.

Mitigation: Review migration effects and backups before irreversible changes, and use a schema-compatible rollback target.

Risk: CLI behavior or flags may differ from historical examples.

Mitigation: Prefer a reviewed fixed CLI version and check the installed CLI's current help before applying commands.

## Reference(s):

- [Zeabur Deployment skill on ClawHub](https://clawhub.ai/theosunny/skills/zeabur-deploy)
- [Zeabur CLI documentation](https://zeabur.com/docs/en-US/developer/cli)
- [Zeabur template format](https://zeabur.com/docs/en-US/template/template-format)
- [Zeabur private networking](https://zeabur.com/docs/en-US/deploy/networking/private-networking)
- [Zeabur service root directory](https://zeabur.com/docs/en-US/deploy/config/root-directory)
- [Zeabur Go deployment guide](https://zeabur.com/docs/en-US/guides/go)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown instructions with shell command and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Project-specific, scoped deployment guidance; not an unattended deployment script.]

## Skill Version(s):

1.0.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
