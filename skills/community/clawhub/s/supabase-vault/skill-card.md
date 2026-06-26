## Description: <br>
Supabase Vault replaces OpenClaw's local file vault with a Supabase-backed encrypted secret store and dashboard workflow for connecting, migrating, and managing API keys and auth tokens. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maverick-software](https://clawhub.ai/user/maverick-software) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to configure Supabase Vault as a secrets backend, migrate existing local secrets, and manage OpenClaw API keys and auth tokens through dashboard and CLI workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may handle plaintext secrets and a Supabase admin-level service_role key. <br>
Mitigation: Use a dedicated test Supabase project or least-privilege setup where possible, avoid production credentials until the flow is verified, and rotate credentials if exposure is suspected. <br>
Risk: Secrets can be migrated without enough confirmation. <br>
Mitigation: Run a dry-run or preview first, confirm the exact keys and configuration changes before migration, and keep backups available until the new provider is verified. <br>
Risk: The service_role key bypasses Supabase row-level security. <br>
Mitigation: Use a project dedicated to OpenClaw secrets, restrict access to the key, and monitor or rotate the key according to the team's credential policy. <br>


## Reference(s): <br>
- [Supabase Vault Architecture & Threat Model](references/architecture.md) <br>
- [Supabase](https://supabase.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/maverick-software/supabase-vault) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell, SQL, TypeScript, JavaScript, and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup and migration guidance for OpenClaw and Supabase Vault; it may handle secret names, secret values, and Supabase bootstrap credentials during use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
