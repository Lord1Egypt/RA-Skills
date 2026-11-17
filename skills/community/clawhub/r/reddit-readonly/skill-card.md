## Description:

Browse and search Reddit in read-only mode using public JSON endpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[buksan1950](https://clawhub.ai/user/buksan1950)

### License/Terms of Use:


## Use Case:

Agents and their users use this skill to find Reddit posts, inspect public comment threads, and prepare shortlists of permalinks for manual review or reply drafting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can retrieve user-specified public Reddit content, which may include low-quality, offensive, or misleading material.

Mitigation: Keep searches scoped to relevant subreddits and small result limits, then review selected posts and comments before using them.

Risk: Draft reply ideas based on retrieved Reddit content could be inaccurate or inappropriate for the thread context.

Mitigation: Use generated reply ideas only as drafts and post manually after human review.

Risk: Large or repeated requests may trigger Reddit rate limits or return incomplete thread context.

Mitigation: Use the documented small limits and slower pacing environment variables when requests fail or Reddit returns HTML.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/buksan1950/skills/reddit-readonly)
- [Output schema](references/OUTPUT_SCHEMA.md)
- [Reddit public website](https://www.reddit.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON command output with concise Markdown summaries and optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only public Reddit data; commands return { ok, data } or { ok, error } envelopes and include permalinks.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
