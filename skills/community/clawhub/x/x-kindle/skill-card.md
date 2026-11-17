## Description:

Send X/Twitter posts to Kindle for distraction-free reading.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brianlu365ai](https://clawhub.ai/user/brianlu365ai)

### License/Terms of Use:


## Use Case:

External users use this skill to turn X/Twitter posts or threads into Kindle-readable email content for later reading on a Kindle device.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SMTP credentials may be exposed if stored directly in TOOLS.md.

Mitigation: Use a dedicated low-risk email account and store the app password in a protected secret store.

Risk: Requested post content and related metadata may be visible to fxtwitter and the configured email provider.

Mitigation: Use the skill only with explicit user consent and avoid sending sensitive content through these third-party services.

Risk: Unescaped post content or unvalidated URLs could produce unsafe or malformed email content.

Mitigation: Validate X/Twitter status URLs and HTML-escape fetched post content before sending the email.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown instructions with URL patterns, HTML email structure, and configuration fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Kindle email address and user-managed SMTP credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
