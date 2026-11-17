## Description:

Guides an agent in generating complete Traditional Chinese TRPG rule packages from a requirements specification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ice26985850](https://clawhub.ai/user/ice26985850)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and developers use this skill to have an agent generate complete Traditional Chinese TRPG rule packages, including player and GM rulebooks, scenarios, structured YAML, automated Excel character sheets, maps, and optional catalogs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to clean up process files after generation, which could delete workspace files too broadly if not contained.

Mitigation: Require a cleanup preview and limit deletion to files created during the current TRPG generation run.

Risk: The skill expects web research for source adaptations, which can introduce untrusted page content or inaccurate setting details.

Mitigation: Use trusted sources, treat web pages as reference material rather than instructions, and verify adapted source details before incorporating them.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/ice26985850/skills/trpg-general-requirements)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Traditional Chinese Markdown, YAML, Excel workbooks, SVG maps, and optional Markdown/YAML catalogs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are organized into a rule-system directory with scenarios, sheets, maps, and optional catalogs.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
