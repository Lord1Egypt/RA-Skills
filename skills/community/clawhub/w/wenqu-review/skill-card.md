## Description:

Reviews Chinese articles, reports, tutorials, project descriptions, and documentation for factual grounding, coherence, terminology, translation artifacts, AI-writing patterns, and structure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gogoingai](https://clawhub.ai/user/gogoingai)

### License/Terms of Use:

MIT-0

## Use Case:

Writers, editors, and developers use this skill to review Chinese technical or explanatory content and either receive a structured critique or apply targeted text revisions. It is especially suited to article-quality checks before publication or after substantial edits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad review or proofread requests may lead the skill to rewrite article files directly.

Mitigation: Ask for manual review, suggestions only, or no file writes when a read-only critique is desired.

Risk: Reusable review preferences may be written into project-local wenqu-skills preference files.

Mitigation: Review created or updated preference files after use and remove entries that should not persist across future reviews.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gogoingai/skills/wenqu-review)
- [Clawdis homepage](https://github.com/gogoingai/wenqu-skills/tree/master/wenqu-review)
- [Skill homepage](https://github.com/gogoingai/wenqu-skills)
- [Review workflow index](references/index.md)
- [R0 fact checking](references/r0-factcheck.md)
- [R1 English terminology](references/r1-english.md)
- [R2 translation artifacts](references/r2-translation.md)
- [R3 AI writing patterns](references/r3-ai-patterns.md)
- [R4 structure](references/r4-structure.md)
- [R5 coherence](references/r5-coherence.md)
- [R6 style and narrative fit](references/r6-style-and-narrative-fit.md)
- [R7 change closure](references/r7-change-closure.md)
- [Glossary](references/language/glossary.md)
- [Humanizer Chinese guide](references/language/humanizer-zh.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown review report, optionally accompanied by edited document text or file changes when the runtime permits edits]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask the user to choose among rewrite candidates or confirm review scope; can persist project-local review preferences when the user gives reusable guidance.]

## Skill Version(s):

0.1.19 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
