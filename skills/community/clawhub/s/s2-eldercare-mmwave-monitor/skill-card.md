## Description:

Detects elder falls and apnea using privacy-safe 60/77 GHz mmWave radar with real-time micro-Doppler STFT analysis for emergency alerts and smart-home response.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spacesq](https://clawhub.ai/user/spacesq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and care-technology operators use this skill to simulate or deploy mmWave-based fall detection and route verified emergency events to Home Assistant actions. It is intended for privacy-sensitive eldercare monitoring where real physical actuation must remain gated and reviewed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Real actuation can unlock doors or control smart-home devices after a fall event.

Mitigation: Keep dry-run mode enabled by default and require explicit human approval or independent sensor confirmation before enabling physical actions.

Risk: Home Assistant credentials may be sent to a configurable HTTP endpoint.

Mitigation: Use HTTPS with a fixed trusted Home Assistant host and a least-privilege token before enabling real actuation.

Risk: Unpinned dependencies can change behavior across installations.

Mitigation: Pin dependencies with a lockfile and review updates before deployment.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/spacesq/skills/s2-eldercare-mmwave-monitor)
- [Publisher profile](https://clawhub.ai/user/spacesq)
- [Project homepage](https://space2.world)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate local console output, simulated Home Assistant routing intents, and DSP analysis artifacts during execution.]

## Skill Version(s):

1.1.0 (source: server release metadata and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
