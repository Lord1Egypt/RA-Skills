## Description:

Generates declarative IoT control templates from device API documentation with a local LLM, mapping open devices to S2 six-element interfaces and blocking unsupported closed protocols.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spacesq](https://clawhub.ai/user/spacesq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and IoT integration engineers use this skill to turn device API or protocol descriptions into S2-compatible declarative control templates. It is intended for cross-protocol device mapping and simulation before any approved downstream execution against physical hardware.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated IoT control templates may be stored as active mounts without enough validation for a physical-device control context.

Mitigation: Review generated adapters and add an approval and validation layer before any downstream engine uses them with real devices.

Risk: Sensitive device documentation or internal endpoint details could be sent to the configured local LLM endpoint.

Mitigation: Use only a trusted local LLM setup and avoid entering proprietary documentation, credentials, or sensitive internal endpoints.

Risk: Connecting generated active_hardware_mounts.json output directly to real hardware could cause unsafe or unintended device behavior.

Mitigation: Keep generated mounts in simulation or staging until they pass human review, policy checks, and device-specific validation.

## Reference(s):

- [S2 Spatial Primitive OS Whitepaper](artifact/S2-Spatial-Primitive-OS-Whitepaper.md)
- [ClawHub Skill Page](https://clawhub.ai/spacesq/skills/s2-nlp-connector)
- [Space2.world](https://space2.world)

## Skill Output:

**Output Type(s):** [text, json, configuration, guidance]

**Output Format:** [Console text plus JSON declarative control-template objects written to active_hardware_mounts.json]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a local OpenAI-compatible chat completions endpoint and stores successful generated adapters as active hardware mounts.]

## Skill Version(s):

1.0.0 (source: release evidence and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
