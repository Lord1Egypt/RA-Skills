## Description:

Helps developers build SendPulse marketplace interfaces using the CDN-hosted UI kit, including layouts, themes, forms, and component styling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ymaievska-lang](https://clawhub.ai/user/ymaievska-lang)

### License/Terms of Use:

MIT

## Use Case:

Developers use this skill to build and refine SendPulse marketplace app, embedded-widget, and standalone interfaces with the prebuilt UI stylesheet. It guides component styling, layout, theming, and validation of the resulting screens.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated pages depend on externally hosted CSS and fonts, which may be unavailable or change independently.

Mitigation: Pin or monitor dependencies where possible, and verify the rendered interface in its target host before release.

Risk: Links may preserve access semantics that are unclear, and credentials in external URLs could be exposed.

Mitigation: Confirm what access each link provides and keep credentials out of external URLs.

## Reference(s):

- [SendPulse UI library documentation](https://login.sendpulse.com/dist/ui-library/index.html)
- [SendPulse component reference](https://login.sendpulse.com/dist/ui-library/components.html)
- [SendPulse JavaScript reference](https://login.sendpulse.com/dist/ui-library/javascript.html)
- [CDN stylesheet](https://cdn.sendpulse.com/dist/css/sp-marketplace-app-ui.min.css)
- [Project homepage (skill metadata)](https://github.com/sendpulse/sendpulse-skills/tree/main/sendpulse-marketplace-ui-cdn)

## Skill Output:

**Output Type(s):** [HTML, CSS, Code, Shell commands, Guidance]

**Output Format:** [Markdown guidance with HTML/CSS examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples and validation steps are intended to be adapted to the target SendPulse interface.]

## Skill Version(s):

1.0.0 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
