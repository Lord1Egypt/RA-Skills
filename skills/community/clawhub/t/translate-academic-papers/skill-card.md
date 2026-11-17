## Description:

Translate complete English academic papers into polished Simplified Chinese while preserving structure, evidence, equations, tables, citation numbering, and the English reference list; deliver Chinese full-text and paragraph-aligned English-Chinese DOCX editions with translated figure text and citation navigation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fangmingqi2005-create](https://clawhub.ai/user/fangmingqi2005-create)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to translate full English scholarly papers into Simplified Chinese DOCX deliverables while preserving scientific structure, citations, equations, tables, figures, and references. It is aimed at complete paper translation rather than summaries or selective reading notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says the skill can automatically process local documents with broad local tooling and can write local caches and DOCX outputs beside the paper unless redirected.

Mitigation: Use it only on papers the user is allowed to process, choose a controlled output directory when needed, and review generated caches and DOCX files before sharing them.

Risk: The security guidance flags runtime loading through --argos-runtime as unsafe when the runtime is not trusted.

Mitigation: Point --argos-runtime only at a trusted, pinned Argos installation, or avoid that local runtime path when it cannot be verified.

Risk: The security guidance warns against running the Windows PowerShell command with ExecutionPolicy Bypass.

Mitigation: Run the renderer through normal local execution controls and avoid policy-bypass shortcuts.

Risk: The workflow can involve Image2/model use and possible network lookup while processing sensitive or unpublished papers.

Mitigation: Require explicit approval for image/model use and any network lookup before processing sensitive, confidential, or unpublished papers.

## Reference(s):

- [Translation standard](references/translation-standard.md)
- [Figure translation contract](references/figure-translation.md)
- [Two-output contract](references/output-variants.md)
- [Final delivery contract](references/delivery-contract.md)
- [Final QA checklist](references/qa-checklist.md)
- [Performance budget](references/performance-budget.md)
- [Figure-interior localization and reference navigation example](examples/figure-localization.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [DOCX deliverables with JSON/JSONL working artifacts and concise text or Markdown QA reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a Chinese-only DOCX, a paragraph-aligned bilingual DOCX, Image2 audit manifests, translation caches, citation links, validation output, and local shell commands for document processing.]

## Skill Version(s):

1.1.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
