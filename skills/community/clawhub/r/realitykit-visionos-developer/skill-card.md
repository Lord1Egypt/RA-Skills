## Description:

Build, debug, and optimize RealityKit scenes for visionOS, including entity/component setup, rendering, animation, physics, audio, input, attachments, and custom systems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomkrikorian](https://clawhub.ai/user/tomkrikorian)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to implement and troubleshoot RealityKit-based spatial experiences on visionOS, including component selection, custom systems, SwiftUI RealityView integration, and performance checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples involving ARKit camera, sensor, body-tracking, room or environment tracking can affect user privacy if copied into an app without review.

Mitigation: Review platform permissions and user disclosures before implementation, and disclose body or environment tracking to users.

Risk: Synchronization examples can share entity state with other participants beyond what an application needs.

Mitigation: Limit synchronized entity data to the minimum required for the experience.

Risk: File-saving examples can write generated assets to unintended locations.

Mitigation: Confirm file destinations before saving generated assets.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tomkrikorian/skills/realitykit-visionos-developer)
- [System and Component Creation](artifact/references/systemandcomponentcreation.md)
- [ModelComponent Reference](artifact/references/modelcomponent.md)
- [InputTargetComponent Reference](artifact/references/inputtargetcomponent.md)
- [AnchoringComponent Reference](artifact/references/anchoringcomponent.md)
- [SynchronizationComponent Reference](artifact/references/synchronizationcomponent.md)
- [Apple RealityKit AccessibilityComponent Documentation](https://developer.apple.com/documentation/realitykit/accessibilitycomponent)
- [Apple RealityKit AnchoringComponent Documentation](https://developer.apple.com/documentation/realitykit/anchoringcomponent)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with Swift code examples and reference file summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to load focused component reference files before answering.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
