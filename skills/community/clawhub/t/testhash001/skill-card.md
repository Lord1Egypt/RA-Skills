## Description:

Log meals, check nutrition, manage medications, and view daily health dashboard via Hash Health.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devak208](https://clawhub.ai/user/devak208)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to log meals, review nutrition, manage medication records, and view daily health summaries through Hash Health.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends identifiable meal, nutrition, medication, schedule, and user identifier data to an external Hash Health API.

Mitigation: Use only with a trusted Hash Health API operator and prefer an opaque account ID instead of an email address for HASH_HEALTH_USER_ID.

Risk: Saving or deleting health records can modify user data.

Mitigation: Require explicit user confirmation before saving or deleting records, and look up record IDs instead of guessing them.

Risk: Authentication and consent safeguards are under-specified in the release evidence.

Mitigation: Review access controls, consent expectations, and deletion behavior before installation or deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/devak208/skills/testhash001)
- [Hash Health API Base URL](https://hash-claude-mcp.vercel.app)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown with concise summaries and API-backed health records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires HASH_HEALTH_USER_ID and explicit user confirmation before saving meal records.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
