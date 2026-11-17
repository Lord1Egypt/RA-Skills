## Description:

Vrio Analysis guides an agent through a VRIO assessment of organizational resources and capabilities, then classifies the resulting competitive advantage based on user-confirmed Value, Rarity, Imitability, and Organization answers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duding-engicool](https://clawhub.ai/user/duding-engicool)

### License/Terms of Use:

MIT-0

## Use Case:

Business, strategy, and quality-management teams use this skill to audit internal resources or capabilities, capture user-confirmed VRIO answers, and turn those answers into a structured competitive-advantage report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may ask users to provide confidential business strategy, resources, capabilities, or quality-management details.

Mitigation: Use it only in an appropriate workspace and omit or sanitize confidential strategy details when they are not needed for the VRIO assessment.

Risk: Generated Markdown or HTML reports may contain sensitive competitive-positioning conclusions.

Mitigation: Review generated reports before distribution and store them according to the organization's information-handling rules.

Risk: The inspected artifact references helper files that were not present, which may limit scripted report generation.

Mitigation: Confirm the referenced files are available before relying on scripted Markdown or HTML report generation.

Risk: VRIO classifications depend on user-provided answers and can be misleading if those answers are incomplete or inaccurate.

Mitigation: Have knowledgeable stakeholders review the input answers and final classifications before using the report for strategic decisions.

## Reference(s):

- [Server-resolved GitHub source repository](https://github.com/duding-engicool/skill-vrio-analysis)
- [ClawHub skill page](https://clawhub.ai/duding-engicool/skills/skill-vrio-analysis)

## Skill Output:

**Output Type(s):** [guidance, markdown, code]

**Output Format:** [Interactive guidance followed by Markdown and HTML report content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided resource or capability names and user-confirmed VRIO answers.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
