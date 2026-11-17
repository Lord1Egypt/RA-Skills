## Description:

Generate social media posts for LevelUpLove and PayLessTax brands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wespeakallday](https://clawhub.ai/user/wespeakallday)

### License/Terms of Use:


## Use Case:

Marketing operators and developers use this skill to generate branded social media PNG assets for LevelUpLove and PayLessTax campaigns, including carousel panels, infographics, single images, and oneliner posts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated PNG files may be written to an unexpected local path if the output argument is not reviewed.

Mitigation: Review the output path before running the generator so files are written only where intended.

Risk: The artifact describes scheduled, manual CLI, and API triggers broadly, which can be ambiguous when adapted for automation.

Mitigation: Clarify the intended trigger mode and approval process before wiring the skill into automated publishing workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wespeakallday/skills/social-media-content)
- [PayLessTax website](https://paylesstax.co.za)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration]

**Output Format:** [PNG files with CLI status text and JSON template inputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports brand and content-type choices and writes generated PNGs to a local output directory.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
