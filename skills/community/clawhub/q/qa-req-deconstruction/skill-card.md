## Description:

Deconstructs requirements into testable inputs, operations, states, outputs, and rules while identifying explicit, implied, and derived requirements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kokxi](https://clawhub.ai/user/kokxi)

### License/Terms of Use:

MIT-0

## Use Case:

QA engineers and product teams use this skill to turn requirements documents or brief feature descriptions into traceable requirement and business-rule tables, risks, and questions for clarification before test-case design.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requirements may contain sensitive customer, payment, identity, or production information.

Mitigation: Remove or mask sensitive data before supplying requirements or examples.

Risk: The optional command to install the larger skill set fetches unpinned remote content.

Mitigation: Run it only after reviewing and trusting the source and accepting the remote-install risk.

## Reference(s):

- [Requirement table template](assets/requirement-table.md)
- [Five dimensions framework](references/five-dimensions.md)
- [Three layers of requirements](references/three-layers.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown requirement and business-rule tables with risks and open questions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses REQ-, RISK-, and RULE- identifiers; flags assumptions and derived requirements for confirmation.]

## Skill Version(s):

1.8.0 (source: skill frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
