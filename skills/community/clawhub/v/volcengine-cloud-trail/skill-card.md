## Description:

Use when the user asks to query Volcengine CloudTrail audit logs, investigate login or resource operations, or manage CloudTrail trails and backfill delivery tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volc-sdk-team](https://clawhub.ai/user/volc-sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and cloud operators use this skill to query Volcengine CloudTrail audit evidence, resolve event names, and manage trails or backfill delivery tasks with explicit confirmation for write actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CloudTrail trail and backfill operations can change audit delivery configuration or task state.

Mitigation: Require a dry-run preview and explicit user confirmation before write actions, then perform read-only verification and report whether the requested state was verified.

Risk: Actions executed in the wrong account, profile, region, or organization scope could affect unintended audit data or delivery targets.

Mitigation: Confirm the account/profile, region, trail name, delivery target, organization or cross-account scope, and parsed time window before confirmed writes.

Risk: Ambiguous time input can query or backfill the wrong CloudTrail window.

Mitigation: Prefer explicit timezone-bearing timestamps and surface the resolved time window before relying on results or confirming backfill tasks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/volc-sdk-team/skills/volcengine-cloud-trail)
- [event-query.md](references/event-query.md)
- [event-trail-management.md](references/event-trail-management.md)
- [backfill-delivery-tasks.md](references/backfill-delivery-tasks.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON, JSONC, table, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include CloudTrail event summaries, annotated raw event JSONC, dry-run plans, write acceptance status, state verification status, account/profile/region context, and request identifiers.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
