## Description:

Control a remote Chrome browser via HTTP API for web automation, form filling, navigation, page inspection, DOM actions, VNC actions, screenshots, accessibility snapshots, and text extraction on sites the user owns or has permission to access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vasyaod](https://clawhub.ai/user/vasyaod)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to control a remote Chrome session for permitted web automation, page inspection, form workflows, and visual fallback through VNC.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The remote-browser provider can receive page contents, screenshots, user actions, and browser session data.

Mitigation: Install only when the provider is trusted, use the service only on sites the user owns or has permission to access, and prefer header-based authentication instead of URL tokens.

Risk: Stored browser sessions can preserve logged-in state and raw browser storage such as cookies, localStorage, sessionStorage, IndexedDB, Service Workers, Cache Storage, and metadata.

Mitigation: Use ephemeral sessions for sensitive work, delete stored sessions when finished, and use encrypted stored sessions where appropriate.

Risk: Directly typing passwords, login codes, or payment details would expose sensitive values to the agent transcript.

Mitigation: Use the service's request-fill flow for secrets and payment fields, or have the user sign in through the live VNC view when request-fill is unavailable.

Risk: Browser actions can report success without changing page state because of overlays, off-viewport elements, or dynamic application updates.

Mitigation: Verify state-changing actions with status, text, DOM, or scoped screenshot checks before relying on the result.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/vasyaod/skills/remote-browser-service)
- [Remote Browser Service API Base](https://rb.all-completed.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with HTTP API examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference screenshots, accessibility trees, extracted text, DOM snapshots, browser session metadata, and VNC framebuffer captures returned by the remote service.]

## Skill Version(s):

1.0.9 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
