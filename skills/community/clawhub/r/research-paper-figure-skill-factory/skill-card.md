## Description:

Research Paper Figure Skill Factory builds reusable, evidence-backed, class-specific figure-making skills for scientific papers, then uses those generated skills for concrete target-paper figures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[c-narcissus](https://clawhub.ai/user/c-narcissus)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, authors, and agent-skill developers use this skill to build reusable paper-figure-making skills from lawful corpus evidence and then apply those generated skills to target-paper diagrams and figures. It emphasizes corpus-backed taxonomy building, text-only planning, image-only rendering turns, candidate-image comparison, and packaging for reuse.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can read provided or local paper material and create local corpus and generated-skill files.

Mitigation: Use it only with paper material the user is allowed to provide, confirm the intended corpus scope before acquisition or extraction, and review generated files before installing or sharing them.

Risk: The workflow may retrieve lawful open-access PDFs and depends on evidence quality for taxonomy and generated-skill claims.

Mitigation: Keep retrieval manifests, source URLs, and evidence maps with the generated skill, and treat unsupported taxonomy claims as generic fallback guidance rather than class-specific evidence.

Risk: Prompts or reference-image context may be sent to approved image-generation tools.

Mitigation: Remove confidential or rights-restricted content before image generation and review each image request for privacy, copyright, and publication constraints.

Risk: Many templates force Chinese headings and follow-up prompts, which may be unsuitable for some users.

Mitigation: Adapt generated templates and examples to the target user's language and review requirements before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/c-narcissus/skills/research-paper-figure-skill-factory)
- [Publisher profile](https://clawhub.ai/user/c-narcissus)
- [Skill documentation](docs/README.md)
- [Master workflow](references/master-workflow.md)
- [Generated specialized skill output spec](references/generated-specialized-skill-output-spec.md)
- [Generated skill multi-candidate policy](references/generated-skill-multi-candidate-policy.md)
- [Strict text/image turn separation policy](references/strict-text-image-turn-separation-policy.md)
- [Visual-first decision board protocol](references/visual-first-decision-board-protocol.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, generated skill-package files, prompts, state artifacts, and optional image-generation requests.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated workflows separate text-only planning and review turns from image-only generation turns, and may create local corpus, taxonomy, template, testing, and packaging artifacts.]

## Skill Version(s):

1.0.1 (source: metadata, SKILL.md frontmatter, changelog, and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
