## Description:

Provides China-focused workplace safety guidance by locating relevant laws and standards and explaining practical compliance steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fengeail](https://clawhub.ai/user/fengeail)

### License/Terms of Use:

MIT

## Use Case:

Safety officers and workplace teams use this skill to locate Chinese safety-production laws and industry standards, assess compliance questions, and plan safer work practices.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Incorrect or outdated safety or legal guidance could lead to unsafe or noncompliant decisions.

Mitigation: Verify consequential answers against current official sources and qualified safety or legal professionals.

Risk: Configured local standards or corpus directories may contain files beyond the intended reference material.

Mitigation: Point SAFETY_STANDARDS_ROOT and SAFETY_CORPUS only to directories you are comfortable having searched.

Risk: Scanned or encrypted standards may not provide searchable text for precise citations.

Mitigation: Check the original standard rather than relying on unverified clause text when extraction is unavailable.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/fengeail/skills/safety-standards-advisor)
- [Server-resolved source repository](https://github.com/fengeail/safety-standards-advisor)
- [Legal reference index](references/law_index.json)
- [Standards number index](references/stdno_index.json)
- [Legal hierarchy quick reference](references/topics/法律层级速查.md)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Organizes legal duties, technical standards, and recommended actions; identifies when source text is unavailable.]

## Skill Version(s):

0.1.0 (source: ClawHub release; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
