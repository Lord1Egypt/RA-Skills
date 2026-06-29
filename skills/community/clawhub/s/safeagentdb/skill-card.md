## Description: <br>
Sets up and maintains SafeAgentDB-style database safety infrastructure for isolated local, develop, preview, and production database workflows in agentic development projects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aidan945](https://clawhub.ai/user/aidan945) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to install, adapt, audit, package, or maintain branch-safe database infrastructure, especially Supabase, Vercel, and GitHub Actions preview workflows and migration guardrails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automate high-privilege database, deployment, and repository changes across Supabase, Vercel, and GitHub. <br>
Mitigation: Install only with intentionally scoped provider tokens, explain each credential before use, and store secrets in approved secret stores rather than committed files. <br>
Risk: Preview provisioning and cleanup can create, hydrate, truncate, refill, or delete non-production database resources. <br>
Mitigation: Use dry-run provisioning first, keep hydration defaults conservative, require explicit approval before copying production data, and preserve cleanup safeguards. <br>
Risk: Service-role keys and preview credentials could expose sensitive database access if leaked to client code, logs, or source control. <br>
Mitigation: Keep service-role keys server-side, avoid printing secret values, and confirm Vercel preview environment variables cannot reach public client bundles. <br>
Risk: Feature or agent work could accidentally target production or shared develop databases. <br>
Mitigation: Maintain separate production, develop, preview, and local database environments and validate branch-specific environment variables before applying migrations. <br>
Risk: Supabase database branching can create ongoing branch-hour costs. <br>
Mitigation: Confirm plan and cost tolerance before first provisioning, then enable PR-close cleanup and scheduled orphan preview cleanup. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/aidan945/safeagentdb) <br>
- [Setup Process](references/setup-process.md) <br>
- [Credentials And Permissions](references/credentials.md) <br>
- [Data Hydration Policy](references/data-hydration-policy.md) <br>
- [Local Development](references/local-development.md) <br>
- [Non-Standard Stacks](references/non-standard-stacks.md) <br>
- [Agent Operating Rules](references/agent-operating-rules.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with code snippets, configuration files, TypeScript scripts, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate or modify project files and automation after user approval.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
