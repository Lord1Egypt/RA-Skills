## Description:

Reviews Agent Skills for specification compliance, completeness, code quality, directory structure, scripts, and file references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hwl1413520](https://clawhub.ai/user/hwl1413520)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and reviewers use this skill to check Agent Skills before installation or publication and to produce advisory Markdown or JSON review reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The review may read outside the target skill through symlinks.

Mitigation: Run the tool only in an isolated workspace on packages without symlinks, and manually inspect nested files before trusting the report.

Risk: A passing result can be mistaken for security approval.

Mitigation: Treat results as advisory structural checks and perform separate manual and security review before installation or publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hwl1413520/skills/skill-review-ai)
- [Agent Skills Specification](references/SPECIFICATION.md)
- [Review Rules](references/RULES.md)
- [FAQ](references/FAQ.md)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown or JSON review report with scores, status, categories, and issues]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only advisory review; optional verbose and JSON modes are documented.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
