## Description:

Builds a reusable brand story bank from user-provided interview, case, testimonial, win-loss, pillar, and claims-ledger material, with each story tagged to one pillar and its proof labels made explicit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

Apache-2.0

## Use Case:

Marketing teams, brand strategists, and content teams use this skill to turn origin, founder, customer, transformation, and proof material into reusable story units. Each unit is mapped to a message-house pillar and claim ID so downstream content can reuse consistent, sourced stories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read project memory and user-provided customer or interview materials.

Mitigation: Use it only in projects where those materials may be processed, and provide only materials the user has rights to use.

Risk: Story-bank outputs and pending proof proposals can be written to project memory after confirmation.

Mitigation: Confirm saving only when those outputs should persist in project memory.

Risk: Customer notes, transcripts, or testimonials can contain unsupported proof claims.

Mitigation: Keep unverified proofs labeled [needs source] and route them for claim review instead of presenting them as substantiated facts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aaron-he-zhu/skills/story-bank-builder)
- [Project Homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)

## Skill Output:

**Output Type(s):** [Markdown, Files, Guidance]

**Output Format:** [Markdown story bank document with story units, proof labels, proof gaps, and a handoff summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Labels proofs as Measured, User-provided, or [needs source]; saves project memory only after user confirmation.]

## Skill Version(s):

19.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
