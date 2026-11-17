## Description:

Helps agents research public Upwork job postings and freelancer profiles through Crawlora, returning structured job and profile data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Freelancers, hiring teams, and researchers use this skill to find public Upwork jobs, inspect job details, compare listed budgets, and review freelancer profiles before making decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, job IDs, freelancer IDs, and the API key are sent to Crawlora.

Mitigation: Use only queries you are comfortable sharing and keep the API key in the environment; never commit it.

Risk: Research could be used beyond public Upwork data or contrary to Upwork's terms.

Mitigation: Limit use to public postings and profiles and respect Upwork's terms.

## Reference(s):

- [Upwork research endpoint reference](reference/endpoints.md)
- [Crawlora](https://crawlora.net)
- [ClawHub skill listing](https://clawhub.ai/crawlora-org/skills/upwork-research)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands]

**Output Format:** [Markdown with shell commands and JSON-based research summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Job searches are paginated; results cover publicly available postings and profiles.]

## Skill Version(s):

1.0.17 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
