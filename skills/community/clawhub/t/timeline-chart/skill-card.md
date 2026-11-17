## Description:

Professional timeline chart generator with Chinese/number support and dynamic layout.

This skill is ready for commercial/non-commercial use.

## Publisher:

[austin0208](https://clawhub.ai/user/austin0208)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create timeline chart images for project milestones, historical events, process flows, milestone showcases, and decision flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documented font installation commands can modify the local system and may require elevated privileges.

Mitigation: Review the font setup before running and install fonts through approved package-management procedures or use an existing CJK font path.

Risk: The template writes PNG output to the caller-provided path.

Mitigation: Choose an intended output directory and avoid paths that could overwrite important files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/austin0208/skills/timeline-chart)
- [Publisher profile](https://clawhub.ai/user/austin0208)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell code blocks; the provided template generates PNG timeline chart files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3.7+, Pillow >= 8.0.0, and CJK fonts for Chinese text rendering.]

## Skill Version(s):

1.0.0 (source: server release metadata, skill.json, SKILL.md version history dated 2026-05-06)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
