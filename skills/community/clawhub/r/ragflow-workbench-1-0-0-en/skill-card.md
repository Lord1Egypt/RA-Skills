## Description:

RAGFlow Workbench automates Windows RAGFlow setup and daily knowledge-base operations, including Docker checks, admin bootstrap, model configuration, document upload and parsing, search, and chat creation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiejingke](https://clawhub.ai/user/jiejingke)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to set up and manage a Windows RAGFlow instance, configure models, manage knowledge bases and documents, run retrieval searches, and create chat sessions from indexed content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles admin credentials and RAGFlow API keys.

Mitigation: Use a strong unique admin password, protect or relocate the .env file, avoid logging JSON output that contains secrets, and rotate credentials created by the default workflow.

Risk: Credentials and API requests can be exposed when using a non-local RAGFlow server over insecure transport.

Mitigation: Use HTTPS for any non-local RAGFlow server and review endpoint configuration before saving credentials.

Risk: Knowledge-base and document deletion can remove user data.

Mitigation: List candidates first, delete only with explicit dataset or document IDs, and obtain user confirmation before destructive actions.

Risk: Bootstrap and model-configuration steps can create accounts, generate API keys, and change model settings.

Mitigation: Confirm the user's intent before running privileged setup flows and review model, account, and API-key settings before execution.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/jiejingke/skills/ragflow-workbench-1-0-0-en)
- [Command Reference](artifact/references/command-reference.md)
- [Output Format Reference](artifact/references/output-format.md)
- [Windows Quick Start Guide](artifact/references/quickstart_windows.md)
- [Troubleshooting Guide](artifact/references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with shell commands and JSON code blocks; scripts support structured JSON output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include tables, status summaries, retrieved chunks, and API error fields preserved verbatim.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
