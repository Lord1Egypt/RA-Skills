## Description:

Super Screenshot helps agents capture, inspect, and compare screenshots across desktop apps, browsers, simulators, and CI runs with appropriate tools, stable viewports, wait strategies, masking, and output formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[subaru0573](https://clawhub.ai/user/subaru0573)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, QA engineers, documentation writers, and support teams use this skill to choose reliable screenshot capture workflows for debugging, visual review, bug reports, release notes, and before/after comparisons.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Screenshots of real desktops or logged-in browser sessions can reveal tabs, URLs, notifications, test data, or secrets.

Mitigation: Prefer region, element, or window capture; mask sensitive areas; and review screenshots before sharing or saving them.

Risk: Unstable viewports, animation, dynamic data, or premature capture can make screenshots misleading for visual comparison.

Mitigation: Use fixed viewport, scale, zoom, and theme settings, wait for the target UI state, and remove avoidable visual noise before capture.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/subaru0573/skills/super-screenshot)
- [Publisher profile](https://clawhub.ai/user/subaru0573)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and tool-selection tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces workflow guidance only; it does not include executable code or credential handling.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
