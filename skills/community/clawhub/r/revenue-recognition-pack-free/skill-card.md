## Description:

A local checker for revenue recognition and settlement worksheets that runs seven built-in checks per project directory and prints one conclusion line per project with source file and line references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Revenue accounting and project finance teams at software, content, and service companies use this skill before monthly or quarterly close to check project materials for arithmetic and consistency issues across revenue recognition and settlement workflows. It is intended to support review, not to replace accounting judgment, audit, tax, or legal advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat arithmetic and consistency findings as accounting, audit, tax, or legal conclusions.

Mitigation: Use the output as review support only, and confirm decisions against company accounting policy, applicable standards, and qualified professional advice.

Risk: Financial and project materials may contain sensitive business information.

Mitigation: Run the checker only against the intended local project directory or input file, and avoid including materials that are not needed for the listed checks.

Risk: The free release omits cross-project summary, risk ranking, common-issue grouping, export features, and additional subchecks listed as withheld.

Mitigation: Rely only on the checks reported as executed, review any withheld or out-of-scope items manually, and do not interpret unexecuted checks as passed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/revenue-recognition-pack-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Plain text or JSON results printed to stdout, with human-readable findings that cite project, check item, source file, line number, severity, and calculated details.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally over user-provided project directories or JSON/text inputs and does not write result files.]

## Skill Version(s):

1.0.21 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
