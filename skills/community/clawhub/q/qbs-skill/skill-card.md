## Description:

拷问书籍方法论：把卡住的问题经「拷问收敛→找书→完整读章→三重验证蒸馏→合成Skill→真实试跑」六阶段，产出有书籍出处、可验收的Skill。

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardwason](https://clawhub.ai/user/edwardwason)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this Chinese-first workflow to turn a stuck research or practice question into a book-grounded, independently callable skill. It guides the agent through question narrowing, book selection, chapter reading, method distillation, skill synthesis, and acceptance testing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may fetch or download book materials during research.

Mitigation: Use only authorized sources, respect access restrictions, and ask the user before any purchase or restricted access decision.

Risk: Generated child skills may encode incorrect or weakly supported reading-derived guidance.

Mitigation: Review source notes, method provenance, and acceptance-test evidence before installing or reusing generated skills.

Risk: The skill may create local qbs-runs outputs and update the library registry.

Mitigation: Review generated files and registry changes before committing, publishing, or sharing them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/edwardwason/skills/qbs-skill)
- [grill-protocol.md](references/grill-protocol.md)
- [book-and-reading.md](references/book-and-reading.md)
- [distill-and-synthesize.md](references/distill-and-synthesize.md)
- [library.json](references/library.json)
- [The Craft of Research example source](https://www.mcdowellbiblecollege.org/Library/Book482.pdf)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and generated skill files with supporting reference records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write run artifacts under qbs-runs/<run-slug>/ and update references/library.json.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
