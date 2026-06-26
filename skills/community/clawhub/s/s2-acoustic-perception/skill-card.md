## Description: <br>
S2-SP-OS Acoustic Radar performs edge-delegated zero-shot acoustic classification with claimed ephemeral privacy and strict LAN-only network enforcement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SpaceSQ](https://clawhub.ai/user/SpaceSQ) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to capture a consented short ambient audio sample, send it to a trusted LAN edge classifier, and receive semantic acoustic tags plus local follow-up suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill records ambient microphone audio and sends short audio clips to a LAN edge server. <br>
Mitigation: Install only with explicit microphone consent, verify the destination is a trusted local server, and do not rely solely on the skill's privacy claims. <br>
Risk: The skill can suggest camera, alarm, security, logging, or smart-home follow-up actions based on acoustic classifications. <br>
Mitigation: Require manual confirmation before executing any follow-up action from the skill's suggestions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/SpaceSQ/s2-acoustic-perception) <br>
- [Project homepage](https://space2.world/s2-sp-os) <br>


## Skill Output: <br>
**Output Type(s):** [json, shell commands, guidance] <br>
**Output Format:** [JSON object emitted to stdout, with setup and execution guidance in Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, sounddevice, numpy, microphone consent, and a trusted LAN edge server.] <br>

## Skill Version(s): <br>
1.0.5 (source: frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
