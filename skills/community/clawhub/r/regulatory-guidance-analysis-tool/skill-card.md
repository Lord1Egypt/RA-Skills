## Description:

Gugu Gaga converts pharmaceutical regulatory PDF, DOCX, DOC, or TXT files into structured analysis reports and generates training PPTX or study PDF outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gxpcode-hezhong](https://clawhub.ai/user/gxpcode-hezhong)

### License/Terms of Use:

MIT-0

## Use Case:

Pharmaceutical regulatory professionals and supporting analysts use this skill to turn source regulations and guidance into structured review notes, compliance-level summaries, lifecycle diagrams, and presentation or PDF materials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Required setup installs mutable dependencies from a third-party package mirror.

Mitigation: Install in a dedicated virtual environment or container, and prefer pinned, hash-verified dependencies from a trusted source.

Risk: Regulatory files may contain sensitive or confidential content.

Mitigation: Use local regulatory files, avoid MarkItDown plugin or cloud options unless that data flow is intended, and review generated HTML before conversion.

Risk: Generated regulatory analysis may be incomplete or misleading if treated as final advice.

Mitigation: Have a qualified regulatory reviewer confirm the structured analysis, traffic-light classifications, and final PPTX or PDF before relying on them.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/gxpcode-hezhong/skills/regulatory-guidance-analysis-tool)
- [Server-resolved source repository](https://github.com/Gxpcode-hezhong/Regulatory-Guidance-Analysis-Tool)
- [Server-resolved source commit](https://github.com/Gxpcode-hezhong/Regulatory-Guidance-Analysis-Tool/tree/84bb568adf16af19ba8a098815fe06a8a3136879)
- [Microsoft MarkItDown](https://github.com/microsoft/markitdown)
- [Microsoft MarkItDown security considerations](https://github.com/microsoft/markitdown#security-considerations)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown analysis files, HTML decks, PPTX presentations, and PDF documents]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local document inputs and user review before final PPTX or PDF conversion.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata; artifact frontmatter reports 2.5.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
