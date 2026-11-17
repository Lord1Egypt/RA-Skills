## Description:

S2-SP-OS Spectrum Radar provides passive spatial perception from GPIO/UART mmWave radar with explicit S2_PRIVACY_CONSENT and quantized biometric status outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spacesq](https://clawhub.ai/user/spacesq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to collect passive occupancy, motion, distance, and quantized vital-status telemetry from mmWave radar modules for higher-level reasoning. Actions such as lighting, audio monitoring, or emergency workflows should remain outside this skill and require explicit policy or user approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says the release presents passive hardware sensing while the packaged code is broken or mocked, so outputs should not be treated as real occupancy or health evidence without validation.

Mitigation: Review and test the runnable implementation against the intended hardware before using outputs for occupancy, health, or safety decisions.

Risk: The security guidance flags autonomous lighting, audio-monitoring, and emergency examples as risky follow-up behavior.

Mitigation: Keep this skill limited to passive telemetry and require explicit per-action user approval or external policy checks before any actuator, audio, or emergency workflow runs.

Risk: The security guidance warns against persisting the consent flag in startup files.

Mitigation: Set S2_PRIVACY_CONSENT only for controlled sessions or managed services where the operator has confirmed consent, and avoid blanket shell startup exports.

Risk: The security guidance recommends dependency control for installation.

Mitigation: Install pyserial in a controlled environment and pin dependencies before deployment.

## Reference(s):

- [S2-SP-OS Wave/Spectrum Radar on ClawHub](https://clawhub.ai/spacesq/skills/s2-spectrum-perception)
- [S2-SP-OS Product Page](https://space2.world/s2-sp-os)
- [S2 Memzero Protocol](artifact/S2-MEMZERO-PROTOCOL.md)
- [Edge Hardware Setup Guide](artifact/edge-setup-guide.md)
- [Agent Reasoning Examples](artifact/AGENT-EXAMPLES.md)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [JSON sensor-state payloads and Markdown setup guidance with bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, pyserial, hardware access, and S2_PRIVACY_CONSENT=1 before execution.]

## Skill Version(s):

2.0.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
