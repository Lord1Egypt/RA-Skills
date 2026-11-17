## Description:

Helps agents access Supabase database tables, authentication users, and storage through a user-authorized Maton connection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other authorized users can guide an agent to query Supabase data and manage users or storage. With separate approval, they can set up functions and triggers for recurring workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad connection access can expose database records, authentication users, or storage objects.

Mitigation: Review connection scopes, prefer read-only and staging access where possible, and confirm every write or administrative action.

Risk: Hosted functions, triggers, and destinations can cause ongoing automated data transfers.

Mitigation: Require explicit approval for each automation and destination; limit forwarded fields and review who can access the receiving endpoint.

## Reference(s):

- [Supabase skill on ClawHub](https://clawhub.ai/byungkyu/skills/supabase-api)
- [Maton](https://maton.ai)
- [Supabase REST API Guide](https://supabase.com/docs/guides/api)
- [PostgREST Documentation](https://postgrest.org/en/stable/)
- [Maton CLI Manual](https://cli.maton.ai/manual)
- [Time trigger reference](artifact/references/time/triggers.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Code, Configuration guidance]

**Output Format:** [Markdown with command and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions require a Maton account, network access, and an authorized Supabase connection.]

## Skill Version(s):

1.2.6 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
