## Description:

Creates numbered US-style SOPs with owners, triggers, steps, exceptions, and sign-off details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rapidworker1](https://clawhub.ai/user/rapidworker1)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and operations managers at US small businesses use this skill to document repeatable processes as numbered SOPs and identify gaps before review.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The checker cannot confirm that every SOP step has an owner or deadline.

Mitigation: Manually review the completed SOP for step owners and deadlines before use.

Risk: Running the checker overwrites an existing lint-report.md in its output folder.

Mitigation: Use a dedicated output folder for each run.

Risk: The optional Windows app is unsigned and is separate from the skill's review.

Mitigation: Evaluate it independently and verify its published SHA-256 before running it.

## Reference(s):

- [How US teams structure an SOP](references/sop-structure.md)

## Skill Output:

**Output Type(s):** [Markdown, Configuration, Guidance]

**Output Format:** [Markdown SOP drafts and lint reports, with a YAML outline template]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Drafts require owner review before adoption as company policy.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
