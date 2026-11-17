## Description:

Rewrites prose in DOCX files that contain Zotero citations without breaking citation fields, or changes the Zotero bibliography style programmatically.

This skill is ready for commercial/non-commercial use.

## Publisher:

[drstrangerujn](https://clawhub.ai/user/drstrangerujn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and writing assistants use this skill to precheck and rewrite Word DOCX manuscripts that contain Zotero Field-mode citations while preserving live citation fields. It can also update the stored Zotero bibliography style before the user refreshes citations in Word.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads and rewrites the full DOCX supplied by the user.

Mitigation: Use trusted documents where possible, avoid very large or untrusted DOCX files, and review the rewritten DOCX before relying on it.

Risk: Bypassing precheck or refusal messages could damage live Zotero citation fields or Word document structure.

Mitigation: Run precheck or dry-run first, honor Refused messages, and rely on the skill's post-write ZIP, XML, relationship, and field-inventory validation before accepting output.

Risk: Optional external validation may run local LibreOffice and pdfinfo processing on the document.

Mitigation: Run external validation only in an environment approved for the document contents and installed local tools.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/drstrangerujn/skills/zotero-docx)
- [findings.md](artifact/references/findings.md)
- [Zotero Nature CSL style](http://www.zotero.org/styles/nature)
- [Zotero GB/T 7714 CSL style](http://www.zotero.org/styles/china-national-standard-gb-t-7714-2015-numeric)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with Python snippets, shell commands, precheck reports, dry-run change lists, and rewritten DOCX files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May refuse processing when DOCX structure, Zotero storage mode, revision state, output path, or rewrite size fails documented safety checks.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
