## Description:

Generates Chinese-language SOUL.md persona configuration files from public-person research, SBTI or MBTI presets, role archetypes, or a custom user description.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adenzhou1350](https://clawhub.ai/user/adenzhou1350)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to create a SOUL.md persona file that captures a desired voice, style, values, response rules, and boundaries. It supports research-based public-person personas, preset SBTI/MBTI styles, role archetypes, and custom descriptions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger phrases or an ambiguous persona name could create or overwrite an unintended SOUL.md file.

Mitigation: Confirm the intended persona name and review the target file path before allowing the skill to write output.

Risk: Research-based persona generation may depend on web search results that are incomplete or inaccurate.

Mitigation: Review generated persona traits, source assumptions, and boundaries before using the SOUL.md file in an agent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/adenzhou1350/skills/soul-generator)
- [Good SOUL.md example](artifact/references/good/01-enfp.md)
- [Combined persona example](artifact/references/examples/01-combined.md)
- [Generic assistant anti-pattern](artifact/references/bad/01-generic.md)
- [Rigid robot anti-pattern](artifact/references/bad/02-robot.md)

## Skill Output:

**Output Type(s):** [Markdown, Files, Guidance]

**Output Format:** [Markdown SOUL.md persona configuration file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes one SOUL.md file for the requested persona; generated content may be based on web search, built-in presets, or user-provided traits.]

## Skill Version(s):

2.0.0 (source: ClawHub release evidence; artifact frontmatter says 3.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
