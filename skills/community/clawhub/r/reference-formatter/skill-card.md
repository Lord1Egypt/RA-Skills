## Description:

Formats user-provided reference lists into specified citation styles such as APA, GB/T 7714, MLA, Chicago Author-Date, or a user-supplied custom style.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zyyfaith](https://clawhub.ai/user/zyyfaith)

### License/Terms of Use:

MIT-0

## Use Case:

Students, researchers, and academic writers use this skill to normalize mixed or messy bibliography entries into a target citation style and produce a reusable references document.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may create reference output files in the workspace.

Mitigation: Confirm the desired filename and location before writing when the bibliography is private, sensitive, or user-specified.

Risk: Optional web lookup for incomplete bibliography details could expose private references, internal URLs, or annotations.

Mitigation: Keep processing local unless the user explicitly approves lookup for the affected entries.

Risk: Automated citation parsing can misclassify incomplete or unusual references.

Mitigation: Flag uncertain entries for human review and preserve original source text rather than inventing missing metadata.

## Reference(s):

- [Citation Format Reference](reference/formats.md)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands, guidance]

**Output Format:** [Formatted bibliography text or document files, with a concise change report in Markdown or plain text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create references.docx by default, with fallback text or Markdown output when document conversion tools are unavailable.]

## Skill Version(s):

1.3.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
