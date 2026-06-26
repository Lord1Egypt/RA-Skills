## Description: <br>
Migrate Next.js projects from Vercel to Cloudflare Workers with Supabase and Hyperdrive support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiafar](https://clawhub.ai/user/jiafar) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to assess and migrate Next.js applications from Vercel to Cloudflare Workers, including Supabase connectivity, Hyperdrive configuration, environment variable access, and database initialization patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The analyzer reads files from a chosen local project path and may surface project structure or configuration details. <br>
Mitigation: Run it only against the intended repository and avoid sharing secrets, private connection strings, or sensitive project output in chat or logs. <br>
Risk: Migration guidance and generated commands can require project changes that may break deployment or database connectivity if applied blindly. <br>
Mitigation: Use version control or backups, review proposed code and configuration changes, and test with Wrangler and the target database environment before release. <br>
Risk: The artifact references a migration script name that is not present in the evidence bundle. <br>
Mitigation: Do not run any referenced migration script unless a trusted copy is separately reviewed. <br>


## Reference(s): <br>
- [Hyperdrive + Supabase Setup Guide](references/hyperdrive-setup.md) <br>
- [Environment Variable Patterns on Cloudflare Workers](references/env-patterns.md) <br>
- [ClawHub skill page](https://clawhub.ai/jiafar/vercel-to-cloudflare) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline code blocks, shell commands, configuration examples, and local analysis output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include project-specific migration findings from a local analyzer script.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
