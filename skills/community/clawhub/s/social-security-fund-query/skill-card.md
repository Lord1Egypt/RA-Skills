## Description:

Queries China social insurance and housing fund contribution bases and rates by region, with cached local results and structured tabular output.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[elysiacwy](https://clawhub.ai/user/elysiacwy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents can use this skill to look up regional China employee social insurance and housing fund contribution information and format the result as a readable table. It should be treated as a prototype unless the publisher verifies official-source retrieval, coverage, and update timestamps.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The skill may present prototype or cached data as current nationwide payroll-policy guidance.

Mitigation: Require official source URLs, last-updated timestamps, cache age disclosure, and clear refresh controls before relying on outputs for payroll or compliance decisions.

Risk: Coverage claims may exceed the implemented data source coverage.

Mitigation: Limit descriptions and user-facing responses to verified supported cities or add verified official-source retrieval for each queried region.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/elysiacwy/skills/social-security-fund-query)
- [Publisher profile](https://clawhub.ai/user/elysiacwy)
- [Skill homepage](https://clawhub.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands]

**Output Format:** [Markdown tables and JSON-formatted CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read and write a local cache file; Python runtime required.]

## Skill Version(s):

1.0.1 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
