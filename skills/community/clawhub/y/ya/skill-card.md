## Description:

Automates authenticated WHUT AI Augmented page access, popup handling, login, and page text/question capture through agent-browser.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dongxingao](https://clawhub.ai/user/dongxingao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and authorized users working with WHUT AI Augmented pages use this skill to open a target page in an authenticated browser session and capture current page text or extracted questions for later processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stored WHUT credentials could be submitted to an unintended page if URL handling is not constrained.

Mitigation: Run only with explicit WHUT AI Augmented target URLs, add URL validation before opening pages, filling credentials, and submitting login forms, and avoid stored credentials until validation exists.

Risk: The generated latest_page_dump.json can contain authenticated page data and extracted questions.

Mitigation: Treat the dump as sensitive local data, avoid sharing it, and remove it when it is no longer needed.

Risk: Automatic answer submission can make unintended changes on authenticated pages.

Mitigation: Require explicit user approval before any answer-filling or submission action.

## Reference(s):

- [WHUT workflow conventions](artifact/references/workflow.md)
- [ClawHub skill page](https://clawhub.ai/dongxingao/skills/ya)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Text, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON runtime output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write latest_page_dump.json containing captured authenticated page text and extracted questions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
