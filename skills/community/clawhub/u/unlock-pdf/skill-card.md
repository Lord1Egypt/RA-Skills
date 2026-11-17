## Description:

Remove password protection from encrypted PDFs via the PDFAPIHub cloud API; the PDF and password are sent to pdfapihub.com for decryption.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rishabhdugar](https://clawhub.ai/user/rishabhdugar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to unlock password-protected PDFs they are authorized to access before downstream PDF processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A PDF file and its decryption password are transmitted to PDFAPIHub for processing.

Mitigation: Use the skill only for documents you are allowed to unlock, avoid highly sensitive PDFs unless cloud processing is acceptable, and handle passwords securely.

Risk: API keys and real passwords could be exposed if copied into examples, logs, or saved files.

Mitigation: Store the CLIENT-API-KEY and document passwords in secure secret handling systems and avoid committing or sharing real credentials.

## Reference(s):

- [PDFAPIHub Documentation](https://pdfapihub.com/docs)
- [PDFAPIHub API](https://pdfapihub.com/api)
- [ClawHub Skill Page](https://clawhub.ai/rishabhdugar/skills/unlock-pdf)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Files, Configuration]

**Output Format:** [Markdown guidance with JSON request examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The API can return an unlocked PDF as a file, URL, or base64 payload depending on the output mode.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
