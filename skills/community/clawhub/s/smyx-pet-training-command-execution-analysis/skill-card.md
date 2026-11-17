## Description:

Analyzes pet-training videos to assess sit, down, and stay command execution and retrieve past training reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Pet owners, trainers, and developers use training videos or media URLs to review a pet's response to sit, down, and stay commands and consult past reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pet-training videos or media URLs are sent to the LifeEmergence cloud service.

Mitigation: Review the service's retention and account controls before submitting sensitive footage.

Risk: Uploads and historical reports are associated with a persistent local/cloud identity.

Mitigation: Treat history queries as cloud account data access and review who can access those reports.

## Reference(s):

- [Pet-training analysis API documentation](artifact/references/api_doc.md)
- [ClawHub skill listing](https://clawhub.ai/18072937735/skills/smyx-pet-training-command-execution-analysis)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Structured analysis report or history list in text, Markdown, or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a report link; results can be saved to a file.]

## Skill Version(s):

1.0.14 (source: ClawHub server release; artifact frontmatter lists 1.0.17)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
