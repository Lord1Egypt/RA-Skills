## Description:

Scaffolds a production-oriented Nuxt app for Cloudflare Workers with Wrangler deployment, NuxtHub bindings, optional Nuxt Content and i18n, SEO, Drizzle, Vitest, and pnpm setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[techvoyage51](https://clawhub.ai/user/techvoyage51)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create a new full-stack Nuxt application targeting Cloudflare Workers. It guides module selection, project structure, NuxtHub binding setup, Wrangler deployment configuration, testing, and release-readiness checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may direct an agent to run package-manager commands and execute build tooling from newly installed dependencies.

Mitigation: Use a clean workspace or container, review generated files and lockfiles, and confirm package install and build commands before execution.

Risk: Wrangler and Cloudflare resource commands can create, modify, or deploy account resources when credentials are present.

Mitigation: Confirm before provisioning D1, KV, R2, or Worker resources; use least-privilege credentials and preview environments before production deployment.

Risk: Incorrect app names, domains, placeholders, or database IDs can produce broken deployments or point generated apps at the wrong resources.

Mitigation: Validate the app name as a simple lowercase identifier, replace all placeholders with project-owned values, and review environment variables before deployment.

## Reference(s):

- [Directory structure reference](references/directory-structure.md)
- [Nuxt configuration example](references/nuxt.config.example.ts)
- [Wrangler configuration example](references/wrangler.example.jsonc)
- [Package manifest example](references/package.example.json)
- [Nuxt Content configuration example](references/content.config.example.ts)
- [NuxtHub deployment specifics](references/nuxthub-deployment.md)
- [Nuxt UI documentation](https://ui.nuxt.com)
- [Antdv Next documentation](https://www.antdv-next.com)
- [Nuxt Content documentation](https://content.nuxt.com)
- [Cloudflare Workers documentation](https://developers.cloudflare.com/workers/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with code blocks and configuration templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a new-project scaffold whose modules and files are selected from the user's requested app scope.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
