## Description:

Parse, read, search, navigate, summarize, and extract tables or structured evidence from PDFs, images, Office files, HTML, OFD, and other supported local documents or document URLs through xparse-cli.

This skill is ready for commercial/non-commercial use.

## Publisher:

[intsig-textin](https://clawhub.ai/user/intsig-textin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and document-analysis agents use this skill to parse local documents or document URLs, navigate parsed content, extract tables and evidence, and manage durable multi-document parsing tasks through TextIn xParse.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected documents, parse outputs, task metadata, and WorkBuddy task context are sent to the TextIn xParse service.

Mitigation: Install and use the skill only when that remote processing is acceptable for the documents being handled.

Risk: Standalone installation or package mirrors can introduce supply-chain risk.

Mitigation: Prefer the connector-managed pinned CLI; when using standalone npm, pin the CLI version and avoid unnecessary mirrors.

Risk: Credentials or secrets could be exposed through shared logs or transcripts.

Mitigation: Do not paste real secrets into logs or conversations, and rely on the documented authentication flows instead of collecting tokens.

Risk: Password-protected document handling may place passwords in command-line arguments.

Mitigation: Use the password flow cautiously, avoid recording real passwords in examples or logs, and delete any temporary task-context files promptly.

## Reference(s):

- [Skill Instructions](SKILL.md)
- [API Reference](references/api-reference.md)
- [Authentication](references/authentication.md)
- [CLI Guidance](references/cli-guidance.md)
- [Structured Error Handling](references/error-handling.md)
- [Document Navigation](references/navigation.md)
- [Durable Task Runtime](references/task-runtime.md)
- [TextIn AppKey Setup](references/textin-key-setup.md)
- [TextIn Parse API v1](https://docs.textin.com/xparse/v1/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON, shell commands, and structured guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can save parsed Markdown or JSON outputs to local directories and can return task identifiers for durable multi-document workflows.]

## Skill Version(s):

0.1.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
