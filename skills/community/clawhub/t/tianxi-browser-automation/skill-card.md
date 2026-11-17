## Description:

Automates browser-based web navigation, form filling, social posting, email actions, file uploads, screenshots, and data extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangyu68](https://clawhub.ai/user/zhangyu68)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to automate browser-based tasks such as navigating websites, filling forms, posting content, managing email, uploading files, taking screenshots, and extracting page data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad browser control across sensitive workflows such as email, social posting, registrations, uploads, private pages, payments, and forms.

Mitigation: Require explicit per-action confirmation for sensitive workflows and limit use to browser tasks the user has clearly authorized.

Risk: Browser automation may auto-confirm dialogs, capture sensitive screenshots, or clear cookies without adequate consent.

Mitigation: Pause before dialogs, screenshots, and browser data-clearing actions; proceed only after the user confirms the specific action.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, text, tool calls]

**Output Format:** [Markdown-style progress updates and structured browser tool calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce screenshots, task summaries, error explanations, and requests for confirmation before sensitive browser actions.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
