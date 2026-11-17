## Description:

Automates Windows PC WeChat through pywinauto UI automation for messages, files, Moments, contacts, and related account workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hello-mr-crab](https://clawhub.ai/user/hello-mr-crab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation-focused users use this skill to generate and run Python scripts that operate a logged-in Windows WeChat desktop session for messaging, file handling, contact workflows, Moments actions, and monitoring. Use should stay limited to explicitly authorized account actions where the WeChat UI is visible and platform rules are respected.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can export private WeChat data and perform account-changing actions from a logged-in Windows WeChat session.

Mitigation: Require explicit confirmation before sending, posting, clearing history, accepting friends or groups, exporting chats or files, or claiming red packets.

Risk: Automated WeChat actions can be misused for bulk outreach, surveillance, or platform-rule evasion.

Mitigation: Use only for authorized workflows, avoid bulk or surveillance use cases, and follow WeChat rules and policies.

Risk: Dependency and UI automation behavior can vary across Windows, Python, and WeChat versions.

Mitigation: Use a dedicated virtual environment with pinned dependencies and run the provided requirement and visibility checks before automation.

## Reference(s):

- [pyweixin RPA API Reference](references/api_reference.md)
- [WeChat 4.1+ UI Automation Notes](references/Weixin4.0.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are constrained by Windows WeChat UI state, dependency availability, and user-provided automation targets.]

## Skill Version(s):

1.0.4 (source: server release metadata and metadata.openclaw.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
