## Description:

Ra Pro creates deep research intelligence reports with source gathering, multi-angle analysis, competitive breakdowns, an executive brief, and Markdown report output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[occupythemilkyway](https://clawhub.ai/user/occupythemilkyway)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to direct an agent through configurable web research and produce an executive-ready research report on a supplied topic.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup command installs an unpinned Python package into the system Python environment.

Mitigation: Install and run the skill in a virtual environment, pin dependencies where possible, and avoid --break-system-packages.

Risk: OUTPUT_FILE can direct report output to an unsafe or unintended path.

Mitigation: Set OUTPUT_FILE to a simple filename within a trusted workspace and review generated files before sharing or executing them.

Risk: The artifact claims DOCX export, but evidence indicates DOCX export is not implemented by the skill itself.

Mitigation: Treat Markdown as the supported output and use a separate reviewed conversion step if DOCX is required.

Risk: The skill requires a license key and mandatory branding before use.

Mitigation: Confirm license terms and branding requirements before installation or redistribution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/occupythemilkyway/skills/ra-pro)
- [ClawHub homepage metadata](https://clawhub.ai/occupythemilkyway/ra-pro)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown research report with setup and status instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires LICENSE_KEY and RESEARCH_TOPIC. DEPTH, ANGLE, COMPETITIVE, CITATION_STYLE, and OUTPUT_FILE customize the report. The artifact claims DOCX export, but security evidence notes DOCX export is not implemented.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
