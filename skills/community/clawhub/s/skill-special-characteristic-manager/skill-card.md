## Description:

Identifies and classifies product and process special characteristics (CC/SC) from mixed engineering inputs, translates customer symbols, and produces reviewable characteristic lists, transmission matrices, control recommendations, and gap notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duding-engicool](https://clawhub.ai/user/duding-engicool)

### License/Terms of Use:

MIT-0

## Use Case:

Quality engineers, design engineers, and APQP team members use this skill to identify CC/SC characteristics from drawings, specifications, emails, spreadsheets, FMEA materials, and verbal notes. It supports APQP special-characteristic list preparation, order review, and audit response with explicit uncertainty and confirmation notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may provide proprietary drawings, customer emails, FMEA data, or other sensitive engineering materials.

Mitigation: Use the skill only in an agent environment approved for that data and avoid submitting sensitive materials when that approval is absent.

Risk: The artifact references a rules file and report-building script that are not present in the release artifact.

Mitigation: Verify required reference and script files before relying on automated report rendering or detailed rule-index behavior.

Risk: CC/SC classifications and control suggestions can affect engineering quality workflows if treated as final decisions.

Mitigation: Treat outputs as an evidence-backed suggestion draft and require review and sign-off by the responsible enterprise owner.

## Reference(s):

- [Server-resolved source repository](https://github.com/duding-engicool/skill-special-characteristic-manager)
- [ClawHub skill page](https://clawhub.ai/duding-engicool/skills/skill-special-characteristic-manager)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown report outline and final Markdown report after user confirmation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are advisory and should be reviewed by the responsible enterprise owner before formal release or sign-off.]

## Skill Version(s):

0.1.0 (source: release metadata; artifact frontmatter declares 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
