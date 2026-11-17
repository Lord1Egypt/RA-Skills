## Description:

Guides developers through migrating Vue 2 projects from Webpack or Vue CLI builds to Vite, including dependency updates, configuration migration, environment-variable compatibility, testing, and optional deployment setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yyyyzj](https://clawhub.ai/user/yyyyzj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan and execute Vue 2 build-tool migrations from Webpack or Vue CLI to Vite. It helps analyze existing project structure, update dependencies and configuration, migrate code patterns, troubleshoot common Vite issues, and validate builds before release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional deployment guidance uses FTP and can upload production artifacts remotely.

Mitigation: Replace FTP with SFTP, HTTPS, or CI deployment; use least-privilege credentials from environment variables and require explicit production approval.

Risk: Migration steps may delete old build and configuration files.

Mitigation: Run deletion steps only from the project root after confirming a clean Git state or backup, and prefer git rm so changes can be restored.

Risk: Dependency and axios upgrades can change runtime behavior or leave known vulnerabilities if versions are not checked.

Mitigation: Review dependency conflicts manually, verify lockfile changes, and choose the current axios 1.x security patch level from official release and security sources at execution time.

## Reference(s):

- [Migration steps](references/migration-steps.md)
- [Vite configuration template](references/vite-config.md)
- [Common migration issues](references/common-issues.md)
- [Deployment configuration](references/deploy-config.md)
- [ClawHub skill page](https://clawhub.ai/yyyyzj/skills/vue2-vite-upgrade)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline code, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes phased migration guidance and optional deployment instructions; review security guidance before production upload.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
