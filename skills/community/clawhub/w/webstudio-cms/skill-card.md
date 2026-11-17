## Description:

Set up, administer, build, design, and publish with Webstudio Cloud or self-hosted deployments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cbertucci33](https://clawhub.ai/user/cbertucci33)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site operators use this skill to administer Webstudio deployments, build and style pages, manage assets and domains, and publish sites. It is intended for authorized Webstudio environments where production changes are confirmed before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide high-impact Webstudio administration actions, including database writes, token changes, domain changes, and publishing.

Mitigation: Use it only for deployments the operator is authorized to administer, confirm the named project or build target, require explicit approval before state-changing or production operations, and back up exact build rows before direct database edits.

Risk: Self-hosted deployments may expose sensitive control surfaces if PostgREST, database, MinIO admin, or publisher control APIs are made public.

Mitigation: Keep those services private to the deployment boundary, prefer authenticated Builder or CLI paths, and validate any hardened PostgREST role before revoking compatibility grants.

Risk: Webstudio share links, tokens, database credentials, storage keys, and login secrets are sensitive.

Mitigation: Use approved secret injection or existing authenticated sessions, avoid reading .env files automatically, never print or log secret values, pin tool and container versions, and remove injected secrets after use.

## Reference(s):

- [Webstudio CMS on ClawHub](https://clawhub.ai/cbertucci33/skills/webstudio-cms)
- [Webstudio CMS Skill Definition](artifact/SKILL.md)
- [Security Boundaries](artifact/security.md)
- [Install and Self-Hosting](artifact/install.md)
- [Database and Stack](artifact/database.md)
- [Build Objects](artifact/build-objects.md)
- [Styling](artifact/styling.md)
- [Publishing and Domains](artifact/publishing.md)
- [Verification](artifact/verification.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose project, database, asset, domain, and publishing operations that require operator approval before execution.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
