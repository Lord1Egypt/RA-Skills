## Description: <br>
Turborepo helps agents configure and troubleshoot JavaScript and TypeScript monorepo task pipelines, caching, filtering, CI/CD, and environment handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wpank](https://clawhub.ai/user/wpank) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to configure turbo.json, package scripts, CI workflows, cache behavior, filters, and environment-variable handling for Turborepo monorepos. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated package.json, turbo.json, or CI changes may be incorrect for a specific repository. <br>
Mitigation: Review proposed configuration and workflow changes before applying them. <br>
Risk: CI and remote cache setup may expose or over-scope secrets if tokens are passed broadly. <br>
Mitigation: Use least-privileged tokens and prefer task-level or scoped environment configuration. <br>
Risk: Remote cache configuration can leak or trust inappropriate build outputs when connected to untrusted providers or endpoints. <br>
Mitigation: Enable remote caching only with trusted providers or endpoints and avoid caching sensitive outputs. <br>


## Reference(s): <br>
- [ClawHub Turborepo Release](https://clawhub.ai/wpank/turborepo) <br>
- [Official Turborepo Documentation](https://turborepo.dev/docs) <br>
- [Repository Structure](references/best-practices/structure.md) <br>
- [Task Configuration Reference](references/configuration/tasks.md) <br>
- [Configuration Gotchas](references/configuration/gotchas.md) <br>
- [Debugging Cache Issues](references/caching/gotchas.md) <br>
- [Remote Caching](references/caching/remote-cache.md) <br>
- [Environment Variable Gotchas](references/environment/gotchas.md) <br>
- [GitHub Actions](references/ci/github-actions.md) <br>
- [Common Filter Patterns](references/filtering/patterns.md) <br>
- [turbo run Flags Reference](references/cli/commands.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline JSON, YAML, and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces guidance and proposed edits for package.json, turbo.json, CI workflows, and monorepo structure; users should review changes before applying them.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
