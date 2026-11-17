## Description:

Helps developers inspect, compare, and selectively update hosted Supabase Auth settings, including magic-link redirects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexbloch-ia](https://clawhub.ai/user/alexbloch-ia)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to troubleshoot hosted Supabase Auth settings and magic-link redirects, review proposed changes, and update only selected configuration fields.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Applying a change to hosted Auth configuration can affect production sign-in behavior.

Mitigation: Pin and review the project reference, inspect the dry-run diff, and treat --apply as a production change.

Risk: A Supabase access token grants sensitive configuration access.

Mitigation: Use a fine-grained or short-lived token where possible and supply it through the environment rather than a file or command argument.

Risk: Replacing the redirect allow-list can remove existing callback URLs.

Mitigation: Use add-redirect to retain existing entries and review the proposed allow-list before applying.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/alexbloch-ia/skills/supabase-config)
- [Supabase API documentation](https://supabase.com/docs/reference/api/introduction)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance]

**Output Format:** [Text and JSON with Markdown command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dry-run diffs, redirect checks, remote advisor findings, and post-change verification.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
