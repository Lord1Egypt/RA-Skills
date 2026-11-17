## Description:

Supports Chinese-English text and batch file translation with terminology alignment and format preservation for documents, code comments, email, and similar text workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to translate Chinese and English text, preserve Markdown or code-comment structure, and handle batches of document or message content. Users should review outputs for important business, technical, or sensitive material.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports broad read, write, and exec authority along with translation content that also advertises broader automation behavior.

Mitigation: Install only after reviewing the requested permissions, and run the skill with minimal workspace access suitable for the translation task.

Risk: Confidential text or files may be processed by an external or unclear translation path.

Mitigation: Avoid using confidential content until the processing location, retention behavior, and data-sharing path are confirmed.

Risk: Automated translation can introduce inaccurate, misleading, or context-inappropriate wording.

Mitigation: Require human review for legal, medical, financial, contractual, or other high-impact translations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/translate-hub)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Plain text or Markdown, with possible JSON examples, code snippets, shell commands, and configuration guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May preserve source formatting and may produce file-oriented translation guidance when batch translation is requested.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter lists 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
