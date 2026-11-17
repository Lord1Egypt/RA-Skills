## Description:

Use UniFuncs Reader API to read web pages and documents such as PDF and Word and Excel and PPTX URL, with AI-powered content extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vinlic](https://clawhub.ai/user/vinlic)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to extract readable text or markdown from web pages and common document URLs through the UniFuncs Reader API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send target URLs and optional authentication cookies to the third-party UniFuncs API.

Mitigation: Use only URLs that are appropriate to send to UniFuncs, avoid private or internal URLs, and do not pass browser session cookies unless account-access exposure is understood.

Risk: The scanner verdict is suspicious because cookie and URL handling are not clearly scoped in the skill documentation.

Mitigation: Review the skill before installation and document approved data-handling boundaries for users.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/vinlic/skills/unifuncs-reader)
- [UniFuncs account setup](https://unifuncs.com/account)
- [UniFuncs Reader API endpoint](https://api.unifuncs.com/api/web-reader/read)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or plain text from the command-line reader, with errors returned as terminal messages.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports URL input, optional CSS selector filtering, link summaries, topic-focused extraction, source preservation, and a maximum extraction size of 1000000 characters.]

## Skill Version(s):

0.0.4 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
