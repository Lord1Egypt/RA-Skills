## Description:

Surfaces relevant public LinkedIn conversations and potential buyers in a weekly Slack digest for human review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cargo-ai](https://clawhub.ai/user/cargo-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing and sales-development teams use this skill to review weekly LinkedIn posts relevant to their buyers and decide which conversations to join. It highlights up to five posts and ten commenters without engaging on the team's behalf.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The digest includes names and quotes from public LinkedIn comments.

Mitigation: Send it only to a locked internal Slack channel and review the selected connectors before installation.

Risk: LinkedIn searches, comment reads, and model usage can incur costs.

Mitigation: Review live usage prices and the Cargo plan before deployment; retain the search and comment limits.

## Reference(s):

- [Project homepage](https://github.com/getcargohq/gtm-skills)
- [Digest format](references/digest.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Slack Markdown digest with links to public posts and quoted comments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One weekly digest; at most five highlighted posts and ten commenters; no automated LinkedIn engagement.]

## Skill Version(s):

0.1.2 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
