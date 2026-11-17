## Description:

Automates authenticated uploads, publishing, and forms in web-only consoles using an installed Chrome or Edge browser, and helps test rich-text formatting before publication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oracis](https://clawhub.ai/user/oracis)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to upload files, complete forms, and publish content through authenticated web consoles that lack a usable API. It also guides checks of rich-text formatting and platform-generated layout changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent can read and change content in an authenticated browser session.

Mitigation: Use a temporary browser profile when possible, and confirm the active tab and domain before running browser actions.

Risk: Uploads and submissions can expose local files or publish unintended content.

Mitigation: Require user confirmation before selecting local files, submitting forms, or publishing content.

Risk: An exposed browser debugging port can grant others control of the browser session.

Mitigation: Keep the debugging port bound to localhost and avoid allowing all origins unless the risk is understood.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/oracis/skills/web-console-cdp-upload)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code]

**Output Format:** [Markdown with shell and JavaScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include browser-state checks, upload steps, and rich-text formatting comparisons.]

## Skill Version(s):

1.3.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
