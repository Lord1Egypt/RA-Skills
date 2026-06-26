## Description: <br>
Generate Supabase API curl commands and SQL query helpers for querying tables, counting rows, inserting records, checking database health, auditing RLS policies, and listing tables. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[loutai0307-prog](https://clawhub.ai/user/loutai0307-prog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and database operators use this skill to draft Supabase REST API, Management API, and SQL helper commands before running them in their own environment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated curl and SQL helper commands can include write-capable operations against Supabase projects. <br>
Mitigation: Review every generated command and SQL statement before execution, and test against non-production projects when possible. <br>
Risk: Generated commands require Supabase API keys or access tokens that may grant sensitive or privileged access. <br>
Mitigation: Use the least-privileged token suitable for the task, avoid sharing tokens in logs or prompts, and rotate any token that may have been exposed. <br>
Risk: Raw SQL, insert payloads, table names, and filters are user-provided and may change data or expose sensitive records if run unchanged. <br>
Mitigation: Validate table names, filters, payloads, and SQL scope before running commands, especially in production environments. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/loutai0307-prog/supabase-tool) <br>
- [Publisher profile](https://clawhub.ai/user/loutai0307-prog) <br>
- [Supabase project API settings](https://app.supabase.com/project/YOUR_PROJECT_REF/settings/api) <br>
- [Supabase access tokens](https://supabase.com/dashboard/account/tokens) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-style text with bash commands and configuration placeholders] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated commands include placeholders for Supabase project references, API keys, access tokens, SQL, tables, filters, and JSON payloads.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
