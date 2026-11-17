## Description:

Browse and search Reddit in read-only mode using public JSON endpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tristanmanchester](https://clawhub.ai/user/tristanmanchester)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to browse subreddits, search Reddit posts, inspect comment threads, and prepare shortlists of Reddit permalinks for manual review or replies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches public Reddit content through a bundled Node script.

Mitigation: Install it only when this network behavior is acceptable, keep use user-directed, and avoid adding Reddit credentials or auth cookies unless the skill is redesigned and re-reviewed.

Risk: Public Reddit results and comment snippets can be incomplete, stale, rate-limited, or unavailable.

Mitigation: Use small request limits first, preserve permalinks, and have the user review source threads before taking action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tristanmanchester/skills/reddit-read-only)
- [Output Schema](references/OUTPUT_SCHEMA.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with shell commands; bundled commands return JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled command output is structured as ok/data or ok/error JSON and includes Reddit permalinks when results are returned.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
