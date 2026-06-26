## Description: <br>
Build, integrate, and troubleshoot SharePlay GroupActivities features, including GroupActivity definitions, activation flows, GroupSession lifecycle, messaging and journals, ShareLink and SharePlay UI surfaces, and visionOS spatial coordination. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tomkrikorian](https://clawhub.ai/user/tomkrikorian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to implement and debug SharePlay experiences across Apple platforms, including GroupActivity definitions, activation flows, session lifecycle handling, state synchronization, and visionOS spatial coordination. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: SharePlay implementations can expose participant or app state if examples are applied without data minimization. <br>
Mitigation: Send only the minimal state required for the shared experience and avoid placing private data in shared journals. <br>
Risk: Incoming SharePlay messages or attachments may be malformed or inappropriate for local app state. <br>
Mitigation: Validate incoming messages and attachments before applying them. <br>
Risk: The SharePlay entitlement could be enabled on unintended app targets. <br>
Mitigation: Enable the Group Activities entitlement only on intended targets. <br>


## Reference(s): <br>
- [SharePlay Example Code References](references/REFERENCE.md) <br>
- [SharePlay Activation UI](references/activation-ui.md) <br>
- [visionOS SharePlay Group Immersive Space](references/visionos-immersive-space.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Configuration instructions] <br>
**Output Format:** [Markdown with Swift code examples and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only helper; does not execute tools or modify projects by itself.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
