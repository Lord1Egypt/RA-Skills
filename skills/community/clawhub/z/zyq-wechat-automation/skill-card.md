## Description:

Automates Windows PC WeChat tasks through pywechat127, including sending messages, batch messaging, reading chat history, retrieving contacts, auto-replies, and Moments management.

This skill is for research and development only.

## Publisher:

[838997125](https://clawhub.ai/user/838997125)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to check a Windows WeChat environment and automate authorized WeChat messaging, contact lookup, and chat-history retrieval from a logged-in desktop session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and send private WeChat messages and contact data.

Mitigation: Use only on Windows accounts and WeChat sessions the operator is authorized to automate, and treat chat and contact output as sensitive data.

Risk: Bulk messaging can send unwanted or policy-violating messages.

Mitigation: Review recipients and message content before sending, avoid unsolicited promotion, and use delays and limits for any batch workflow.

Risk: Generated Windows batch files may execute unsafe recipient, path, or message values.

Mitigation: Do not run generated .bat files with untrusted input; inspect generated files before execution.

Risk: The artifact relies on a hard-coded local pywechat import path and unpinned dependencies.

Mitigation: Remove or control the hard-coded D:\code\pywechat3 path and pin dependencies before deployment.

## Reference(s):

- [pywechat127 PyPI](https://pypi.org/project/pywechat127/)
- [pywechat GitHub](https://github.com/Hello-Mr-Crab/pywechat)
- [FAQ](references/faq.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python snippets, shell commands, and optional JSON or Windows batch files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Windows 10 or 11, Python 3, PC WeChat 3.9.12.x or 4.0+, and a logged-in desktop WeChat session.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
