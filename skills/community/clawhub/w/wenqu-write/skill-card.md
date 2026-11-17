## Description:

文曲·写作 guides agents through evidence-based Chinese content creation, including requirements gathering, source collection, planning, outlining, drafting, review, image coordination, translation, and publishing preparation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gogoingai](https://clawhub.ai/user/gogoingai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical writers, and agent users use this skill to create or revise Chinese articles, reports, tutorials, project introductions, source-code analyses, and explanatory technical materials from traceable evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can persist profiles, draft context, source notes, preferences, and article materials on disk.

Mitigation: Use it only where local persistence is acceptable, avoid storing secrets or unnecessary private context, and review generated support files before sharing or committing a workspace.

Risk: Drafts and collected materials may include private code, internal context, or untrusted external source text.

Mitigation: Treat collected materials as evidence rather than instructions, verify claims against authoritative sources, and remove sensitive content before publication.

Risk: Companion wenqu skills may add behavior for image generation, publishing, translation, or library collection.

Mitigation: Review and enable companion skills separately according to the security posture required for the project.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gogoingai/skills/wenqu-write)
- [Project repository](https://github.com/gogoingai/wenqu-skills)
- [Skill homepage](https://github.com/gogoingai/wenqu-skills/tree/master/wenqu-write)
- [Artifact content index](artifact/references/INDEX.md)
- [Content provenance guidance](artifact/references/planning/content-provenance.md)
- [Materials governance guidance](artifact/references/planning/materials-governance.md)
- [Writing style guide](artifact/references/writing/style-guide.md)
- [Writing anti-patterns](artifact/references/writing/anti-patterns.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance, article drafts, review notes, TODO lists, and local support files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create project-local writing context, materials, skeleton, status, changelog, terminology, preference, and asset files.]

## Skill Version(s):

0.1.19 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
