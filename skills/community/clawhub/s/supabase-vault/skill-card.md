## Description:

Replace OpenClaw's local file vault with Supabase Vault for AES-256 encrypted-at-rest secret storage, dashboard-based connection and migration, and exec-provider secret retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maverick-software](https://clawhub.ai/user/maverick-software)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to configure Supabase as the OpenClaw secrets backend, migrate existing local secrets, and manage secrets through the OpenClaw dashboard.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires persistent access to a Supabase service_role key, which can bypass Row Level Security in the target project.

Mitigation: Use a dedicated Supabase project for OpenClaw secrets, validate the project URL yourself, monitor access, and rotate the service_role key if it may have been exposed.

Risk: The migration flow rewrites OpenClaw secret configuration and leaves the original local secrets file in place as a backup.

Mitigation: Run a dry-run or review the migration output first, verify the updated SecretRefs, and manually decide whether to retain, move, or delete ~/.openclaw/secrets.json after migration.

Risk: The skill installs executable bridge code and depends on @supabase/supabase-js for secret retrieval.

Mitigation: Pin and verify dependencies, keep the skill directory trusted and permission-restricted, and review the copied gateway and dashboard files before deployment.

## Reference(s):

- [Supabase Vault Architecture & Threat Model](references/architecture.md)
- [Supabase](https://supabase.com)
- [Supabase Dashboard API Settings](https://supabase.com/dashboard/project/_/settings/api)
- [Supabase Dashboard SQL Editor](https://supabase.com/dashboard/project/_/sql)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with TypeScript, SQL, JavaScript, JSON, and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces OpenClaw integration files and setup guidance for Supabase-backed secret storage.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
