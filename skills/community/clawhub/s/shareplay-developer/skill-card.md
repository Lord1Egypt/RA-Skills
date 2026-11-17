## Description:

Build, integrate, and troubleshoot SharePlay GroupActivities features, including GroupActivity definitions, activation flows, GroupSession lifecycle, messaging and journals, ShareLink and SharePlay UI surfaces, and visionOS spatial coordination.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomkrikorian](https://clawhub.ai/user/tomkrikorian)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to implement and debug SharePlay experiences across Apple platforms, especially GroupActivities flows for activation, session lifecycle, state synchronization, UI sharing surfaces, and visionOS spatial coordination.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated SharePlay code or guidance may affect app collaboration behavior through entitlements, activation paths, or shared GroupSessionJournal data.

Mitigation: Review proposed app changes before applying them, with particular attention to Group Activities entitlements, SharePlay activation paths, and data shared through GroupSessionJournal.

Risk: Incorrect SharePlay session lifecycle or spatial-coordination code can lead to broken joins, stale shared state, or participants not colocating in visionOS immersive spaces.

Mitigation: Verify session references are retained, SystemCoordinator is configured before join, late joiners receive state snapshots, and teardown calls leave or end sessions cleanly.

## Reference(s):

- [SharePlay Developer Skill Page](https://clawhub.ai/tomkrikorian/skills/shareplay-developer)
- [SharePlay Example Code References](artifact/references/REFERENCE.md)
- [SharePlay Activation UI](artifact/references/activation-ui.md)
- [visionOS SharePlay Group Immersive Space](artifact/references/visionos-immersive-space.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Configuration]

**Output Format:** [Markdown with Swift code examples and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include entitlement, activation-flow, session-lifecycle, synchronization, and visionOS spatial-coordination recommendations.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
