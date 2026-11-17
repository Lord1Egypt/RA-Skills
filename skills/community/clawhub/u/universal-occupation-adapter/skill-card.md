## Description:

Generates complete occupation-specific cognitive Skills from any occupation name using a five-dimension occupation model and preset templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kingofzhao](https://clawhub.ai/user/kingofzhao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill authors use this skill to generate occupation-specific cognitive skill packages from a profession name, including five-dimensional models, verification protocols, and supporting documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Batch generation and auto_publish can publish generated skills before adequate human review.

Mitigation: Review generated files and avoid auto_publish until the target workspace, generated content, and publication destination are confirmed.

Risk: Generated occupation guidance may be incorrect or misleading for regulated or safety-sensitive professions.

Mitigation: Have qualified domain reviewers check redlines, verification methods, and generated claims before deployment or reuse.

Risk: Generated skills may include private or organization-specific context when run in sensitive workspaces.

Mitigation: Run generation in a clean workspace and scan generated artifacts before sharing or publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kingofzhao/skills/universal-occupation-adapter)
- [Project homepage](https://github.com/KingOfZhao/AGI_PROJECT)
- [A Survey of Self-Evolving Agents](https://arxiv.org/abs/2507.21046)
- [SAGE: Multi-Agent Self-Evolution](https://arxiv.org/abs/2603.15255)
- [Group-Evolving Agents](https://arxiv.org/abs/2602.04837)
- [Self-evolving Embodied AI](https://arxiv.org/abs/2602.04411)
- [Memory in the Age of AI Agents](https://arxiv.org/abs/2512.13564)
- [Beyond RAG for Agent Memory](https://arxiv.org/abs/2602.02007)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown skill files with code snippets and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate SKILL.md, README.md, VERIFICATION_PROTOCOL.md, and HEARTBEAT.md for a requested occupation; generated outputs require review before publication.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
