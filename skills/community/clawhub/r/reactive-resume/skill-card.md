## Description:

Reactive Resume open-source resume builder development guidance for TanStack Start, React 19, Vite, PostgreSQL, Drizzle ORM, ORPC, and Better Auth workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pupuking723](https://clawhub.ai/user/pupuking723)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to set up, extend, template, migrate, export, and self-host Reactive Resume installations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Database reset guidance can delete all data if pointed at a non-disposable database.

Mitigation: Run scripts/db-reset.py only against disposable development databases and confirm DATABASE_URL before execution.

Risk: Deployment examples include placeholder secrets, tokens, and credentials.

Mitigation: Replace all example values with strong environment-specific secrets before deployment.

Risk: Browserless, databases, Docker, sudo, cron, and restore operations can become high-impact if exposed or run without review.

Mitigation: Keep these services private, require explicit user approval for privileged operations, and review commands before execution.

## Reference(s):

- [Reactive Resume Skill Page](https://clawhub.ai/pupuking723/skills/reactive-resume)
- [Templates Guide](references/templates-guide.md)
- [Deployment Reference](references/deployment.md)
- [API Reference](references/api-reference.md)
- [Reactive Resume Getting Started](https://docs.rxresu.me/getting-started)
- [Reactive Resume Self-Hosting](https://docs.rxresu.me/self-hosting/docker)
- [Reactive Resume Development](https://docs.rxresu.me/contributing/development)
- [Reactive Resume Architecture](https://docs.rxresu.me/contributing/architecture)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with inline code, shell commands, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create React template scaffolds and propose database, deployment, API, and PDF export steps for Reactive Resume projects.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
