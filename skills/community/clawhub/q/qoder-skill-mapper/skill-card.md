## Description:

Generates a Qoder skill-mapping markdown file from a provided SKILL.md by extracting frontmatter and body content, filling mapped fields, and removing fields that cannot be mapped.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanyi-github](https://clawhub.ai/user/yuanyi-github)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to migrate or adapt agent skills to Qoder by converting a source SKILL.md into a Qoder-formatted skill description and mapping summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill silently sends a usage report to an external server when loaded.

Mitigation: Review the telemetry behavior before installing and remove or disable scripts/record_usage.py if that external reporting is not acceptable.

Risk: The conversion rules remove fields and sections that cannot be extracted or mapped, which can omit source-skill details.

Mitigation: Review the generated Qoder markdown and mapping table before publishing or relying on the converted skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanyi-github/skills/qoder-skill-mapper)
- [Qoder output template](artifact/assets/qoder-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown file plus markdown mapping table]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated markdown may include install commands and removes fields or sections that cannot be extracted or mapped.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
