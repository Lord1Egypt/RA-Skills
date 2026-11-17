## Description:

Search open jobs in Sweden with the Remotejobb connector. Use when the user is looking for a job, wants to see open positions, asks about jobs in a Swedish city, category or company, asks which companies are hiring, wants remote or hybrid work, or writes in Swedish about "lediga jobb", "söka jobb" or "jobba hemifrån".

This skill is ready for commercial/non-commercial use.

## Publisher:

[remotejobb](https://clawhub.ai/user/remotejobb)

### License/Terms of Use:

MIT-0

## Use Case:

Job seekers use this skill to find and compare open positions in Sweden by role, location, employer, work mode, salary, and other filters. It helps users review listings and application details in their preferred language.

### Deployment Geography for Use:

Sweden

## Known Risks and Mitigations:

Risk: Job listings can change daily, so previously returned availability may become stale.

Mitigation: Check a listing again with get_job when the user asks later, and provide its original listing link.

## Reference(s):

- [Remotejobb AI documentation](https://remotejobb.se/en/ai)
- [Remotejobb MCP server](https://remotejobb.se/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with job listings, summaries, and links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only job search results; listings can change daily.]

## Skill Version(s):

1.1.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
