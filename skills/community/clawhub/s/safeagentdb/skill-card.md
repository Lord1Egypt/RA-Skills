## Description:

Sets up and maintains SafeAgentDB-style database safety infrastructure for AFK agentic development.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aidan945](https://clawhub.ai/user/aidan945)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to install, adapt, audit, package, or maintain isolated local, develop, preview, and production database workflows for agent-assisted projects. It is most directly applicable to Supabase, Vercel, and GitHub Actions stacks, and provides guidance for adapting the same safety model to other platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled workflow can use powerful Supabase, Vercel, and GitHub credentials to create, modify, or delete cloud database and preview resources.

Mitigation: Require explicit user approval before using credentials, store secrets only in approved secret stores, keep service-role values server-only, and use dry-run modes before real provisioning or cleanup.

Risk: Preview database hydration can expose production data if copied without a clear policy.

Mitigation: Define a written hydration policy first, default previews to develop or seed data, and copy production data only after explicit privacy and compliance approval.

Risk: Cleanup scripts can remove preview resources if branch scoping is too broad.

Mitigation: Restrict cleanup to managed preview branches, preserve configured persistent previews, and require explicit execute modes for cleanup operations.

Risk: Migration automation can apply feature-branch schema changes to shared environments too early.

Mitigation: Apply feature migrations only to isolated preview databases until merge and run migration checks for duplicate timestamps and potentially destructive SQL.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aidan945/skills/safeagentdb)
- [Setup Process](artifact/references/setup-process.md)
- [Credentials And Permissions](artifact/references/credentials.md)
- [Data Hydration Policy](artifact/references/data-hydration-policy.md)
- [Agent Operating Rules](artifact/references/agent-operating-rules.md)
- [Local Development](artifact/references/local-development.md)
- [Non-Standard Stacks](artifact/references/non-standard-stacks.md)
- [Troubleshooting](artifact/references/troubleshooting.md)
- [Optional Agent Packaging](artifact/references/agent-packaging.md)
- [Database And Branching Architecture Template](artifact/templates/docs/database-branching.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code, shell command, and configuration file snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or adapt project files, scripts, package scripts, CI workflows, and architecture documentation when used by an agent with repository access.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
