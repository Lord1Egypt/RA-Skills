## Description:

Star Office UI helps an agent set up and operate a pixel office dashboard for multi-agent status visualization, mobile viewing, public sharing, and collaborator joins.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[dponxiaodong](https://clawhub.ai/user/dponxiaodong)

### License/Terms of Use:

Code: MIT; art assets: non-commercial learning/demo use only

## Use Case:

Developers and agent operators use this skill to launch a local pixel office dashboard, update agent status, invite other agents, and optionally expose the dashboard for viewing. It is best treated as a demo or internal collaboration visualization until access controls and content handling are hardened.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public exposure may leave control and memo endpoints unauthenticated.

Mitigation: Use the dashboard only locally or in an isolated environment until authentication and authorization are added for control and memo endpoints.

Risk: Bundled reusable join keys could allow unintended agent access.

Mitigation: Replace bundled join keys with deployment-specific secrets and rotate them before sharing any instance.

Risk: Local memory summaries and rendered status details may reveal sensitive information.

Mitigation: Disable or curate memory summaries and avoid putting private content into rendered status details.

Risk: XSS-prone pages may render unsafe content.

Mitigation: Fix unsafe HTML rendering paths before public use and review user-controlled fields before display.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dponxiaodong/skills/star-office-ui)
- [Star Office UI README](artifact/README.md)
- [Star Office UI Overview](artifact/docs/STAR_OFFICE_UI_OVERVIEW.md)
- [Animated Mini Characters 2 (Platformer) [FREE]](https://limezu.itch.io/animated-mini-characters-2-platform-free)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, local file edits, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce commands for running a Flask backend, updating local JSON state, inviting agents, and exposing a local dashboard through a tunnel.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
