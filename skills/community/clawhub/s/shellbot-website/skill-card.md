## Description:

Build, deploy, and design micro apps and websites on Cloudflare Workers. Scaffolds from templates (React Router + Hono, Next.js, Astro, Remix), deploys, sets up custom domains, provisions resources (D1, KV, R2, Queues), manages secrets, and applies production-grade frontend design. Use when creating websites, web apps, landing pages, or any project on Cloudflare Workers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cohnen](https://clawhub.ai/user/cohnen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to scaffold, configure, deploy, and operate Cloudflare Workers websites and micro apps with supporting D1, KV, R2, Queues, custom domain, secret management, and frontend design guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use Cloudflare credentials with edit authority to create, deploy, configure, and delete remote resources.

Mitigation: Use a narrowly scoped Cloudflare API token, confirm the target account and environment before execution, and avoid OAuth fallback for agent or CI runs.

Risk: Secret handling can expose sensitive values through command-line arguments or temporary bulk secret files.

Mitigation: Avoid passing real secrets directly as command-line arguments, keep bulk secret files out of the repository, and delete temporary secret files after use.

Risk: Generated templates, deployments, and configuration changes can introduce unintended application behavior or infrastructure changes.

Mitigation: Review generated templates and Wrangler configuration before deployment, use dry-run behavior where available, and review destructive actions before using force flags.

## Reference(s):

- [Shellbot Website ClawHub listing](https://clawhub.ai/cohnen/skills/shellbot-website)
- [Shell homepage](https://getshell.ai)
- [Cloudflare Workers Docs](https://developers.cloudflare.com/workers/)
- [Wrangler CLI](https://developers.cloudflare.com/workers/wrangler/)
- [D1 Docs](https://developers.cloudflare.com/d1/)
- [R2 Docs](https://developers.cloudflare.com/r2/)
- [KV Docs](https://developers.cloudflare.com/kv/)
- [Workers Templates](https://developers.cloudflare.com/workers/get-started/quickstarts/)
- [Cloudflare Workers Templates](references/cf-templates.md)
- [Custom Domains for Cloudflare Workers](references/custom-domains.md)
- [Wrangler Configuration Reference](references/wrangler-config.md)
- [Typography](references/typography.md)
- [Color & Contrast](references/color-and-contrast.md)
- [Spatial Design](references/spatial-design.md)
- [Motion Design](references/motion-design.md)
- [Interaction Design](references/interaction-design.md)
- [Responsive Design](references/responsive-design.md)
- [UX Writing](references/ux-writing.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, code snippets, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local project files and mutate Cloudflare resources when the user executes the provided scripts with credentials.]

## Skill Version(s):

1.1.0 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
