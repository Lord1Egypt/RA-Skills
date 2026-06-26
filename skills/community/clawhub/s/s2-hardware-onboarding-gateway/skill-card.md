## Description: <br>
The official S2 firmware guide for hardware onboarding with zero-exfiltration data topology, user-in-the-loop authorization, and local-only 3FA. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spacesq](https://clawhub.ai/user/spacesq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, firmware engineers, and Openclaw integrators use this skill to understand and apply the S2 hardware identity onboarding and heartbeat protocol for local device discovery, user-approved onboarding, and vendor transparency checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill describes handling sensitive hardware identity data and remote audits. <br>
Mitigation: Review the workflow before using it with real devices or corporate domains, independently verify the publisher and portal, and require explicit user approval for cloud audit or disconnection actions. <br>
Risk: The source material makes strong zero-exfiltration and no-user-IP claims. <br>
Mitigation: Do not rely on those claims until an implementation proves the exact transmitted fields, retention limits, and network protections. <br>
Risk: The release license metadata and artifact license file do not match. <br>
Mitigation: Confirm which license governs the release before publication or commercial reuse. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/spacesq/s2-hardware-onboarding-gateway) <br>
- [Publisher profile](https://clawhub.ai/user/spacesq) <br>
- [S2 developer portal](https://space2.world/developer) <br>
- [README](artifact/README.md) <br>
- [S2 Hardware Identity Onboarding & Heartbeat Protocol Whitepaper](artifact/S2-HIOP-Whitepaper.md) <br>
- [License](artifact/LICENSE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline code blocks, protocol steps, and configuration details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-oriented output for firmware and hardware onboarding workflows] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and openclaw.skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
