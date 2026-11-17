## Description:

Retrieves and answers questions from local Markdown, text, PDF, and Excel knowledge bases using hierarchical indexes and bounded, source-cited searches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dtsola](https://clawhub.ai/user/dtsola)

### License/Terms of Use:

MIT

## Use Case:

Developers and knowledge workers use the skill to find information in a named local knowledge-base directory and receive concise answers with file and location citations. On explicit request and confirmation, it can also build indexes or create derived PDF text and page images within that knowledge base.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated security review has medium confidence and partial Skillspector coverage, so it cannot establish that the skill is risk-free.

Mitigation: Review the skill before deployment, and keep optional index or PDF maintenance writes limited to the explicitly named knowledge-base root after user confirmation.

## Reference(s):

- [PDF Reading Guide](references/pdf_reading.md)
- [Excel Reading Guide](references/excel_reading.md)
- [Excel Analysis Guide](references/excel_analysis.md)
- [Project Documentation](https://github.com/dtsola/xiaoyaoclaw-kb-retriever)
- [ClawHub Release Page](https://clawhub.ai/dtsola/skills/xiaoyaoclaw-kb-retriever)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Concise Markdown answers with file and location citations; optional index, extracted PDF text, or page images]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Retrieval is limited to at most five rounds. Optional maintenance files are written only after explicit request and confirmation, inside the knowledge-base root.]

## Skill Version(s):

1.0.14 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
