## Description:

Generate a compact weekly changelog from a git repository, grouped by author and day, for reports, standups, or release notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to summarize recent git commit history for weekly reports, standups, and release-note drafts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running the utility on untrusted repositories can surface misleading or unsafe commit metadata in a sensitive terminal.

Mitigation: Use it on repositories you trust or in a low-privilege terminal, and review the changelog before sharing or acting on it.

Risk: JSON output may be unsafe for downstream automation that assumes commit metadata is complete, trusted, or sanitized.

Mitigation: Validate and sanitize commit authors, dates, hashes, and subjects before feeding the JSON into automated workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/weekly-gitlog)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Plain text changelog grouped by author and day, with optional JSON output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires git and a git work tree; the default window is the last 7 days, and merge commits are skipped unless requested.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
