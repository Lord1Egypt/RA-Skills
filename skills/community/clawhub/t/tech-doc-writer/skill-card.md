## Description:

Guides an agent to produce detailed Chinese-oriented technical learning documentation, study notes, and knowledge summaries with formulas, code examples, comparison tables, and decision guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hiqishen](https://clawhub.ai/user/hiqishen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical writers, and learners use this skill to draft comprehensive technical documentation for deep learning, machine learning, algorithms, command-line tools, and other technical topics. It emphasizes up-to-date coverage, structured outlines, formulas, examples, comparisons, and self-checks for omissions or outdated material.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may browse user-provided reference URLs and incorporate source material into generated documentation.

Mitigation: Provide trusted URLs and review generated documentation for accuracy, attribution needs, and outdated or unsupported claims.

Risk: The skill may run simple local checks on generated Markdown, such as section-structure validation commands.

Mitigation: Review proposed shell commands before execution and run them only in an appropriate workspace.

Risk: The skill is oriented toward Chinese technical documentation by default.

Mitigation: State the desired output language explicitly when a different language is required.

Risk: Private or sensitive documents could be exposed in generated summaries if supplied as source material.

Mitigation: Avoid providing sensitive private documents unless necessary, and review outputs before sharing.

## Reference(s):

- [Tech Doc Writer Skill Page](https://clawhub.ai/hiqishen/skills/tech-doc-writer)
- [Activation Functions Example](artifact/references/activation-functions-example.md)
- [Normalization Example](artifact/references/normalization-example.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with formulas, tables, code blocks, checklists, and occasional shell commands for validation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce long, multi-part documents and Chinese-language technical prose unless the user requests another language.]

## Skill Version(s):

1.3.4 (source: server release metadata; artifact frontmatter reports 1.5.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
