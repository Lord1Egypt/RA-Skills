## Description:

Controls a remote Chrome browser via HTTP API for web automation, form filling, navigation, page inspection, screenshots, DOM actions, and VNC actions on sites the user owns or has permission to access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vasyaod](https://clawhub.ai/user/vasyaod)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use this skill to operate a hosted Chrome browser through HTTP endpoints for permitted web automation, inspection, interaction, and visual fallback workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote browser sessions can expose page contents, screenshots, actions, and logged-in browser state to the remote browser provider.

Mitigation: Install only when the provider is trusted, prefer ephemeral sessions, and avoid using sensitive accounts unless necessary.

Risk: Persistent stored sessions can retain full browser profile state, including cookies and web storage, after a workflow ends.

Mitigation: Delete stored sessions when finished and use explicit session termination when persistent state is no longer needed.

Risk: URL access tokens can be exposed through logs, browser history, or shared links.

Mitigation: Use Authorization headers or X-API-Key authentication instead of URL tokens when possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vasyaod/skills/remote-browser)
- [Remote Browser Service endpoint](https://rb.all-completed.com)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown with HTTP API examples, JSON payloads, and concise operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to retrieve text, accessibility snapshots, screenshots, VNC framebuffer images, session status, and stored-session metadata from the remote browser service.]

## Skill Version(s):

1.0.9 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
