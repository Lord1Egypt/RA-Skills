## Description:

Checks whether a testing request includes clear requirements and enough context before test design begins, and asks for missing information when needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kokxi](https://clawhub.ai/user/kokxi)

### License/Terms of Use:

MIT-0

## Use Case:

QA practitioners and developers use this skill before test design to check whether a request has enough detail to test. It scores input quality and identifies missing requirements and follow-up questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Testing requests may contain customer, payment, identity, or production data.

Mitigation: Mask sensitive information before providing requests, attachments, or links.

Risk: The optional related-skill installation suggestion uses an unpinned npx command.

Mitigation: Use a pinned version or a trusted source if installing the broader skill set.

## Reference(s):

- [Input validation output formats](references/output-formats.md)
- [ClawHub skill page](https://clawhub.ai/kokxi/skills/qa-input-validation)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [Structured JSON validation result with a quality score, missing information, and clarification questions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Result is pass, need_more_info, or fail; input quality is scored from 1 to 10.]

## Skill Version(s):

1.8.0 (source: frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
